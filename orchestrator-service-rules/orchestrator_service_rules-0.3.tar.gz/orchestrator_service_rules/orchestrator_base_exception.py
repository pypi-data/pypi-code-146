class OrchestratorBaseException(Exception):
    temp_data = dict()
    steps = dict()
    """Base Exception class to manage custom exceptions"""
    def __init__(self, message) -> None:
        super().__init__(message)


class ApplicationException(OrchestratorBaseException):
    pass


def handle_exception(**kwargs):
    exception = ApplicationException(kwargs.get('message'))
    exception.temp_data = kwargs.get('temp_data')
    exception.steps = kwargs.get('steps')
    raise exception
