"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Alberti disk:
    The Alberti disk is a mechanical device used to encrypt and decrypt messages using the polyalphabetic
    substitution cipher. It was invented by the Italian humanist and scientist Leon Battista Alberti in
    the 15th century. The disk consists of two overlapping wheels, each with an alphabet printed on its
    rim. The top wheel, known as the recorder wheel, is free to rotate and has a hole in the center through
    which the bottom wheel, known as the decryption wheel, can be seen.
    
See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""

# --------------------APP--------------------
class Alberti:
    
    outer_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    inner_alphabet = "XZYWVUTSRQPONMLKJIHGFEDCBA"

    def encrypt(message:str, inner_alphabet:str or list=inner_alphabet, outer_alphabet:str or list=outer_alphabet):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(inner_alphabet, str), TypeError("The message argument must be a string or list.")
        assert isinstance(outer_alphabet, str), TypeError("The message argument must be a string or list.")
        assert check_alphabets(inner_alphabet, outer_alphabet), ValueError("Invalid Alphabets. Please enter a valid alphabet.\nBoth alphabets must be the same length")
        
        ciphertext = ""
        
        for char in message:
            
            if char.isalpha():
                
                outer_index = outer_alphabet.index(char.upper())
                ciphertext += inner_alphabet[outer_index]
                
            else:ciphertext += char
            
        return ciphertext
        
    def decrypt(message:str, inner_alphabet:str or list=inner_alphabet, outer_alphabet:str or list=outer_alphabet):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(inner_alphabet, str), TypeError("The message argument must be a string or list.")
        assert isinstance(outer_alphabet, str), TypeError("The message argument must be a string or list.")
        assert check_alphabets(inner_alphabet, outer_alphabet), ValueError("Invalid Alphabets. Please enter a valid alphabet.\nBoth alphabets must be the same length")
        
        plaintext = ""
        
        for char in message:
            
            if char.isalpha():
                
                inner_index = inner_alphabet.index(char.upper())
                plaintext += outer_alphabet[inner_index]
                
            else:plaintext += char
            
        return plaintext

def check_alphabets(inner_alphabet:str or list=Alberti.inner_alphabet, outer_alphabet:str or list=Alberti.outer_alphabet):

    inner_alphabet = [char for char in inner_alphabet]
    outer_alphabet = [char for char in outer_alphabet]
    
    if len(outer_alphabet) != len(inner_alphabet):return False
    elif len(inner_alphabet) == 26:
        
        alphabets = [inner_alphabet,outer_alphabet]
        
        for list in alphabets:
            
            letter_set = set(list)
            
            if len(letter_set) == len(list):return True
            else:return False
    