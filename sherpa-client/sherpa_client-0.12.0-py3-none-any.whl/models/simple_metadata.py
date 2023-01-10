from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="SimpleMetadata")


@attr.s(auto_attribs=True)
class SimpleMetadata:
    """
    Attributes:
        name (str): name of the metadata
        value (str): value of the metadata: leave empty or null to remove the metadata
    """

    name: str
    value: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        value = d.pop("value")

        simple_metadata = cls(
            name=name,
            value=value,
        )

        return simple_metadata
