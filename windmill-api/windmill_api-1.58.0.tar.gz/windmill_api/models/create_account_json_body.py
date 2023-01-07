from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAccountJsonBody")


@attr.s(auto_attribs=True)
class CreateAccountJsonBody:
    """
    Attributes:
        expires_in (int):
        owner (str):
        client (str):
        refresh_token (Union[Unset, str]):
    """

    expires_in: int
    owner: str
    client: str
    refresh_token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expires_in = self.expires_in
        owner = self.owner
        client = self.client
        refresh_token = self.refresh_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expires_in": expires_in,
                "owner": owner,
                "client": client,
            }
        )
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expires_in = d.pop("expires_in")

        owner = d.pop("owner")

        client = d.pop("client")

        refresh_token = d.pop("refresh_token", UNSET)

        create_account_json_body = cls(
            expires_in=expires_in,
            owner=owner,
            client=client,
            refresh_token=refresh_token,
        )

        create_account_json_body.additional_properties = d
        return create_account_json_body

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
