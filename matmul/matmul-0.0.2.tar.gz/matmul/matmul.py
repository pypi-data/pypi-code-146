def matrixMultiplication(mat1,mat2):
    mul_result=[]
    for i in range(len(mat1)):
        sub_list=[]
        for j in range(len(mat2[0])):
            result=0
            for k in range(len(mat2)):
                result = result + mat1[i][k]*mat2[k][j]
            sub_list.append(result)
        mul_result.append(sub_list)
    print(mul_result)
    return mul_result