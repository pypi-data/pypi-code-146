# -*- Coding: utf-8 -*-

# col spanish
# version 0.0.4

# ---- List of functions ----

# del_punctuation
# del_accent

delete_punctuation_dict = {
    "¿": "",
    "?": "",
    "!": "",
    "¡": "",
    '"': "",
    "(": "",
    ")": "",
    "/": "",
    "*": "",
    ",": "",
    ".": "",
    "-": "",
    "*": "",
    ":": "",
    "…": "",
    "#": "",
    "@": "",
    "'": "",
    "|": "",
    "“": "",
    "”": "",
    "%": "",
    "&": "",
    "_": "",
}

delete_accent_dict = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u"}

# clean the text, delete punctuation marks
def del_punctuation(text):
    """
    Function to delete all the punctuation marks that are inside a text

    Params:
    ------
    text: str : text to be clean

    Usage:
    ------
    >>> from col_spanish import del_punctuation
    >>> text = 'hola, este es un texto! que necesita? remover signos de puntuacion!!'
    >>> del_punctuation(text)
    """
    new_text = ""
    words = text.split()
    for wl in words:
        # delete punctuation marks to keep only words
        for punctuation, new_value in delete_punctuation_dict.items():
            wl = wl.replace(punctuation, new_value)
        # add the words without punctuation marks to the final text
        new_text += f"{wl} "

    return new_text[:-1]


# clean the text, delete accents
def del_accent(text):
    """
    Function to delete accents from the text

    Params:
    ------
    text: str : text to be clean

    Usage:
    ------
    >>> from col_spanish import del_acce
    >>> text = 'hola, este es un texto! que necesita? remover signos de puntuacion!!'
    >>> del_acce(text)
    """
    new_text = ""
    words = text.split()
    for w in words:
        wl = w.lower()
        # delete accent mark
        for accent, new_value in delete_accent_dict.items():
            wl = wl.replace(accent, new_value)
        # add the words without punctuation marks to the final text
        new_text += f"{wl} "

    return new_text[:-1]
