def getInputMatrix(row,col):
    A=[]
    print('enter numbers row wise')
    for i in range(row):
        a=[]
        for j in range(col):
            a.append(int(input('enter number ')))
        A.append(a)
    for i in range(row):
        for j in range(col):
            print(A[i][j])
    return A