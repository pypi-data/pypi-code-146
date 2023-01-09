from blockly_executor.core.block_templates.simple_block import SimpleBlock


class VariablesGet(SimpleBlock):
    required_param = ['VAR']

    async def _calc_value(self, node, path, context, block_context):
        try:
            return self.get_variable(context, block_context['VAR'])
        except KeyError as key:
            raise Exception(f'Variable {key} not defined')


