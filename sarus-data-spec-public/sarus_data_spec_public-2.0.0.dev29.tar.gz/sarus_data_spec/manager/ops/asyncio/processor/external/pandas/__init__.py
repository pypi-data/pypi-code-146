"""
For ease of lecture we split DP implementations from standard implementations.

However, the DP op need to be defined before the standard op since the standard
op holds a reference to the DP op.

isort:skip_file
"""
import logging

logger = logging.getLogger(__name__)

try:
    from .pandas_dp import *  # noqa: F403
except NameError:
    logger.info("DP pandas ops not available.")

from .pandas import *  # noqa: F403,E402
