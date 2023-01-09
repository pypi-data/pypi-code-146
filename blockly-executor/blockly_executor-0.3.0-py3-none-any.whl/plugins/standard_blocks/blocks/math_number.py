from blockly_executor.core.block_templates.simple_block import SimpleBlock


class MathNumber(SimpleBlock):
    required_param = ['NUM']

    async def _calc_value(self, node, path, context, block_context):
        value = block_context['NUM']
        float_value = float(value)
        int_value = int(float_value)
        if int_value == float_value:
            return int_value
        else:
            return float_value
