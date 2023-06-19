class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self is a reference to the current object

    def move(self):
        print("move")

    def draw(self):
        print("draw")


point = Point(10, 20)
print(point.x)
print(point.y)