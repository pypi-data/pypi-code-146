from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ControlsForeach(SimpleBlock):
    required_param = ['VAR', 'LIST']

    async def _calc_value(self, node, path, context, block_context):
        if '_INDEX' not in block_context:
            block_context['_INDEX'] = 0
        if block_context['LIST']:
            while block_context['_INDEX'] < len(block_context['LIST']):
                self.set_variable(context, block_context['VAR'], block_context['LIST'][block_context['_INDEX']])
                await self.execute_all_next(node[2], path, context, block_context, True)
                block_context['_INDEX'] += 1
                context.set_step(self.block_id)
