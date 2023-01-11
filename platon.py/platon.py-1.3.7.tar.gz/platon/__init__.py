import sys
import warnings

import pkg_resources

from platon_account import (
    Account
)
from platon.main import (
    Web3
)
from platon.providers.platon_tester import (
    PlatonTesterProvider,
)
from platon.providers.ipc import (
    IPCProvider,
)
from platon.providers.rpc import (
    HTTPProvider,
)
from platon.providers.async_rpc import (
    AsyncHTTPProvider,
)
from platon.providers.websocket import (
    WebsocketProvider,
)

if (3, 5) <= sys.version_info < (3, 6):
    warnings.warn(
        "Support for Python 3.5 will be removed in platon.py v5",
        category=DeprecationWarning,
        stacklevel=2)

if sys.version_info < (3, 5):
    raise EnvironmentError(
        "Python 3.5 or above is required. "
        "Note that support for Python 3.5 will be removed in platon.py v5")


__version__ = pkg_resources.get_distribution("platon.py").version

__all__ = [
    "__version__",
    "Web3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "PlatonTesterProvider",
    "Account",
    "AsyncHTTPProvider",
]
