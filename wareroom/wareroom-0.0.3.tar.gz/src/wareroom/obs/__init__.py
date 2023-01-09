"""Huawei Object Based Storage (OBS) backend."""

from .client import Client
from .config import read_config

__all__ = ["Client", "read_config"]