temperature = int(input("What's the temperature?"))
is_weekend = True
is_sunny = True

if temperature > 80:
    print("It's hot outside!")
elif temperature > 65:
    print("Nice weather!")
    # Check the other conditions only when it's nice weather
    if is_weekend and is_sunny:
        print("Perfect day for coding outside!")
elif temperature > 55:
    print("It's cool outside.")
else:
    print("It's cold!")