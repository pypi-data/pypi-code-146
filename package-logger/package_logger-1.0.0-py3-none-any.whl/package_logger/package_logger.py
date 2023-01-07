import inspect
from colorama import Fore, init

class TextType:
    INFO: str = "INFO"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"

class ColorType:
    COLOR_INFO: int = Fore.LIGHTWHITE_EX
    COLOR_ERROR: int = Fore.LIGHTRED_EX
    COLOR_WARNING: int = Fore.LIGHTBLUE_EX

class LoggerClass:
    def __init__(self):
        pass
    @property
    def __getParent(self):
        return inspect.stack()[2][3]
    @property
    def __getLineNo(self):
        cf = inspect.currentframe()
        return cf.f_back.f_lineno
    def __whoami(self):
        return inspect.stack()[1][3]
    def print(self, *array, type_: TextType = TextType.INFO):
        print(f"""[{type_}]
[From] {self.__getParent}
[Line] {self.__getLineNo}
[Statement(s)]
{" ".join(array)}
        """)
    def colorPrint(self, *array, type_: TextType = TextType.INFO, color: ColorType = ColorType.COLOR_INFO):
        print(f"""{color}[{type_}]
[From] {self.__getParent}
[Line] {self.__getLineNo}
[Statement(s)]
{" ".join(array)}{Fore.RESET}
        """)
        
if __name__ == "__main__":
    logger = LoggerClass()
    logger.print("Hello")
    logger.colorPrint("Hello", color=ColorType.COLOR_WARNING)
        