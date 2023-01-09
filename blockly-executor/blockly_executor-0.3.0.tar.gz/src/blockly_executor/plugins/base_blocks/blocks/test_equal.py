from blockly_executor.core.block_templates.simple_block import SimpleBlock
from blockly_executor import ExtException


class TestEqual(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        if block_context['ACTUAL_VALUE'] != block_context['DESIRED_VALUE']:
            raise ExtException(
                message='Test failed',
                detail=f"{block_context['NAME']} = "
                       f"{block_context['ACTUAL_VALUE']} должно быть {block_context['DESIRED_VALUE']}")
