x = int(input("Enter the number 1(x)"))
y = int(input("Enter the number 2(y)"))
z = int(input("Enter the number 3(z)"))
if x > y > z:
    print("zis smallest ,x is biggest")
elif x > z > y:
    print("xsbiggest,y is smallest")
elif y > x > z:
    print("yis bigghest,z is smallest")
elif y > z > x:
    print("yis biggest , x is smalles")
elif z > x > y:
    print("zis biggest , y is smalles")
elif  z > y > x:
    print("zis biggest,x is smallest")
else:
    print("code is not valid")
