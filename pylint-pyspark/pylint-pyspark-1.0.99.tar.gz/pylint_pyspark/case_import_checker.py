
import astroid
from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.imports import ImportsChecker

class CaseImportChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "import-case-checker"

    priority = -1
    msgs = {
        'C4003': ('pyspark.sql.functions module should be imported as F instead of f',
                  'lower-case-function-import',
                  'Follow AstrumU convention by importing the functions module as capital F.'),
        'C4004': ('pyspark.sql.types module should be imported as T instead of t',
                  'lower-case-type-import',
                  'Follow AstrumU convention by importing the types module as capital T.'),
        'C4005': ('pyspark.sql.utils module should be imported as U instead of u',
                  'lower-case-utils-import',
                  'Follow AstrumU convention by importing the utils module as capital U.'),
    }
    def __init__(self, linter):
        super(CaseImportChecker, self).__init__(linter)
        self._check_import_stack = []

    def _check_import(self, node: nodes.Import):
        if node.names[0][0] == "pyspark.sql.functions" and node.names[0][1] == 'f':
            self.add_message(
                "lower-case-function-import", node=node
            )
        elif node.names[0][0] == "pyspark.sql.types" and node.names[0][1] == 't':
            self.add_message(
                "lower-case-type-import", node=node
            )
        elif node.names[0][0] == "pyspark.sql.utils" and node.names[0][1] == 'u':
            self.add_message(
                "lower-case-utils-import", node=node
            )

    def visit_import(self, node):
        self._check_import_stack.append([])
        

    def leave_import(self, node):
        self._check_import(node)
        self._check_import_stack.pop()