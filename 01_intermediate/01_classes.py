# Naming Convention : For variables and functions, we use lower case letters.
# Also, we separate multiple words with an underscore
# For classes, we do not use underscore. Instead, we capitalize the first letter of every word.
# Ex. Point or EmailClient
# this is called Pascal Naming Convention.
class Point:
    def move(self):
        # What is this self? We will get to this later
        print("move")

    def draw(self):
        print("draw")


# Add two line breaks. This will show the end of the class definition
# with this Class, we have identified a new type. With this class we create a new Object.
# Object : Instance of a class.
# A class simply defines a blueprint or template for create an object
# Objects are actual instances based on that blueprint
# So, we can hgave 10s or 100s of Points on screen. These are the objects or instances

point1 = Point()  # Will create a new object and return it
point1.move()

# Apart from Methods, Objects can have variable. These variables are like attributes for the objects
point2 = Point()
point2.x = 10
point2.y = 20
print(point2.x)
point2.move()

point3 = Point()
# print(point3.x) -- will  throw a error. Since point 3 does not have an attribute x.
point3.x = 3
print(point3.x)

# Note: there is a small problem with this class. You can create a Point object without x or y.
# This does not make sense. A point object should have x and y co-ordinate.
