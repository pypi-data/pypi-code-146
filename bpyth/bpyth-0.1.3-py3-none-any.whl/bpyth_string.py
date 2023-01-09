
#############################################################################################################
###
### String
###
############################################################################################################# 

import random, string, re
from itertools          import zip_longest
from . import remove_dups
#print(remove_dups)

def superstrip(my_str):
    '''
    Convenient function
    * replaces all Unicode whitespaces with ASCII whitespace    
    * replaces multiple whitespaces with single whitespace
    * removes whitespaces at the beginning and at the end    
    '''
    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    return _RE_COMBINE_WHITESPACE.sub(" ", my_str).strip()
    

      
def remove_words( text, list_of_stopwords ):
    '''Removes stopwords'''
    list_of_stopwords = [re.escape(w) for w in list_of_stopwords]
    pattern = re.compile(r'\b(' + r'|'.join(list_of_stopwords) + r')\b\s*')
    return pattern.sub('', text)
    
    
    
def remove_dupwords(data,sep=' '):
    '''Removes dup words from a string whilst-preserving-order''' 
    return sep.join(remove_dups(data.split(sep)))    




def longest_substr(data):
    '''Finds the longest common substring in a list of strings'''
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr




def random_str(size=10, size_min=None, size_max=None, mix=string.ascii_letters):
    '''
    Returns a random string
    * size: desired length
    * size_min: desired minimum length
    * size_max: desired maximum length    
    * mix: Characters to use. 
      See https://docs.python.org/3/library/string.html
      e.g. mix = string.digits + string.punctuation + 'AAAAAAAAA'      
    '''
    if size_min or size_max  and  size_max!=0:
        size = random.randint(size_min,size_max)  

    result = ''.join(random.choice(mix) for x in range(size))
    return result



