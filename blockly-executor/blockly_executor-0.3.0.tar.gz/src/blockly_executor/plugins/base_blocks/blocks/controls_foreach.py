from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ControlsForeach(SimpleBlock):
    required_param = ['VAR', 'LIST']

    async def _calc_value(self, node, path, context, block_context):
        if 'INDEX' not in block_context:
            block_context['INDEX'] = 0
        self.set_variable(context, block_context['VAR'], block_context['INDEX'])
        if block_context['LIST']:
            while block_context['INDEX'] < len(block_context['LIST']):
                await self.execute_all_next(node[2], path, context, block_context, True)
                block_context['INDEX'] += 1
                self.set_variable(context, block_context['VAR'], block_context['INDEX'])
                context.set_step(self.block_id)
