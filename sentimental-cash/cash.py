while True:
    try:
        change = float(input("Change: "))
        if change > 0:
            break
    except:
        continue

cents = round(change * 100)
coins = 0

while cents >= 25:
    cents -= 25
    coins += 1
while cents >= 10:
    cents -= 10
    coins += 1
while cents >= 5:
    cents -= 5
    coins += 1
while cents >= 1:
    cents -= 1
    coins += 1

print(coins)
