class MissingFieldError(Exception):
    """Raised when fields are missing from mlops_settings.yaml"""


class MissingMetadataError(Exception):
    """Raised when fields are missing from the metadata (from mlops_settings.yaml)"""


class TestError(Exception):
    """Raised when tests are failing"""


class DeploymentError(Exception):
    """Raised when deployment fails"""


class FunctionNameError(Exception):
    """Raised when function name (in CDF) is invalid"""


class MissingClientError(Exception):
    """Raised when a global cognite client is missing, i.e. not set up"""


class VirtualEnvironmentError(Exception):
    """Raised when something is wrong when creating or deleting a virtual environment during deployments"""


class MLOpsError(Exception):
    """Generic MLOps exception"""
