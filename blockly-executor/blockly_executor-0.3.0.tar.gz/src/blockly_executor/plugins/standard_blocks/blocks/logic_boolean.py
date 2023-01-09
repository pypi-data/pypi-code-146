from blockly_executor.core.block_templates.simple_block import SimpleBlock


class LogicBoolean(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        return True if block_context['BOOL'] == 'TRUE' else False
