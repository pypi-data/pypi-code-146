class GtdbLibException(Exception):
    """Base exception for all gtdb-lib exceptions thrown in this project."""

    def __init__(self, message: str = ''):
        Exception.__init__(self, message)

class GtdbLibExit(GtdbLibException):
    """Raised when gtdblib has been asked to quietly exit."""

    def __init__(self, message: str = ''):
        GtdbLibException.__init__(self, message)

