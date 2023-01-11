# -*- coding: utf-8 -*-
"""
===============
text_name_tools
===============
"""
from typing import Union
import re
import unidecode
import random
from string import punctuation
import gender_guesser.detector as gender
from nameparser import HumanName

d = gender.Detector(case_sensitive=False)


char_nb_map = {
    'a': ('a', '4', '@'),
    'b': ('b', '6', '8', 'I3', '13', '!3'),
    'c': ('c', '('),
    'd': ('d', ')', '!)', 'cl'),
    'e': ('e', '3', '€'),
    'f': ('f', '7', '/='),
    'g': ('g', '9', '6'),
    'h': ('h', '8', '#', '!-!'),
    'i': ('i', '1', '!'),
    'j': ('j', '1', '_)'),
    'k': ('k', '7'),
    'l': ('1', '!', '(_'),
    'm': ('m', 'nn', '(V)', '/VA'),
    'n': ('n', '/V'),
    'o': ('o', '0'),
    'p': ('p', '?'),
    'q': ('q', '9', '2', '()_'),
    'r': ('r', '8', '12'),
    's': ('s', '5', '$', '§'),
    't': ('t', '7', '+'),
    'u': ('u', '(_)'),
    'v': ('v',),
    'w': ('w', 'vv', 'uu'),
    'x': ('x', '><'),
    'y': ('y', '7', '?'),
    'z': ('z', '2', '7_')
}


def and_list(
    elements: list,
    et: str = 'and'
) -> str:
    """ creates a human-readable list, including "and"
    (or any similar word, i.e. in another language)
    """

    elements = [str(el) for el in elements]
    return re.sub(r', (\w+)$', r' {} \1'.format(et), ', '.join(elements))


NAME_PREFIXES = (
    'de',
    'del',
    'du',
    'la',
    'von',
    'van'
    'der'
)


def capitalize_name(
    text: str
) -> str:
    """ Capitalize name

    This is specially handy for names which otherwise
    would be capitalized wrongly with string's "title"
    method like:

       - Conan McArthur
       - Susanne Mayr-Grünwald
       - Maria de Angelis

    """
    return normalize_name(
        name=text,
        returning='str'
    )


def could_be_a_name(
    name: str = None,
    default: bool = True,
    prename: bool = False
) -> bool:
    """
    Checks if a string is possibly a name

    name is preferably a full name

    Checks:

    - is alpha (only alpha characters)
    - there are no two consecutive uppercase characters
    - last character in any word is not uppercase
    - gender can be determined for prename or middlename

    :param default: the default boolean value returned if no check was successfull
                    (neither positively nor negatively)
    :param prename: if True, a prename is acceptable (otherwise the full name is needed)
    """
    if not name.replace(
        ' ', ''
    ).replace(
        '-', ''
    ).isalpha():
        return False

    # 2 consecutive uppercase chars
    if re.search('[A-Z]{2}', name):
        return False

    human_name = normalize_name(
        name=name,
        returning='HumanName'
    )

    first = human_name.first
    middle = human_name.middle
    last = human_name.last

    if not prename and not last:
        return False

    for n in (first, middle, last):
        if not n:
            continue
        # last char is capital
        if n[-1].isupper():
            return False

        # more than 2 capitals
        if sum(1 for c in n if c.isupper()) > 2:
            return False

    for n in (first, middle):
        if get_gender(prename=n) != 'unknown':
            return True

    sum_upper = sum(1 for c in n if c.isupper())
    if sum_upper != len(n) and sum_upper > 1:
        return False

    return default


def get_gender(
    prename: str
) -> str:
    """ returns: male, female or unknown """
    gender = 'unknown'
    prenames = prename.replace('-', ' ').split()

    for n in prenames:
        gender = d.get_gender(n)
        if gender in ('male', 'female'):
            return gender

    return gender


def leet(
    text: str,
    max_length: int = None,
    change_uppercase: int = 4,
    symbol_chance: int = 0,
    start_at_begin: bool = True
) -> str:
    """ Leet a string

    leet any string

    :param symbol_chance: 1 out of n that a random symbol will be added
    """

    text = unidecode.unidecode(text).lower()  # remove Umlaute

    leeted_text = ''

    for c in text:
        if not c.isalnum():
            continue  # without counting

        c = random.choice(char_nb_map[c])

        if not random.randrange(change_uppercase):
            c = c.upper()

        leeted_text += c

        if symbol_chance and random.randrange(symbol_chance):
            leeted_text += random.choice(punctuation)

    if max_length and len(leeted_text) > max_length:
        if start_at_begin:
            leeted_text = leeted_text[:max_length]
        else:
            text_length = len(leeted_text)
            start_position = random.randint(1, int(text_length / 2))
            end_position = start_position + max_length
            leeted_text = leeted_text[start_position:end_position]

    return leeted_text


def sort_names(names: list) -> list:
    """ Sort names

    Sorts by name, prename: splits only at the last space before sorting

    Correctly sorts names

        - with special characters, like umlauts
        - combined names
        - names with prefixes (like de or von)

    examples:

        - Susanne Mayr-Grünwald
        - Maria de Angelis
        - Bea-Regina Hofstätter
        - Rafael
    """

    name_dict = {}

    for name in names:
        human_name = normalize_name(
            name=name,
            returning='HumanName'
        )

        first = human_name.first
        middle = human_name.middle
        last = human_name.last

        if not last:  # only prename
            last = first

        split_at = ' '
        for name_prefix in NAME_PREFIXES:
            if f' {name_prefix} ' in last:
                split_at = f' {name_prefix} '
            break

        last = split_at.join(
            name.rsplit(split_at, 1)[::-1]
        )

        name_dict[unidecode.unidecode(last).lower()] = name
        """
        split_at = ' '
        for name_prefix in NAME_PREFIXES:
            if f' {name_prefix} ' in name:
                split_at = f' {name_prefix} '
            break

        reversed_name = split_at.join(
            name.rsplit(split_at, 1)[::-1]
        )

        name_dict[unidecode.unidecode(reversed_name).lower()] = name
        """

    sort_list = list(name_dict)
    sort_list.sort()

    sorted_list = [name_dict.get(n) for n in sort_list]

    return sorted_list


def map_special_chars(
    text: str,
    sort: bool = False
) -> str:
    """ map special characters

    .. note:: Umlauts are even recognized if the do not use the appropriate characters but
              a vowel followed by a COMBINING DIAERESIS (U+0308) character instead.

    :param sort: case is preserved in any case. If you want lowercase, you have to feed
                 the function appropriately.
                 If sort is set to True, all character lengths are preserved.
    """
    text = normalize_text(text)

    intab = 'AAAÁÀÂÃ?aaaáàâãå?CCCCccccçDÐddEEEEEÉÈÊËeeeeeéèêëGGggÍÌÎÏíìîïÓÒÔóòôõøñÚÙÛúùûÝýÿ'

    if sort is False:
        outtab = 'AAAAAAAAaaaaaaaaaCCCCcccccDDddEEEEEEEEEeeeeeeeeeGGggIIIIiiiiOOOooooonUUUuuuYyy'

        transDict = {
            'ä': 'ae',
            'Ä': 'Ae',
            'ö': 'oe',
            'Ö': 'Oe',
            'ü': 'ue',
            'Ü': 'Ue',
            'ß': 'ss',
            'æ': 'ae',
            'Æ': 'Ae'
        }
    else:
        outtab = 'AAAAAAAAaaaaaaaaaCCCCcccccDDddEEEEEEEEEeeeeeeeeeGGggIIIIiiiiOOOooooonUUUuuuYyy'

        transDict = {
            'ä': 'a',
            'Ä': 'A',
            'ö': 'o',
            'Ö': 'O',
            'ü': 'u',
            'Ü': 'U',
            'ß': 's',
            'æ': 'a',
            'Æ': 'A'
        }

    for it, ot in zip(intab, outtab):
        transDict[it] = ot

    try:
        text + 1
        text = str(text)
    except Exception:
        pass

    # text = translate(text, transTable)
    for key in list(transDict.keys()):
        text = text.replace(key, transDict[key])

    return text


def normalize_text(
    text
):
    """ normalize text

    replace problematic (two-character) unicode characters
    """
    transDict = {
        'ä': 'ä',  # a and unicode cc 88 (), etc...
        'ö': 'ö',
        'ü': 'ü',
        'Ä': 'Ä',
        'Ö': 'Ö',
        'Ü': 'Ü'
    }

    for key in list(transDict.keys()):
        text = text.replace(key, transDict[key])

    return text


def normalize_name(
    name,
    returning: str = 'str'
) -> Union[str, dict, HumanName]:
    """ normalize name

    This function uses the nameparser package

    :param returning:
        - str: return the name as a string
        - dict: return a dictionary with the name elements
        - other: return the HumanName object from nameparser
    """
    parsed_name = HumanName(name)
    parsed_name.capitalize()

    if 'str' in returning:
        return str(parsed_name)
    elif 'dict' in returning:
        return parsed_name.as_dict()
    else:  # return the HumanName object
        return parsed_name


def sort_word_list(
    word_list: list
) -> list:
    """ sorts a list of words, taking into account special characters """

    sort_list = []
    val_dict = {}

    for word in word_list:
        trans = map_special_chars(word, sort=True).lower()

        sort_list.append(trans)
        val_dict[trans] = word

    sort_list.sort()

    new_word_list = []

    for w in sort_list:
        new_word_list.append(val_dict[w])

    return new_word_list
