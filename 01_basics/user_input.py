name = input("What's your name?")
age = input("How old are you?")

#Converting the age string to integer
age_as_number = int(age)
years_until_100 = 100 - age_as_number

print(f"Hello {name}!")
print(f"You'll be 100 in {years_until_100} years")