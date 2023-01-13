"""
██╗    ██╗██╗   ██╗ █████╗ ██╗     
██║    ██║██║   ██║██╔══██╗██║     
██║ █╗ ██║██║   ██║███████║██║     (code by wual)
██║███╗██║██║   ██║██╔══██║██║     
╚███╔███╔╝╚██████╔╝██║  ██║███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

Morse Code:
    Morse code is a system of representing letters, numbers, and punctuation
    marks by means of a series of dots and dashes of variable length. It was 
    developed by Samuel Morse in the 19th century and was mainly used in telegraphy
    (telegraphing), to transmit messages through electrical signals.

    In Morse code, each letter, number, or punctuation mark is represented by a 
    unique pattern of dots and dashes. For example, the letter "A" is represented 
    by a dot followed by a dash, while the letter "N" is represented by three consecutive
    dashes. The space between letters is represented by a dot, while the space between 
    words is represented by three consecutive dots.
    
See proyect >> https://github.com/14wual/pycryptools
Follow me >> https://twitter.com/codewual
"""

# --------------------APP--------------------
class Morse:
    
    morse_code = { 'A':'.-', 'B':'-...',
        'C':'-.-.', 'D':'-..', 'E':'.',
        'F':'..-.', 'G':'--.', 'H':'....',
        'I':'..', 'J':'.---', 'K':'-.-',
        'L':'.-..', 'M':'--', 'N':'-.',
        'O':'---', 'P':'.--.', 'Q':'--.-',
        'R':'.-.', 'S':'...', 'T':'-',
        'U':'..-', 'V':'...-', 'W':'.--',
        'X':'-..-', 'Y':'-.--', 'Z':'--..',
        '1':'.----', '2':'..---', '3':'...--',
        '4':'....-', '5':'.....', '6':'-....',
        '7':'--...', '8':'---..', '9':'----.',
        '0':'-----', ', ':'--..--', '.':'.-.-.-',
        '?':'..--..', '/':'-..-.', '-':'-....-',
        '(':'-.--.', ')':'-.--.-'}

    def encrypt(message:str):
        
        assert isinstance(message, str), TypeError("The message argument must be a string.")
        
        morse_text = ""
        message = message.upper()
        
        for letter in message:
            
            if letter != " ":morse_text += Morse.morse_code[letter] + " "
            else:morse_text += " "
            
        return morse_text

    def decrypt(morse_message:str):
        
        assert Morse.valid_morse(morse_message), ValueError("Invalid String. Strings should only be composed of ['.(points)','_(low bar)',' (spaces)']")
        
        morse_code = {value:key for key,value in Morse.morse_code.items()}
        
        text = ""
        morse_text = morse_text.split(" ")
        
        for letter in morse_text:
            
            if letter != "" and letter != " ":text += morse_code[letter]
            else:text += " "
            
        return text
    
    def valid_morse(morse_text):
        
        for letter in morse_text:
            if letter != "." and letter != "-" and letter != " ":return False
            
        return True