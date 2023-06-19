x = 10 + 3 * 2
# In Math, + and / have higher precedence than + and -
# - i.e. 3 * 2 is evaluated first and the results added to 10
# In Python, it is the same.
print(x)

# Now, say we want the addition to be evaluated first and result multiplied by 2
x = (10 + 3) * 2
print(x)
