import random

def madlib_peom(color,noun,name):
    print("Roses are ",color)
    print(noun," is blue")
    print("I love ", name)

def roll_dice():
    number = random.randint(1,6)
    print(number)

def password():
    char_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    password = ''

    for len in range(8,16):
        random_char = random.choice(char_seq)
        password += random_char
    print(password)

