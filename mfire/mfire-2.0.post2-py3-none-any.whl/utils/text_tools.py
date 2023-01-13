import re
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="text_tools.mod", bind="text_tools")


def start_sentence_with_capital(s: str) -> str:
    """
    Strip unecessary white space.
    Also start every sentence with a capital.
    Sentence should be ended by a point.
    Args:
        s (str): the input text.

    Returns:
        str: The output texte
    """
    sentence = []

    for x in s.split("."):
        x = x.strip()
        if len(x) == 0:
            continue
        if len(x) > 2:
            x = x[0].upper() + x[1:]
        sentence.append(x)
    final = ". ".join(sentence)
    final = re.sub(" +", " ", final)
    if s.endswith(".") or s.endswith(". "):
        final += "."

    return final


def modify_unit(s: str) -> str:
    return s.replace(" celsius", "°C")


def transforme_syntaxe(s: str) -> str:
    """transformation d'un texte pour éviter des erreurs de français dues aux templates

    Args:
        s (str): Texte à modifier

    Returns:
        str: Texte modifié
    """
    s = re.sub(r"jusqu.à en", "jusqu'en", s)
    s = re.sub(r"\.[ ]*\.", ".", s)  # Replaces ".." or ".   ." with "."
    s = re.sub(r"\,[ ]*\.", ".", s)  # Replaces ",." or ",   ." with "."
    s = re.sub(r"de en ce", "du", s)
    s = re.sub(r"de en milieu", "du milieu", s)
    s = re.sub(r"de en fin", "de la fin", s)
    s = re.sub(r"de aujourd'hui", "d'aujourd'hui", s)
    s = re.sub(r"de en première", "de la première", s)
    return s


if __name__ == "__main__":
    s1 = (
        "je suis un petit test.Et je suis pas trop content.     "
        "par contre... . .C'est vide ? et là pas de    majuscule."
        "et là on ne voit pas la phrase vide ? ."
        "mais qui met des ... ou des ? ou ! dans un bulletin ?"
        "ce test est historiquement incompréhensible, il doit le rester !"
    )
    print(start_sentence_with_capital(s1))
