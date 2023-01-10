#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Dict, Optional
from katonic.fs.value_type import ValueType


class Feature:
    """
    A Feature represents a class of serveable feature.

    Args:
        name: Name of the feature.
        dtype: The type of the feature, such as string or float.
    """

    def __init__(
        self,
        name: str,
        dtype: ValueType,
        description: Optional[str] = None,
    ):
        """Creates a Feature object."""
        self._name = name
        if not isinstance(dtype, ValueType):
            raise ValueError("dtype is not a valid ValueType")
        if dtype is ValueType.UNKNOWN:
            raise ValueError(f"dtype cannot be {dtype}")
        self._dtype = dtype
        self._description = "" if description is None else description

    def __eq__(self, other):
        return self.name == other.name and self.dtype == other.dtype and self.description == other.description

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        # return string representation of the reference
        return f"{self.name}-{self.dtype}-{self.description}"

    def __str__(self):
        # readable string of the reference
        return f"Feature<{self.__repr__()}>"

    @property
    def name(self):
        """
        Gets the name of this feature.
        """
        return self._name

    @property
    def dtype(self) -> ValueType:
        """
        Gets the data type of this feature.
        """
        return self._dtype

    @property
    def description(self) -> str:
        """
        Gets the description of this feature.
        """
        return self._description

    def to_dict(self) -> Dict[str, str]:
        """
        Converts Feature object to its Dictionary representation.

        Returns:
            A Feature dictionary.
        """

        return {
            "name": self.name,
            "value_type": self.dtype.name,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, feature_dict: Dict[str, str]):
        """
        Args:
            feature_dict: list of dictionaries

        Returns:
            Feature object
        """
        return cls(
            name=feature_dict.name,
            dtype=ValueType(feature_dict.value_type),
            description=feature_dict.description,
        )
