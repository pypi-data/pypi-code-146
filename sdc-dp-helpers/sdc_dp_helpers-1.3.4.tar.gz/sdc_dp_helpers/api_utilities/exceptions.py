"""
sdc_dp_helpers.exceptions
~~~~~~~~~~~~~~~~~~~~
Exceptions used in sdc_dp_helpers.
"""


class SDCHelpersException(Exception):
    """A base class for sdc_dp_helpers' exceptions."""


class AuthenticationError(SDCHelpersException):
    """An error during authentication process."""


class QueryHandlerError(SDCHelpersException):
    """An exception raise when query handler fails."""


class DataNotFoundError(SDCHelpersException):
    """An error raised when we do not find data from the API Call."""


class RequestURITooLongError(SDCHelpersException):
    """Request-URI Too Long Error."""


class InvalidEndPointError(SDCHelpersException):
    """Invalid endpoint Error."""


class APICallError(SDCHelpersException):
    """Error for API Call that calls for retry."""


class TimeIntervalError(SDCHelpersException):
    """Exception Raised When you provide a wrong time interval value

    Args:
        SDCHelpersException (_type_): _description_
    """


class DateValueError(SDCHelpersException):
    """Exception Raised When you provide a wrong time interval value

    Args:
        SDCHelpersException (_type_): _description_
    """


class CadenceError(SDCHelpersException):
    """Exception Raised When you provide a wrong time cadence value

    Args:
        SDCHelpersException (_type_): _description_
    """


class TimeBucketError(SDCHelpersException):
    """Exception Raised When you provide a wrong time bucket value

    Args:
        SDCHelpersException (_type_): _description_
    """


class CadenceTimeBucketError(SDCHelpersException):
    """Exception Raised When you provide a wrong cadence or time bucket value

    Args:
        SDCHelpersException (_type_): _description_
    """
