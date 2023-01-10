'''encrypt(or decrypt) str'''

import base64
from Crypto import Random
from Crypto.Cipher import AES


BS = 16
pad = lambda s: s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ) )

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

def des(encrypted_data : str, key : list[int]) :
    decrypted_data = AESCipher(bytes(key)).decrypt(encrypted_data)
    decrypted_data.decode('utf-8')
    return decrypted_data

def ens(data : str, key : list[int]) :
    return AESCipher(bytes(key)).encrypt(data) 

def make_key(text : str = None , test : bool = False) :
    if text == None :   
        raise ValueError("Untyped variable: 'text'")
    if len(text) != 32 and test == False:
        raise ValueError("Text must be 32 characters")
    return [int(hex(ord(s)), 16) for s in text]
    
key = [0x18, 0x82, 0x19, 0x89, 0x91, 0x71, 0x38, 0x58, 0x10, 0x47, 0x89, 0x65, 0x86, 0x75, 0x26, 0x58,
        0x66, 0x44, 0x74, 0x72, 0x47, 0x11, 0x13, 0x30, 0x46, 0x13, 0x58, 0x28, 0x81, 0x55, 0x61, 0x23]
'''
default key
'''

# data encrypt : encrypted_data = AESCipher(bytes(key)).encrypt(data)  
# data decrypt : decrypted_data = AESCipher(bytes(key)).decrypt(encrypted_data)
#                decrypted_data.decode('utf-8')

