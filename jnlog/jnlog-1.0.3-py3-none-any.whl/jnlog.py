import datetime
from colorama import Fore, init

class jnlog:

    def __init__(self, name: str, visible: bool = False):

        self.visible = visible
        self.name = name
        init()

    def _log(self, color, e, txt):
        """
        internal log backend
        """
        if not self.visible:
            return
        t = datetime.datetime.now().time()

        hour = str(t.hour)
        min = str(t.minute)
        if len(min) == 1:
            min = '0'+min
        sec = str(t.second)
        if len(sec) == 1:
            sec = '0'+sec

        print(f'{Fore.LIGHTWHITE_EX}[{hour}/{min}/{sec}] {color}[{self.name}] [{e}] {txt}\033[0m')
    
    def info(self, *args):
        self._log(Fore.LIGHTCYAN_EX, 'INFO', ' '.join(args))

    def warn(self, *args):
        self._log(Fore. LIGHTYELLOW_EX, 'WARN', ' '.join(args))

    def error(self, *args):
        self._log(Fore.LIGHTRED_EX, 'ERROR', ' '.join(args))
