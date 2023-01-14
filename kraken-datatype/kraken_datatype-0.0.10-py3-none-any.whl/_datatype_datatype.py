"""
Methods to normalize datatype
"""



def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False




def normalize(datatype):
    """Normalize datatype
    """

    _datatype = datatype

    if not _datatype:
        return None


    _datatype = _datatype.lower()

    _datatype = _datatype.replace('schema:', '')

    _datatype = _datatype.strip()

    return _datatype