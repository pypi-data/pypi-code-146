
def tuitse_boolean(kiamtsa_tinliat):
    for tsua in kiamtsa_tinliat:
        if not tsua[-1]:
            return False
    else:
        return True
