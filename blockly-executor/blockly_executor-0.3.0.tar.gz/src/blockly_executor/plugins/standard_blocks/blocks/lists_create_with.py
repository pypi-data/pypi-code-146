from blockly_executor.core.block import Block


class ListsCreateWith(Block):

    @classmethod
    def get_list_size(cls, node):
        mutation = node.find(f"./b:mutation", cls.ns)
        if mutation is None:
            return 0
        return int(mutation.get('items', '0'))

    @classmethod
    def get_node_add(cls, node, number):
        return node.find(f"./b:value[@name='ADD{number}']", cls.ns)

    async def _execute(self, node, path, context, block_context):
        total_size = self.get_list_size(node)
        result = []
        if not total_size:
            return result
        if 'value' not in block_context:
            block_context['value'] = []
        current_size = len(block_context['value'])
        if current_size != total_size:
            for j in range(current_size, total_size):
                node_value = self.get_node_add(node, j)
                if node_value is None:
                    raise Exception(f'плохой блок ADD{j}')
                result = await self.execute_all_next(node_value, f'{path}.{j}', context, block_context)
                block_context['value'].append(result)
        self._check_step(context, block_context)
        return block_context['value']
    #
    # @classmethod
    # def set_friendly_id(cls, node, index, executor):
    #     friendly_name = 'create_list'
    #     cls._set_friendly_id(node, index, friendly_name)
    #     size = cls.get_list_size(node)
    #     if not size:
    #         return
    #     for j in range(size):
    #         node_add = cls.get_node_add(node, j)
    #         cls.set_friendly_id_for_all_next(node_add, index, executor)
