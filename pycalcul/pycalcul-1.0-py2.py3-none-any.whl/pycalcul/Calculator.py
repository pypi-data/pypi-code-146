sign = "+"
a = input()
while not sign == "=":
    sign = input()
    b = input()
    if sign ==  "+":
        result = int(a)+int(b)
    if sign == "-":
        result = int(a)-int(b)
    if sign == "*":
        result = int(a)*int(b)
    if sign == "/":
        result = int(a)/int(b)
    if sign == "%":
        result = int(a)%int(b)
    if sign == "^":
        result = int(a)**int(b)
    a = result
    print (a)