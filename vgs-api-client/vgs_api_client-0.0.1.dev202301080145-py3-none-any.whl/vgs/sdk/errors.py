import types


def get_error_details(e):
    if e.response.body and e.response.body["errors"]:
        return [x["detail"] for x in e.response.body["errors"]]


class VgsSDKError(Exception):
    def __init__(self, message, ctx=None):
        self.message = message
        self.ctx = ctx


class VaultNotFoundError(VgsSDKError):
    def __init__(self, vault_id, ctx=None):
        self.message = "Vault " + vault_id + " doesn't exist."
        self.ctx = ctx


class TokenNotValidError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = "Please run `vgs login` because your session has been expired."
        self.ctx = ctx


class AuthenticationRequiredError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = "Please run `vgs login` because your session has been expired."
        self.ctx = ctx


class AuthenticationError(VgsSDKError):
    def __init__(self, ctx=None, details=None):
        self.message = (
            "Authentication error occurred"
            if ctx and ctx.obj.debug
            else "Authentication error occurred."
        )

        if details:
            self.message = "{message} {details}".format(message=self.message, details=details)

        self.ctx = ctx


class ClientCredentialsAuthenticationError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = (
            """Authentication error occurred.

NOTE: You may see this error if you're using an account with enabled OTP. 
Auto login via environment variables with OTP is not supported. 
 """
            if ctx and ctx.obj.debug
            else """Authentication error occurred. (Run with --debug for a traceback.)

NOTE: You may see this error if you're using an account with enabled OTP. 
Auto login via environment variables with OTP is not supported. 
 """
        )
        self.ctx = ctx


class ApiError(VgsSDKError):
    def __init__(self, e, ctx=None):
        details = get_error_details(e)
        if details:
            self.message = f"API error occurred: {details}"
        elif ctx and ctx.obj.debug:
            self.message = "API error occurred."
        else:
            self.message = "API error occurred. (Run with --debug for a traceback.)"
        self.ctx = ctx


class UnhandledError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = (
            "An unexpected error occurred."
            if ctx and ctx.obj.debug
            else "An unexpected error occurred. (Run with --debug for a traceback.)"
        )
        self.ctx = ctx


class RouteNotValidError(VgsSDKError):
    def __init__(self, error_message: str, ctx=None):
        error_message = f"Route cannot be applied due to errors:\n{error_message}"
        self.message = (
            error_message
            if ctx and ctx.obj.debug
            else f"{error_message} (Run with --debug for a traceback.)"
        )
        self.ctx = ctx


class SchemaValidationError(VgsSDKError):
    def __init__(self, message, ctx=None):
        self.message = f"Error during validation of the file input: {message}."
        self.ctx = ctx


class ServiceClientCreationError(VgsSDKError):
    def __init__(self, e, ctx=None):
        details = get_error_details(e)
        self.message = f"Service Account creation failed with error: {details}"
        self.ctx = ctx


class ServiceClientDeletionError(VgsSDKError):
    def __init__(self, e, ctx=None):
        details = get_error_details(e)
        self.message = f"Service Account deletion failed with error: {details}"
        self.ctx = ctx


class ServiceClientListingError(VgsSDKError):
    def __init__(self, e, ctx=None):
        details = get_error_details(e)
        self.message = f"Service Account listing failed with error: {details}"
        self.ctx = ctx


class NoSuchFileOrDirectoryError(VgsSDKError):
    def __init__(self, message, ctx=None):
        self.message = f"No such file or directory: {message}"
        self.ctx = ctx


class InsufficientPermissionsError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = (
            "You don't have enough permissions to perform this operation. Please contact "
            "support@verygoodsecurity.com. "
        )
        self.ctx = ctx


class PermissionDeniedError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = "You don't have enough permissions to the requested resource"
        self.ctx = ctx


class MaxNumberOfCredentialsExceededError(VgsSDKError):
    def __init__(self, ctx=None):
        self.message = (
            "Maximum number of access credentials (10 per vault) reached.. Please contact "
            "support@verygoodsecurity.com to increase the limit. "
        )
        self.ctx = ctx


def status_code_error(**kwargs):
    def init(self, e, ctx=None):
        error_handler = kwargs.get(f"e{e.response.status_code}")
        if error_handler:
            self.message = (
                error_handler(e) if isinstance(error_handler, types.FunctionType) else error_handler
            )
            self.ctx = ctx
        else:
            ApiError.__init__(self, e, ctx=ctx)

    return type(
        "StatusCodeError",
        (ApiError,),
        {"__init__": init},
    )
