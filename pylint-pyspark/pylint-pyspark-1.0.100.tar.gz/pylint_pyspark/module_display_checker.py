from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

from .pylint_utils import module_contains_display

class ModuleDisplayChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "module-display"
    priority = -1
    msgs = {
        "C4006": (
            "Production notebooks should not contain .display() or display() calls.",
            "module-contains-display",
            "Calling .display() or display() can clutter the module when running a pipeline.",
        ),
    }

    def __init__(self, linter=None):
        super(ModuleDisplayChecker, self).__init__(linter)
        self._function_stack = []

    def visit_functiondef(self, node):
        self._function_stack.append([])

    def visit_expr(self, node):
        if module_contains_display(node):
            self.add_message("module-contains-display", node=node)

    def leave_functiondef(self, node):
        self._function_stack.pop()
