"""Deprecated"""

from truera.client.nn.wrappers import tf1
from truera.client.util.func_utils import Deprecate

Deprecate.module(
    name=__name__,
    message="Use truera.client.nn.wrappers.tf1 instead.",
    dep_version="0.0.1",
    remove_version="0.1.0"
)

# replicate names from new location
tf = tf1.tf
Backend = tf1.Backend
