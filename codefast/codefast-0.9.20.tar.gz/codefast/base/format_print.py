from typing import List, Tuple

from termcolor import colored


class FormatPrint(object):
    
    yes = colored('✓', 'green')
    no = colored('✗', 'red')


    @staticmethod
    def readable_time(seconds: int)->str:
        n = int(seconds)
        days = n // 86400
        hours = n // 3600 % 24
        minutes = n // 60 % 60
        seconds = n % 60
        return f'{days}d {hours}h {minutes}m {seconds}s'

    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    @staticmethod
    def magenta(text: str, attrs: List[str] = None) -> str:
        """Colorize text.
        Available text colors:
            red, green, yellow, blue, magenta, cyan, white.

        Available text highlights:
            on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

        Available attributes:
            bold, dark, underline, blink, reverse, concealed.

        Example:
            colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
            colored('Hello, World!', 'green')

        attrs=['bold', 'underline', 'reverse', 'blink', 'concealed']
        """
        return colored(text, 'magenta', attrs=attrs)

    @classmethod
    def yellow(cls, text: str, attrs: List[str] = None) -> str:
        return colored(text, 'yellow', attrs=attrs)

    @classmethod
    def red(cls, text: str, attrs: List[str] = None) -> str:
        return colored(text, 'red', attrs=attrs)

    @classmethod
    def add_attrs(cls, text_: str, attrs: List[str]) -> str:
        if "bold" in attrs:
            text_ += "\033[1m"
        if "underline" in attrs:
            text_ += "\033[4m"
        if "reverse" in attrs:
            text_ += "\033[7m"
        if "blink" in attrs:
            text_ += "\033[5m"
        if "concealed" in attrs:
            text_ += "\033[8m"
        text_ += "\033[0m"
        return text_

    @classmethod
    def red_ansi(cls, text: str, attrs: List[str] = None) -> str:
        # use ANSI escape codes to support formatting with width
        text_ = f"\033[91m{text}"
        return cls.add_attrs(text_, attrs)

    @classmethod
    def yellow_ansi(cls, text: str, attrs: List[str] = None) -> str:
        # use ANSI escape codes to support formatting with width
        text_ = f"\033[93m{text}"
        return cls.add_attrs(text_, attrs)

    @classmethod
    def green_ansi(cls, text: str, attrs: List[str] = None) -> str:
        # use ANSI escape codes to support formatting with width
        text_ = f"\033[92m{text}"
        return cls.add_attrs(text_, attrs)

    @classmethod
    def green(cls, text: str, attrs: List[str] = None) -> str:
        return colored(text, 'green', attrs=attrs)

    @classmethod
    def cyan(cls, text: str, attrs: List[str] = None) -> str:
        return colored(text, 'cyan', attrs=attrs)


# Pretty print dict/list type of data structure.
def pretty_print(js: Tuple[list, dict],
                 indent: int = 0,
                 prev: str = '') -> None:
    _margin = ' ' * indent
    nxt_margin = _margin + ' ' * 3
    if isinstance(js, dict):
        print('{' if prev == ':' else _margin + '{')
        for k, v in js.items():
            print(nxt_margin + FormatPrint.cyan(k), end=': ')
            if isinstance(v, dict) or isinstance(v, list):
                pretty_print(v, indent + 3, prev=':')
            else:
                print(v)
        print(_margin + '}')
    elif isinstance(js, list):
        print('[')
        for v in js:
            pretty_print(v, indent + 3)
        print(_margin + ']')
    elif isinstance(js, str):
        print(_margin + js)
    else:
        raise Exception("Unexpected type of input.")
