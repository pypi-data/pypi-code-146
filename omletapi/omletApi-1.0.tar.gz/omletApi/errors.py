#API errors

class UsernameError(Exception):
    pass

class TokenNotFound(Exception):
    pass

#timeout errors

class TimeoutError(Exception):
    pass