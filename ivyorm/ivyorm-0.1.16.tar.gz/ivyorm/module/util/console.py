import inspect
import os
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\33[101m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\33[90m'
    RED = '\033[91m'

class Console:

    @classmethod
    def stack(cls):
        frame = inspect.stack()[2]
        filepath= frame.filename
        lineno = frame.lineno
        function = frame.function
        filename = os.path.basename(filepath)

        return(f'{Color.HEADER}{Color.BOLD}{filename}:{function}:{lineno}{Color.END}')


    @classmethod
    def log(cls, string):
        stack = Console.stack()
        print(f"{stack}: {Color.OKCYAN}{string}{Color.END}")
        

    @classmethod
    def warn(cls, string):
        stack = Console.stack()
        print(f"{stack}: {Color.WARNING}{string}{Color.END}")

    @classmethod
    def error(cls, string):
        stack = Console.stack()
        print(f"{Color.FAIL}{stack}: {string}{Color.END}")
    
    @classmethod
    def fail(self, string):
        self.error(string)

    @classmethod
    def ok(cls, string):
        stack = Console.stack()
        print(f"{stack}: {Color.OKGREEN}{string}{Color.END}")

    @classmethod
    def success(self, string):
        stack = Console.stack()
        self.ok(string)

    @classmethod
    def info(cls, string):
        
        stack = Console.stack()
        print(f"{stack}: {Color.OKCYAN}{string}{Color.END}")

    # formatting for data retrieval
    @classmethod
    def db(cls, string):
        stack = Console.stack()
        print(f"{stack}: {Color.GREY}{string}{Color.END}")