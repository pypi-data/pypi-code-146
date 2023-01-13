"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

AtBash:
    Atbash is a monoalphabetic substitution encryption algorithm. This means that
    it uses a single substitution table to encode all the letters in the original 
    message. In the case of Atbash encryption, the substitution table is built from
    a given keyword and consists of reversing the order of the letters of the alphabet
    to substitute each letter of the original message.

See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""

# --------------------APP--------------------
class Atbash:

   atbash_alphabet = {'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U',
      'G': 'T', 'H': 'S', 'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O',
      'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K', 'Q': 'J', 'R': 'I',
      'S': 'H', 'T': 'G', 'U': 'F', 'V': 'E', 'W': 'D', 'X': 'C',
      'Y': 'B', 'Z': 'A'}

   def encrypt(message:str):

      assert isinstance(message, str), TypeError("The message argument must be a string.")

      cipher_text = ""

      for char in message.upper():
         if char.isalpha():cipher_text += Atbash.atbash_alphabet[char]
         else:cipher_text += char

      return cipher_text

   def decrypt(message:str):

      assert isinstance(message, str), TypeError("The message argument must be a string.")
         
      decrypted_text = ""

      for char in message.upper():
         if char.isalpha():decrypted_text += Atbash.atbash_alphabet[char]
         else:decrypted_text += char

      return decrypted_text
