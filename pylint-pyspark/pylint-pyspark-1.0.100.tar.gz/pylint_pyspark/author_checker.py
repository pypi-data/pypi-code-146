from __future__ import annotations

import sys

from astroid import nodes

from pylint.checkers import utils
from pylint.checkers.base.basic_checker import _BasicChecker

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

def _infer_dunder_doc_attribute(
    node: nodes.Module | nodes.ClassDef | nodes.FunctionDef,
) -> str | None:
    # Try to see if we have a `__doc__` attribute.
    try:
        docstring = node["__doc__"]
    except KeyError:
        return None

    docstring = utils.safe_infer(docstring)
    if not docstring:
        return None
    if not isinstance(docstring, nodes.Const):
        return None
    return str(docstring.value)

class AuthorChecker(_BasicChecker):
    name = 'missing-author'
    priority = -1
    msgs = {
        'C4002': (
            'Module docstring must have at least one author.',
            'missing-author',
            'This module is missing an author.'
        ),
    }

    def visit_module(self, node: nodes.Module) -> None:
        self._check_documentation_author(node)

    def _check_documentation_author(self, node: nodes.Module, report_missing: bool = True) -> None:
        docstring = node.doc_node.value if node.doc_node else None
        if docstring is None:
            docstring = _infer_dunder_doc_attribute(node)
        if docstring is None:
            self.add_message('missing-author', node=node)
            if not report_missing:
                return
        elif "Author" not in docstring:
            self.add_message('missing-author', node=node)
