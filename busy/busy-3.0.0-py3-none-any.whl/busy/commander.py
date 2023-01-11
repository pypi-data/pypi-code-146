from argparse import ArgumentParser
from tempfile import TemporaryDirectory
import sys
from tempfile import TemporaryFile
from pathlib import Path

import busy
from busy import do_import


class Commander:

    def __init__(self, root):
        self._root = root
        self._ui = None
    
    def setUI(self, ui):
        self._ui = ui
 
    def parse(self, *args):
        parsed, remaining = self._parser.parse_known_args(args)
        parsed.criteria = remaining
        return parsed

    def handle(self, *args):
        parsed = self.parse(*args)
        if hasattr(parsed, 'command'):
            command = parsed.command(self._root, self._ui)
            result = command.execute(parsed)
            command.save()
            return result

    @classmethod
    def register(self, command_class):
        if not hasattr(self, '_parser'):
            self._parser = ArgumentParser()
            self._subparsers = self._parser.add_subparsers()
        subparser = self._subparsers.add_parser(command_class.command)
        subparser.set_defaults(command=command_class)
        command_class.register(subparser)
        if not hasattr(self, '_keys'):
            self._keys = {}
        if hasattr(command_class, "key"):
            self._keys[command_class.key] = command_class


class Command:

    def __init__(self, root, ui):
        self._root = root
        self.status = None
        self.ui = ui

    def _list(self, queue, tasklist):
        fmtstring = "{0:>6}  " + queue.itemclass.listfmt
        texts = [fmtstring.format(i, t) for i, t in tasklist]
        return '\n'.join(texts)
    
    @classmethod
    def register(self, parser):  # pragma: nocover
        pass

    def save(self):
        self._root.save()

    @classmethod
    def register(self, parser):
        pass

    def confirmed(self, parsed, itemlist, verb):
        if hasattr(parsed, 'yes') and parsed.yes:
            return True
        else:
            return self.ui.confirmed(parsed, itemlist, verb)


class QueueCommand(Command):

    @classmethod
    def register(self, parser):
        super().register(parser)
        parser.add_argument('--queue', nargs=1, dest="queue")

    def execute(self, parsed):
        key = parsed.queue[0] if getattr(parsed, 'queue') else 'tasks'
        queue = self._root.get_queue(key)
        return self.execute_on_queue(parsed, queue)

    def execute_on_queue(self, parsed, queue):
        method = getattr(queue, self.command)
        self.status = method(*parsed.criteria)

    def get_args_in_term(self, stdscr): #pragma: nocover
        return [self.command]


class TodoCommand(QueueCommand):

    def execute(self, parsed):
        # key = parsed.queue[0] if hasattr(parsed, 'queue') else 'tasks'
        # assert key is 'tasks'
        queue = self._root.get_queue('tasks')
        return self.execute_on_queue(parsed, queue)


do_import(Path(__file__).parent / 'commands', 'busy.commands')
