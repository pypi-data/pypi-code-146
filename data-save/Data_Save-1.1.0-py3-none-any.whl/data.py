import os
from time import sleep

class Data():
    def __init__(self, file_name, text, onePress=False):
        self.file_name = file_name
        self.text = text
        self.onePress = onePress

        if onePress == True:
            sleep(0.100)
            try:
                self.file = open(file_name, "r")
            except:
                try:
                    self.my_file = open(file_name, "w+")
                    self.my_file.write(text)
                    self.my_file.close()
                except:
                    self.my_file = open(file_name, "w+")
                    self.my_file.write(text)
                    self.my_file.close()

        if onePress == False:
            sleep(2)
            try:
                file = open(file_name, "r")
            except:
                try:
                    os.mkdir("Data")
                    my_file = open(f"Data/{file_name}", "w+")
                    my_file.write(text)
                    my_file.close()
                except:
                    my_file = open(f"Data/{file_name}", "w+")
                    my_file.write(text)
                    my_file.close()

class Upload_data():
    def __init__(self, file_name, text_start, onePress=False):
        self.file_name = file_name
        self.text_start = text_start
        self.onePress = onePress
    def up1(self, file_name, text, text_if2, onclickFunction=None, onclickFunction_2=None):
        self.file_name = file_name
        self.text = text
        self.text_if2 = text_if2
        self.onclickFunction = onclickFunction
        self.onclickFunction_2 = onclickFunction_2
        try:
            if text in open(rf'Data/{file_name}'):
                fons = 'gray'
                self.onclickFunction()
            elif text_if2 in open(rf'Data/{file_name}'):
                fons = '#DCDCDC'
                self.onclickFunction_2()
            else:
                my_file = open(rf"Data/{file_name}", "w")
                my_file.write(text)
                my_file.close()
        except:
            pass
    def up2(self, file_name, text, text_if2, text_if3, onclickFunction=None, onclickFunction_2=None, onclickFunction_3=None):
        self.file_name = file_name
        self.text = text
        self.text_if2 = text_if2
        self.onclickFunction = onclickFunction
        self.onclickFunction_2 = onclickFunction_2
        self.onclickFunction_3 = onclickFunction_3
        try:
            if text in open(rf'Data/{file_name}'):
                self.onclickFunction()
            elif text_if2 in open(rf'Data/{file_name}'):
                self.onclickFunction_2()
            elif text_if3 in open(rf'Data/{file_name}'):
                self.onclickFunction_3()
            else:
                my_file = open(rf"Data/{file_name}", "w")
                my_file.write(text)
                my_file.close()
        except:
            pass
# False = лож
# True = правда


