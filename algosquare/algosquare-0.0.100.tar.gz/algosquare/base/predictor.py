"""Predictor base class."""
from __future__ import annotations

from abc import ABC, abstractmethod

class Predictor(ABC):
    """Base class for all predictors."""
    @classmethod
    @abstractmethod
    def load(cls, filename: str) -> Predictor:
        """
        Loads a model.

        Args:
            filename: string.

        Returns:
            Predictor subclass.
        """
        pass

    @abstractmethod
    def save(self, filename: str) -> None:
        """
        Saves model to file.

        Args:
            filename: string.

        Returns:
            None.
        """
        pass