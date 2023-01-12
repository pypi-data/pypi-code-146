from __future__ import annotations

from os.path import basename

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from winval.antlr.winvalLexer import winvalLexer
from winval.antlr.winvalParser import winvalParser
from winval.parsed_workflow_inputs import ParsedWorkflowInputs
from winval.python_extensions import defined, prefix, suffix, iff, imply
from winval.constraint_eval import ConstraintEval
from winval import logger


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        raise SyntaxError("ERROR: when parsing line %d column %d: %s\n" % (line, column, msg))


class Winval:

    def __init__(self, workflow_inputs: ParsedWorkflowInputs, constraints: list[str]):
        self.workflow_inputs = workflow_inputs
        self.constraints = constraints
        self.__exemplify_extensions()

    def workflow_input_validation(self) -> bool:
        validations: list[tuple[bool, str]] = self.eval_constraints()
        passed = [v for v in validations if v[0]]
        failed = [v for v in validations if not v[0]]
        all_passed = len(failed) == 0
        if len(passed) > 0:
            logger.debug('Passed validations:')
        for validation in passed:
            logger.debug(f'True: {validation[1]}')
        if not all_passed:
            logger.error('Failed validations:')
        for validation in failed:
            logger.error(f'False: {validation[1]}')
        if all_passed:
            logger.info(f'Passed all {len(passed)} winval validations!')
        return all_passed

    def eval_constraints(self) -> list[tuple[bool, str]]:
        validations = []
        error_listener = MyErrorListener()
        for constraint_str in self.constraints:
            # lexer
            lexer = winvalLexer(InputStream(constraint_str))
            # def recover(self, e): pass
            # lexer.recover = recover
            lexer.removeErrorListeners()
            lexer.addErrorListener(error_listener)
            try:
                stream = CommonTokenStream(lexer)
                # parser
                parser = winvalParser(stream)
                tree = parser.constraint()
                # evaluator
                visitor = ConstraintEval(self.workflow_inputs.workflow_vars)
                try:
                    validation_result = visitor.visit(tree)
                except (KeyError, TypeError) as e:
                    validation_result = False
                    constraint_str += f' : ( {str(e).strip()} )'
            except (SyntaxError, ValueError) as e:
                validation_result = False
                constraint_str += f' : ( {str(e).strip()} )'
            validations.append((validation_result, constraint_str))
        return validations

    @staticmethod
    def __exemplify_extensions():
        # Use winval_python_extensions, so that import is not unused
        assert defined(6)
        assert prefix('a.bam') == 'a'
        assert suffix('a.bam') == '.bam'
        assert suffix(['a.bam']) == {'.bam'}
        assert basename('gs://bucket/a.bam') == 'a.bam'
        assert iff(True, True)
        assert imply(False, True)
        assert imply(1 > 2, True)
        assert imply(4 > 1, 2 > 1)
