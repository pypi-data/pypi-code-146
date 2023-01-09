from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="LocalizedMessage")


@attr.s(auto_attribs=True)
class LocalizedMessage:
    """
    Attributes:
        body (str):
        title (str):
    """

    body: str
    title: str

    def to_dict(self) -> Dict[str, Any]:
        body = self.body
        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "body": body,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("body")

        title = d.pop("title")

        localized_message = cls(
            body=body,
            title=title,
        )

        return localized_message
