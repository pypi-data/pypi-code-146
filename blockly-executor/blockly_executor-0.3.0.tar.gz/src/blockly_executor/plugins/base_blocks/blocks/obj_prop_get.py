from blockly_executor.core.block_templates.simple_block import SimpleBlock
from blockly_executor import ExtException
from blockly_executor import Helper


class ObjPropGet(SimpleBlock):
    async def _calc_value(self, node, path, context, block_context):
        obj_name = block_context.get('VAR', '')
        path = block_context.get('PATH', '')
        try:
            obj = self.get_variable(context, obj_name)
        except KeyError:
            raise ExtException(
                message='variable not defined',
                detail=obj_name,
                dump={
                    'block_context': block_context,
                    'block_id': self.block_id,
                    'full_name': self.full_name
                }
            )
        if path and path[0] == "\"":
            path = path[1:]
            if path[-1] == "\"":
                path = path[:-1]
            return obj.get(path)
        else:
            return Helper.obj_get_path_value(obj, path, delimiter='.')
