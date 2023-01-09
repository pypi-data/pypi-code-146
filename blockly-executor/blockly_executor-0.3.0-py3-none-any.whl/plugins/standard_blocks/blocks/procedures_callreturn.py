from blockly_executor.plugins.standard_blocks.blocks.procedures_callnoreturn import ProceduresCallnoreturn


class ProceduresCallreturn(ProceduresCallnoreturn):

    async def _execute(self, node, path, context, block_context):
        return await self._execute2(node, path, context, block_context)
