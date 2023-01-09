from blockly_executor.core.block_templates.simple_block import SimpleBlock


class VariablesSet(SimpleBlock):
    required_param = ['VAR']

    async def _calc_value(self, node, path, context, block_context):
        self.set_variable(context, block_context['VAR'], block_context.get('VALUE'))
        return

