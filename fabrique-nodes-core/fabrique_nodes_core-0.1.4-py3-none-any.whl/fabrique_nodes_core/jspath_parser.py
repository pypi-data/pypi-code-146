import re

num_exp = re.compile(r"\[([0-9]+)\]")
code_validator = re.compile(r"\w+(\[\d+\])?\.?")


def _level_wo_brackets(level: str) -> str:
    """returns level wo brackets ('level[1]' -> 'level')

    :param level: level
    :type level: str
    :return: level wo brackets
    :rtype: str
    """
    return level.split('[')[0]


def _index_in_level(level: str) -> int | None:
    """ returns index of current level ('.'-separeted substring of path code)

    :param level: '.'-separeted substring of path code
    (in code 'level0.level1[0].level2', is one of ['level0', 'level1[0]', 'level2'])
    :type level: str
    :return: number in [], if level has one
    :rtype: int | None
    """
    nums = num_exp.findall(level)
    if not nums:
        return None
    else:
        return int(nums[0])


def _make_list(lst: list, ind: int) -> list:
    """extends the list if its length is not enough to store the ind-th element

    :param lst: list to extend
    :type lst: list
    :param ind: index of element
    :type ind: int
    :return: extended (or same) list
    :rtype: list
    """
    if len(lst) > ind:
        return lst
    inc = ind + 1 - len(lst)
    return lst + [None] * inc


def upd_output(init_dict: dict, code: str, value):
    """Injects 'value' in 'init_dict' by path in 'code'

    :param init_dict: dict to modify
    :type init_dict: dict
    :param code: path for value
    :type code: str
    :param value: value to set
    """
    if not isinstance(init_dict, dict):
        init_dict = {}

    levels = code.split('.')
    last_level = len(levels) - 1
    cursor = init_dict

    for i, level in enumerate(levels):
        clean_level = _level_wo_brackets(level)
        index = _index_in_level(level)
        if index is not None:
            expected_type = list
            empty_val = []
        else:
            expected_type = dict
            empty_val = {}

        if clean_level not in cursor or not isinstance(cursor[clean_level], expected_type):
            cursor[clean_level] = empty_val

        if index is not None:

            if not isinstance(cursor[clean_level], list):
                # print(cursor[clean_level])
                cursor[clean_level] = []
            cursor[clean_level] = _make_list(cursor[clean_level], index)
            if i == last_level:
                cursor[clean_level][index] = value
                break

            if not isinstance(cursor[clean_level][index], dict):
                cursor[clean_level][index] = {}

            cursor = cursor[clean_level][index]
            continue

        if i == last_level:
            cursor[clean_level] = value
            break

        cursor = cursor[clean_level]


def is_valid_code(code: str) -> bool:
    """validate jspath code

    :param code: code to validate
    :type code: str
    :return: True if code is valid
    :rtype: bool
    """
    if not code:
        return False
    matched = ''.join([m.group() for m in code_validator.finditer(code)])
    return len(matched) == len(code)
