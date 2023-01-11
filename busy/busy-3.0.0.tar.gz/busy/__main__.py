import sys
from argparse import ArgumentParser

from .file_system_root import FilesystemRoot
from .commander import Commander
from .launcher import Launcher
from .ui.curses_ui import CursesUI
from .ui.shell_ui import ShellUI
from . import PYTHON_VERSION

MESSAGE = "Busy requires Python version %i.%i.%i or higher"

def main():
    if sys.version_info < PYTHON_VERSION:
        raise RuntimeError(MESSAGE % PYTHON_VERSION)
    parser = ArgumentParser()
    parser.add_argument('--root', action='store')
    parser.add_argument('--ui', choices=['shell', 'curses', 'tk'], \
        action='store', default='shell')

    known, unknown = parser.parse_known_args(sys.argv)
    if known.root:
        root = FilesystemRoot(known.root)
    else:
        root = FilesystemRoot()
    commander = Commander(root)
    try:
        if known.ui == 'shell':
            ui = ShellUI(commander)
            commander.setUI(ui)
            result = commander.handle(*unknown[1:])
            if result: print(result)
        elif known.ui == 'curses':
            ui = CursesUI(commander)
            commander.setUI(ui)
            ui.start()
    except (RuntimeError, ValueError) as error:
        print(f"Error: {str(error)}")

if __name__ == '__main__':
    main()
