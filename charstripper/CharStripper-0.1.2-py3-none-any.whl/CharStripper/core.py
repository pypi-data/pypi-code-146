"""
This is the CharStripper, allows you to strip and lowercase the any text. Written by yagiziskirik.

Usage:
from CharStripper.core import CharStripper
cs = CharStripper({'o': 'e', 'r': 't', ' ': ''}, True)
cs.strip('Bo aR L  OS')  # returns 'beatles'
"""
class CharStripper:
    """
    charsDict: [dictionary] Defines the dictionary that the characters will be replaced:
    - {'a': 'b'}
    isLowercase: [boolean] Gives you the opportunity to lower the entire word in the end.
    """
    def __init__(self, charsDict, isLowercase=False):
        self._isLowercase = isLowercase
        self._charsDict = charsDict

    def _replaceChars(self, txt):
        return "".join([self._charsDict.get(c, c) for c in txt])

    def _checkIfAnyCharactersInList(self, txt):
        tList = list(self._charsDict.keys())
        for c in txt:
            if c in tList:
                return True
        return False

    """
    text: [string] Value you want to strip.
    """
    def strip(self, text):
        if self._checkIfAnyCharactersInList(text):
            return self._replaceChars(text).lower() if self._isLowercase else self._replaceChars(text)
        return text.lower() if self._isLowercase else text
