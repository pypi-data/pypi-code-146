import json
from typing import List

from ..native import *
from .definition import Definition


def write_list(left: str, right: str, lines=List[object], indent: int = 0):
    if lines is None:
        return left + right + '\n'
    if len(lines) == 0:
        return left + right
    return left + '\n' + ',\n'.join([' ' * (indent + 1) * 4 + x for x in lines]) + '\n' + ' ' * indent * 4 + right


def write_definition(definition, indent):
    s = f'Definition.create({definition.node_type.__name__}'
    if definition.identifier:
        s += f", '{definition.identifier}'"
    s += ')'  # of create
    kwargs = [f'{key}={write_template(value, indent + 1)}' for key, value in definition.kwargs.items()]
    if len(definition.children) > 0:
        kwargs.append(f'children={write_template(definition.children, indent + 1)}')
    s += write_list('(', ')', kwargs, indent)
    return s


def write_indent(indent):
    return ' ' * indent * 4


def _write_template(template, indent):
    s = f'\n\nclass {template.__name__}({template.Definition.class_name}):\n'
    s += write_indent(indent + 1) + 'Definition = ' + write_template(template.Definition, 1)
    s += '\n\n' \
         '    class Named:\n' \
         '\n' \
         '        def __init__(self):\n'
    for name, cls in template.Definition.iterate_identifiers():
        s += f'            self.{name}: {cls.__name__} = None\n'
    s += '            pass'
    s += '\n\n' \
         '    def __init__(self, **kwargs):\n' \
         '        self.named = self.Named()\n' \
         '        super().__init__(**{**self.Definition.derive_kwargs_for(self), **kwargs})\n'
    return s


writer = {
    Em: lambda input, _: f'{input.value:g} | em',  # 'g' removes trailing zeros and point
    Px: lambda input, _: f'{input.value:g} | px',
    Rem: lambda input, _: f'{input.value:g} | rem',
    Percentage: lambda input, _: f'{input.value:g} | percent',
    float: lambda input, _: f'{input:g}',
    int: lambda input, _: f'{input}',
    str: lambda input, _: input.encode('utf-8'),
    bytes: lambda input, _: input,
    bool: lambda input, _: 'True' if True else 'False',
    None: lambda input, _: f'None',
    Position: lambda input, _: f'{type(input).__name__}.{input.name}',
    Alignment: lambda input, _: f'{type(input).__name__}.{input.name}',
    Justification: lambda input, _: f'{type(input).__name__}.{input.name}',
    Direction: lambda input, _: f'{type(input).__name__}.{input.name}',
    tuple: lambda input, _: '({})'.format(', '.join([write_template(e) for e in input])),
    list: lambda input, indent: write_list('[', ']', [writer[type(x)](x, indent + 1) for x in input], indent),
    Definition: write_definition,
    Color: lambda input, _: str(input)
}


def write_template(item, indent=0):
    if item is None:
        return 'None'
    if hasattr(item, 'Definition'):
        return _write_template(item, indent)
    t = type(item)
    if t in writer:
        return writer[t](item, indent)
    else:
        return ' ' * indent + json.dumps(item)
