def printTable(Lista, Titulo = False):
    Len = dict()
    for i in range(len(Lista[0])): Len[i] = 0
    for i in Lista:
        for j in range(len(i)):
            N = len(str(i[j]))
            if N > Len.get(j):
                Len[j] = N
    R = "+"
    for i in Len.values(): R += "-" * (i + 2) + "+"

    # Titulo
    if Titulo != False and Titulo != True:
        Titulo = str(Titulo)
        LTitulo = len(Titulo) + 2
        LR = len(R)
        if LR > LTitulo:
            C = ""
            for i in range(int((LR - LTitulo) / 2)):
                C += "*"
            if LTitulo % 2 == 0: 
                print(C + " " + Titulo + " " + C + "*")
            else: print(C + " " + Titulo + " " + C)
        else: print(Titulo)

    for i in range(len(Lista)):
        print(R)
        C = "| "
        Count = 0
        for j in Lista[i]:
            C += str(j)
            for i in range(Len.get(Count) - len(str(j))): C += " "
            C += " | "
            Count += 1
        print(C[:-1])
    print(R)