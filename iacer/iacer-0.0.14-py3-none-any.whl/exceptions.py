class IacerException(Exception):
    """Raised when iacer experiences a fatal error"""

    def __init__(self, message, code=None):
        self.code = code or 'IacerException'
        self.message = message


class InvalidActionError(IacerException):
    """Exception raised for error when invalid action is supplied

    Attributes:
        expression -- input expression in which the error occurred
    """

    def __init__(self, expression):
        self.expression = expression
        super().__init__(expression)
