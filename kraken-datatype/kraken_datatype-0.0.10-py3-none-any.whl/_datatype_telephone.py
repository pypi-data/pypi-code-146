import phonenumbers




def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False


def normalize(data):
    
    try:
        x = phonenumbers.parse(data, "CA")

        if phonenumbers.is_valid_number(x):
            return phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.NATIONAL)
        else:
            return None

    except:
        None
