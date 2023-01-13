"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Jefferson Wheel:
    The Jefferson Wheel Cipher is a mechanical encryption device that uses a set of rotating disks to encrypt
    and decrypt messages. Each disk has the alphabet written on it in a different order, and the order of the
    disks can be changed to create a unique encryption key.
    
See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""
# --------------------Extern Import--------------------
import random
from typing import List

# --------------------APP--------------------
class Jefferson:
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    disks = ["ZYXWVUTSRQPONMLKJIHGFEDCBA", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "QWERTYUIOPASDFGHJKLZXCVBNM"]

    def encrypt(message:str, disks:list = disks):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(disks, list), TypeError("The disks argument must be a list.")
        
        message = message.upper()
        ciphertext = ""
        
        for i, letter in enumerate(message):
            
            if letter in Jefferson.alphabet:ciphertext += disks[i % len(disks)][Jefferson.alphabet.index(letter)]
            else:ciphertext += letter
                
        return ciphertext

    def decrypt(message:str, disks:list = disks):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(disks, list), TypeError("The disks argument must be a list.")
        
        message = message.upper()
        plaintext = ""
        
        for i, letter in enumerate(message):
            
            if letter in Jefferson.alphabet:plaintext += Jefferson.alphabet[disks[i % len(disks)].index(letter)]
            else:plaintext += letter
                
        return plaintext
    
    def generate_disks() -> List[str]:
        
        disks = []
        
        for _ in range(3):
            
            disk = ''.join(random.sample(Jefferson.alphabet, len(Jefferson.alphabet)))
            disks.append(disk)
            
        return disks
    