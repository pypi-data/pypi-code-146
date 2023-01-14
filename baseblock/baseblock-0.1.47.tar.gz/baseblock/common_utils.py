# -*- coding: utf-8 -*-


import traceback

from pathlib import Path


def odds_of(odds: int) -> bool:
    """ Help randomize decisions
        odds_of(20) gives a 20% chance of being True

    Returns:
        True: if a True value is selected
    """

    if odds == 0:
        return False
    if odds == 100:
        return True

    from random import randint

    MIN = 1
    MAX = 100

    if odds >= MAX:
        return True
    if odds <= MIN:
        return False

    return randint(MIN, MAX) <= odds


def prov_stack():
    """ Returns an Execution Stack Trace """

    stack = [str(x) for x in traceback.extract_stack()]

    stack = [[y for y in x.split(' ') if '.py' in y][0]
             for x in stack]  # reduce to python file only

    stack = [Path(x).name for x in stack]  # filename only

    stack = [x.replace(',', '') for x in stack]  # remove trailing commas

    stack = [x for x in stack if x != 'stack_utils.py']  # remove this call

    # remove duplicates without changing the order
    stack2 = []
    for x in stack:
        if x not in stack2:
            stack2.append(x)

    return stack2


def flatten_list(values: list) -> list:
    """ Flatten a List

    Args:
        values (list): a list of any nested proportion
        Sample Input:
            [
                [
                    [
                        'alpha'
                    ],
                    [
                        'beta'
                    ]
                ]
            ]

    Raises:
        ValueError: expects only lists and strings; other data types raise this error

    Returns:
        list: a flat list of strings
        Sample Output:
            [
                'alpha', 'beta'
            ]
    """
    if type(values) != list:
        raise ValueError(type(values))

    normalized = []

    def iter(item: object) -> None:
        if type(item) == str:
            normalized.append(item)
        elif type(item) == list:
            [iter(x) for x in item]
        else:
            raise ValueError(type(item))

    [iter(x) for x in values]

    return normalized
