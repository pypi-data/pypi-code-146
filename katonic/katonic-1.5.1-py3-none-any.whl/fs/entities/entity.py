#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import yaml
from datetime import datetime
from typing import Dict, Optional
from katonic.fs.value_type import ValueType


class Entity:

    _name: str
    _value_type: ValueType
    _description: str
    # _join_key: str
    # _labels: Dict[str, str]
    # _created_timestamp: Optional[datetime]
    # _last_updated_timestamp: Optional[datetime]

    def __init__(
        self,
        name: str,
        value_type: ValueType = ValueType.UNKNOWN,
        description: str = "",
    ):
        """Creates an Entity object."""
        self._name = name
        self._description = description
        self._value_type = value_type
        # if join_key:
        #     self._join_key = join_key
        # else:
        #     self._join_key = name

        # if labels is None:
        #     self._labels = dict()
        # else:
        #     self._labels = labels

        # self._created_timestamp: Optional[datetime] = None
        # self._last_updated_timestamp: Optional[datetime] = None

    def __hash__(self) -> int:
        return hash((id(self), self.name))

    def __eq__(self, other):
        if not isinstance(other, Entity):
            raise TypeError(
                "Comparisons should only involve Entity class objects.")

        return (
            self.name == other.name
            and self.description == other.description
            and self.value_type == other.value_type
        )

    def __str__(self):
        return str(self.to_dict())

    @property
    def name(self) -> str:
        """
        Gets the name of this entity.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this entity.
        """
        self._name = name

    @property
    def description(self) -> str:
        """
        Gets the description of this entity.
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this entity.
        """
        self._description = description

    # @property
    # def join_key(self) -> str:
    #     """
    #     Gets the join key of this entity.
    #     """
    #     return self._join_key

    # @join_key.setter
    # def join_key(self, join_key):
    #     """
    #     Sets the join key of this entity.
    #     """
    #     self._join_key = join_key

    @property
    def value_type(self) -> ValueType:
        """
        Gets the type of this entity.
        """
        return self._value_type

    @value_type.setter
    def value_type(self, value_type: ValueType):
        """
        Sets the type of this entity.
        """
        self._value_type = value_type

    # @property
    # def labels(self) -> Dict[str, str]:
    #     """
    #     Gets the labels of this entity.
    #     """
    #     return self._labels

    # @labels.setter
    # def labels(self, labels: Dict[str, str]):
    #     """
    #     Sets the labels of this entity.
    #     """
    #     self._labels = labels

    # @property
    # def created_timestamp(self) -> Optional[datetime]:
    #     """
    #     Gets the created_timestamp of this entity.
    #     """
    #     return self._created_timestamp

    # @property
    # def last_updated_timestamp(self) -> Optional[datetime]:
    #     """
    #     Gets the last_updated_timestamp of this entity.
    #     """
    #     return self._last_updated_timestamp

    def is_valid(self):
        """
        Validates the state of this entity locally.

        Raises:
            ValueError: The entity does not have a name or does not have a type.
        """
        if not self.name:
            raise ValueError("No name found in entity.")

        if not self.value_type:
            raise ValueError("No type found in entity {self.value_type}")

    def to_dict(self) -> Dict:
        """
        Converts entity to dict.

        Returns:
            Dictionary object representation of entity.
        """
        # if self.created_timestamp:
        #     entity["created_timestamp"] = self.created_timestamp

        # if self.last_updated_timestamp:
        #     entity["created_timestamp"] = self.last_updated_timestamp

        return {
            "name": self._name,
            "description": self._description,
            "value_type": self._value_type,
        }

    @classmethod
    def from_dict(cls, entity_dict: Dict[str, str]):
        """
        Creates an entity from a Dictionary representation of an entity.

        Args:
            entity_dict: A Dictionary representation of an entity.

        Returns:
            An Entity object based on the entity details.
        """
        return cls(
            name=entity_dict.name,
            description=entity_dict.description,
            value_type=ValueType(entity_dict.value_type),
        )

    def to_yaml(self):
        """
        Converts a entity to a YAML string.

        Returns:
            An entity string returned in YAML format.
        """
        entity_dict = self.to_dict()
        return yaml.dump(entity_dict, allow_unicode=True, sort_keys=False)
