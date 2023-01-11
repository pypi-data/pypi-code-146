import re


def equals_ignore_case(str1, str2):
    return re.fullmatch(str1, str2, flags=re.IGNORECASE) is not None


def validate(value, validations):
    if validations is None:
        raise ValueError("Validations cannot be None")
    elif not isinstance(validations, list):
        validations = [validations]
    if len(validations) == 0:
        return True
    else:
        for valid in validations:
            if re.fullmatch(valid, value):
                return True
        return False


def dict_to_table(dictionary, compact=False):
    if not isinstance(dictionary, dict):
        raise TypeError("Invalid type for parameter 'dictionary'. Must be a Python dictionary")
    longest_key = -1
    longest_value = -1
    for k, v in dictionary.items():
        if len(str(k)) > longest_key:
            longest_key = len(str(k))
        if len(str(v)) > longest_value:
            longest_value = len(str(v))

    if not isinstance(compact, bool):
        raise TypeError("Invalid type for the parameter 'compact'. It must be bool")
    elif compact:
        pad = "_"
        table_border = f"{'_' * (longest_key * 2 + 8)}"
        final = [table_border, "\n"]
    else:
        pad = " "
        table_border = f"+{'-' * (longest_key + 2)}+{'-' * (longest_value + 2)}+"
        final = [table_border, table_border + "\n"]
    for k, v in dictionary.items():
        final.insert(
            len(final) - 1,
            f"|{pad}{k}{pad * (longest_key - len(str(k)))}{pad}|{pad}{v}{pad * (longest_value - len(str(v)))}{pad}|"
        )
    return "\n".join(final)


def text_padding(msg, padding=2, decorator=None, decorate_lines=None):
    valid_dl = [None, 'all', 'first', 'last', 'even', 'odd', []]
    if (decorator is None) ^ (decorate_lines is None):
        raise ValueError("The parameters 'decorator' and 'decorate_lines' must be used together")
    if not isinstance(padding, int):
        raise ValueError("The parameter 'padding' must be a integer number")
    counter = 0
    final = []
    for ln in msg.split('\n'):
        counter += 1
        if decorator is None:
            final.append(f'{" " * padding}{ln}')
        else:
            if (decorate_lines is None) or decorate_lines == '' or \
                    (isinstance(decorate_lines, list) and counter not in decorate_lines) or \
                    (decorate_lines == 'first' and counter != 1) or \
                    (decorate_lines == 'last' and counter != len(msg.split('\n'))) or \
                    (decorate_lines == 'even' and counter % 2 != 0) or \
                    (decorate_lines == 'odd' and counter % 2 == 0):
                _decorator = ' '
            elif not isinstance(decorate_lines, list) and decorate_lines not in valid_dl:
                raise ValueError("Unexpected value for parameter 'decorate_lines'")
            else:
                _decorator = decorator
            final.append(f'{" " * padding}{_decorator} {ln}')
    return "\n".join(final)


def sort_dict(dictionary: dict, sortby='keys', reverse=False):
    if sortby == 'keys':
        sort_key = lambda ele: ele[0]
    elif sortby == 'values':
        sort_key = lambda ele: ele[1]
    else:
        raise ValueError("Invalid value for parameter 'sortby'. Valid: keys | values")
    return {key: val for key, val in sorted(dictionary.items(), key=sort_key, reverse=reverse)}


def join_by(join_char, iterable):
    """
    Joins an <iterable> with <join_char>. Uses list-comprehension
    :param join_char: Char to be used as join
    :param iterable: Iterable to be joined using <join_char>
    :return: A string with all the elements of <iterable> joined by <join_char>
    """
    return str(join_char).join([str(val) for val in iterable])


if __name__ == '__main__':
    # Do some quick tests here
    pass
