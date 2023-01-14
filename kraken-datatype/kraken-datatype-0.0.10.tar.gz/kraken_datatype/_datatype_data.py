"""Methods to normalize data
"""

def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False


def normalize(data):

    _data = data

    if not _data: 
        return None

    #List of one to one
    while isinstance(_data, list) and len(_data) == 1:
        _data = _data[0]

    return _data