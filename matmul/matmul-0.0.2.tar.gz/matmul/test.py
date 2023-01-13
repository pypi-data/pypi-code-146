import matinput as i
import matmul as m
a = int(input('enter number of rows in mat1 '))
b = int(input('enter number of columns in mat1 '))
mat1 = i.getInputMatrix(a, b)
c = int(input('enter number of rows in mat2 '))
d = int(input('enter number of columns in mat2 '))
mat2 = i.getInputMatrix(c, d)
result = m.matrixMultiplication(mat1, mat2)