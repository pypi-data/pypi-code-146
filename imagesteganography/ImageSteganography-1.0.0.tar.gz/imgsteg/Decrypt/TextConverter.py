import sys


class Convert():

    def __init__(self):
        pass

    def convert_pw(self, password):
        self.pass_key =  sum([int(bin(ord(i))[2::]) for i in password])
        self.pass_key = sum([int(i) for i in str(self.pass_key)])
        return int(self.pass_key)

    def convert_text_helper(self, pass_key):
        self.key = int(int(pass_key)**0.5)
        if (int(self.key) > 99 or int(self.key) < 23):
            print('Shared Key error')
            sys.exit()
        else :
            print('Shared Key is valid')
            return self.key
        
    def secret_message(self, lst, key):
        self.list = lst
        self.key = key
        self.message = ''.join(self.list)
        temp = self.message.strip().split(',')
        temp_1 = [chr(int(i) + self.key) for i in temp if i.isdigit()]
        return ''.join(temp_1)
