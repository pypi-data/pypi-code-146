from blockly_executor.core.block import Block


class ControlsIf(Block):
    async def _execute(self, node, path, context, block_context):
        if_count = int(self._get_mutation(node, 'elseif', 0)) + 1
        defined_else = int(self._get_mutation(node, 'else', 0))
        if_complete = False
        j = None
        for j in range(if_count):
            # рассчитываем все if
            _key = f'IF{j}'
            complete = _key in block_context
            if complete:
                result = block_context.get(_key)
            else:
                node_if = self._get_node_if(node, j)
                if node_if is None:
                    raise Exception(f'Bad {_key} {path}')
                result = await self.execute_all_next(node_if, f'{path}.if{j}', context, block_context)
                block_context[_key] = result
            if result:
                if_complete = True
                break
        self._check_step(context, block_context)
        if if_complete and j is not None:
            if '_do' not in block_context:
                node_do = self._get_node_do(node, j)
                if node_do is None:
                    return
                    # raise Exception(f'Bad if DO {j} {path}')
                await self.execute_all_next(node_do, f'{path}.do{j}', context, block_context, True)
                block_context['_do'] = None
        else:
            if defined_else:
                if '_do' not in block_context:
                    node_do = self._get_node_else(node)
                    if node_do is None:
                        return
                        # raise Exception(f'Bad else DO {path}')
                    await self.execute_all_next(node_do, f'{path}.else', context, block_context, True)
                    block_context['_do'] = None

        # return self.get_next_statement(node)

    @classmethod
    def set_friendly_id(cls, node, index, executor):
        friendly_name = 'if'
        cls._set_friendly_id(node, index, friendly_name)
        if_count = int(cls._get_mutation(node, 'elseif', 0)) + 1
        defined_else = int(cls._get_mutation(node, 'else', 0))
        for j in range(if_count):
            node_if = cls._get_node_if(node, j)
            cls.set_friendly_id_for_all_next(node_if, index, executor)
            node_do = cls._get_node_do(node, j)
            cls.set_friendly_id_for_all_next(node_do, index, executor)
        if defined_else:
            node_else = cls._get_node_else(node)
            cls.set_friendly_id_for_all_next(node_else, index, executor)

    @classmethod
    def _get_node_if(cls, node, number):
        return node.find(f"./b:value[@name='IF{number}']", cls.ns)

    @classmethod
    def _get_node_do(cls, node, number):
        return node.find(f"./b:statement[@name='DO{number}']", cls.ns)

    @classmethod
    def _get_node_else(cls, node):
        return node.find(f"./b:statement[@name='ELSE']", cls.ns)
