class PyPlatonPMError(Exception):
    """
    Base class for all Py-PlatonPM errors.
    """

    pass


class InsufficientAssetsError(PyPlatonPMError):
    """
    Raised when a Manifest or Package does not contain the required assets to do something.
    """

    pass


class PlatonPMValidationError(PyPlatonPMError):
    """
    Raised when something does not pass a validation check.
    """

    pass


class CannotHandleURI(PyPlatonPMError):
    """
    Raised when the given URI cannot be served by any of the available backends.
    """

    pass


class FailureToFetchIPFSAssetsError(PyPlatonPMError):
    """
    Raised when an attempt to fetch a Package's assets via IPFS failed.
    """

    pass


class BytecodeLinkingError(PyPlatonPMError):
    """
    Raised when an attempt to link a contract factory's bytecode failed.
    """

    pass


class ManifestBuildingError(PyPlatonPMError):
    """
    Raised when an attempt to build a manifest failed.
    """

    pass
