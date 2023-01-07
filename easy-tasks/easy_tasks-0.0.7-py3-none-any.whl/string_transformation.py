def upper_case_first_letter_of_word(String: str, lower_case_words: list = []):
    """Get a string with your string transformed to have the firts letter in upper case.

    Args:
        String (str): Your string to transform. (not in place)
        lower_case_words (list, optional): List of words which should allways be in lower case. Defaults to [].

    Returns:
        string: AThe transformed string.
    """
    wörter = String.split(" ")
    _ws = []
    for w in wörter:
        dw = ""
        for iw, cw in enumerate(w):
            if iw == 0:
                dw += cw.upper()
            else:
                dw += cw
        if w.lower() in [w.lower() for w in lower_case_words]:
            dw = w.lower()
        _ws.append(dw)
    dn = " ".join(_ws)
    return dn


def upper_case_first_letter_of_words(List: list[str], lower_case_words: list = []):
    """Get a list with the strings transformed to have the firts letter in upper case in your list.

    Args:
        Liste (list[str]): Your list of strings to transform. (not in place)
        lower_case_words (list, optional): List of words which should allways be in lower case. Defaults to [].

    Returns:
        list: A list containing the transformed strings.
    """
    result = []
    for n in List:
        dn = upper_case_first_letter_of_word(n, lower_case_words)
        result.append(dn)
    return result
