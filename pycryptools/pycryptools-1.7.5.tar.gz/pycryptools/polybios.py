"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Polybios:
    The Polybios cipher is a polyalphabetic substitution cipher technique that uses a 5x5 table 	 
    to assign a pair of numerical coordinates to each letter of the alphabet. The table is built 
    using a 5x5 matrix where the letters of the alphabet are placed in a specific order, rather 
    than in alphabetical order.

See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""

# --------------------APP--------------------
class Polybios:

    def encrypt(message:str):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        
        polybios_table = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J'],
            ['K', 'L', 'M', 'N', 'Ñ'],
            ['O', 'P', 'Q', 'R', 'S'],
            ['T', 'U', 'V', 'W', 'X'],
            ['Y', 'Z']
        ]

        message = message.upper()

        ciphertext = ""

        for char in message:

            if char == " ":ciphertext += " "

            elif char in [polybios_table[i][j] for i in range(len(polybios_table)) for j in range(len(polybios_table[i]))]:

                alphabet_index = "ABCDEFGHIJLMNÑOPQRSTUVWXYZ".index(char)
                num1 = alphabet_index // 5 + 1
                num2 = alphabet_index % 5 + 1
                ciphertext += str(num1) + str(num2)

            else:ciphertext += char

        return ciphertext


    def decrypt(encrypt_message:int):
        
        assert isinstance(encrypt_message, str), TypeError("The encrypt message argument must be int.")

        polybios_table = [
            ['A', 'B', 'C', 'D', 'E'],
            ['F', 'G', 'H', 'I', 'J'],
            ['L', 'M', 'N', 'Ñ', 'O'],
            ['P', 'Q', 'R', 'S', 'T'],
            ['U', 'V', 'W', 'X', 'Y'],
            ['Z']
        ]

        plaintext = ""

        for i in range(0, len(encrypt_message), 2):
            if i+1 < len(encrypt_message):
            
                if encrypt_message[i].isnumeric():num1 = int(encrypt_message[i]) - 1
                else:num1 = None

                if encrypt_message[i+1].isnumeric():num2 = int(encrypt_message[i+1]) - 1
                else:num2 = None

                if num1 is not None and num2 is not None:plaintext += polybios_table[num1][num2]

        return plaintext
