from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from .pylint_utils import module_contains_show

class ModuleShowChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "module-show"
    priority = -1
    msgs = {
        "C4007": (
            "Production notebooks should not contain .show() or show() calls.",
            "module-contains-show",
            "Calling .show() or show() can clutter the module when running a pipeline.",
        ),
    }

    def __init__(self, linter=None):
        super(ModuleShowChecker, self).__init__(linter)
        self._function_stack = []

    def visit_functiondef(self, node):
        self._function_stack.append([])

    def visit_expr(self, node):
        if module_contains_show(node):
            self.add_message("module-contains-show", node=node)

    def leave_functiondef(self, node):
        self._function_stack.pop()
