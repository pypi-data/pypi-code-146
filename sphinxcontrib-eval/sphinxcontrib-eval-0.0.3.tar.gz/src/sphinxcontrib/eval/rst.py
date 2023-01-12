"""RST
======

Provide ``RSTEvalParser``.
"""
from sphinx.parsers import RSTParser

from .utils import patch_parser

TEMPLATE = r""".. eval-LANG::
(.*?)

"""

RSTEvalParser = patch_parser(TEMPLATE, RSTParser)
