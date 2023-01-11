"""Utilities for wrapping tensorflow models of both v1/v2 types."""

from truera.client.nn import get_tf


def import_tf(version=None):
    """
    Import the specified tensorflow version. Raise exception if not found.
    """

    version = str(version)

    if version not in set(['1', '2']):
        raise RuntimeError("Only tensorflow versions 1 or 2 are supported.")

    tf = get_tf(version)

    if not tf:
        raise RuntimeError(
            f"Could not load tensorflow version {version}.*. "
            f"If you are wrapping a tensorflow {version} model, make sure you have an appropriate tensorflow version installed."
            f"If you intend to wrap a tensorflow {3-version} model, implement TensorFlowV{3-version}[ModelRunWrapper] instead."
        )

    return tf
