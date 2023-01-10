def read_to_dict(path: str, fill: str="Do not fill", sep='\t') -> dict:
    """
    Reads a .txt file into a dictionary. The .txt file must be TAB separated.
    The first entry in each line will be the key and the remaining items will
    be collected as a list.
    Multi=0 means you read only the first two items {key:value}.
    The fill kwarg fills in the end of lines shorter than the head with fill.
    """
    result = {}
    
    with open(path, 'r') as f:
        head = f.readline()
        head = head.strip().split(sep)
        multi = len(head)
        print(multi)
        if multi < 2:
            for line in f:
                x = line.strip().split(sep)
                result[x[0]] = None
        
        if multi == 2:
            for line in f:
                x = line.strip().split(sep)
                if len(x) < 2 and fill != "Do not fill":
                    result[x[0]] = fill
                else:
                    continue
                result[x[0]] = x[1]
        else:
            for line in f:
                x = line.strip().split(sep)
                if len(x) < 2:
                    result[x[0]] = None
                    continue
                result[x[0]] = x[1:]
                if fill != "Do not fill":
                    while len(result[x[0]]) < len(head)-1:
                        result[x[0]].append(fill)

    return result


def read_to_dict_of_dicts(path: str, fill: str="Do not fill", sep='\t') -> dict:
    """
    Reads a .txt file into a dictionary of dictionaries. The first item on each line will be
    the master key. Each item in the dictionary identified by the master key will then have
    each item on the line identified by the header on its line. example:
    name    rank    country
    Sergei  private russia
    John    sergeant USA

    will be read as
    {'Sergei': {'name': 'Sergei', 'rank': 'private, 'country': 'russia'},
     'John': {'name': 'John', 'rank': 'sergeant, 'country': 'USA'}}
    """
    result = {}
    
    error_message = False
    with open(path, 'r') as f:
        head = f.readline()
        head = head.strip().split(sep)
        multi = len(head)
        if multi < 2:
            for line in f:
                x = line.strip().split(sep)
                if len(x) > multi:
                    error_message = "There are lines longer than the header. The extra data has been ignored."
                result[x[0]] = None
        
        if multi == 2:
            for line in f:
                x = line.strip().split(sep)
                if len(x) > multi:
                    error_message = "There are lines longer than the header. The extra data has been ignored."
                if len(x) < 2 and fill != "Do not fill":
                    result[x[0]] = fill
                else:
                    result[x[0]] = {head[0]: x[0], head[1]: x[1]}
        else:
            for line in f:
                x = line.strip().split(sep)
                if len(x) > multi:
                    error_message = "There are lines longer than the header. The extra data has been ignored."
                if len(x) < 2:
                    result[x[0]] = None
                    continue
                temp = {}
                i = 0
                for item in head:
                    try:
                        temp[item] = x[i]
                    except IndexError:
                        if fill != "Do not fill":
                            temp[item] = fill
                        else:
                            continue
                    i += 1
                result[x[0]] = temp

    if error_message:
        print(error_message)          
    return result


def read_to_list(path: str, fill: str="Do not fill", sep='\t') -> list:
    """
    Reads a TAB separated .txt file into a list of lists.
    The fill keyword appends fill to the end of every line shorter than the header.
    If there is only one item in the header, each line in the file will be read
    as a string without splitting.
    """
    with open(path, 'r') as f:
        head = f.readline()
        head = head.strip().split(sep)
        result = [head]
        if len(head) == 1:
            result = [head[0]]
            for line in f:
                result.append(line.strip())
        for line in f:
            temp = line.strip().split(sep)
            if fill != "Do not fill" and len(temp) < len(head):
                while len(temp) < len(head):
                    temp.append(fill)
            result.append(temp)

    return result


def list_printer(source_list: list, output_filename: str, sep='\t') -> str:
    """
    Prints a list or dict to a sep separated .txt file. Can print a list of dicts,
    a list of lists, a dict of lists, and a dict of dicts. Should return identical
    output as the input from any of the basic_tab_functions.
    """
    printer = ''
    if type(source_list) == list:
        for row in source_list:
            if type(row) == str:
                printer += row
                printer += sep
                printer += '\n'
            elif type(row) == list:
                for cell in row:
                    printer += str(cell)
                    printer += sep
                printer += '\n'
            elif type(row) == dict:
                for cell in row.values():
                    printer += str(cell)
                    printer += sep
                printer += '\n'
    
    if type(source_list) == dict:
        for key, value in source_list.items():
            if type(value) == str:
                printer += value
                printer += sep
                printer += '\n'
            elif type(value) == list:
                printer += key
                printer += '\t'
                for cell in value:
                    printer += str(cell)
                    printer += sep
                printer += '\n'
            elif type(value) == dict:
                for cell in value.values():
                    printer += str(cell)
                    printer += sep
                printer += '\n'

    with open(f'{output_filename}.txt', 'w') as f:
        f.write(printer)
    return printer

