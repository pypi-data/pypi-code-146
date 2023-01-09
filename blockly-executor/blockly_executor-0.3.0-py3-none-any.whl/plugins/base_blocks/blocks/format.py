from blockly_executor.core.block_templates.simple_block import SimpleBlock
from datetime import datetime


def format_to_date(value, format_string):
    date = datetime.strptime(value, format_string)
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')


def format_from_date(value, format_string):
    date = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    return date.strftime(format_string)


def format_to_string(value, format_string=None):
    return str(value)


def format_to_number(value, format_string=None):
    try:
        float_value = float(value)
        int_value = int(float_value)
        if int_value == float_value:
            return int_value
        else:
            return float_value
    except:
        return 0


operations = {
    'to_date': format_to_date,
    'from_date': format_from_date,
    'to_number': format_to_number,
    'to_string': format_to_string
}


class Format(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        try:
            operation = operations[block_context['type']]
        except KeyError as key:
            raise NotImplemented(f'block {self.__class__.__name__} operation {block_context["type"]} ')
        block_context['result'] = operation(block_context['value'], block_context['template'])
        return block_context['result']
