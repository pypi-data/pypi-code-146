#!/usr/bin/env python3

"""
Toolbox.
"""

import enum
import itertools
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Union

import ruamel.yaml
import yaml
from colored import attr, fg
from dotmap import DotMap
from pudb import set_trace as bp  # noqa

DOTMAP_NONE = (None, DotMap())


class AutoEnum(enum.Enum):
    def _generate_next_value_(  # type: ignore
        name: str, start: int, count: int, last_values: List[str]
    ) -> str:
        return name


class GetAttributes:
    def get_attributes(self) -> Dict[str, Any]:
        return {
            attribute: self.__getattribute__(attribute)
            for attribute in self.__dir__()
            if not attribute.startswith("__")
            and not callable(self.__getattribute__(attribute))
        }


def directories(
    PATH: Path,
    INCLUDES: Optional[Union[str, List[str]]] = None,
    EXCLUDES: Optional[Union[str, List[str]]] = None,
) -> Iterator[Path]:
    """Iterate over the directories of a given path."""
    # Parse inputs.
    if INCLUDES is None:
        INCLUDES = [
            "*",
        ]
    elif type(INCLUDES) is str:
        INCLUDES = [
            INCLUDES,
        ]
    if EXCLUDES is None:
        EXCLUDES = []
    elif type(EXCLUDES) is str:
        EXCLUDES = [
            EXCLUDES,
        ]

    # Filter directory.
    FILTER_INCLUDING = itertools.chain.from_iterable(PATH.glob(F) for F in INCLUDES)
    FILTER_EXCLUDING = itertools.chain.from_iterable(PATH.glob(F) for F in EXCLUDES)
    return iter(set(FILTER_INCLUDING) - set(FILTER_EXCLUDING))


def format_info(MESSAGE: str) -> str:
    """Format an info message."""
    return f"{fg('yellow')}{MESSAGE}{attr(0)}"


def format_validation(MESSAGE: str) -> str:
    """Format a validation message."""
    return f"{fg('green')}{MESSAGE}{attr(0)}"


def format_error(MESSAGE: str) -> str:
    """Format an error message."""
    return f"{fg('red')}{MESSAGE}{attr(0)}"


def print_info(MESSAGE: str) -> None:
    """Print an info message with a template format."""
    print(format_info(MESSAGE))


def print_validation(MESSAGE: str) -> None:
    """Print a validation message with a template format."""
    print(format_validation(MESSAGE))


def print_error(MESSAGE: str) -> None:
    """Print an error message with a template format."""
    print(format_error(MESSAGE))


def raise_error(MESSAGE: str, ERROR: type = ValueError) -> None:
    """Raise an error with a template format."""
    raise ERROR(format_error(MESSAGE))


def form_yes_or_no(QUESTION: str, DEFAULT_NO: bool = True) -> bool:
    """
    Single yes or no question without recursion.

    Credit:
        Inspired from
        @icamys commented on 29 Nov 2020 on Github,
        https://gist.github.com/garrettdreyfus/8153571
    """
    CHOICES = " [y/N]: " if DEFAULT_NO else " [Y/n]: "
    DEFAULT_ANSWER = "n" if DEFAULT_NO else "y"
    REPLY = str(input(f"{QUESTION} {CHOICES}\n>> ")).lower().strip() or DEFAULT_ANSWER
    print()
    if REPLY[:1] == "y":
        return True
    elif REPLY[:1] == "n":
        return False
    else:
        return not DEFAULT_NO


def form_choice(QUESTION: str, CHOICES: Iterable[Any], DEFAULT: int = 0) -> int:
    """Form to ask a choice"""
    CHOICES_LIST = [f"+ {CHOICE} [{INDEX}]\n" for (INDEX, CHOICE) in enumerate(CHOICES)]
    NUMBER_CHOICES = len(CHOICES_LIST)
    FORMATTED_CHOICES = "".join(CHOICES_LIST)
    FULL_QUESTION = (
        f"{QUESTION} [0-{NUMBER_CHOICES - 1}] (default: {DEFAULT})\n"
        f"{FORMATTED_CHOICES}>> "
    )
    CHOICE = int(input(FULL_QUESTION) or DEFAULT)
    print()
    return CHOICE


def form_overwrite_file(
    PATH: Path, QUESTION: Optional[str] = None, DEFAULT_NO: bool = True
) -> bool:
    """Yes/no form to ask whether file should be overwritten if already existing."""
    if QUESTION is None:
        QUESTION = "Overwrite {PATH}?"

    save = True
    if PATH.is_file():
        save = form_yes_or_no(QUESTION, DEFAULT_NO=DEFAULT_NO)
    return save


def yaml_represent_none(self: Any, _: Any) -> Any:
    return self.represent_scalar("tag:yaml.org,2002:null", "")


def yaml_add_representer_none() -> None:
    yaml.add_representer(type(None), yaml_represent_none)


def read_yaml(PATH: Path) -> DotMap:
    """Load the yaml file."""
    CFGF_DICT, IND, BSI = ruamel.yaml.util.load_yaml_guess_indent(PATH.open())
    return DotMap(CFGF_DICT)
