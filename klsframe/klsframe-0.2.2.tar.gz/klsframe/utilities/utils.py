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


def get_df_rows(df, rindex=None):
    """
    Get the specified rows of a Pandas data frame
    :param df: Pandas dataframe to be scrapped
    :param rindex: Index of the rows to retrieve. It accepts strings and integer numbers. Accepted:
        - None (default): all the rows are retrieved
        - 1: single number, single index
        - 1-4: indexes from 1 to 4, included
        - 2,3,4: indexes 2,3,4
        - 2,3,7-9: combination of the two previous modes
        - head-N: first N rows
        - tail-N: last N rows
        - first: acronym for head-1
        - last: acronym for tail-1
    :return: a list containing one dict per each row (the dict's keys are the column names, its values the row values)
    """
    data = []
    if rindex is None:
        data = []
        for index, row in df.iterrows():
            data.append({k: v for k, v in row.items()})
    elif isinstance(rindex, int):
        data = []
        for index, row in df.iterrows():
            if index == rindex:
                # data.append({k: v for k, v in row.items()})
                return {k: v for k, v in row.items()}
    else:
        rindex = str(rindex)
        if rindex == 'first':
            return get_df_rows(df, df.first_valid_index())
        elif rindex == 'last':
            return get_df_rows(df, df.last_valid_index())
        elif re.fullmatch('head-[0-9]+', rindex):
            rindex = range(df.first_valid_index(), int(rindex.split('-')[1]))
        elif re.fullmatch('tail-[0-9]+', rindex):
            rindex = range(df.last_valid_index() + 1 - int(rindex.split('-')[1]), df.last_valid_index() + 1)
        elif re.fullmatch('[0-9]+-[0-9]+', rindex):
            rindex = range(int(rindex.split('-')[0]), int(rindex.split('-')[1]) + 1)
        elif re.fullmatch('([0-9](-[0-9]+)?,)*[0-9]+(-[0-9]+)?', rindex):
            # rindex = [int(i) for i in rindex.split(',')]
            aux = []
            for i in rindex.split(','):
                try:
                    aux.append(int(i))
                except ValueError:
                    aux.extend(range(int(i.split('-')[0]), int(i.split('-')[1]) + 1))
            rindex = aux
        else:
            raise ValueError("Unexpected value for parameter 'rindex'")

        for index, row in df.iterrows():
            if index in rindex:
                data.append({k: v for k, v in row.items()})
    return data


if __name__ == '__main__':
    # Do some quick tests here
    pass
