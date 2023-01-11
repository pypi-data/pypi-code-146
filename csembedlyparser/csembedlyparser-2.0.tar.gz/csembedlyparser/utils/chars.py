import re

def check_uppercase(text):
    if not text:
        return False
    words = re.split(u'\W+', text, re.UNICODE)
    for word in words:
        if not word.isupper():
            return False
    return True

def get_longest_string(list_of_strings):
    lo = 0
    lo_s = None
    for s in list_of_strings:
        if len(s) > lo:
            lo_s = s
            lo = len(s)
    return lo_s

