# This file will be called first whenever any file from within this directory is imported.
# Thus, we'll test dependencies only here, once.
try:
    import torch  # noqa: F401
except ImportError as exc:
    raise ModuleNotFoundError(str(exc) + ". Please install `classiq-qml`.") from exc

from ..qnn import circuit_utils, data_sets, qlayer

__all__ = ["data_sets", "qlayer", "circuit_utils"]


def __dir__():
    return __all__
