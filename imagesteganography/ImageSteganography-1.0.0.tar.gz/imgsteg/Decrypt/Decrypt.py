from .GetMatrix import GetMatrix
from .TextConverter import Convert
import sys

class Decrypt():

    def __init__(self, address, password, shared_key):

        self.matrix = GetMatrix(address)
        if not GetMatrix(address):
            print('address error')
            sys.exit()
        data = Convert()
        self.pass_key = data.convert_pw(password)

        #Check if password is correct
        if self.pass_key != int(self.matrix.matrix[0][0][0]):
            print('Incorrect Password !')
            sys.exit()
        else:
            print('Passwords match...')
        self.shared_key =  data.convert_text_helper(shared_key)

        #extract list of characters and add pass key to decrypt the text
        self.extracted_text = []
        self.length = int(self.matrix.matrix[0][0][1])
        x = 0
        for i in range(0, len(self.matrix.matrix), self.pass_key):
            for m in range(0, len(self.matrix.matrix[i]), self.pass_key):
                if i == 0 and m == 0:
                    pass
                elif x < self.length:
                    #print(i, m)
                    for k in range(1, len(self.matrix.matrix[i][m])):
                        self.extracted_text.append(str(self.matrix.matrix[i][m][k])[-1])
                        if  len(str(self.matrix.matrix[i][m][-1])) > 1:
                            if int(str(self.matrix.matrix[i][m][k])[-k]) == 0:
                                break
                    self.extracted_text.append(',')
                    x += 1
                else:
                    break
        self.message = data.secret_message(self.extracted_text, self.shared_key)
        print('\n\n', self.message)

        

