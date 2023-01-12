import re
import os
import random

class Substitute():
    """
    Substitue parameters in text using specified or randomly generated variables
    
    Defaults to recognising variables within double curly braces {{varname}}.
    
    Variable names beginning with rndpw (e.g. {{rndpw-xyz}} ) will be replaced
    with a random password of 10 characters. This will be consistent, so
    subsequent repalcements of the same varaiable name will get the same random
    password.
    """
    def __init__(self,regex=None,subs=None):
        """
        regex - is regular expression matching variable strings, must include
        a single capture group () which holds the name of the variable
        subs - is a dictionary with values for each variable
        """
        if regex:
            self.regex = regex  # regex for sub original
        else:
            self.regex = '\{\{([\w\-\_]+)\}\}'
        if subs:
            self.subs = subs
        else:
            self.subs = dict()  # store of variables to sub
    def sub(self,s):
        """
        Substitute variables in this string and return modified string
        """
        regex = re.compile('(.*)' + self.regex + '(.*)')
        chars = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        random.seed = (os.urandom(1024))
        done = False
        out = s
        while not done:
            var = re.sub(regex,r'\2',out)  # get variable string
            if var != out:  # did sub and now we have the first variable name
                m = re.match(regex, out) # capture before var, var, and after var
                if var in self.subs:
                    out = m.group(1) + self.subs[var] + m.group(3)
                elif var[0:3] == 'pw@':
                    # generate random password and store it
                    self.subs[var] = ''.join(random.choice(chars) for i in range(10))
                    # do substitution
                    out = m.group(1) + self.subs[var] + m.group(3)
            else:
                done = True
        return out
        
    def __str__(self):
        """
        Display variables, including any random passwords generated
        """
        lines = []
        for k in self.subs:
            lines.append(k + " : " + self.subs[k])
        return '\n'.join(lines)
        
