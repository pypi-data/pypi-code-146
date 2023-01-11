"""
Base classes with custom attributes for updating, serializing and deserializing data classes and enums.
"""
import base64
import json
from abc import ABC
from datetime import date, datetime, tzinfo

from pydantic import BaseModel

from algora.common.date import date_to_timestamp, datetime_to_timestamp


class Base(ABC, BaseModel):
    """
    Base class used for all data classes.
    """

    class Config:
        # use enum values when using .dict() on object
        use_enum_values = True

        json_encoders = {
            date: date_to_timestamp,
            datetime: datetime_to_timestamp,
            tzinfo: str
        }

    @classmethod
    def cls_name(cls) -> str:
        """
        Get class name.

        Returns:
            str: Class name
        """
        return cls.__name__

    def request_dict(self) -> dict:
        """
        Convert data class to dict. Used instead of `.dict()` to serialize dates as timestamps.

        Returns:
            dict: Serialized data class as dict
        """
        return json.loads(self.json())

    def base64_encoded(self, exclude=None) -> bytes:
        """
        Base-64 encode data class.

        Returns:
            bytes: Base-64 encoded data class as bytes
        """
        json_str = json.dumps(self.json(exclude=exclude), sort_keys=True)
        bytes_rep = bytes(json_str, 'utf-8')
        return base64.b64encode(bytes_rep)
