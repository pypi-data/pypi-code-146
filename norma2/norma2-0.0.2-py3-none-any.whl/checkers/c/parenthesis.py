from typing import List

from norma2.errors.norm import BadSpace, _TemplateNormError
from norma2.parser.cfile import CFile

list_ok = [
    "do",
    "while",
    "for",
    "return",
    "if",
    "switch",
    "+",
    "-",
    "/",
    "*",
    "%",
    "=",
    "&",
    "|",
    ":",
    "?",
    ",",
    ";",
    "<",
    ">",
    ")",
]


def check_parenthesis(file: CFile) -> List[_TemplateNormError]:
    errs = []
    for i, line in enumerate(file.lines_origin):
        line = line if "//" not in line else line[: line.index("//")]
        if "){" in line:
            errs.append(BadSpace(file.filepath, i + 1, "need space between `){`"))
        for e, char in enumerate(line, start=1):
            if char == "(" and line[e - 2] == " ":
                found = 0
                for to_check in list_ok:
                    if line[e - len(to_check) - 2 : e] == f"{to_check} (":
                        found = 1
                    if to_check in ("&", "*"):
                        found = 1
                if line.strip().startswith("("):
                    found = 1
                if found == 0:
                    errs.append(
                        BadSpace(
                            file.filepath,
                            i + 1,
                            "no need space between function call an its parenthesis",
                        )
                    )
            if char == "(" and line[e - 2] != " ":
                found = 0
                for to_check in list_ok:
                    if line[
                        e - len(to_check) - 1 : e
                    ] == f"{to_check}(" and to_check not in ("*", "&"):
                        errs.append(
                            BadSpace(
                                file.filepath,
                                i + 1,
                                f"need space between {to_check} and parenthesis",
                            )
                        )
    return errs
