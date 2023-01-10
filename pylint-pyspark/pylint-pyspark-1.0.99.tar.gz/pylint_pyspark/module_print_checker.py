from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from .pylint_utils import module_contains_print


class ModulePrintChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "module-print"
    priority = -1
    msgs = {
        "C4008": (
            "Production notebooks should not contain print() calls.",
            "module-contains-print",
            "Calling print() can clutter the module when running a pipeline.",
        ),
    }

    def __init__(self, linter=None):
        super(ModulePrintChecker, self).__init__(linter)
        self._function_stack = []

    def visit_functiondef(self, node):
        self._function_stack.append([])

    def visit_expr(self, node):
        if module_contains_print(node):
            self.add_message("module-contains-print", node=node)

    def leave_functiondef(self, node):
        self._function_stack.pop()
