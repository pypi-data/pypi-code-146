import distutils
import distutils.util



def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False



def normalize(data):
    if data:
        data = data
    
    try:
        data = bool(distutils.util.strtobool(data))
    except:
        pass

    if not isinstance(data, bool):
        data = None

    return data
