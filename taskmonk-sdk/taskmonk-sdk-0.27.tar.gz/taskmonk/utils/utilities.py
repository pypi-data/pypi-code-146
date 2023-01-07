def argumentVerifier(args):
    error = False
    for param in args:
        if param == None:
            error = True
            break

    return error
