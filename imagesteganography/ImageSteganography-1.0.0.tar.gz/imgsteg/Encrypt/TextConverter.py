import sys

class Convert():

    def __init__(self):
        pass

   
    def convert_sum(self, password):
        self.pass_key =  sum([int(bin(ord(i))[2::]) for i in password])
        self.pass_key = sum([int(i) for i in str(self.pass_key)])
        #print(self.pass_key)
        return self.pass_key

    
    def convert_ascii(self, text):
        secret_message = [ord(i) for i in text]
        self.private_key = min(secret_message)
        self.message = [int(i-self.private_key) for i in secret_message]
        if self.private_key < 23 or max(self.message) > 99:
            print('Error encrypting')
            sys.exit()
        print('Your private key is: ',(self.private_key)**2)
        #print(self.message)
        return self.message
