from argparse import ArgumentParser

from .ui.curses_ui import CursesUI
from .file_system_root import FilesystemRoot
from .commander import Commander


class Launcher:

    def __init__(self, *input):
        self._parser = ArgumentParser()
        self._parser.add_argument('--root', action='store')
        self._parser.add_argument('--ui', choices=['shell', 'curses', 'tk'], \
            action='store', default='shell')

        known, unknown = self._parser.parse_known_args(input)
        self.commands = unknown
        if known.root:
            self.root = FilesystemRoot(known.root)
        else:
            self.root = FilesystemRoot()
        if known.ui == 'curses':  # pragma: nocover
            commander = Commander(self.root)
            self.ui = CursesUI(commander)
            self.ui.start()
        # elif known.ui == 'shell':
        #     self.ui = ShellUI
        # elif known.ui == 'tk':
        #     self.ui = TkUI
