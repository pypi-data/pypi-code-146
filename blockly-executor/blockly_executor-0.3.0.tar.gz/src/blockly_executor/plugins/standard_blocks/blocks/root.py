from blockly_executor.core.block import Block


class Root(Block):

    async def _execute(self, node, path, context, block_context):
        await self.execute_all_next(node, path, context, block_context, True)
        return

