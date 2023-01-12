"""MyST
=======

Provide ``MystEvalParser``.
"""
from myst_parser.parsers.sphinx_ import MystParser

from .utils import patch_parser

TEMPLATE = r"""```\{eval-LANG\}
(.*?)
```
"""

MystEvalParser = patch_parser(TEMPLATE, MystParser)
