class ChangeMatrix():

    def __init__(self, row, number):
        self.number = str(number)
        self.matrix_row = row
        #Checks the length of number if 0 returs since nothing to add
        '''
        if int(self.number) == 0:
               #has length eg. 1,2,3
            #print('length: ', self.length)
        else:
            return
        '''
        
        for i in range(1, len(self.matrix_row)):
            if len(self.number) == 1 and i == 2:
                self.matrix_row[-i] = str(round(int(self.matrix_row[-i]), -1))
                break
            self.matrix_row[-i] = str(round(int(self.matrix_row[-i]), -1) + int(self.number[-i]))
        #print(self.matrix_row)
