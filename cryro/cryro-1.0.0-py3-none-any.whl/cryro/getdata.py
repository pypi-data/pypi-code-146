from bs4 import BeautifulSoup
import requests

prac_id = {
    1:'prac1',
    2:'prac2a',
    3:'prac2b',
    4:'prac2c',
    5:'prac3',
    6:'prac4',
    7:'prac5',
    8:'prac6a',
    9:'prac6b',
    10:'prac7',
    11:'prac8',
}

prac_name = {
    'prac1':"Salting",
    'prac2a':"substitution/shift cipher",
    'prac2b':"Vigenere Cipher",
    'prac2c':"Affine Cipher",
    'prac3':"Vigener Cipher",
    'prac4':"Advanced Encryption Standard (AES)",
    'prac5':"Steganography",
    'prac6a':"ElGamal cryptosystem",
    'prac6b':"Elliptic Curve Cryptography (ECC)",
    'prac7':"Hash-based Message Authentication Code (HMAC)",
    'prac8':"RSA",
}

prac_link = {
    'prac1':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/Prac1.py",
    'prac2a':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/Prac2a.py",
    'prac2b':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/Prac2b.py",
    'prac2c':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/Prac2c.py",
    'prac3':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/Prac3.py",
    'prac4':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/prac4/Prac4.py",
    'prac5':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/prac5/Prac5.py",
    'prac6a':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/prac6a.py",
    'prac6b':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/prac6b.py",
    'prac7':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/prac7.py",
    'prac8':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/prac8.py",
}

prac_desc_link = {
    'prac1':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac1",
    'prac2a':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac2a",
    'prac2b':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac2b",
    'prac2c':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac2c",
    'prac3':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac3",
    'prac4':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac4",
    'prac5':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac5",
    'prac6a':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac6a",
    'prac6b':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac6b",
    'prac7':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac7",
    'prac8':"https://raw.githubusercontent.com/BRAINIFII/cryptog/master/desc/prac8",
}

def extract(url):
    # url = "http://www.example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text

def get_desc(val):
    return extract(prac_desc_link[prac_id[val]])

def get_script(val):
    # print(prac_link[prac_id[val]])
    return extract(prac_link[prac_id[val]])

def get():
    for data in prac_id:
        print(data," - ",prac_name[prac_id[data]])
    pr = int(input("> "))
    final_script = get_script(pr)
    final_script_desc = get_desc(pr)

    req = input("s or d\n\n> ")
    if req == 'd':
        print(final_script_desc)
    else:
        print(final_script)