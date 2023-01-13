"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Caesar:
    The Caesar cipher is a single substitution cipher method in which each letter in the original
    text is replaced by another letter that is a fixed number of positions later in it. This fixed
    number is known as the encryption key. For example, if the key is 3, then 'A' is replaced with
    'D', 'B' is replaced with 'E', and so on. The registered Caesar is one of the earliest and simplest
    known methods.
    
See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""

# --------------------APP--------------------
class Caesar:

    def encrypt(message:str, keyword:int):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(keyword, int), TypeError("The message argument must be int.")
        assert check_keyword(keyword), ValueError("Invalid keyword. Please enter a valid keyword.\nThis cannot be a negative number or greater than 26.")
        
        ciphertext = ""
        
        for char in message:
            
            if char.isalpha():
                
                shift = ord(char) + keyword
                
                if char.isupper():ciphertext += chr((shift - 65) % 26 + 65)
                else:ciphertext += chr((shift - 97) % 26 + 97)
                
            else:ciphertext += char
            
        return ciphertext
    
    def decrypt(message:str, keyword:int):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(keyword, int), TypeError("The message argument must be int.")
        assert check_keyword(keyword), ValueError("Invalid keyword. Please enter a valid keyword.\nThis cannot be a negative number or greater than 26.")
        
        plaintext = ""
        keyword = -keyword
        
        for char in message:
            
            if char.isalpha():
                
                shift = ord(char) + keyword
                
                if char.isupper():plaintext += chr((shift - 65) % 26 + 65)
                else:plaintext += chr((shift - 97) % 26 + 97)
                
            else:plaintext += char
            
        return str(plaintext.upper())
        
def check_keyword(keyword:int):
    
    if keyword < 0 or keyword > 26:return False
    elif keyword == str: return False
    elif keyword == float:return False
    else:return True
    