class AppNoRowsFound(Exception):
    code = 404


class AppException(Exception):
    message = "Error"
    code = 500
    custom_exception = True
    silent = False
    use_default_response_message_key = True


class AppSilentException(AppException):
    silent = True


class AppNotSilentException(AppException):
    silent = False


class AppValidationError(AppSilentException):
    code = 400
    message = "Validation Error"


class AppMicroFetcherError(AppSilentException):
    code = 400
    message = "Fetcher Service Error"


class AppThirdPartyError(AppNotSilentException):
    code = 400
    message = "Third Party Call Error"


class AppFetchServiceDataError(AppNotSilentException):
    code = 400
    message = "Error while fetch relational data from service"


class AppNotFoundError(AppSilentException):
    code = 404
    message = "Not found"


class AppMissingAuthError(AppSilentException):
    code = 401
    message = "You are unauthenticated"


class CustomNotFoundError(AppSilentException):
    def __init__(self, message):
        self.message = message

    code = 404
