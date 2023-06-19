numbers = [1, 2, 3, 4, 5]
print(numbers)  # Will show exactly like what we input

# What if we want to show each items separately?
numbers = [1, 2, 3, 4, 5]
for item in numbers:
    print(item)

# We can do this via While loop too
i = 0
while i < len(numbers):
    print(numbers[i])
    i = i + 1
