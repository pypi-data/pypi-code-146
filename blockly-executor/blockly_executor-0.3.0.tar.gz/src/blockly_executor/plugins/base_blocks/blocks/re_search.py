from blockly_executor.core.block_templates.simple_block import SimpleBlock
import re


class ReSearch(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        _res = re.search(re.compile(block_context['re']), block_context['value'])
        if not _res:
            return ''
        return _res.group(0)
