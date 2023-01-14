import typer
import os

from rich.prompt import Confirm
from fu.common.errors import InvalidPathError

from fu.utils.console import console
from fu.utils.path import (
    is_dir,
    path_files
)


def iterate_and_open(path: str, step: int = 1) -> None:
    """Will iterate each file found inside given path
    and will open it in default system program

    Args:
        path (str): Path to iterate over its files
        step (int): How many files open at a time
    """
    if not is_dir(path):
        console.print(
            'Path is not a valid directory: {}'.format(path),
            style='error'
        )

    currently_open_count = 0
    for file in path_files(path, ):
        typer.launch(file)
        console.print(
            ' Opening {}'.format(file),
            style='info'
        )
        currently_open_count += 1

        if currently_open_count == step:
            if Confirm.ask('Open next {} file(s)'.format(step)):
                currently_open_count = 0
            else:
                break

def iterate_from_file(path: str, step: int = 1) -> None:
    """Will iterate each line of given file as a path \
    and will open it in default system program.       \
                                                      \
    If line starts with '#' it will be ignored.

    Args:
        path (str): Path to file containing paths to iterate
        step (int, optional): How many files open at a time. \
            Defaults to 1.
    """
    if not os.path.isfile(path):
        console.print(f'Path is not a valid file: { path }', style='error')
        raise InvalidPathError()

    with open(path) as pathsfile:
        curr_open_count = 0

        for filepath in pathsfile:
            filepath = filepath.strip("\n")

            if filepath and not filepath.startswith('#'):

                # Pause opening files if step has been reached
                if curr_open_count == step:
                    console.print()
                    if Confirm.ask(f'Open next { step } file(s)'):
                        curr_open_count = 0
                    else:
                        break

                console.print(f'Opening: "{ filepath }"', style='info')
                typer.launch(filepath)
                curr_open_count += 1
