# main.py
# Text formatting using Minecraft color codes.
# https://github.com/woidzero/MCFC.git

from __future__ import annotations

import os
import sys


if sys.platform.lower() == "win32": 
    os.system('color')


DARK_RED = '\033[31m'
DARK_GREEN = '\033[32m'
DARK_YELLOW = '\033[33m'
DARK_BLUE = '\033[34m'
DARK_PURPLE = '\033[35m'
DARK_AQUA = '\033[36m'

BLUE = '\033[94;1m'
GREEN = '\033[92;1m'
AQUA = '\033[36;1m'
RED = '\033[31;1m'
PURPLE = '\033[35;1m'
YELLOW = '\033[33;1m'

DARK_GRAY = '\033[30;1m'
BLACK = '\u001b[38;5;235m'
GRAY = '\u001b[38;5;250m'
WHITE = '\u001b[38;5;255m'

RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\u001b[4m'
STRIKETHROUGH = '\033[9m'
ITALIC = '\033[3m'

colorCodes = {
    "&0": BLACK,          "&f": WHITE,
    "&8": DARK_GRAY,      "&7": GRAY,
    "&1": DARK_BLUE,      "&9": BLUE,
    "&2": DARK_GREEN,     "&a": GREEN,
    "&3": DARK_AQUA,      "&b": AQUA,
    "&4": DARK_RED,       "&c": RED,
    "&5": DARK_PURPLE,    "&d": PURPLE,
    "&6": DARK_YELLOW,    "&e": YELLOW,
    "&r": RESET,
    "&l": BOLD,
    "&n": UNDERLINE,
    "&m": STRIKETHROUGH,
    "&o": ITALIC
}


def echo(*values, sep: str = ' ', end: str = "\n") -> None:
    """Prints the colored text to a stream, or to sys.stdout by default. 

    ### Arguments
    `sep` (str): 
        separator between strings. Defaults a space.
    `end` (str): 
        string appended after the last value. Defaults a newline.
    """
    text = sep.join(tuple(map(str, values)))

    for code in colorCodes:
        text = text.replace(code, RESET + colorCodes[code])

    sys.stdout.write(u"{}".format(text) + RESET + end)


def info():
    """
    Prints all available formatting codes.
    """
    echo("""
        Formatting code must start with &    
            
    &00            &88            &77            &ff
    &11            &99            &22            &aa
    &33            &bb            &44            &cc
    &55            &dd            &66            &ee

    &rr (reset)&r                 &ll (bold)      
    &nn (underline)&r             &oo (italic)
    &mm (strikethrough)&r
    """)
