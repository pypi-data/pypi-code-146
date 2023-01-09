from blockly_executor.core.block import Block


class SimpleBlock(Block):
    required_param = []

    @classmethod
    def get_nodes_fields(cls, node):
        return node.findall("./b:field", cls.ns)

    @classmethod
    def get_nodes_args(cls, node):
        return node.findall("./b:value", cls.ns)

    async def get_fields(self, node, path, context, block_context):
        fields = self.get_nodes_fields(node)
        if fields is not None:
            for i in range(len(fields)):
                _param_name = fields[i].get('name')
                block_context[_param_name] = fields[i].text

    async def get_args(self, node, path, context, block_context):
        args = self.get_nodes_args(node)
        if args is not None:
            for i in range(len(args)):
                _param_name = args[i].get('name')
                if _param_name not in block_context:
                    block_context[_param_name] = await self.execute_all_next(args[i], f'{path}.{_param_name}', context,
                                                                             block_context)

    async def _execute(self, node, path, context, block_context):
        await self.get_args(node, path, context, block_context)
        await self.get_fields(node, path, context, block_context)

        if 'result' not in block_context:
            self._check_step(context, block_context)
            self.check_required_param_in_block_context(block_context)
            block_context['result'] = await self._calc_value(node, path, context, block_context)
        else:
            self.logger.debug('skip calc')
        return block_context['result']

    def check_required_param_in_block_context(self, block_context):
        for param in self.required_param:
            if param not in block_context:
                raise Exception(f'{self.__class__.__name__} required param not defined ({param})')

    async def _calc_value(self, node, path, context, block_context):
        raise NotImplemented(f'{self.__class__.__name__}._calc_value')

