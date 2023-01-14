import pycountry



def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False




    
def normalize(data):


    if not isinstance(data, str):
        return None

    if len(data) == 2:
        country = pycountry.countries.get(alpha_2=data)
        if country:
            return country.alpha_2

    elif len(data) == 3:
        country = pycountry.countries.get(alpha_3=data)
        if country:
            return country.alpha_2

    else:
        country = pycountry.countries.get(name=data)
        if country:
            return country.alpha_2  

    return None