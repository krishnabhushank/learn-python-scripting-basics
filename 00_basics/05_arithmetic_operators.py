# Same as arithmetic operators we have in math. Ex. Add, Subtract, Multiple, Divide etc.
print(10 + 3)  # Addition Operator
print(10 - 3)  # Subtraction Operator
print(10 * 3)  # Multiplication Operator
print(10 / 3)  # Division Operator

# Technically, we have two types of Division operator
print(10 / 3)  # Single slash, result will be a floating point number (Number with a decimal point)
print(10 // 3)  # Double slash, result will be an integer (Whole Number)

# We also have Modulus operator
print(10 % 3)  # Will result in remainder after division

# Finally, we have exponent operator
print(10 ** 3)  # 10 to the power of 3

# For all these operators, we have augmented assignment operator
x = 10
x = x + 3  # Python will change it at run time to, x = 10 + 3
# or
x += 3  # Augmented Assignment Operator. i.e. Assignment oeprator (=) Augmented with +
# Similarly we have,
x -= 3
x /= 3
x *= 3
