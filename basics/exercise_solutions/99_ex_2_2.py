first = input("First: ")
second = input("Second: ")
sum_val = int(first) + int(second)
print(sum_val)
# Try 1: If you give 10, 20 as input, what will be the result?
# Try 2: How about we give 10.1 and 10 and input, what will be the result?



# Try 1: Run is ok.
# Try 2: Will throw an error. Reason, We gave a Decimal value as string and trying to convert to Int
# First: 10.1
# Second: 10
# Traceback (most recent call last):
#   File "C:\Users\kkoneru\PycharmProjects\pythonByExamples\99_ex_2_2.py", line 3, in <module>
#     sum_val = int(first) + int(second)
# ValueError: invalid literal for int() with base 10: '10.1'

