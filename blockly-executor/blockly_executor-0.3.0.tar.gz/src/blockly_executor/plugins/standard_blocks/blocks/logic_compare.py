from blockly_executor.core.block_templates.simple_block import SimpleBlock


class LogicCompare(SimpleBlock):
    required_param = ['A', 'B', 'OP']

    async def _calc_value(self, node, path, context, block_context):
        operation = block_context['OP']
        if operation == 'EQ':
            return block_context['A'] == block_context['B']
        elif operation == 'NEQ':
            return block_context['A'] != block_context['B']
        else:
            raise Exception(f'LogicCompare operation "{operation}" not supported')
