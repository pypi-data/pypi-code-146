from typing import Literal
def with_linebreaks(css: str) -> str:
    return css.replace('{', '{\n').replace('}', '}\n').replace(';', ';\n')


def with_indents(
    css: str, 
    indent_mode: Literal['tabs', 'spaces'] = 'tabs'
) -> str:

    css_lines = css.split('\n')
    tab = '\t' if indent_mode == 'tabs' else '    '
    indentation_level = 0
    for line_num, content in enumerate(css_lines):
        if '}' in content: indentation_level -= 1
        css_lines[line_num] = (tab * indentation_level) + content
        if '{' in content: indentation_level += 1
    return '\n'.join(css_lines)

