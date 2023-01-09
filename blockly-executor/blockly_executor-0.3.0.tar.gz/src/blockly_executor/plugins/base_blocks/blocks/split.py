from blockly_executor.core.block_templates.simple_block import SimpleBlock


class Split(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        return block_context['value'].split(block_context['delimiter'])
