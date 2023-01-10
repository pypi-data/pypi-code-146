from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="TermIdentifier")


@attr.s(auto_attribs=True)
class TermIdentifier:
    """
    Attributes:
        identifier (str):
    """

    identifier: str

    def to_dict(self) -> Dict[str, Any]:
        identifier = self.identifier

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "identifier": identifier,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        identifier = d.pop("identifier")

        term_identifier = cls(
            identifier=identifier,
        )

        return term_identifier
