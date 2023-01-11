from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigItemsUnarchive")


@attr.s(auto_attribs=True, repr=False)
class AppConfigItemsUnarchive:
    """  """

    _item_ids: List[str]

    def __repr__(self):
        fields = []
        fields.append("item_ids={}".format(repr(self._item_ids)))
        return "AppConfigItemsUnarchive({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        item_ids = self._item_ids

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if item_ids is not UNSET:
            field_dict["itemIds"] = item_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_item_ids() -> List[str]:
            item_ids = cast(List[str], d.pop("itemIds"))

            return item_ids

        try:
            item_ids = get_item_ids()
        except KeyError:
            if strict:
                raise
            item_ids = cast(List[str], UNSET)

        app_config_items_unarchive = cls(
            item_ids=item_ids,
        )

        return app_config_items_unarchive

    @property
    def item_ids(self) -> List[str]:
        """ Array of app configuration item IDs """
        if isinstance(self._item_ids, Unset):
            raise NotPresentError(self, "item_ids")
        return self._item_ids

    @item_ids.setter
    def item_ids(self, value: List[str]) -> None:
        self._item_ids = value
