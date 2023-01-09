from blockly_executor.core.block_templates.simple_block import SimpleBlock


class ListsGetIndex(SimpleBlock):

    async def _calc_value(self, node, path, context, block_context):
        array = self.get_variable(context, block_context['VAR'])
        mode = block_context['MODE']
        where = block_context['WHERE']
        if mode == 'GET':
            if where == 'FROM_START':
                return array[block_context['AT']]
            elif where == 'FROM_END':
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
            elif where == 'FIRST':
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
            elif where == 'LAST':
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
            elif where == 'RANDOM':
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
            else:
                raise NotImplemented(f'block {self.__class__.__name__} where {where} ')
        elif mode == 'GET_REMOVE':
            raise NotImplemented(f'block {self.__class__.__name__} mode {mode} ')
        elif mode == 'REMOVE':
            raise NotImplemented(f'block {self.__class__.__name__} mode {mode} ')
        else:
            raise NotImplemented(f'block {self.__class__.__name__} mode {mode} ')
