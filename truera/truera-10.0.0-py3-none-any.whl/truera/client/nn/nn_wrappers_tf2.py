"""Deprecated"""

from truera.client.nn.wrappers import tf2
from truera.client.util.func_utils import Deprecate

Deprecate.module(
    name=__name__,
    message="Use truera.client.nn.wrappers.tf2 instead.",
    dep_version="0.0.1",
    remove_version="0.1.0"
)

# replicate names from new location
tf = tf2.tf
Backend = tf2.Backend
