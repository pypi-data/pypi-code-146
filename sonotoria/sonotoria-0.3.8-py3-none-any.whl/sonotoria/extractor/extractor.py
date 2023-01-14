import re

from .cast import ensure_data_types
from .cond_extractor import prepare_cond_template
from .var_extractor import prepare_var_template
from . import for_loop


ESCAPE_CHARS = ['(', ')', '?', '.']


def escape_char(tpl):
    for char in ESCAPE_CHARS:
        tpl = tpl.replace(char, f'\\{char}')
    return tpl

def add_border(tpl):
    return f'^{tpl}$'

def prepare_regex(regex, loops):
    regex = for_loop.extract_top(regex, loops)
    regex = prepare_var_template(regex)
    regex = prepare_cond_template(regex)
    return regex

def extract(template, input_):
    regex = escape_char(template)
    loops = for_loop.find_top(regex)

    regex = prepare_regex(regex, loops)
    regex = add_border(regex)

    data = ensure_data_types(re.search(regex, input_, re.DOTALL).groupdict())
    data = extract_data_from_loops(loops, data)
    return data

def extract_data_from_loop(loop, data):
    regex = loop.content
    loops = for_loop.find_top(regex)
    regex = prepare_regex(regex, loops)

    local_data_per_iteration = [
        item.groupdict()
        for item in re.finditer(regex, data[loop.id])
    ]

    loop_variables = {
        loop.name: {
            local_data[loop.vars[0]]: local_data[loop.vars[1]]
            for local_data in local_data_per_iteration
        } if loop.is_dict else [
            local_data[loop.vars[0]]
            for local_data in local_data_per_iteration
        ]
    }

    variables_unrelated_to_loop = {
        key: value
        for key, value in local_data_per_iteration[0].items()
        if key not in loop.vars
    }

    data_with_nested_loops_data = extract_data_from_loops(loops, data)

    return {
        **data_with_nested_loops_data,
        **ensure_data_types(loop_variables),
        **ensure_data_types(variables_unrelated_to_loop)
    }

def extract_data_from_loops(loops, data):
    for loop in loops:
        data = extract_data_from_loop(loop, data)
    return data
