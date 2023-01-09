from blockly_executor.core.block_templates.simple_block import SimpleBlock


class MathArithmetic(SimpleBlock):
    required_param = ['OP', 'A', 'B']

    async def _calc_value(self, node, path, context, block_context):
        return operations[block_context['OP']](block_context['A'], block_context['B'])


def add(a, b):
    return a + b


def minus(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def power(a, b):
    return a ^ b


operations = {
    'ADD': add,
    'MINUS': minus,
    'MULTIPLY': multiply,
    'DIVIDE': divide,
    "POWER": power
}
