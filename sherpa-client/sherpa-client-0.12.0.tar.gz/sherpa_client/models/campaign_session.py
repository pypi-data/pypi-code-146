from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CampaignSession")


@attr.s(auto_attribs=True)
class CampaignSession:
    """
    Attributes:
        duration (int):
        id (str):
        label (str):
        split_size (float):
        reconciliation_username (Union[Unset, str]):
    """

    duration: int
    id: str
    label: str
    split_size: float
    reconciliation_username: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        duration = self.duration
        id = self.id
        label = self.label
        split_size = self.split_size
        reconciliation_username = self.reconciliation_username

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "duration": duration,
                "id": id,
                "label": label,
                "splitSize": split_size,
            }
        )
        if reconciliation_username is not UNSET:
            field_dict["reconciliationUsername"] = reconciliation_username

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        duration = d.pop("duration")

        id = d.pop("id")

        label = d.pop("label")

        split_size = d.pop("splitSize")

        reconciliation_username = d.pop("reconciliationUsername", UNSET)

        campaign_session = cls(
            duration=duration,
            id=id,
            label=label,
            split_size=split_size,
            reconciliation_username=reconciliation_username,
        )

        return campaign_session
