# -*- Coding: utf-8 -*-

# col spanish. encrypt
# version 0.0.4

# ---- List of functions ----

# 1. set_characters
# 2. create_dictionary
# 3. generate_pass

dict_lists = {
    '0':['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p',
        'q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G',
        'H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W',
        'X','Y','Z'],
    '1':['0','1','2','3','4','5','6','7','8','9'],
    '2':['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o',
                'p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G',
                'H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W',
                'X','Y','Z','0','1','2','3','4','5','6','7','8','9','!','¡','(',')',
                '-','.','?','¿','[',']','_','´','~',';',':','@','#','$','%','&','^',
                '/','+','*','|','°','=',',','>','<'],
}

def set_characters(sentence):
    """
    delete duplicate characters inside the sentence. save it in the same order, 
    as it appears in the sentence not in an aleatory order as set()
    
    Params:
    ------
    *sentence : string : sentence where the duplicates will be eliminated

    Usage:
    ------
    >>> from col_spanish import set_characters
    >>> set_characters('sentence')
    """
    sentence = sentence.replace(" ","")
    
    sentence_list = []
    for character in sentence:
        if character not in sentence_list:
            sentence_list.append(character)
    
    return sentence_list


def create_dictionary(key_list:list, value_list:list):
    """
    Recieves two lists and create a dictionary, both of the lists should have
    the same length.
    
    Params: 
    ------
    key_list : list : list that will work as the keys inside the dictionary
    value_list : list : list that contains the values that we want to call with the keys

    Usage:
    ------
    >>> from col_spanish import create_dictionary
    >>> key_list = ['k','h','l','p']
    >>> value_list = ['8','d','g','a']
    >>> create_dictionary(key_list, value_list)

    """
    
    # check that the two list have the same length and are not empty
    if len(key_list) < 1 or key_list is None:
        return 'key_list param should be a list with a length bigger than 1'
    if len(value_list) < 1 or value_list is None:
        return 'value_list param should be a list with a length bigger than 1'
    
    key_dictionary = {}
    for idx, character in enumerate(value_list):
        dict_append = {f'{key_list[idx]}':f'{character}'}
        key_dictionary.update(dict_append)
    
    return key_dictionary


def generate_pass(option:int, sentence:str, password:str, encrypt:int):
    
    """
    This function create a safe encrypted version of any password that you have.
    
    Params:
    ------
    * option : int : 0. only letters, 1. only numbers and 2. any character
    * sentence : str : a sentence that will be the key to lock and unlock the password
    * password : str : password to encrypt
    * encrypt : int : 0. encrypt, 1. decrypt

    Usage:
    ------
    >>> from col_spanish import generate_pass
    >>> generate_pass(2, 'sentence', 'password', 0)
    """
    
    # checking the options is inside the available options
    if int(option) in [0,1,2]:
        pass
    else: 
        return "the option is not inside the valide options. 0,1,2"
    
    # checking that there is a sentence to create the password encription
    if len(sentence) < 1:
        return "you need to write a sentence to be able to encrypt the password"
    
    # checking that there is a password to encrypt
    if len(password) < 1:
        return "you need to write a password to encrypt"
    
    # checking the encrypt param is inside the valide options
    if int(encrypt) in [0,1]:
        pass
    else:
        return "the encrypt value is not inside the valid options. 0,1"
    
    # delete blanck spaces
    sentence = sentence.replace(' ','')
    password = password.replace(' ','')
    
    # checking the option is according to the params
    if int(option):
        for character in sentence:
            if character not in dict_lists[f'{option}']:
                return "the option is not adecuate for the sentence you wrote"
        for character in password:
            if character not in dict_lists[f'{option}']:
                return "the option is not adecuate for the password"
        
    # delete duplicate inside the sentence to create the alphabet for the encryption
    set_sentence = set_characters(sentence)
    
    # create the new alphabet
    for character in dict_lists[f'{option}']:
        if character not in set_sentence:
            set_sentence.append(character)
            
    
    
    # create the encrypted or decrypted password
    if int(encrypt) == 0:
        
        # create a dictionary with the keys to encrypt the sentence/password
        key_dictionary = create_dictionary(dict_lists[f'{option}'], set_sentence)
        
        encrypted_password = ''
        for character in password:
            encrypted_password = f'{encrypted_password}{key_dictionary[character]}'
        
        return encrypted_password
    
    if int(encrypt) == 1:
        
        # create a dictionary with the keys to encrypt the sentence/password
        key_dictionary = create_dictionary(set_sentence,dict_lists[f'{option}'])
        
        decrypted_password = ''
        for character in password:
            decrypted_password = f'{decrypted_password}{key_dictionary[character]}'
    
        return decrypted_password