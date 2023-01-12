"""Utilities
============
"""
import re
from typing import Callable, Type

from docutils.nodes import document
from sphinx.parsers import Parser


def get_lang_map(
    template: str,
    eval_funcs: dict[str, Callable[[str], str]],
) -> dict[str, tuple[re.Pattern, Callable[[str], str]]]:
    """Get lang map.

    :param template:
    :type template: str
    :param eval_funcs:
    :type eval_funcs: dict[str, Callable[[str], str]]
    :rtype: dict[str, tuple[re.Pattern, Callable[[str], str]]]
    """
    lang_map = {}
    for lang, eval_func in eval_funcs.items():
        string = template.replace("LANG", lang)
        pat = re.compile(string, re.M | re.DOTALL)
        lang_map[lang] = (pat, eval_func)
    return lang_map


def replace(
    inputstring: str, pat: re.Pattern, eval_func: Callable[[str], str]
) -> str:
    """Replace.

    :param inputstring:
    :type inputstring: str
    :param pat:
    :type pat: re.Pattern
    :param eval_func:
    :type eval_func: Callable[[str], str]
    :rtype: str
    """
    outputstring = inputstring
    for m in pat.finditer(inputstring):
        input = m.group(1)
        output = eval_func(input)
        b, e = m.span()
        outputstring = outputstring.replace(inputstring[b:e], output)
    return outputstring


def patch_parser(template: str, parser: Type[Parser]) -> Type[Parser]:
    """Patch parser.

    :param template:
    :type template: str
    :param parser:
    :type parser: Type[Parser]
    :rtype: Type[Parser]
    """

    class subparser(parser):
        """subparser."""

        lang_map = None

        def parse(self, inputstring: str, document: document) -> None:
            """parse.

            :param inputstring:
            :type inputstring: str
            :param document:
            :type document: document
            :rtype: None
            """
            if not self.lang_map:
                self.lang_map = get_lang_map(
                    template, self.env.app.config.eval_funcs
                )
            for pat, eval_func in self.lang_map.values():
                inputstring = replace(inputstring, pat, eval_func)
            super().parse(inputstring, document)

    return subparser
