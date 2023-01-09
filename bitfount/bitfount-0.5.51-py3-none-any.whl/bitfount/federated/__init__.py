"""Manages the federated communication and training of models.

Federated algorithm plugins can also be imported from this package.
"""
from typing import List

from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.aggregators.secure import SecureAggregator
import bitfount.federated.algorithms as algorithms
from bitfount.federated.algorithms import *  # noqa: F401, F403
from bitfount.federated.authorisation_checkers import IdentityVerificationMethod
from bitfount.federated.early_stopping import FederatedEarlyStopping
from bitfount.federated.exceptions import (
    AggregatorError,
    BitfountTaskStartError,
    DecryptError,
    EncryptError,
    EncryptionError,
    MessageHandlerNotFoundError,
    MessageRetrievalError,
    PodConnectFailedError,
    PodNameError,
    PodRegistrationError,
    PrivateSqlError,
    PSIMultiTableError,
    PSIUnsupportedDataSourceError,
    SecureShareError,
)
from bitfount.federated.helper import combine_pod_schemas
from bitfount.federated.keys_setup import RSAKeyPair
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.modeller import _Modeller
from bitfount.federated.pod import Pod
from bitfount.federated.privacy.differential import DPModellerConfig, DPPodConfig
import bitfount.federated.protocols as protocols
from bitfount.federated.protocols import *  # noqa: F401, F403
from bitfount.federated.roles import Role
from bitfount.federated.secure import SecureShare
from bitfount.federated.shim import BackendTensorShim
from bitfount.federated.transport import MAXIMUM_GRPC_MESSAGE_SIZE_BYTES
from bitfount.federated.transport.config import (
    PRODUCTION_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.types import AggregatorType, AlgorithmType, ProtocolType

_logger = _get_federated_logger(__name__)

__all__: List[str] = [
    "Aggregator",
    "AggregatorError",
    "AggregatorType",
    "AlgorithmType",
    "BackendTensorShim",
    "BitfountModelReference",
    "BitfountTaskStartError",
    "DPModellerConfig",
    "DPPodConfig",
    "DecryptError",
    "EncryptError",
    "EncryptionError",
    "FederatedEarlyStopping",
    "IdentityVerificationMethod",
    "MAXIMUM_GRPC_MESSAGE_SIZE_BYTES",
    "MessageHandlerNotFoundError",
    "MessageRetrievalError",
    "MessageServiceConfig",
    "_Modeller",
    "Pod",
    "PodConnectFailedError",
    "RSAKeyPair",
    "PodNameError",
    "PodRegistrationError",
    "PrivateSqlError",
    "ProtocolType",
    "PRODUCTION_MESSAGE_SERVICE_URL",
    "PSIMultiTableError",
    "PSIUnsupportedDataSourceError",
    "Role",
    "SecureAggregator",
    "SecureShare",
    "SecureShareError",
    "combine_pod_schemas",
]

# Protocols and algorithms are imported from their own respective subpackages because
# of how we handle plugins for these components.
__all__.extend(algorithms.__all__)
__all__.extend(protocols.__all__)

# See top level `__init__.py` for an explanation
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False
