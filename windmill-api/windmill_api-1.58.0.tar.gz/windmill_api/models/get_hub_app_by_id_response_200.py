from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.get_hub_app_by_id_response_200_app import GetHubAppByIdResponse200App

T = TypeVar("T", bound="GetHubAppByIdResponse200")


@attr.s(auto_attribs=True)
class GetHubAppByIdResponse200:
    """
    Attributes:
        app (GetHubAppByIdResponse200App):
    """

    app: GetHubAppByIdResponse200App
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        app = self.app.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "app": app,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        app = GetHubAppByIdResponse200App.from_dict(d.pop("app"))

        get_hub_app_by_id_response_200 = cls(
            app=app,
        )

        get_hub_app_by_id_response_200.additional_properties = d
        return get_hub_app_by_id_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
