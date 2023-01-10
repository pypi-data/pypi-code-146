"""Exceptions for EcoPanel"""


class EcoPanelError(Exception):
    """Generic EcoPanel exception."""


class EcoPanelEmptyResponseError(Exception):
    """ "EcoPanel API response is empty exception."""


class EcoPanelConnectionError(EcoPanelError):
    """EcoPanel connection exception."""


class EcoPanelConnectionTimeoutError(EcoPanelConnectionError):
    """EcoPanel connection timeout exception."""


class EcoPanelConnectionClosed(EcoPanelConnectionError):
    """EcoPanel connection closed."""
