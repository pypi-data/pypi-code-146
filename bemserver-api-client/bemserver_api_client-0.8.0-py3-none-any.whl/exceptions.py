"""BEMServer API client errors"""


class BEMServerAPIVersionError(Exception):
    """BEMServer API version error"""


class BEMServerAPIError(Exception):
    """BEMServer API error"""

    def __init__(self, status_code=501):
        self.status_code = status_code


class BEMServerAPIValidationError(BEMServerAPIError):
    """BEMServer API validation error"""

    def __init__(self, errors=None):
        super().__init__(status_code=422)
        self.errors = errors


class BEMServerAPINotFoundError(BEMServerAPIError):
    """BEMServer API not found error"""

    def __init__(self):
        super().__init__(status_code=404)


class BEMServerAPINotModified(BEMServerAPIError):
    """BEMServer API not modified"""

    def __init__(self):
        super().__init__(status_code=304)


class BEMServerAPIAuthenticationError(BEMServerAPIError):
    """BEMServer API authentication error"""


class BEMServerAPIPreconditionError(BEMServerAPIError):
    """BEMServer API precondition error"""


class BEMServerAPIInternalError(BEMServerAPIError):
    """BEMServer API internal error"""

    def __init__(self, status_code=500):
        super().__init__(status_code=status_code)


class BEMServerAPIClientValueError(ValueError):
    """BEMServer API client value error"""
