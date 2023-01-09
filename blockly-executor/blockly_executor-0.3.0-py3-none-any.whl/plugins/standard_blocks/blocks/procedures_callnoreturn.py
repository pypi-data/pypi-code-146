from blockly_executor.core.block import Block
from blockly_executor.core.block import ReturnFromFunction


class ProceduresCallnoreturn(Block):

    @classmethod
    def get_params(cls, node):
        mutation = node.find(f'./b:mutation', cls.ns)
        if mutation is None:
            raise Exception('Не поддерживаемый callnoreturn')
        func_name = mutation.get('name')
        args_name_nodes = mutation.findall("./b:arg", cls.ns)
        args = []
        value_nodes = None
        if args_name_nodes is not None:
            count_args = len(args_name_nodes)
            for i in range(count_args):
                args.append(args_name_nodes[i].get('name'))
                pass
            value_nodes = node.findall("./b:value", cls.ns)
        return func_name, args, value_nodes

    async def _execute2(self, node, path, context, block_context):
        try:
            endpoint, args, values = self.get_params(node)
            if values:
                for i in range(len(args)):
                    if args[i] not in block_context:
                        if len(values) <= i:
                            _value = None
                        else:
                            _value = await self.execute_all_next(values[i], f'{path}.{i}', context, block_context)
                        self.set_variable(context, args[i], _value)
                        block_context[args[i]] = _value
                    pass
            handler = self.executor.functions[endpoint]
            self._check_step(context, block_context)
            if 'result' not in block_context:
                res = await handler.execute(handler.node, path, context, block_context)
                block_context['result'] = res
            return block_context['result']
        except ReturnFromFunction as err:
            context.set_next_step(self.block_id)
            context.clear_child_context(block_context)
            return err.args[0]

    async def _execute(self, node, path, context, block_context):
        await self._execute2(node, path, context, block_context)
        return self.get_next_statement(node)
