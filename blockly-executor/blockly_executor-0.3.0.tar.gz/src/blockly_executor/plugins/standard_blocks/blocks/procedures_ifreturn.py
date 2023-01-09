from blockly_executor.core.block_templates.simple_block import SimpleBlock
from blockly_executor.core.block import ReturnFromFunction


class ProceduresIfreturn(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        if block_context['CONDITION']:
            raise ReturnFromFunction(block_context.get('VALUE'))
