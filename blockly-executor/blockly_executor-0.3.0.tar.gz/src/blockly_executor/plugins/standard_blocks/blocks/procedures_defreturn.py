from blockly_executor.plugins.standard_blocks.blocks.procedures_defnoreturn import ProceduresDefnoreturn


class ProceduresDefreturn(ProceduresDefnoreturn):

    @classmethod
    def get_node_return(cls, node):
        return node.find("./b:value[@name='RETURN']", cls.ns)

    async def _execute(self, node, path, context, block_context):
        await super()._execute(node, path, context, block_context)

        _return_node = self.get_node_return(node)
        res = await self.execute_all_next(_return_node, f'{path}.{self.name}', context, block_context)
        return res
