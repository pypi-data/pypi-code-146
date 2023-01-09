from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ObjPropSet(SimpleBlock):
    async def _calc_value(self, node, path, context, block_context):
        variable_name = block_context.get('VAR', '')
        obj = self.get_variable(context, variable_name)
        obj[block_context.get('PATH', '')] = block_context.get('VALUE', '')
        self.set_variable(context, variable_name, obj)
