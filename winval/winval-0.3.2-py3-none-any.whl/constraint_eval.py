from __future__ import annotations

import argparse
import json
from os.path import basename, splitext

from antlr4 import *

from winval.antlr.winvalLexer import winvalLexer
from winval.antlr.winvalParser import winvalParser
from winval.antlr.winvalVisitor import winvalVisitor
from winval.python_extensions import iff, imply, defined, prefix, suffix
from winval.wdl_parser import WdlParser
from winval.workflow_var import WorkflowVar


def strip_string(string: str) -> str:
    return string.replace('"', '').replace("'", '')


class ConstraintEval(winvalVisitor):

    def __init__(self, workflow_variables: dict[str, WorkflowVar]):
        self.workflow_variables = workflow_variables

    def visitConstraint(self, ctx):
        if not ctx.EOF():
            # evaluate expression for further error reporting
            self.visit(ctx.expr())
            return False
        expression_value = self.visit(ctx.expr())
        if type(expression_value) != bool:
            raise ValueError(f'constraint evaluated to non-boolean value: {expression_value} , {ctx.getText()}')
        return expression_value

    def visitIntExpr(self, ctx):
        return int(ctx.getText())

    def visitBoolExpr(self, ctx):
        return ctx.getText() == 'True'

    def visitFloatExpr(self, ctx):
        return float(ctx.getText())

    def visitStringExpr(self, ctx):
        return strip_string(ctx.getText())

    def visitEmptySetExpr(self, ctx):
        return set()


    def visitAccessExpr(self, ctx):
        collection = self.visit(ctx.struct)
        key = self.visit(ctx.key)
        return collection[key]

    def visitListExpr(self, ctx):
        if len(ctx.elements().INT()) > 0:
            return [int(elm.getText()) for elm in ctx.elements().INT()]
        elif len(ctx.elements().FLOAT()) > 0:
            return [float(elm.getText()) for elm in ctx.elements().FLOAT()]
        elif len(ctx.elements().STRING()) > 0:
            return [strip_string(elm.getText()) for elm in ctx.elements().STRING()]
        elif len(ctx.elements().VARIABLE()) > 0:
            return [self.workflow_variables[elm.getText()].value for elm in ctx.elements().VARIABLE()]

    def visitSetExpr(self, ctx):
        return set(self.visitListExpr(ctx))

    def visitParenExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitInfixExpr(self, ctx):
        left = self.visit(ctx.left)
        op = ctx.op.text

        # Don't eval right expression (could contain runtime error) under some cases
        if op == '->' and left is False:
            return True
        if op == 'and' and left is False:
            return False
        if op == 'or' and left is True:
            return True

        right = self.visit(ctx.right)

        operation = {
            '<->': lambda: iff(left, right),
            '->': lambda: imply(left, right),
            'and': lambda: left and right,
            'or': lambda: left or right,
            '>': lambda: left > right,
            '>=': lambda: left >= right,
            '==': lambda: left == right,
            '!=': lambda: left != right,
            '<=': lambda: left <= right,
            '<': lambda: left < right,
            'in': lambda: left in right,
            '+': lambda: left + right,
            '-': lambda: left - right,
            '*': lambda: left * right,
            '/': lambda: left / right,
            '**': lambda: left ** right,
            '&': lambda: left & right,
            '|': lambda: left | right,
            '%': lambda: left % right,
        }
        return operation.get(op, lambda: None)()

    def visitPrefixExpr(self, ctx):
        operand = self.visit(ctx.operand)
        op = ctx.op.text
        operation = {
            'defined': lambda: defined(operand),
            'len': lambda: len(operand),
            'set': lambda: set(operand),
            'prefix': lambda: prefix(operand),
            'suffix': lambda: suffix(operand),
            'basename': lambda: basename(operand),
            'splitext': lambda: splitext(operand),
            'not': lambda: not operand,
        }
        return operation.get(op, lambda: None)()

    def visitVariableExpr(self, ctx):
        if ctx.getText() in self.workflow_variables:
            return self.workflow_variables[ctx.getText()].value
        else:
            raise ValueError(f'Undeclared variable: {ctx.getText()}\n')

    def visitVariableExpr2(self, ctx):
        return self.visitVariableExpr(ctx)


def get_args():
    parser = argparse.ArgumentParser("winval")
    parser.add_argument('--wdl', required=True)
    parser.add_argument('--json', required=True)
    parser.add_argument('--log_level', default='INFO')
    return parser.parse_args()


def main():
    args = get_args()
    workflow_inputs = WdlParser(args.wdl).parse_workflow_variables()
    with open(args.json) as json_file:
        json_dict = json.load(json_file)
        workflow_inputs.fill_values_from_json(json_dict)

    while 1:
        data = InputStream(input(">>> "))
        # lexer
        lexer = winvalLexer(data)
        stream = CommonTokenStream(lexer)

        # parser
        parser = winvalParser(stream)
        tree = parser.constraint()
        # evaluator
        visitor = ConstraintEval(workflow_inputs.workflow_vars)
        try:
            output = visitor.visit(tree)
            print(output)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
