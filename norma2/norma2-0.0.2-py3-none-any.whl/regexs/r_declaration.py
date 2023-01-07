import sys
from typing import Optional

import regex

from norma2.regexs import regexs_class

# https://regex101.com/r/fBLUOp/2 (old)
# re = r"\w{1,}( \*{0,} {0,}\w{1,}(\[[0-9]{0,}\]){0,}){1,} {0,}= {0,}(([0-9]{1,})|(\".*\")|(\{.*\})|([&*]{1,}\w{1,})|(NULL)) {0,};{1}" # noqa: E501
# https://regex101.com/r/ohzzuZ/1 (old)
# re = r"\w{1,} {0,}\n{0,}( \*{0,} {0,}\n{0,} {0,}\w{1,} {0,}\n{0,} {0,}(\[ {0,}\n{0,} {0,}[0-9]{0,} {0,}\n{0,} {0,}\]){0,} {0,}\n{0,} {0,}){1,} {0,}= {0,}\n{0,} {0,}(([0-9]{1,})|((\".*\" {0,}\\){0,}(\".*\"){1})|(\{.*\})|([&*]{1,} {0,}\n{0,} {0,}\w{1,})|(NULL)|(\(.{2,}\).*)) {0,}\n{0,} {0,};{1}"  # noqa: E501
# https://regex101.com/r/ohzzuZ/2
re = r"\w{1,} {0,}\n{0,}( \*{0,} {0,}\n{0,} {0,}\w{1,} {0,}\n{0,} {0,}(\[ {0,}\n{0,} {0,}[0-9]{0,} {0,}\n{0,} {0,}\]){0,} {0,}\n{0,} {0,}){1,} {0,}= {0,}\n{0,} {0,}(([0-9]{1,})|((\".*\" {0,}\\){0,}(\".*\"){1})|(\{.*\})|([&*]{1,} {0,}\n{0,} {0,}\w{1,})|(NULL)|(\(.{2,}\).*)) {0,}\n{0,} {0,};{1}"  # noqa: E501
reg = regex.compile(re)


def search(text: str, timeout=1) -> Optional[regexs_class.RegexsResult]:
    try:
        res = reg.search(text, timeout=timeout)
    except TimeoutError as esc:
        print(f"ERROR: {__file__}:search: {esc}: {text}", file=sys.stderr)
        return None
    if not res:
        return None
    return regexs_class.RegexsResult(
        text, res.start(), res.end(), add_extra=False
    )  # noqa: E501


def sub(text: str, replace: str, timeout=1) -> Optional[str]:
    try:
        return reg.sub(text, replace, timeout=timeout)
    except TimeoutError as esc:
        print(f"ERROR: {__file__}:sub: {esc}: {text}", file=sys.stderr)
