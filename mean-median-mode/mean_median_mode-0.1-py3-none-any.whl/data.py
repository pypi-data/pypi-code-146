def getlist():
    l=[]
    n=int(input("enter the number of elements:"))
    for i in range(n):
        x=float(input("enter a number:"))
        l.append(x)
    return l
def sortlist(l):
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if l[i] > l[j]:
               l[i], l[j] = l[j], l[i]
    return l

