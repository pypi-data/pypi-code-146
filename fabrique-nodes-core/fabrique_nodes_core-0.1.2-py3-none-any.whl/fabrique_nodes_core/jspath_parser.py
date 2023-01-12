import re

num_exp = re.compile(r"\[([0-9]+)\]")
code_validator = re.compile(r"\w+(\[\d+\])?\.?")


def level_wo_brackets(level: str):
    return level.split('[')[0]


def index_in_level(level):
    nums = num_exp.findall(level)
    if not nums:
        return None
    else:
        return int(nums[0])


def make_list(lst, ind):
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
        clean_level = level_wo_brackets(level)
        index = index_in_level(level)
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
                print(cursor[clean_level])
                cursor[clean_level] = []
            cursor[clean_level] = make_list(cursor[clean_level], index)
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


def is_valid_code(code: str):
    if not code:
        return False
    matched = ''.join([m.group() for m in code_validator.finditer(code)])
    return len(matched) == len(code)
