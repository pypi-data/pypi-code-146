"""ByteBlower traffic endpoint interfaces."""
from ._endpoint.ipv4.nat import NattedPort
from ._endpoint.ipv4.port import \
    DEFAULT_IPV4_NETMASK  # noqa: F401; for user convenience
from ._endpoint.ipv4.port import VlanConfig  # noqa: F401; for user convenience
from ._endpoint.ipv4.port import IPv4Port
from ._endpoint.ipv6.port import IPv6Port
from ._endpoint.port import Port

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.endpoint import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
# NOTE
#   Exporting imported variables does not introduce them in the (Sphinx) docs.
#   For example 'DEFAULT_IPV4_NETMASK'.
#   It does introduce their name and value in `help()` of this module though.
#
__all__ = (
    # Constants:
    'DEFAULT_IPV4_NETMASK',
    # ByteBlowerPort base interface:
    Port.__name__,
    # ByteBlowerPort interfaces:
    IPv4Port.__name__,
    NattedPort.__name__,
    IPv6Port.__name__,
)
