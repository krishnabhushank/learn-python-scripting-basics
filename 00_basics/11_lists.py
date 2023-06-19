# To declare a List we have Square brackets. We separate elements with a Comma
names = ["Bob", "Amit", "Raj", "Mary", "Sam"]
print(names)

# To get individual elements from the list. Use the Index within Square brackets. Index of First element is Zero.
print(names[0])

# In Python, we can also use negative index. I have not come across this in other programming languages
# If names[0] is first element, what do you think names[-1] refers to?
print(names[-1])

# names[-1] refers to last element in the list. In this case, Sam
# What about names[-2]?
print(names[-2])

# Say, we want to change the value of first element in the list. i.e, set as Rob. How do we do it?
names[0] = "Rob"
print(names)

# Say, we want to get first three elements of the index. Start index is 0 and everything before index 3
print(names[0:3])
# Note the above expression does not modify the original list. It returns a new List
print(names)
