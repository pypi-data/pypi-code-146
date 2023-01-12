import os
import re
from glob import glob


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


def dict_to_table(dictionary, compact=False, overflow='hide', _max_line_len=200):
    """

    :param dictionary: Dictionary to be represented as a table
    :param compact: Enable/disable compact table output. May be deprecated soon
    :param overflow: 'hide'| 'wrap'. Controls overflowed lines (those longer than 70 chars)
    :param _max_line_len: Optional. Specifies the max line length. The table overflow is adapted according to it
    :return: a string representing a table with the dictionary keys and values
    """
    __max_line_len__ = _max_line_len
    __max_column_width__ = int(__max_line_len__ / 2)
    __ellips__ = '...'
    __min__pad_size__ = 2
    if not isinstance(dictionary, dict):
        raise TypeError("Invalid type for parameter 'dictionary'. Must be a Python dictionary")
    if overflow not in ['hide', 'wrap']:
        raise ValueError("Unexpected value for parameter 'overflow'. Allowed: hide|wrap")
    if compact:
        overflow = 'hide'
    # lines_len = []
    keys_len = []
    values_len = []
    # Compute the length of each line, key and value
    # Using list comprehension is smaller in code size, but slower in execution (3 loops VS 1)
    # keys_len = [len(str(k)) for k in dictionary.keys()]
    # values_len = [len(str(v)) for v in dictionary.values()]
    # lines_len = [sum(a, b) for a, b in zip(keys_len, values_len)]
    for k, v in {str(_k): str(_v) for _k, _v in dictionary.items()}.items():
        # lines_len.append(len(k) + len(v))
        keys_len.append(len(k))
        values_len.append(len(v))
    # longest_line = max(lines_len), longest_key = max(keys_len), longest_value = max(values_len)
    key_size_limit = min(max(keys_len), __max_column_width__)  # Maximum line length or max column width
    value_size_limit = min(max(values_len), __max_column_width__)  # Maximum line length or max column width
    if not isinstance(compact, bool):
        raise TypeError("Invalid type for the parameter 'compact'. It must be bool")
    elif compact:
        pad_char = "_"
        table_border = f"{'_' * (key_size_limit + value_size_limit + 7)}"  # 7 => table borders and spacing
        final = [table_border, "\n"]
    else:
        pad_char = " "
        table_border = f"+{'-' * (key_size_limit + 3)}+{'-' * (value_size_limit + 3)}+"
        final = [table_border, table_border + "\n"]
    trim_size = __max_column_width__ - len(__ellips__) + 1
    for k, v in {str(_k): str(_v) for _k, _v in dictionary.items()}.items():
        real_kpad = key_size_limit - len(k) + __min__pad_size__ if len(k) <= key_size_limit else 1
        real_vpad = value_size_limit - len(v) + __min__pad_size__ if len(v) <= value_size_limit else 1
        after_key_padding = text_padding(f'|', pad_char=pad_char, padding=real_kpad)
        after_value_padding = text_padding(f'|', pad_char=pad_char, padding=real_vpad)
        if overflow == 'hide':
            # trim + place '...' where necessary + padding
            if len(k) >= __max_column_width__ and len(v) >= __max_column_width__:  # Trim keys and values
                pt1 = f"|{pad_char}{k[0:trim_size]}{__ellips__}{after_key_padding}"
                pt2 = f"{pad_char}{v[0:trim_size]}{__ellips__}{after_value_padding}"
            elif len(k) >= __max_column_width__:  # Trim only keys
                pt1 = f"|{pad_char}{k[0:trim_size]}{__ellips__}{after_key_padding}"
                pt2 = f"{pad_char}{v}{after_value_padding}"
            elif len(v) >= __max_column_width__:  # Trim only values
                pt1 = f"|{pad_char}{k}{after_key_padding}"
                pt2 = f"{pad_char}{v[0:trim_size]}{__ellips__}{after_value_padding}"
            else:  # Do not trim
                pt1 = f"|{pad_char}{k}{after_key_padding}"
                pt2 = f"{pad_char}{v}{after_value_padding}"
            final.insert(len(final) - 1, f"{pt1}{pt2}")
        else:
            # extend row height to fit the content, without exceeding __max_col_width__
            # Add as many row as necessary
            __ellips__ = __ellips__.replace('.', ' ')
            if len(k) >= __max_column_width__ and len(v) >= __max_column_width__:  # Trim keys and values
                trim_start = 0
                while trim_start < max(len(k), len(v)):
                    if trim_start > len(k):
                        pt1 = f"|{pad_char}{' ' * trim_size}{after_key_padding}"
                    else:
                        pt1 = f"|{pad_char}{k[trim_start:trim_start + trim_size]}{after_key_padding}"
                    if trim_start > len(v):
                        pt2 = f"{pad_char}{' ' * trim_size}{after_value_padding}"
                    else:
                        pt2 = f"{pad_char}{v[trim_start:trim_start + trim_size]}{after_value_padding}"
                    final.insert(len(final) - 1, f"{pt1}{pt2}")
                    trim_start += trim_size
            elif len(k) >= __max_column_width__:  # Trim only keys
                trim_start = 0
                while trim_start < len(k):
                    if trim_start == 0:
                        pt2 = f"{pad_char}{v}{after_value_padding}"
                    else:
                        pt2 = f"{pad_char}{' ' * len(v)}{after_value_padding}"
                    if trim_start + trim_size >= len(k):  # If last line
                        k_str = k[trim_start:trim_start + trim_size]
                        pt1 = f"|{pad_char}{k_str}{' ' * (__max_column_width__ - len(k_str) + 1)}{after_key_padding}"
                    else:
                        pt1 = f"|{pad_char}{k[trim_start:trim_start + trim_size]}{__ellips__}{after_key_padding}"
                    final.insert(len(final) - 1, f"{pt1}{pt2}")
                    trim_start += trim_size
            elif len(v) >= __max_column_width__:  # Trim only values
                trim_start = 0
                while trim_start < len(v):
                    if trim_start == 0:
                        pt1 = f"|{pad_char}{k}{after_key_padding}"
                    else:
                        pt1 = f"|{pad_char}{' ' * len(k)}{after_key_padding}"
                    if trim_start + trim_size >= len(v):  # If Last line
                        v_str = v[trim_start:trim_start + trim_size]
                        pt2 = f"{pad_char}{v_str}{' ' * (__max_column_width__ - len(v_str) + 1)}{after_value_padding}"
                    else:
                        pt2 = f"{pad_char}{v[trim_start:trim_start + trim_size]}{__ellips__}{after_value_padding}"
                    final.insert(len(final) - 1, f"{pt1}{pt2}")
                    trim_start += trim_size
            else:  # Do not trim
                pt1 = f"|{pad_char}{k}{after_key_padding}"
                pt2 = f"{pad_char}{v}{after_value_padding}"
                final.insert(len(final) - 1, f"{pt1}{pt2}")
    return "\n".join(final)


def text_padding(msg, padding=2, pad_char=' ', decorator=None, decorate_lines=None):
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
            final.append(f'{pad_char * padding}{ln}')
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
            final.append(f'{pad_char * padding}{_decorator} {ln}')
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


def find_files(rootdir=None, regex=None):
    """
    Find files in a folder. Regex can be applied in the file name

    :param rootdir: Root dir to search for the files. If None, the current dir is used
    :param regex: Regex to be matched against the file names. If None, wild card * is used
    :return: A list of the file names (not full path) from the directory ```rootdir``, that are matching the ``regex``
    """
    if rootdir is None:
        rootdir = '.'
    if regex is None:
        regex = '*'
    return glob(os.path.join(rootdir, regex))


if __name__ == '__main__':
    # Do some quick tests here
    pass
