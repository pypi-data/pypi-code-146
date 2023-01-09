def pretty_dict(content):
    pretty_code = str(content)
    pretty_code = pretty_code.replace(',', ',\n\t')
    pretty_code = pretty_code.replace('{', '{\n\t')
    pretty_code = pretty_code.replace('}', '\n}')
    return (pretty_code)


divider = '\n----------*----------\n'


CODE = {
    'default': '\033[0m',
    'warning': '\033[93m',
    'error': '\033[91m',
    'blue': '\033[94m',
    'success': '\033[92m',
    'header': '\033[95m',
    'red': '\033[91m',
    'green': '\033[92m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'yellow': '\033[93m',
    'magenta': '\033[95m',
    'grey': '\033[90m',
    'black': '\033[90m',
}


def printify(*args, **kwargs):
    # Check Color
    color = 'default'
    if 'color' in kwargs:
        color = kwargs['color']

    # Format Dict
    list_args = list(args)
    for i, arg in enumerate(list_args):
        if isinstance(arg, dict):
            list_args[i] = pretty_dict(arg)
    tuple_args = tuple(list_args)

    # Print
    if color != 'pretty':
        print(CODE[color], *tuple_args, CODE["default"],
              sep=divider)
    else:
        # Set auto color
        for i, arg in enumerate(args):
            if isinstance(arg, dict):
                print(CODE['yellow'], tuple_args[i], divider, CODE['default'])
                continue
            elif isinstance(arg, list) or isinstance(arg, tuple):
                print(CODE['magenta'], tuple_args[i], divider, CODE['default'])
                continue
            print(CODE['cyan'], tuple_args[i], divider, CODE['default'])
