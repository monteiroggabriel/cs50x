import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Query all shares owned grouped by symbol
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    portfolio = []
    total_portfolio_value = 0

    for stock in stocks:
        symbol = stock["symbol"]
        shares = stock["total_shares"]
        quote_data = lookup(symbol)
        if quote_data:
            current_price = quote_data["price"]
            total_value = current_price * shares
            total_portfolio_value += total_value
            portfolio.append({
                "symbol": symbol,
                "name": quote_data["name"],
                "shares": shares,
                "price": current_price,
                "total": total_value
            })

    user_rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = user_rows[0]["cash"]
    grand_total = cash + total_portfolio_value

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares:
            return apology("must provide shares", 400)

        # Validate shares is a positive integer
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be a positive integer", 400)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        price = stock["price"]
        total_cost = price * shares

        if cash < total_cost:
            return apology("can't afford", 400)

        # Execute purchase
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, price)

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        user_id
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate inputs
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must confirm password", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # Hash password and save user
        hash_password = generate_password_hash(password)
        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_password)
        except ValueError:
            return apology("username already exists", 400)

        # Log user in
        session["user_id"] = user_id
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must select symbol", 400)
        if not shares:
            return apology("must provide shares", 400)

        # Validate shares is a positive integer
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares must be a positive integer", 400)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        # Check if user owns enough shares of that stock
        owned_rows = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            user_id, symbol
        )

        if not owned_rows or owned_rows[0]["total_shares"] < shares:
            return apology("not enough shares", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        price = stock["price"]
        sale_value = price * shares

        # Execute sale
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
                   user_id, symbol, -shares, price)

        flash("Sold!")
        return redirect("/")
    else:
        # Get only stocks user actually owns
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id
        )
        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change password"""
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not current_password or not new_password or not confirmation:
            return apology("must fill all fields", 400)

        if new_password != confirmation:
            return apology("new passwords do not match", 400)

        user_id = session["user_id"]
        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        current_hash = rows[0]["hash"]

        if not check_password_hash(current_hash, current_password):
            return apology("incorrect current password", 400)

        # Update password
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        flash("Password updated successfully!")
        return redirect("/")
    else:
        return render_template("change_password.html")
