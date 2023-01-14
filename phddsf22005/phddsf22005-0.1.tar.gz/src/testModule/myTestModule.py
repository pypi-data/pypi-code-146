NAME = 'Ali Harris'
ID = 'PHDDSF2022M005'

#get_factorial(n) finds the factorial of a given number n\n",
def get_factorial(n):
    if n == 0:
        return 1
    fac = 1
    for i in range(1, n + 1):
        fac = fac * i
        
    return fac


#find_largest(a,b) takes in two parameters and returns the largest number of the two \n",
def find_largest(a, b):
    if a > b:
        large = a
    else:
        large = b
    return large


#find_cube(x) returns the cube of a given number x
def find_cube(x):
    return x * x * x
   

#find_power(v1,v2) returns the v1 power v2\n",
def find_power(v1, v2):
    return v1 ** v2


#is_multiple(x,y) returns true if x is a multiple of y and false otherwise\n",
def is_multiple(x, y):
    if x % y == 0:
        return True
    else:
        return False