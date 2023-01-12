from .TextConverter import Convert
from .GetMatrix import ChangeMatrix
from .ImageReader import GetMatrix



class Encrypt():
    '''will import modules and do nessacary calculations and return to you an image with your message encrypted'''
    def __init__(self, text, password, address):
        
        #data is object and returns encoded data
        data = Convert()
        self.message = data.convert_ascii(text)     #a list of length(text)
        #print(self.message)
        self.pass_key = data.convert_sum(password)
        
        #returns 3D matrix of your given image address
        self.image = GetMatrix(address)
        #print(self.image.matrix)
        #print(self.message)

        x = 0
        #traversing through image matrix to do manipulations
        for i in range(0, len(self.image.matrix), self.pass_key):
            for j in range(0, len(self.image.matrix[i]), self.pass_key):
                if i == 0 and j == 0:
                    pass
                else:
                    if x < len(self.message):
                       # print(i, j)
                        #print(self.image.matrix[i][j], self.message[x])
                        self.image.matrix[i][j] = ChangeMatrix(self.image.matrix[i][j], self.message[x]).matrix_row
                        #print(self.image.matrix[i][j])
                        x += 1
                    else:
                        break
                    
        self.image.matrix[0][0][0] = self.pass_key
        self.image.matrix[0][0][1] = len(self.message)
        #reserved----- self.matrix[0][0][2]
        #print(self.pass_key)
        #print(self.image.matrix)

        #save matrix as .png
        self.verify = self.image.save(input('Enter the name of your encrypted image:\n'), self.image.matrix)  
                        
        #verify images
        #print(self.image.matrix)
        #print(ChangeMatrix(self.image.matrix).inverted_image)
        #print(self.verify)
