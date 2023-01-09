from blockly_executor.core.block import Block


class TextJoin(Block):
    async def _execute(self, node, path, context, block_context):
        text_count = int(self._get_mutation(node, 'items', 0))
        result = ""
        for j in range(text_count):
            _key = f'ADD{j}'
            complete = _key in block_context
            if complete:
                result = block_context.get(_key)
            else:
                node_text = self._get_node_text(node, j)
                next_node_result = await self.execute_all_next(node_text, f'{path}.add{j}', context, block_context)
                result += str(next_node_result)
        return result

    @classmethod
    def _get_node_text(cls, node, number):
        return node.find(f"./b:value[@name='ADD{number}']", cls.ns)
