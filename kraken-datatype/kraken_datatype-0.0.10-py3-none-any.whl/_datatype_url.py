
from url_normalize import url_normalize
import validators



def validate(data):

    if validators.url(data):
        return True
    else:
        return False


def normalize(data):
    """ Standardize url
    """
    try:
        value = url_normalize(data)
        if validate(value):
            return value
        else:
            return None
    except:
        return None

