from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="CategoryAction")


@attr.s(auto_attribs=True)
class CategoryAction:
    """
    Attributes:
        add (bool): add or remove
        label_name (str): category label name
    """

    add: bool
    label_name: str

    def to_dict(self) -> Dict[str, Any]:
        add = self.add
        label_name = self.label_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "add": add,
                "labelName": label_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        add = d.pop("add")

        label_name = d.pop("labelName")

        category_action = cls(
            add=add,
            label_name=label_name,
        )

        return category_action
