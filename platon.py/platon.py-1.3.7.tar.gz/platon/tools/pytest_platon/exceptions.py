class PytestPlatonError(Exception):
    """
    Base class for all Pytest-Platon errors.
    """

    pass


class DeployerError(PytestPlatonError):
    """
    Raised when the Deployer is unable to deploy a contract type.
    """

    pass


class LinkerError(PytestPlatonError):
    """
    Raised when the Linker is unable to link two contract types.
    """

    pass
