import qrcode

img = qrcode.make("https://www.youtube.com/watch?v=Rl0ludWTLxs")
img.save("qr.png", "PNG")
