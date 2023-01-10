'''crypt file module'''

from cryptography.fernet import Fernet
import os

def make_bkey() :
    return Fernet.generate_key()

def encfile(file_name : str, key : bytes = Fernet.generate_key(), 
            extension : str = '.enc') :
    print(f'''---------------warning---------------
You must remember this.
If you don't put anything in the key value, 
you can't decrypt the file forever.
If you can touch the code and not just 
try to use it, use this key.
key : {key}
---------------warning---------------''')
    f = Fernet(key)
    with open(file_name, 'rb') as original_file :
        original = original_file.read()
    encrypted = f.encrypt(original)
    os.path.splitext(file_name)[0]
    with open(file_name + extension, 'wb') as encrypted_file :
        encrypted_file.write(encrypted)
    return 1
    
def decfile(file_name : str, key : bytes, origin_extension : str) :
    f = Fernet(key)
    with open(file_name, 'rb') as encrypted_file :
        encrypted = encrypted_file.read()
    os.remove(file_name)
    decrypted = f.decrypt(encrypted)
    os.path.splitext(file_name)[0]
    with open(file_name + origin_extension, 'wb') as decrypted_file :
        decrypted_file.write(decrypted)
    




