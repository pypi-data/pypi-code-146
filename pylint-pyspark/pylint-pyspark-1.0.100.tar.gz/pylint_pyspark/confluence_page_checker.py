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

class ConfluencePageChecker(_BasicChecker):
    name = 'missing-documentation-link'
    priority = -1
    msgs = {
        'C4001': (
            'Module docstring must link to a *.atlassian.net page.',
            'missing-documentation-link',
            'This module is missing a link to a Confluence documentation page. Each module should have a corresponding documentation page.'
        ),
    }

    def visit_module(self, node: nodes.Module) -> None:
        self._check_documentation_link(node)

    def _check_documentation_link(self, node: nodes.Module, report_missing: bool = True) -> None:
        docstring = node.doc_node.value if node.doc_node else None
        if docstring is None:
            docstring = _infer_dunder_doc_attribute(node)
        if docstring is None:
            self.add_message('missing-documentation-link', node=node)
            if not report_missing:
                return
        elif "atlassian.net" not in docstring:
            self.add_message('missing-documentation-link', node=node)
