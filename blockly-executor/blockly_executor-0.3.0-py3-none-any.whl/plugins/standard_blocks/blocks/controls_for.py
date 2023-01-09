from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ControlsFor(SimpleBlock):
    required_param = []

    async def _calc_value(self, node, path, context, block_context):
        if 'INDEX' not in block_context:
            block_context['INDEX'] = block_context['FROM']
        node_loop = node.find("./b:statement[@name='DO']", self.ns)
        while block_context['INDEX'] <= block_context['TO']:
            self.set_variable(context, block_context['VAR'], block_context['INDEX'])
            await self.execute_all_next(node_loop, path, context, block_context, True)
            block_context['INDEX'] += block_context['BY']
            context.set_step(self.block_id)
