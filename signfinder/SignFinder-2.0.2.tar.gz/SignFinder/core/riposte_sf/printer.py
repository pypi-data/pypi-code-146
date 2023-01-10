import sys
from rich.console import Console


class PrinterSF:

    def __init__(self):
        self.console = Console()
        self.block_stdout = False

    def print(self, *objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        if self.block_stdout: return
        self.console.print(*objects, sep = sep, end = end, highlight=False)

    def log(self, *args):
        self.console.log(*args, highlight=False)

    def error(self, *args):
        self.print('[red][!][/red]', *args)

    def status(self, *args):
        self.print('[blue][*][/blue]', *args)

    def info(self, *args):
        self.print('[i]', *args)

    def success(self, *args):
        self.print('[green][+][/green]', *args)  

    def debug(self, *args):
        self.print('[yellow1]\[debug][/yellow1]', *args)

    def new_line(self):
        self.print('')

    def disable(self):
        self.block_stdout = True

    def enable(self):
        self.block_stdout = False

    def get_max_width(self):
        return self.console.width
