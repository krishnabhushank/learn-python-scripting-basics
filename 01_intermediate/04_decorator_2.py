def check(func):
    def inside(a, b):
        if b == 0:
            print("Can't divide by Zero")
            return
        return func(a, b)

    return inside


def div(a, b):
    return a / b


div = check(div)

print(div(10, 0))
