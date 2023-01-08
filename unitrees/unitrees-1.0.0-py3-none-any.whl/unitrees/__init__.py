import sys

# Important!!
# This module uses recrusive functions to print the unicode trees!! 
sys.setrecursionlimit(999999)

version = '1.0.0'
author = 'Pigeon Nation'
block = '█'
characters_thick = [
    '┣', '┓', '┛', '┃', '━'
]

characters_thin = [
    '├', '┐', '┘', '│', '─'
]

characters_unicode = [
    '+', '\\', '/',  '|', '-'
]

characters_alt = [
    ',', '[', ']', '"', '?'
]

characters_dubl = [
    '╠', '╗', '╝', '║', '═'
]

characters_audiowaves = [
    '.', '..', '...', '....', '..... '
]

class ModeError(BaseException):
    pass

def visual_standard(data, charset=characters_thin, depthpad='', nl='\n', startend=True):
    out = charset[1] + '\n' if startend == True else ''
    for i in data:
        if type(i) == str:
            out += depthpad + charset[0] + charset[4] + i + nl
        elif type(i) == list or type(i) == tuple:
            out += depthpad + charset[0] + charset[1] + nl
            out += visual_standard(i, charset, depthpad=depthpad + charset[3], startend=False)
            out += depthpad + charset[0] + charset[2] + nl
    return out + (charset[2] + '\n' if startend == True else '')
            
def visual_space(data, space=' ', depthpad='', nl='\n'):
    out = ''
    for i in data:
        if type(i) == str:
            out += depthpad + i + nl
        elif type(i) == list or type(i) == tuple:
            out += visual_space(i, space, depthpad + space)
    return out

def visual_ascii(data, depthpad='', nl='\n'):
    out = ''
    for i in data:
        if type(i) == str:
            out += depthpad + '+' + '-' + i + nl
        elif type(i) == list or type(i) == tuple:
            out += depthpad + '+' + '\\' + nl
            out += visual_ascii(i, depthpad + '|')
            out += depthpad + '+' + '/' + nl
    return out