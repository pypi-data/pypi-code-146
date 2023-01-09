import argparse
import os
from typing import AnyStr, Iterable, Optional

from .count_func import func_count, len_func
from .exception import MyException


def condition_func(args: Optional) -> Optional:
    if not args.file and not args.string:
        raise MyException('Use the --help command to continue')
    if args.file:
        read_file = open_file(args.file)
        return len_func(read_file)
    return func_count(args.string)


def open_file(input_file: AnyStr) -> Iterable:
    if not isinstance(input_file, str):
        raise MyException('The data type error')
    elif not os.path.isfile(input_file):
        raise MyException('This file do not exist')
    else:
        with open(input_file) as data:
            return data.read()


def args_func() -> Optional:

    parser = argparse.ArgumentParser(description='A brief overview of functions')

    parser.add_argument('--file', help='Open and reading file')
    parser.add_argument('--string', type=str, help='Calculating characters for string')

    args = parser.parse_args()

    return args
