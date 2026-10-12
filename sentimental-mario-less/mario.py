def draw_pyramid(height):
    for i in range(1, height + 1):
        print(" " * (height - i), end="")
        print("#" * i)

while True:
    try:
        h = int(input("Height: "))
        if h >= 1 and h <= 8:
            break
    except ValueError:
        continue

draw_pyramid(h)
