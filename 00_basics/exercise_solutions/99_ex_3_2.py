weight = int(input("Weight: "))
unit = input("(K)g or (L)bs: ")

if unit.upper() == 'K':
    converted = weight / 0.45
    print("Weight in Lbs: " + converted)
else:
    converted = weight * 0.45
    print("Weight in Kgs: " + converted)

# When you run this code, there is an error. Can you provide a reason?
