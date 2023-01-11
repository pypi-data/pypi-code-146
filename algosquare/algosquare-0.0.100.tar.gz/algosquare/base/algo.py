"""Algo base class."""
from abc import ABC, abstractmethod
from typing import Optional

from .errors import ValidationError

class Algo(ABC):
    """Base class for all algos."""
    @staticmethod
    def is_private() -> bool:
        """
        Describes the prediction_methods that the classifier supports.
        
        Returns: 
            Bool.

        Note:
            A private algorithm cannot generate any earnings.
        """
        return True

    @staticmethod
    def hourly_rate() -> Optional[int]:
        """
        Describes the prediction_methods that the classifier supports.
        
        Returns: 
            None for private algorithms, int otherwise.
        """
        return None


def extract_algo_statics(algo_class: type[Algo]) -> dict:
    """Extracts static information from algo subclasses.

    Args:
        algo_class: subclass of Algo.

    Returns: 
        dict.

    Raises:
        ValidationError
    """
    if not issubclass(algo_class, Algo):
        raise ValidationError('algo must be a subclass of Algo')

    statics = dict()
    is_private = algo_class.is_private()

    if not isinstance(is_private, bool):
        raise ValidationError('is_private must be a bool')

    statics['is_private'] = is_private

    if not is_private:
        hourly_rate = algo_class.hourly_rate()

        if not isinstance(hourly_rate, int):
            raise ValidationError('hourly rate must be an int')

        if hourly_rate <= 0: 
            raise ValidationError('hourly_rate must be positive')

        statics['hourly_rate'] = hourly_rate

    return statics