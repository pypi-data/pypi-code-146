"""Utility functions for the CLI and CLI testing"""
import argparse
import difflib
import sys
import textwrap
from contextlib import contextmanager
from typing import Callable, List, NamedTuple, TypeVar


@contextmanager
def set_argv(args: List[str]):
    """Temporarily override sys.argv

    Args:
        args (List[str]): List of new args
    """
    original_argv = sys.argv
    sys.argv = args
    yield
    sys.argv = original_argv


class CLIExample(NamedTuple):
    example: str
    description: str

    def __str__(self) -> str:
        message = f"""
        # {self.description}
        {self.example}
        """
        return textwrap.dedent(message).strip()


def get_example_text(*examples: CLIExample) -> str:

    message = '\n'.join(f'\n{ex}\n' for ex in examples)
    message = f"""
    Examples:
    {message}
    """

    return textwrap.dedent(message).strip()


def extract_first_examples(*example_lists: List[CLIExample]) -> str:

    message = '\n'.join(f'\n{items[0]}\n' for items in example_lists)
    message = f"""
    Examples:
    {message}
    """

    return textwrap.dedent(message).strip()


class Description(str):
    """Simple string wrapper that formats a description nicely from triple-quote strings

    This can be used for argparse descriptions.
    """

    def __new__(cls, text: str):
        text = textwrap.dedent(text).strip()
        return super().__new__(cls, text)


# pylint: disable-next=invalid-name
T = TypeVar('T')


def _identity(ss: T) -> T:
    return ss


def comma_separated(arg: str, fun: Callable[[str], T] = _identity) -> List[T]:
    """Get a list of strings from a comma-separated string

    Arg:
        arg: String to process for comma-separated values
        fun: Callable applied to each value in the comma-separated list. Default None.

    Returns:
        List of function outputs
    """
    values = [v.strip() for v in arg.split(',')]
    return [fun(v) for v in values]


def get_choice_message(value: str, action: argparse.Action):
    assert action.choices

    suggestions_str = ''

    # Try and make suggestions to the user
    matches = difflib.get_close_matches(value, list(action.choices))
    if matches:
        # If choices are argparse arguments, we can parse "prog" which is the full
        # command to suggest to the user. Otherwise, we suggest matching values only
        try:
            suggestions = {action.choices[match].prog for match in matches}  # pyright: ignore
        except (TypeError, AttributeError):
            suggestions = matches

        suggestions_str = '\n\nDid you mean'
        if len(suggestions) > 1:
            suggestions_str += ' one of the following'
        suggestions_str += ':\n' + '\n'.join(sorted(suggestions))

    # Filter choices to exclude duplicated commands created as aliases
    progs_found, choose_from = set(), []
    for val in action.choices:
        try:
            prog = action.choices[val]  # pyright: ignore
        except TypeError:
            prog = val

        # this assumes sorted dicts, picks the first choice value for the prog
        if prog in progs_found:
            continue

        progs_found.add(prog)
        choose_from.append(val)

    choose_from.sort()

    # Return the error string
    default_argparse_error = f'invalid choice: {value!r} (choose from {", ".join(choose_from)})'
    return f'{default_argparse_error}{suggestions_str}'


# This should be used everywhere instead of argparse.ArgumentParser to allow for choice suggestions
class MCLIArgumentParser(argparse.ArgumentParser):
    """
    MCLI Instance of argparse.ArgumentParser that provides custom choice messages
    """

    def _check_value(self, action, value):
        # This overrides argparse.ArgumentParser with identical logic, except
        # specifying and calling get_choice_message
        if action.choices is not None and value not in action.choices:
            args = {'value': value, 'choices': ', '.join(map(repr, action.choices))}
            msg = get_choice_message(value, action)
            raise argparse.ArgumentError(action, msg % args)
