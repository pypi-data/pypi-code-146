"""Diligent module."""

from .cli import cli
from .storage import Client

__all__ = ["Client", "cli"]
