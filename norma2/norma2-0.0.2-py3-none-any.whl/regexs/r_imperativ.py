import sys
from typing import Optional

import regex

from norma2.regexs import regexs_class

#  https://regex101.com/r/Kybx1Z/1
re = r"^(.*?\\\n){0,}(.*);"
reg = regex.compile(re, regex.MULTILINE)


def search(text: str, timeout=1) -> Optional[regexs_class.RegexsResult]:
    try:
        res = reg.search(text, timeout=timeout)
    except TimeoutError as esc:
        print(f"ERROR: {__file__}:search: {esc}: {text}", file=sys.stderr)
        return None
    if not res:
        return None
    return regexs_class.RegexsResult(text, res.start(), res.end(), add_extra=False)


def sub(text: str, replace: str, timeout=1) -> Optional[str]:
    try:
        return reg.sub(text, replace, timeout=timeout)
    except TimeoutError as esc:
        print(f"ERROR: {__file__}:sub: {esc}: {text}", file=sys.stderr)
