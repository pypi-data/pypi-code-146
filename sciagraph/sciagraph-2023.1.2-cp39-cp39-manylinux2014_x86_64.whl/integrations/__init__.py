"""
Integrations for Sciagraph.
"""
import warnings

# Backwards compatibility:
from .mlflow import install_handler as _install_mlflow_handler


def install_mlflow_handler():
    warnings.warn(
        "Deprecated since 2022.7.0. "
        + "Use sciagraph.integrations.mlflow.install_handler() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    _install_mlflow_handler()


__all__ = ["install_mlflow_handler"]
