


def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False


def normalize(data):
    """ Standardize url
    """
    
    _data = data

    if not isinstance(_data, str):
        _data = str(_data)

    return _data