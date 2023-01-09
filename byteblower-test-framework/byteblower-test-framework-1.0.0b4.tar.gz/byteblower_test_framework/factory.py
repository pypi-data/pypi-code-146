"""Factory helper functions."""
from ._factory.frame import create_frame

# Export the user interfaces.
#
# Outcomes:
# * Limits import on `from byteblower_test_framework.factory import *`
# * Exposes the interfaces in the (Sphinx) documentation
#
__all__ = (
    # Frame factory functions:
    create_frame.__name__, )
