from blockly_executor.core.block_templates.simple_block import SimpleBlock
from datetime import datetime


class GetCurrentDatetime(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
