class Dog:
    def walk(self):
        print("walk")


class Cat:
    def walk(self):
        print("walk")


# Assume that we have lot of action to do under Walk()
# Walk is same for Dog and Cat classes. In the future let's say, we find an issue in Walk.
# In the above code organization, we would need to change in multiple location.
