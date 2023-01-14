import dateparser
import datetime



def validate(data):

    new_value = normalize(data)
    if new_value: 
        return True
    else:
        return False



def normalize(data = None):
    """Return date in datetime format from input
    """
    
    if not data or data is None:
        return

    elif isinstance(data, datetime.datetime):
        return data

    elif isinstance(data, str):

        # Try loading as iso
        try:
            result = datetime.datetime.fromisoformat(data)
            return result
        except:
            a=1

        # Try dateparser to figure out date (slower)
        try:
            result = dateparser.parse(data)
            if result:
                return result
        except:
            a=1

    return None