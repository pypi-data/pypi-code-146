"""Custom exceptions for the federated package."""
from __future__ import annotations

from concurrent.futures import Future as ConcurrentFuture
from typing import TYPE_CHECKING, List, Union

from bitfount.exceptions import BitfountError

if TYPE_CHECKING:
    from bitfount.federated.transport.handlers import _PriorityHandler


class BitfountTaskStartError(BitfountError, RuntimeError):
    """Raised when an issue occurs whilst trying to start a task with pods."""

    pass


class MessageHandlerDispatchError(BitfountError):
    """Error raised when there is a problem dispatching messages to handlers."""

    pass


class MessageHandlerNotFoundError(MessageHandlerDispatchError):
    """Error raised when no registered message handler can be found."""

    pass


class MessageTypeSpecificHandlerNotFoundError(MessageHandlerDispatchError):
    """Error raised when no non-universal registered message handler can be found."""

    universal_dispatches: List[Union[ConcurrentFuture, _PriorityHandler]]


class MessageRetrievalError(BitfountError, RuntimeError):
    """Raised when an error occurs whilst retrieving a message from message service."""

    pass


class PodConnectFailedError(BitfountError, TypeError):
    """The message service has not correctly connected the pod."""

    pass


class PodRegistrationError(BitfountError):
    """Error related to registering a Pod with BitfountHub."""

    pass


class PodResponseError(BitfountError):
    """Pod rejected or failed to respond to a task request."""

    pass


class PodNameError(BitfountError):
    """Error related to given Pod name."""

    pass


class PrivateSqlError(BitfountError):
    """An exception for any issues relating to the PrivateSQL algorithm."""

    pass


class SecureShareError(BitfountError):
    """Error related to SecureShare processes."""

    pass


class AggregatorError(BitfountError, ValueError):
    """Error related to Aggregator classes."""

    pass


class EncryptionError(BitfountError):
    """Error related to encryption processes."""

    pass


class EncryptError(EncryptionError):
    """Error when attempting to encrypt."""

    pass


class DecryptError(EncryptionError):
    """Error when attempting to decrypt."""

    pass


class RSAKeyError(EncryptionError):
    """Error related to RSA keys."""

    pass


class DPParameterError(BitfountError):
    """Error if any of given dp params are not allowed."""

    pass


class PSIError(BitfountError):
    """Error related to the PrivateSetIntersection protocol."""

    pass


class BlindingError(PSIError):
    """Error when attempting to blind."""

    pass


class UnBlindingError(PSIError):
    """Error when attempting to unblind."""

    pass


class OutOfBoundsError(PSIError):
    """Error when a value is out of bounds."""

    pass


class PSINoDataSourceError(PSIError):
    """Error when modeller tries to run a PSI task without a datasource."""

    pass


class PSIMultiplePodsError(PSIError):
    """Error when modeller tries to run a PSI task on multiple pods."""

    pass


class PSIMultiTableError(PSIError):
    """Error when trying perform PSI on a multitable datasource without specifying a table name."""  # noqa: B950

    pass


class PSIUnsupportedDataSourceError(PSIError):
    """Error when trying to perform PSI on an unsupported datasource."""

    pass
