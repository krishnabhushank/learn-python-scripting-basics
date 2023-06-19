first = input("First: ")
second = input("Second: ")
sum_val = float(first) + float(second)
print("Sum:" + sum_val)
# How about we give 10.1 and 10 and input, what will be the result?



# It will throw an error. Reason: We are trying to add a String to a Float
# First: 10.1
# Second: 10
# Traceback (most recent call last):
#   File "C:\Users\kkoneru\PycharmProjects\pythonByExamples\99_ex_2_3.py", line 4, in <module>
#     print("Sum:" + sum_val)
# TypeError: can only concatenate str (not "float") to str


