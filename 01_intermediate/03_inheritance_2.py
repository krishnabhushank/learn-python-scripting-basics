class Mammal:
    def walk(self):
        print("walk")


class Dog(Mammal):
    pass


class Cat(Mammal):
    pass

dog1 = Dog()
dog1.walk()

# Python does not like empty classes. Therefore, you need to add pass in line 7 and 11 to make Python happy
