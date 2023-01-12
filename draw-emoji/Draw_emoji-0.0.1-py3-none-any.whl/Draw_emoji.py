# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 18:28:38 2023

@author: PorallaPradhyumna
"""
import re

class Draw_emoji:
    def __init__(self):
        self.Skins = [ '\U0001f3fb','\U0001f3fc','\U0001f3fd','\U0001f3fe','\U0001f3ff'	]
        return
    def extract_emojis(self,text):
        """
        

        Parameters
        ----------
        text : The input text which contains emojis.

        Returns
        -------
        A list of emojis present in the input 'text'.

        """
        
        text = str(text)
        encode_txt = text.encode()
        code = re.findall(r'\\x[a-zA-Z0-9][a-zA-Z0-9]',str(encode_txt))
        code = ("").join(code)
        codes = code.replace("\\x","")
        codes = bytes.fromhex(codes)
        codes = codes.decode()
        return [*codes]
    
    
    def extract_skintoned_emojis(self,text):
        
        """
        

        Parameters
        ----------
        text : The input text which contains emojis.

        Returns
        -------
        A list of skintonned emojis present in the input 'text'.

        """
        
        text = str(text)
        emojis = []
        for skin in self.Skins:
            indexes = [match.start() for match in re.finditer(r''+skin, text)]
            if indexes:
                for id in indexes:
                    if text[id] == skin:
                        e = "".join([text[id-1],text[id]])
                        emojis.append(e)
        return emojis
    
    def UnicodeExtractor(self,text):
        
        """
        

        Parameters
        ----------
        text : The input text which contains emojis.

        Returns
        -------
        A list of pair of emojis and ther unicodes.

        """
        
        ls=[]
        text = str(text)
        encode_txt = text.encode()
        code = re.findall(r'\\x[a-zA-Z0-9][a-zA-Z0-9]',str(encode_txt))
        code = ("").join(code)
        codes = code.replace("\\x","")
        codes = bytes.fromhex(codes)
        codes = codes.decode()
        emojis = codes
        codes = codes.encode('unicode-escape')
        codes = str(codes).split('\\\\')[1:]
        for code,emoji in zip(codes,emojis):
            val = {'unicode':code,'emoji':emoji}
            ls.append(val)
        if not ls:
            return "No emoji in text"
        
        return ls
