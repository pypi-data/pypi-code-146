import typing as tp

import mypy.nodes


class Name:
    def __init__(self, name, type_='Other'):
        self.name = name
        self.type_ = type_

class ModuleName(Name):
    def __init__(self, name):
        super().__init__(name, 'Module')


class TypeName(Name):
    def __init__(self, name):
        super().__init__(name, 'Type')


def get_names(table: mypy.nodes.SymbolTable) -> tp.List[Name]:
    result: tp.List[Name] = []
    for name in table.keys():
        # TODO: remove synthetic names

        node = table[name].node

        if isinstance(node, mypy.nodes.TypeInfo):
            result.append(TypeName(name))
        
        elif isinstance(node, mypy.nodes.MypyFile):
            result.append(ModuleName(name))
        
        else:
            result.append(Name(name))
    
    return result
