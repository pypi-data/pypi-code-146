import email_normalize
import validators

"""Normalize email
"""



def validate(data):

    if validators.email(data):
        return True
    else:
        return False



def normalize(data):

    try: 
        value = email_normalize.normalize(data).normalized_address
        if validate(value):
            return value
        else:
            return None
    except:
        return None