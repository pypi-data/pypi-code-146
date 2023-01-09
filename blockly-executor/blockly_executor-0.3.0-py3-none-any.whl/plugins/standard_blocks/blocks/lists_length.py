from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ListsLength(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        array = block_context.get('VALUE', [])
        if isinstance(array, list):
            return len(array)
        return 0
