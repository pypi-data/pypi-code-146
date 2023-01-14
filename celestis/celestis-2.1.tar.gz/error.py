def generate_error(code, message):
    response = "HTTP/1.1 {} {}\n\n".format(code, message)
    return response