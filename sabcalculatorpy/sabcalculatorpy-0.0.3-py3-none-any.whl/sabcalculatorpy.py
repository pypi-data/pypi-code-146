import numpy as np



def add(a,b):
    c=a+b
    print(c)

def sub(a,b):

    c=a-b
    print(c)

def mult(a,b):
    c=a*b
    print(c)

def div(a,b):
    c=a/b
    print(c)




def det():
    order=int(input("enter the no of rows/columns "))
    main_list=[]
    for x in range(order):
        a=[]
        for y in range(order):
            
            z=int(input("enter the value "))
            a.append(z)
        main_list.append(a)

    n_array=np.array(main_list)
    print(int(np.linalg.det(n_array)))

def solve2():
    a1=int(input("enter the a1 value in a1*x + b1*y= c1\n"))
    b1=int(input("enter the b1 value in a1*x + b1*y= c1\n"))
    c1=int(input("enter the c1 value in a1*x + b1*y= c1\n"))

    a2=int(input("enter the a2 value in a2*x + b2*y= c2\n"))
    b2=int(input("enter the b2 value in a2*x + b2*y= c2\n"))
    c2=int(input("enter the c2 value in a2*x + b2*y= c2\n"))

    x=(c1*b2 - c2*b1)/(a1*b2 - a2*b1)
    y=(c1*a2-c2*a1)/(b1*a2-b2*a1)

    print(f"x= {x}")
    print(f"y={y}")

def solve3():
    a3=int(input("a1?"))
    b3=int(input("b1?"))  
    c3=int(input("c1?"))
    d3=int(input("d1?"))

    a4=int(input("a2?"))
    b4=int(input("b2?"))
    c4=int(input("c2?"))
    d4=int(input("d2?"))   

    a5=int(input("a3?"))
    b5=int(input("b3?"))
    c5=int(input("c3?"))
    d5=int(input("d3?"))

    a1= b3*a4 - b4*a3 
    b1=c3*a4 - c4*a3
    c1=d3*a4 - d4*a3

    a2= a5*b4 - b5*a4
    b2= c4*a5-c5*a4
    c2=d4*a5-d5*a4

    y=(c1*b2 - c2*b1)/(a1*b2 - a2*b1)
    z=(c1*a2-c2*a1)/(b1*a2-b2*a1)
    x=(d3-c3*z-b3*y)/a3

    print(x)
    print(y)
    print(z)

solve2()