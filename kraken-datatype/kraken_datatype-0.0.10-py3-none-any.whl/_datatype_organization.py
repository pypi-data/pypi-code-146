import cleanco
#from cleanco import prepare_terms, basename



def validate(data):

    new_value = normalize(data)

    if new_value: 
        return True
    else:
        return False


def normalize(data):

    try:
        #terms = prepare_terms()
        #return basename(data, terms, prefix=False, middle=False, suffix=True)
        return
    except:
        return None