from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_message_localized import NewMessageLocalized


T = TypeVar("T", bound="NewMessage")


@attr.s(auto_attribs=True)
class NewMessage:
    """
    Attributes:
        localized (NewMessageLocalized):
        group (Union[Unset, str]):
        index (Union[Unset, int]):
        scope (Union[Unset, str]):
    """

    localized: "NewMessageLocalized"
    group: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    scope: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        localized = self.localized.to_dict()

        group = self.group
        index = self.index
        scope = self.scope

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "localized": localized,
            }
        )
        if group is not UNSET:
            field_dict["group"] = group
        if index is not UNSET:
            field_dict["index"] = index
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_message_localized import NewMessageLocalized

        d = src_dict.copy()
        localized = NewMessageLocalized.from_dict(d.pop("localized"))

        group = d.pop("group", UNSET)

        index = d.pop("index", UNSET)

        scope = d.pop("scope", UNSET)

        new_message = cls(
            localized=localized,
            group=group,
            index=index,
            scope=scope,
        )

        return new_message
