import re
from typing import List

from norma2.errors.norm import BadSpace, _TemplateNormError
from norma2.parser.cfile import CFile

smart_match = {
    ":ALL:": ".",
    ":NOTHING:": "{0}",
    ":ALPHANUM:": "[0-9a-zA-Z]",
    ":NUM:": "[0-9]",
    ":ALPHA:": "[a-zA-Z]",
    ":NOSPACE:": r"\S",
}

operator_list = [
    (" ([+", "+", "+])= ", r"(\+\+\w)|(\w\+\+)"),
    (" ([-{", "-", "-])=> ", r"(--\w)|(\w--)"),
    (r" ([/*", "*", "/", r"[\[\{\( ]\*{2,}"),
    (" (/*", "/", "*/= ", r'(<.*?\/.*?\.h>)|(".*?\/.*?\.h")'),
    ("< ", "<", ":ALL:"),
    (":ALL:", ">", " >="),
    (" ({[", "&", ":NOTHING:", "&&"),
    ("([ ", "!", ":ALL:"),
    ("/+*-=! ", "=", "= "),
    (":ALL:", "(", ":ALL:"),
    (":ALL:", ")", "}]) ;", r"\)\)"),
]


def _get_escape_regex(s: str, need: bool) -> str:
    escape = ""
    for c in s:
        if c in r"\^$.|?*+()[]{}":
            escape += "\\"
        escape += c
    new = smart_match.get(escape, escape)
    if new != escape:
        return new
    if need:
        escape = f"[{escape}]"
    return escape


def _check_line(file: CFile, line: str, line_nb: int, op: tuple):
    errs = []
    if len(op) == 4:
        line = re.sub(op[3], "", line)
    for _ in range(2):
        rex = _get_escape_regex(op[0], True)
        line = re.sub(f"{rex}{_get_escape_regex(op[1], False)}", "", line)
        rex = _get_escape_regex(op[2], True)
        line = re.sub(f"{_get_escape_regex(op[1], False)}{rex}", "", line)
    if line.endswith(op[1]):
        line = line[: -len(op)]
    if op[1] in line:
        errs.append(BadSpace(file.filepath, line_nb, f"bad space for operator {op[1]}"))
    return errs


def check_op(file: CFile) -> List[_TemplateNormError]:
    errs = []
    lines = file.text_origin_without_text.split("\n")
    for i, line in enumerate(lines):
        line = re.sub("'.'", "", line)
        line = line if "//" not in line else line[: line.index("//")]
        for op in operator_list:
            errs.extend(_check_line(file, line, i + 1, op))
    return errs
