from blockly_executor.core.block import Block


class ProceduresDefnoreturn(Block):
    def __init__(self, executor, **kwargs):
        super().__init__(executor, **kwargs)
        self.name = None
        self.node = None

    @classmethod
    def get_func_name(cls, node):
        return node.find("./b:field[@name='NAME']", cls.ns).text

    @classmethod
    def get_node_stack(cls, node):
        return node.find("./b:statement[@name='STACK']", cls.ns)

    async def _execute(self, node, path, context, block_context):
        self._check_step(context, block_context)
        code = self.get_node_stack(node)
        if code and '_stack' not in block_context:
            await self.execute_all_next(code, f'{path}.{self.name}', context, block_context, True)
            block_context['_stack'] = None


