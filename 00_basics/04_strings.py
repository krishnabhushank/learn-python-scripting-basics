# 'IBL Course for Python' is an object.  Similar to a Real-world object, it has a bunch of capabilities.
# ex. Like a TV remote. i.e. Bunch buttons that you can press to do stuff.
course = 'IBL Course for Python'
# You have already seen the Input function.
# - However, it is a generic function. The string object has more specific function. ex. lower, find etc.
print(course.upper())
# Note: upper will not modify our string. It will return a new string.
print(course)
# Here, you will see Course variable is not affected.

print(course.lower())
# Similar to upper, we have lower for converting string to lower case

print(course.find('y'))
# Another function is find. It will provide the index of first occurence of 'y'
# In Python, index of character in String is Zero.
# IBL Course for Python
# 012345678901234567890
#           11111111112
# Note : Python is case-sensitive
print(course.find('Y'))  # Y is not present in our string, what will be the output?
# You can also pass sequence of characters to find
print(course.find('for'))

# There are times, when we want to replace a string. We use replace method
print(course.replace('for', '4'))
# If you try to replace string or sequence of characters not present, nothing is going to happen
print(course.replace('x', '4'))
# Note : Like the upper method, replace will not modify the original string. It will return a new string
# This is because strings in Python (like many other languages) are Immutable. We cannot change then once we create them

# Finally, sometimes, we want to check if a Search String is present in a reference string
# You have already seen find method.
print(course.find('Python'))
# It returns the Index of the first occurrence of the search string
# There is another option using 'in' operator
print('Python' in course)
# This is more readable than find method.
# in returns a Boolean value. This might be more desirable
