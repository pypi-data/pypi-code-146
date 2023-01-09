from blockly_executor.core.block_templates.simple_block import SimpleBlock


class LogicOperation(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        if block_context['OP'] == 'AND':
            return block_context['A'] and block_context['B']
        elif block_context['OP'] == 'OR':
            return block_context['A'] or block_context['B']
        else:
            raise Exception(f'LogicCompare operation \'{block_context["OP"]}\' not supported')

