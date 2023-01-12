from typing import Any, List

from colorama import Fore, Style

from bin.process.io.io import Io


class ConsoleIo(Io):
    def text(self, message: str) -> None:
        self.__write(message, [])

    def title(self, message: str) -> None:
        self.__write(message, [Fore.LIGHTCYAN_EX, Style.BRIGHT])

    def success(self, message: str) -> None:
        self.__write(message, [Fore.GREEN, Style.BRIGHT])

    def error(self, message: str) -> None:
        self.__write(message, [Fore.RED, Style.BRIGHT])

    def warning(self, message: str) -> None:
        self.__write(message, [Style.BRIGHT])

    def __write(self, message: str, styles: List[Any]) -> None:
        print("".join(styles) + message)
