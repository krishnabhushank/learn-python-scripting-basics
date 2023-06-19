numbers = [1, 2, 3, 4, 5]
numbers.append(6)
print(numbers)
# To view Parameter Info for a Method, use Ctrl+P in PyCharm IDE (Windows)

# What if we want to insert a number somewhere in the middle or in the beginning
# Insert at beginning
numbers = [1, 2, 3, 4, 5]
numbers.insert(0, -1)
print(numbers)

# Remove the third element from the list
numbers = [1, 2, 3, 4, 5]
numbers.remove(3)
print(numbers)

# Remove all items in the list
numbers.clear()
print(numbers)

# Sometimes, we want to know if a given item exists in a list or not. We use in operator.
numbers = [1, 2, 3, 4, 5]
print(1 in numbers)  # The expression with in operator will return Boolean value
print(9 in numbers)

# Finally, there are times, you want to know how many items are there in the list
numbers = [1, 2, 3, 4, 5]
print(len(numbers))
# len is a built-in function, similar to Print function.
# It returns the number of elements in the list
