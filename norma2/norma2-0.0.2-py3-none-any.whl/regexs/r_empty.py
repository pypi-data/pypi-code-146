import sys
from typing import Optional

import regex

from norma2.regexs import regexs_class

# https://regex101.com/r/M7NU4a/1
re_end = r"\n[ \t\f]{0,}$"
reg_end = regex.compile(re_end)
# https://regex101.com/r/MCuFZJ/1
re_first = r"^[ \t\f]{0,}\n"
reg_first = regex.compile(re_first)


def search(text: str, timeout=1) -> Optional[regexs_class.RegexsResult]:
    try:
        res = reg_first.search(text, timeout=timeout)
        if not res:
            res = reg_end.search(text, timeout=timeout)
    except TimeoutError as esc:
        print(f"ERROR: {__file__}:search: {esc}: {text}", file=sys.stderr)
        return None
    if not res:
        return None
    return regexs_class.RegexsResult(text, res.start(), res.end())


def sub(text: str, replace: str, timeout=1) -> Optional[str]:
    is_ok = True
    while is_ok:
        patr = search(text, timeout=timeout)
        if patr:
            text = text.replace(patr.matching, replace)
        else:
            is_ok = False
    return text
