from blockly_executor.core.block import Block


class Text(Block):

    async def _execute(self, node, path, context, block_context):
        return node[0].text
