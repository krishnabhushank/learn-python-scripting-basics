# For a tuple, we do not see any methods like append, insert, remove etc.
# We only have count and index.

# Count : Number of occurrences of an element
numbers = (1, 2, 3, 3)
print(numbers.count(3))

# Index : Index of First Occurrence of the given element
print(numbers.index(3))  # In this case, 2

# Practically, you will you use lists rather than tuples.
# However, once you create a list of objects and if you want to ensure that no one modifies the list, then use tuple
