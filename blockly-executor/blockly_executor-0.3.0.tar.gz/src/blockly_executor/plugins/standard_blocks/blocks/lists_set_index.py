from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ListsSetIndex(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        array = self.get_variable(context, block_context['VAR'])
        mode = block_context['MODE']
        where = block_context['WHERE']
        if mode == 'SET':
            if where == 'FROM_START':
                array[block_context['AT']] = block_context['TO']
                return
            elif where == 'FROM_END':
                array[block_context['AT'] * -1] = block_context['TO']
                return
            elif where == 'FIRST':
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
            elif where == 'LAST':
                array.append(block_context['TO'])
                return
            elif where == 'RANDOM':
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
            else:
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
        else:
            raise NotImplemented(f'block {self.__class__.__name__} mode {mode} ')
