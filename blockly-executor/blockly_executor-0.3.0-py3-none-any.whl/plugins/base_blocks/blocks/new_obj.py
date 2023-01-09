from blockly_executor.core.block import Block


class NewObj(Block):

    async def _execute(self, node, path, context, block_context):
        mutation_count = int(self._get_mutation(node, 'PROP', 0))
        if 'result' not in block_context:
            block_context['result'] = {}
        if mutation_count:
            for j in range(mutation_count):
                # рассчитываем все мутации
                prop_name = node.find(f"./b:field[@name='PROP{j}_NAME']", self.ns).text
                if not prop_name or prop_name in block_context['result']:
                    continue
                node_prop_value = node.find(f"./b:value[@name='PROP{j}_VALUE']", self.ns)
                prop_value = await self.execute_all_next(node_prop_value, f'{path}.PROP{j}_VALUE', context,
                                                         block_context)
                block_context['result'][prop_name] = prop_value
        self._check_step(context, block_context)
        return block_context['result']
