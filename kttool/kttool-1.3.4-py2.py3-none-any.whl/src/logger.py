MIT License

Copyright (c) 2022 heiseish

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
from .context import supports_color

__all__ = [
    'color_cyan',
    'color_green',
    'color_red',
    'log',
    'log_green',
    'log_cyan',
    'log_red'
]

BOLD_SEQ = '\033[1m'
RESET_SEQ = '\033[0m'
BLACK = '\033[6;90m'
RED = '\033[6;91m'
GREEN = '\033[6;92m'
YELLOW = '\033[6;93m'
BLUE = '\033[6;94m'
MAGENTA = '\033[6;95m'
CYAN = '\033[6;96m'
WHITE = '\033[6;97m'

def color_cyan(text: str) -> str:
    if not supports_color:
        return text
    return f'{CYAN}{text}{RESET_SEQ}'


def color_green(text: str) -> str:
    if not supports_color:
        return text
    return f'{GREEN}{text}{RESET_SEQ}'


def color_red(text: str) -> str:
    if not supports_color:
        return text
    return f'{RED}{text}{RESET_SEQ}'


log = print

def log_green(*args, **kwargs) -> None:
    log(color_green(*args, **kwargs))


def log_cyan(*args, **kwargs) -> None:
    log(color_cyan(*args, **kwargs))


def log_red(*args, **kwargs) -> None:
    log(color_red(*args, **kwargs))