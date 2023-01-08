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
# False = лож
# True = правда
