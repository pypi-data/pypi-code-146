from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ObjPropAppend(SimpleBlock):
    async def _calc_value(self, node, path, context, block_context):
        obj = self.get_variable(context, block_context['VAR'])
        if block_context['PATH']:
            obj[block_context['PATH']].append(block_context['VALUE'])
        else:
            obj.append(block_context['VALUE'])
        self.set_variable(context, block_context['VAR'], obj)  #todo для объектов не заменять объект, а обновлять свойство


