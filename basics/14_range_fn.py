# range() functions will generate a sequence of number starting from
# 0 up to the number specified, excluding the provided number.
numbers = range(5)
for number in numbers:
    print(number)

# Two values : The first value is considered the starting value. Second value is ending value and is excluded.
numbers = range(5, 10)
for number in numbers:
    print(number)

# Three values : The third value will be considered as a step.
# Ex. Let's say we want Odd numbers between 5 and 10
numbers = range(5, 10, 2)
for number in numbers:
    print(number)

# Quite often, we will see range function used in For loop instead of storing the range object in a variable
for number in range(5, 10, 2):
    print(number)
