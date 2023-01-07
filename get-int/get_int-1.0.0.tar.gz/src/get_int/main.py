
def valid_int(possible_num):
    '''Checks to make sure possible_num is in valid integer format.
    param: possible_num is a string that should be a valid integer.
    returns: True if possible_num is a valid integer, otherwise False.
    '''
    if len(possible_num) == 0: #it's an empty string.
        return False
    elif possible_num[0] == "-":
        #Neg. sign in right spot. Check everything else.
        possible_num = possible_num[1:] #Slice the neg. sign keep everything else.    
        if possible_num == "": #just in case it's just a neg sign which we sliced.
            return False
    for c in possible_num:
        
        if c not in "1234567890":
            return False #we found a non-integer character
        
    return True #got to the end and all characters check out.

def get_int(prompt):
    '''Shows the prompt and only gets valid integers from the user.
    param: prompt - string - the prompt that is shown to the user.
        returns: the integer value that the user types in.'''
    val = input(prompt)
        
    while valid_int(val) == False:
        print("Type in a valid integer.")
        val = input(prompt)
            
    return int(val)#val is proper int format. Cast it to an int and return it.
