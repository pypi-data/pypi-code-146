from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="MessageMark")


@attr.s(auto_attribs=True)
class MessageMark:
    """
    Attributes:
        read (bool):
    """

    read: bool

    def to_dict(self) -> Dict[str, Any]:
        read = self.read

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "read": read,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        read = d.pop("read")

        message_mark = cls(
            read=read,
        )

        return message_mark
