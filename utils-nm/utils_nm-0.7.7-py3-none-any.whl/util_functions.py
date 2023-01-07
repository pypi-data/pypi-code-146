# util_functions.py
# -*- coding: utf-8 -*-

"""
Functions which serve for general purposes
"""

import os
import sys
import psutil
from pathlib import Path

import re

import typing
import inspect

from colorama import (
    Fore,
    Style,
)

import logging
import warnings
import traceback

from datetime import datetime, timedelta


# ______________________________________________________________________________________________________________________


def print_yellow(*args, **kwargs) -> None:
    """
    colors the text yellow which will be printed

    Args:
        *args: arguments with are passed on to the builtin print function
        **kwargs: keyword arguments with are passed on to the builtin print function

    Returns:
        None, but prints the text in yellow
    """
    sep = kwargs.pop('sep', ' ')
    original_string = sep.join(str(stmt) for stmt in args)
    print(f'{Fore.YELLOW}{original_string}{Style.RESET_ALL}', **kwargs)


# ______________________________________________________________________________________________________________________


def input_yellow(prompt: str) -> str:
    """
    colors the text yellow which will be printed by the prompt for input

    Args:
        prompt: the argument which will be passed on to the builtin function input

    Returns:
        the user input
    """
    return input(f'{Fore.YELLOW}{prompt}{Style.RESET_ALL}')


# ______________________________________________________________________________________________________________________


def determine_main_script_path() -> str:
    """
    Determines the path of the main script using psutil.Process().cmdline()

    Returns:
        a pathlib.Path object with the path to the main script
    """
    args = psutil.Process().cmdline()
    if len(args) > 1:
        path = args[1]
    else:
        path = args[0]
    return path


def runs_in_repl_mode() -> bool:
    """
    Determines if the execution is in repl (read-evaluate-print-loop) mode.

    Returns:
        True if reple else False
    """
    return hasattr(sys, 'ps1') or Path(determine_main_script_path()).name == 'pydevconsole.py'


# ______________________________________________________________________________________________________________________


def add_to_namespace(name: str, value: object, namespace: dict) -> None:
    """
    adds a variable to the namespace

    Args:
        name: the name of the variable
        value: the value of the variable
        namespace: the namespace where it should be added

    Returns:
        None
    """

    if name in namespace:
        warnings.warn(
            f'Function <{inspect.currentframe().f_code.co_name}>: '
            f'overwriting <{name}> which already existed in the namespace!'
        )
    namespace[name] = value
    return None


# ______________________________________________________________________________________________________________________


def check_if_in_argv(arg, argument) -> bool:
    """
    checks if -arg or --argument is in sys.argv

    Args:
        arg: the name of the argument in short notation
        argument: the name of the argument in verbose notation

    Returns:
        True if the argument is part of argv, else False
    """
    import sys
    return f'-{arg}' in sys.argv or f'--{argument}' in sys.argv


# ______________________________________________________________________________________________________________________


def parse_bool(arg: str) -> bool:
    """
    parse a script argument to a boolean value

    Args:
        arg: the input argument

    Returns:
        Boolean value of arg
    """
    inp = str(arg).lower()
    if 'true'.startswith(inp):
        return True
    elif 'false'.startswith(inp):
        return False
    else:
        raise ValueError(f'arg needs to be one of [ True | False ], but arg was {str(arg)}')


# ______________________________________________________________________________________________________________________


def input_prompt(
        name: str,
        message: str = None,
        choices: tuple = (None, ),
        multi: bool = False,
        default: object = None,
        enum: bool = False
) -> str | list[str]:
    """
    wrapper for pythons input() with choices, default value and continuous prompting if an invalid input was supplied

    Args:
        name: the name of the variable
        message: the custom message to be printed.
                    If not None, name is omitted, else `please set the {name}:` will be printed
        choices: the allowed values for input. If None, anything can be input
        multi: whether to allow multiple selection (comma separated)
        default: the default value. If None, the user will continue to be prompted
        enum: enumerate the choices and allow for numerical input

    Returns:
        user input
    """
    print()
    if message is not None:
        print_yellow(f'{message}:')
    else:
        print_yellow(f'please set the {name}:')

    inp = None
    if choices == (None, ) and default is None:
        inp = input().strip()
        if multi:
            inp = [el.strip() for el in inp.split(',')]
    elif choices == (None, ) and default is not None:
        inp = input_yellow(f'\t-> defaults to: {default}').strip()
        inp = default if inp == '' else inp
        if multi:
            inp = [el.strip() for el in inp.split(',')]
    elif not enum:
        set_inp = set()
        while inp is None or not set_inp.issubset(set(choices)):
            inp = input_yellow(
                f'\t-> choose between [{", ".join(str(e) for e in choices)}], defaults to: {default} '
            ).strip()
            inp = default if inp == '' else inp
            if multi:
                inp = [el.strip() for el in inp.split(',')]
            set_inp = set(inp) if multi else {inp}
    else:
        available_choices = {i: item for i, item in enumerate(choices, start=1)}
        print_yellow('  choose from', end='')
        print_yellow('\t', *available_choices.items(), sep='\n\t')
        print_yellow(f'  default will be {default}')
        set_inp = set()
        while inp is None or not (inp == ''
                                  or set_inp.issubset(set(available_choices.values()))
                                  or set_inp.issubset(set([str(i) for i in available_choices.keys()]))):
            inp = input_yellow('\t-> enter the number or value of your choice ')
            inp = default if inp == '' else inp
            if multi:
                inp = [el.strip() for el in inp.split(',')]
            set_inp = set(inp) if multi else {inp}

        if not multi and inp.isdigit():
            inp = available_choices[int(inp)]
        elif multi and all(el.isdigit() for el in inp):
            inp = [available_choices[int(el)] for el in inp]

    print_yellow(f'user input: {inp}')
    print()

    return inp


# ______________________________________________________________________________________________________________________


def prompt_file_name(open_or_save: str = 'open', gui: bool = True) -> str:
    """
    Prompts the user to select a file.

    Args:
        open_or_save: whether it should prompt for an existing file (open) or to save a new file (save)
        gui: whether to use tkinter gui or just plain input

    Returns:
        the path to the file
    """
    file_path = None
    if open_or_save not in ('open', 'save'):
        raise ValueError(f"Argument open_or_save must be 'open' or 'save'. Input was {open_or_save}")

    if gui:
        import tkinter as tk
        window = tk.Tk()
        window.wm_attributes('-topmost', 1)
        window.withdraw()
        if open_or_save == 'open':
            from tkinter.filedialog import askopenfilename
            file_path = askopenfilename(parent=window, title='please select the file name')
        elif open_or_save == 'save':
            from tkinter.filedialog import asksaveasfilename
            file_path = asksaveasfilename(parent=window, title='please set the file name to be saved')
    else:
        file_path = str(input_prompt(name='path/to/file'))
        if open_or_save == 'open' and not Path(file_path).exists():
            raise ValueError(f'{file_path} does not exist!')
        if open_or_save == 'open' and not Path(file_path).is_file():
            raise ValueError(f'{file_path} is not a file!')

    return file_path


# ______________________________________________________________________________________________________________________


def determine_default_value_for_argparse(
        repl: bool, arg_name: tuple, choices: tuple = (None, ), default: object = None, enum: bool = False
) -> object:
    """
    only use for argparse.add_argument default value
    this function determines the default value based on execution mode and user input

    Args:
        repl: whether the script is executed in interactive repl (read-evaluate-print-loop) mode
        arg_name: the name of the arguments, e.g. ('-arg', '--argument')
        choices: the allowed values for input. If None, anything can be input
        default: the default value. If None, the user will continue to be prompted
        enum: enumerate the choices and allow for numerical input

    Returns:
        the determined default value
    """

    arg_name = tuple(arg.lstrip('-') for arg in arg_name)
    determined_default = default
    if repl:
        determined_default = input_prompt(arg_name[-1], choices=choices, default=default, enum=enum)
    else:
        if not check_if_in_argv(*arg_name):
            if default is not None:
                determined_default = default
            else:
                determined_default = input_prompt(arg_name[-1], choices=choices, default=default, enum=enum)

    return determined_default


# ______________________________________________________________________________________________________________________


def create_logger(name: str, log_file_path: str | Path = None) -> logging.Logger:
    """
    logger factory function

    Args:
        name: the name of the logger
        log_file_path: the path to the logging file, if None, then no file handler will be added

    Returns:
        an instance of a logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logging_console_formatter = logging.Formatter('%(levelname)-8s | %(message)s')
    logging_console_handler = logging.StreamHandler()
    logging_console_handler.setLevel(logging.DEBUG)
    logging_console_handler.setFormatter(logging_console_formatter)
    logger.addHandler(logging_console_handler)

    if log_file_path is not None:
        logging_file_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | module: %(module)s | %(message)s')
        logging_file_handler = logging.FileHandler(log_file_path)
        logging_file_handler.setLevel(logging.INFO)
        logging_file_handler.setFormatter(logging_file_formatter)
        logger.addHandler(logging_file_handler)

    return logger


# ______________________________________________________________________________________________________________________


def format_email_error_message(exception: Exception, project: str, wd: Path, log_file_path: Path) -> tuple:
    """
    prepares a formatted subject and body for the e_mail message

    Args:
        exception: the raised exception from the try block
        project: the project name
        wd: the working directory
        log_file_path: the Path object to the log file

    Returns:
        tuple of strings (e_mail_subject, e_mail_message)
    """

    tb = traceback.TracebackException.from_exception(exception)
    traceback_error = ''.join(tb.format())
    error = tb.exc_type.__name__

    e_mail_subject = f'Error {error} in {project}'
    with open(wd / 'templates' / 'email' / 'error_message.html', 'r', encoding='utf-8') as f:
        e_mail_message = f.read()
    e_mail_message = e_mail_message.replace('{{ project }}', project)
    e_mail_message = e_mail_message.replace('{{ datetime_now }}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    e_mail_message = e_mail_message.replace('{{ error }}', error)
    e_mail_message = e_mail_message.replace('{{ traceback_error }}', traceback_error)
    e_mail_message = e_mail_message.replace('{{ log_file_path }}', str(log_file_path.resolve()))

    return e_mail_subject, e_mail_message

# ______________________________________________________________________________________________________________________


def chunker(seq: typing.Sequence, size: int) -> typing.Generator:
    """
    creates a generator object of the sequence in fixed size chunks

    Args:
        seq: the input sequence
        size: the chunk size (last chunk will only contain the leftover)

    Returns:
        generator object with chunked sequence elements of the specified size
    """

    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


# ______________________________________________________________________________________________________________________


def split_text(text: str, n_chars: int = 50):
    """
    inserts `\n` into a long text at the first whitespace before `n_chars`.

    Args:
        text: the input text
        n_chars: the maximum number of chars per line

    Returns:
        text with `\n` inserted
    """

    result = ''
    start = 0
    while True:
        # loop exit condition
        if len(text[start:]) <= n_chars:
            result += text[start:]
            break

        # set the scope to analyse
        sub_text = text[start:start+n_chars]

        # first find the nearest whitespace to the end of text[:n_chars]
        ws_pos = sub_text.rfind(' ')

        # assembling the result string
        result += text[start:start+ws_pos] + '\n'

        # setting the new start point
        start = start + ws_pos + 1

    return result if result != '' else text


# ______________________________________________________________________________________________________________________


def last_day_of_month(any_date: datetime.date) -> datetime.date:
    """
    calculates the last day of the month for the supplied date

    Args:
        any_date: the input date

    Returns:
        date of the last day from that month
    """

    next_month = any_date.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)


# ______________________________________________________________________________________________________________________


def date_to_integer(any_date: datetime.date) -> int:
    """
    converts any date object to integer

    Args:
        any_date: the date which should be converted to int

    Returns:
        date as int
    """
    return (10000 * any_date.year) + (100 * any_date.month) + any_date.day


# ______________________________________________________________________________________________________________________


def display_formatted_time(seconds: int, granularity: str = 's') -> str:
    """
    outputs a string of the time passed in second, minutes, hours, days, weeks

    Args:
        seconds: the time passed in seconds
        granularity: controls how much unit details should be shown. Default 's' shows all non-zero units

    Returns:
        formatted string with elapsed time
    """

    result = []

    d_granularity = {s: i for s, i in zip(['w', 'd', 'h', 'm', 's'], [1, 2, 3, 4, 5])}
    granularity = d_granularity[granularity]

    intervals = (
        ('w', 604800),  # 60 * 60 * 24 * 7
        ('d', 86400),  # 60 * 60 * 24
        ('h', 3600),  # 60 * 60
        ('m', 60),
        ('s', 1),
    )

    seconds = int(round(seconds))
    if seconds == 0:
        return '0 s'

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f'{value} {name}')

    return ', '.join(result[:granularity])


# ______________________________________________________________________________________________________________________


def clean_umlauts(s: str | list) -> str | list:
    """
    replaces some German, French, Slavic umlauts to plain english characters

    Args:
        s: the input string or list of strings

    Returns:
        input object with replaced umlauts
    """

    d_trans = {
        'Ä': 'Ae',
        'Ü': 'Ue',
        'Ö': 'Oe',
        'É': 'E',
        'È': 'E',
        'À': 'A',
        'Ó': 'O',
        'Â': 'A',
        'Ê': 'e',
        'Ç': 'C',
        'Ć': 'C',
        'Č': 'C',

        'ä': 'ae',
        'ü': 'ue',
        'ö': 'oe',
        'é': 'e',
        'è': 'e',
        'à': 'a',
        'ó': 'o',
        'â': 'a',
        'ê': 'e',
        'ç': 'c',
        'ć': 'c',
        'č': 'c'
    }

    for key, val in d_trans.items():
        if isinstance(s, str):
            s = s.replace(key, val)

        elif isinstance(s, list):
            s = [el.replace(key, val) for el in s]

    return s


# ______________________________________________________________________________________________________________________


def calc_equidistant_weights(n: int) -> list:
    """
    calculates the equidistant weights for n inputs. Sum of all weights equals 1

    Args:
        n: the number of weights needed

    Returns:
        list of equidistant weights
    """

    if n < 2:
        print('n needs to be at least 2')
        return [1]

    unidist = ((1 / n) / 2) / (n // 2)

    if n % 2 == 0:
        rng = [i for i in range(-(n // 2), n // 2 + 1) if i != 0]
    else:
        rng = [i for i in range(-(n // 2), n // 2 + 1)]

    return [round(1 / n + i * unidist, 10) for i in reversed(rng)]


# ______________________________________________________________________________________________________________________


yaml_env_resolver = re.compile(r'\${.+}')


def yaml_env_constructor(loader, node):
    value = node.value
    match = yaml_env_resolver.match(value)
    env_var = match.group()[2:-1]
    return os.environ.get(env_var) + value[match.end():]


# ______________________________________________________________________________________________________________________
