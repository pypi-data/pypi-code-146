from copy import deepcopy
from enum import Enum
from typing import List, Union

from norma2.config.config_class import Config
from norma2.parser._file import _File
from norma2.regexs import r_comment  # 1
from norma2.regexs import r_declaration  # 3
from norma2.regexs import r_empty  # 10
from norma2.regexs import r_for  # 8
from norma2.regexs import r_function  # 10
from norma2.regexs import r_if  # 7
from norma2.regexs import r_imperativ  # 13
from norma2.regexs import r_macro  # 2
from norma2.regexs import r_prototype  # 4
from norma2.regexs import r_struct  # 5
from norma2.regexs import r_union  # 6
from norma2.regexs import r_while  # 9
from norma2.regexs import r_text
from norma2.regexs.regexs_class import RegexsResult


class CContextType(Enum):
    DECLARATION = "variable declaration"
    FOR = "for loop"
    FUNCTION = "function implementation"
    IF = "if statement"
    MACRO = "macro definition"
    PROTOTYPE = "function prototype"
    STRUCT = "struct definition"
    UNION = "union definition"
    WHILE = "while loop"
    COMMENT = "block comment"
    EMPTY = "empty line"
    IMPERATIV = "imperativ line"
    UNKNOW = "line type unknow"


order_parsers = [
    (r_comment, CContextType.COMMENT),
    (r_macro, CContextType.MACRO),
    (r_if, CContextType.IF),
    (r_for, CContextType.FOR),
    (r_while, CContextType.WHILE),
    (r_declaration, CContextType.DECLARATION),
    (r_prototype, CContextType.PROTOTYPE),
    (r_struct, CContextType.STRUCT),
    (r_union, CContextType.UNION),
    (r_function, CContextType.FUNCTION),
    (r_empty, CContextType.EMPTY),
    (r_imperativ, CContextType.IMPERATIV),
]


def find_ccontext(stack: List[str]) -> Union[None, "CContext"]:
    joined = "\n".join(stack)
    for mod, _type in order_parsers:
        match = mod.search(joined)
        if not match:
            continue
        index_newline = len(joined)
        if "\n" in joined:
            index_newline = joined.index("\n")
        if match.start > index_newline:
            continue
        nb_line = joined.count("\n", match.start, match.end + 1)
        if nb_line == 0:
            nb_line = 1
        context = CContext(_type, match, nb_line)
        return context
    return None


def parse_text_lines(text: List[str]) -> Union[None, List["CContext"]]:
    stack = deepcopy(text)
    res = []

    while stack:
        matching = find_ccontext(stack)
        if not matching:
            # res.append(
            #     CContext(
            #         CContextType.UNKNOW, RegexsResult(stack[0], 0, len(stack[0])), 1  # noqa: E501
            #     )
            # )
            stack.pop(0)
            continue
        res.append(matching)
        for _ in range(min(len(stack), matching.nb_lines)):
            stack.pop(0)
    return res


class CContext:
    def __init__(
        self, type: CContextType, matching: RegexsResult, nb_line: int
    ) -> None:
        self.type = type
        self.matching = matching
        self.nb_lines = nb_line
        self.childs: List["CContext"] = []
        if self.type not in (
            CContextType.COMMENT,
            CContextType.UNKNOW,
            CContextType.EMPTY,
            CContextType.DECLARATION,
        ):
            to_parse = matching.matching.split("\n")[1:]
            if matching.extra_end_line and to_parse:
                to_parse.pop(-1)
            if to_parse:
                parsed = parse_text_lines(to_parse)
                if parsed:
                    self.childs = parsed

    def __str__(self):
        ret = f"\n---> type:{self.type}|lenght:{self.nb_lines}\n"
        ret += f"matchin: `{self.matching}`"
        if not str(self.matching).endswith("\n"):
            ret += "\n"
        ret += f"- nb childs: {len(self.childs)}\n"
        childs = ""
        for chil in self.childs:
            childs += str(chil)
        childs = childs.replace("\n", "\n-- ")
        ret += childs
        return ret


class CFile(_File):
    def __init__(self, filepath: str, config: Config) -> None:
        super().__init__(filepath, config)
        self.lines_origin: List[str] = []
        self.parsed_context: List[CContext] = []
        self.text_origin_without_text: str = ""

    def init(self):
        if not self.text_origin:
            return
        self.lines_origin = self.text_origin.split("\n")
        parsed = parse_text_lines(self.lines_origin)
        if parsed:
            self.parsed_context = parsed
        if self.config.debug:
            print(self)
        without_text = r_text.sub(self.text_origin, "")
        if without_text:
            self.text_origin_without_text = without_text
        self.is_init = True

    def __str__(self):
        ret = f"file: {self.filepath}\n"
        for i, ctx in enumerate(self.parsed_context):
            ret += f"ctx n{i}:"
            ret += str(ctx)
        return ret
