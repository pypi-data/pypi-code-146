class TruException(Exception):
    """
    Base class for all custom exceptions.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# Simple client exceptions get only their message printed out when they are caught.
class SimpleException(TruException):
    """
    Base class for exceptions simple enough to only display their message upon exception.
    """


class UsageException(TruException):
    """Raised when the indicated error is correctable by the user"""


class MissingProject(UsageException):
    """Project was not specified"""


class MissingProjectPath(UsageException):
    """project path was not specified"""


class IncorrectModelSpecification(UsageException):
    """Bad Model specification"""


class FileNotFound(UsageException):
    """a file or path was not found"""


class ModelNotFound(UsageException):
    """model was not found at the path specified"""


class AILensHomeError(UsageException):
    """env ${AILENS_HOME} not set"""


class FileNotCSVError(UsageException):
    """file name was not a CSV file"""


class InsufficientCSVColumns(UsageException):
    """CSV file does not have enough columns"""


class InvalidVersion(TruException):
    """Raised if a Version of a ML Model is incorrect"""


class InvalidSegmentation(TruException):
    """Raised when a constructed Segmentation is invalid"""


class AuthorizationDenied(SimpleException):
    """Passed through from the RBAC service."""


class NotFoundError(SimpleException):
    pass


class FileDoesNotExistException(SimpleException):
    pass


class MetadataNotFoundException(SimpleException):
    pass


class DirectoryAlreadyExistsException(SimpleException):
    pass


class InvalidFrameworkWrapperException(SimpleException):
    pass


class MissingEnvironmentSpecException(SimpleException):
    pass


class PackageVerificationException(SimpleException):
    pass


class FeatureDisabledException(TruException):
    pass
