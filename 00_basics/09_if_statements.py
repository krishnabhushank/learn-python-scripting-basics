# Create a variable called Temperature. Display messages based on different values of Temperature
temperature = 5

if temperature > 30:
    print("It's a hot day")
    print("Drink plenty of water")
    # Note use of Comparison operator.
    # Also, note the indentation. This identifies a block of code.
    # Finally, Note the Double Quotes in the string. Reason: String has Single Quote as an Apostrophe.
    # - Using a Single Quote would confuse Python.
    # In Programming Languages like C, C++, C#, Java, we have Curly braces to show block of code.
    # - In Python, we do not have curly braces. We have indentation to show the block of code
    # Tip: In PyCharm IDE, use Shift + Tab to remove indent at the end of the block
elif temperature > 20:  # (20, 30]
    print("It's a nice day")
elif temperature > 10:  # (10, 20]
    print("It's a bit cold")
else:
    print("It's cold")
print("Done")
# Since this is not indented, this is not part of If Block. It will always run

# Change the temperature to 25 and re-run to see what happens
# Now, Change it to 15 and re-run. Repeat for temperature = 5
