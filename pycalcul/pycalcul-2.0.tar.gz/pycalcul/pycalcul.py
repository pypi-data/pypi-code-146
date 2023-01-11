import sys
import os
import math 

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def rest_div(x, y):
    return x % y

def power(x, y):
    return x ** y

def square_root(x):
    return x ** 0.5

def logarithm(x):
    return math.log(x)

def exponential(x):
    return math.exp(x)

def factorial(x):
    return math.factorial(x)

def sine(x):
    return math.sin(x)

def cosine(x):
    return math.cos(x)

def tangent(x):
    return math.tan(x)

def cotangent(x):
    return 1 / math.tan(x)



print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")
print("5.Rest of division")
print("6.Power")
print("7.Square root")
print("8.Logarithm")
print("9.Exponential")
print("10.Factorial")
print("11.Sine")
print("12.Cosine")
print("13.Tangent")
print("14.Cotangent")
print("15.Exit")

while True:
    choice = input("Enter choice: ")
    if choice == '15':
        print("Exiting...")
        sys.exit()
    
    if choice in ('1', '2', '3', '4', '5', '6'):
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))

        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))

        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))

        elif choice == '4':
            print(num1, "/", num2, "=", divide(num1, num2))

        elif choice == '5':
            print(int(num1), "%", int(num2), "=", rest_div(num1, num2))
        
        elif choice == '6':
            print(num1, "^", num2, "=", power(num1, num2))
          
    if choice in ('7', '8', '9', '10', '11', '12', '13', '14', '15'):
        try:
            num1 = float(input("Enter number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == '7':
            print(num1, "^ 0.5", "=", square_root(num1))
        
        elif choice == '8':
            print("log", num1, "=", logarithm(num1))
        
        elif choice == '9':
            print("exp", num1, "=", exponential(num1))

        elif choice == '10':
            print(num1, "!", "=", factorial(num1))
        
        elif choice == '11':
            print("sin", num1, "=", sine(num1))
        
        elif choice == '12':
            print("cos", num1, "=", cosine(num1))

        elif choice == '13':
            print("tan", num1, "=", tangent(num1))

        elif choice == '14':
            print("cot", num1, "=", cotangent(num1))
    
    next_calculation = input("Continue? (yes/no): ")
    if next_calculation == "no":
        sys.exit()
else:
    print("Invalid input. Please enter a number from 1 to 15.")

    
    