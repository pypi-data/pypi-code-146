class ServicefusionException(Exception):
    """Base exception for all library errors."""
    pass


class ServicefusionAuthError(ServicefusionException):
    """Something is wrong with authentication."""
    pass


class ServicefusionTokenError(ServicefusionAuthError):
    """Something is wrong with the tokens."""
    pass


class ServicefusionDataError(ServicefusionException, ValueError):
    """Something is wrong with the data."""
    pass


class ServicefusionConnectionError(ServicefusionException, ConnectionError):
    """Something is wrong with the connection."""
    pass

class ServicefusionException(Exception):
    pass


class ServicefusionForbiddenException(ServicefusionException):
    pass


class ServicefusionUnauthorizedException(ServicefusionException):
    pass


class ServicefusionTokenExpiredException(ServicefusionException):
    pass