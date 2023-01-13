#multiplication table of a number 
def print_table(num): 
    for i in range(1,11): 
        print(num,' x ', i, ' = ',num*i) 

# function to check string is palindrome or not
def isPalindrome(str):
 
    # Run loop from 0 to len/2
    for i in range(0, int(len(str)/2)):
        if str[i] != str[len(str)-i-1]:
            return False
    return True

#mean of 2 numbers
def mean(a,b):
    c = a+b
    return c/2

#print unique elements of a list
def unique_list(l):
  x = []
  for a in l:
    if a not in x:
      x.append(a)
  return x

#find divisors of a number
def findDivisors(num):
    for i in range(1, num + 1):
        if num % i == 0:
            print(i)

#sum of 2 numbers
def sum(a,b):
    return a+b

#subtract two numbers
def sub(a,b):
    return a-b

#multiply 2 number
def mul(a,b):
    return a*b

#divide 2 numbers
def div(a,b):
    return a/b

#which number is greater
def greater(a,b):
    if a>b:
        return a
    else:
        return b

#which number is smaller
def smaller(a,b):
    if a<b:
        return a
    else:
        return b
