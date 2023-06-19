birth_year = input("What is your birth year? ")
age = 2023 - birth_year
print(age)
# If you provide input as, Say 1982, What will be the result on executing the program





# It will throw error like this:
# What is your birth year? 1982
# Traceback (most recent call last):
#   File "C:\Users\kkoneru\PycharmProjects\pythonByExamples\03_type_conversion_1.py", line 2, in <module>
#     age = 2023 - birth_year
# TypeError: unsupported operand type(s) for -: 'int' and 'str'
# What is int and str? int - Short for Integer (whole number), str - Short for String
# In this example, in Line 2,
# - 2023 is example of an Int.
# - birth_year is a String. Why is it so? You gave an input as 1982.
#   Reason: Input function returns a value as a String.
#           I.e. it returns value as "1982" (a string) instead of 1982 (Number)
# Explanation for the failure:
# - Line 2 becomes : age = 2023 - "1982". Python does not know how to subtract String from an Integer
# Solution : We need to convert String to an Integer. How do we do that?
