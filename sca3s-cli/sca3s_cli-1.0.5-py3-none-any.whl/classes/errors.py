class OKException(Exception):
    """
    Class to define a 200 OK Exception for known recoverable errors.
    """
    status = None

    def __init__(self, status):
        super()
        self.status = status