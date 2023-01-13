"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Scytale:
    To encrypt a message, the message is written on a strip of paper or a stick
    and wrapped around the cylindrical object using the keyword to determine the
    number of columns. The message is then read across the columns, from top to 
    bottom. The result is an encrypted message in which the letters appear in a 
    different order than in the original message.

    To decrypt the message, you need to know the keyword used to encrypt it, since
    it determines the number of columns and the order in which the letters must be read.

See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""

# --------------------APP--------------------
class Scytale:

    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    def encrypt(message:str, keyword:str):

        assert check_keyword(keyword), ValueError("Invalid keyword. Please enter a valid keyword.\nDo not repeat letters in the keyword.")
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(keyword, str), TypeError("The keyword argument must be a string.")

        generated_alphabet = generate_alphabet(keyword)

        cipher_text = ""

        for char in str(message.upper()):
            if char.isalpha():cipher_text += generated_alphabet[char]
            else:cipher_text += char

        return cipher_text
      
    def decrypt(message:str, keyword:str):

        assert check_keyword(keyword), ValueError("Invalid keyword. Please enter a valid keyword.\nDo not repeat letters in the keyword.")
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        assert isinstance(keyword, str), TypeError("The keyword argument must be a string.")
        
        generated_alphabet = generate_alphabet(keyword)
        generated_alphabet = {val: key for key, val in generated_alphabet.items()}
         
        decrypted_text = ""

        for char in str(message.upper()):
            if char.isalpha():decrypted_text += generated_alphabet[char]
            else:decrypted_text += char

        return decrypted_text

def check_keyword(input):
        list_keyword_input = []
        for letter in input:
            if letter in list_keyword_input:return False
            else:list_keyword_input.append(letter)
        return True

def generate_alphabet(keyword):
        alphabet = []
        for char in keyword:alphabet.append(char.upper())
        for letter in Scytale.alphabet:
            if letter in alphabet:pass
            else:alphabet.append(letter)

        dic_alphabet = {'A': alphabet[0], 'B': alphabet[1], 'C': alphabet[2], 'D': alphabet[3],
            'E': alphabet[4], 'F': alphabet[5], 'G': alphabet[6], 'H': alphabet[7], 
            'I': alphabet[8], 'J': alphabet[9], 'K': alphabet[10], 'L': alphabet[11],
            'M': alphabet[12], 'N': alphabet[13], 'O': alphabet[14], 'P': alphabet[15],
            'Q': alphabet[16], 'R': alphabet[17], 'S': alphabet[18], 'T': alphabet[19],
            'U': alphabet[20], 'V': alphabet[21], 'W': alphabet[22], 'X': alphabet[23],
            'Y': alphabet[24], 'Z': alphabet[25]}

        return dic_alphabet
            
