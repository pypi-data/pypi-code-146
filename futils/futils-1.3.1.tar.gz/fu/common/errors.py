
class InvalidPathError(Exception):
    pass

class PathAlreadyExistsError(Exception):
    pass

class MissingRequiredDataError(Exception):
    """Error indicates user did not enter enough info \
        for required operation

    Args:
        Exception (Exception): Python base exception
    """
    pass
