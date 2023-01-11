"""Deprecated"""

from truera.client.nn.wrappers import tf
from truera.client.util.func_utils import Deprecate

Deprecate.module(
    name=__name__,
    message="Use truera.client.nn.wrappers.tf instead.",
    dep_version="0.0.1",
    remove_version="0.1.0"
)

# replicate names from new location
import_tf = tf.import_tf
