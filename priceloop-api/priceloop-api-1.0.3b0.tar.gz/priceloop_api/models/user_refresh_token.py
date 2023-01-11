from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="UserRefreshToken")


@attr.s(auto_attribs=True)
class UserRefreshToken:
    """
    Attributes:
        refresh_token (str):
        seller_id (str):
        workspace_name (str):
    """

    refresh_token: str
    seller_id: str
    workspace_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        refresh_token = self.refresh_token
        seller_id = self.seller_id
        workspace_name = self.workspace_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "refreshToken": refresh_token,
                "sellerId": seller_id,
                "workspaceName": workspace_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        refresh_token = d.pop("refreshToken")

        seller_id = d.pop("sellerId")

        workspace_name = d.pop("workspaceName")

        user_refresh_token = cls(
            refresh_token=refresh_token,
            seller_id=seller_id,
            workspace_name=workspace_name,
        )

        user_refresh_token.additional_properties = d
        return user_refresh_token

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
