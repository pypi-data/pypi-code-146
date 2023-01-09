from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_hub_script_by_path_response_200_language import GetHubScriptByPathResponse200Language
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetHubScriptByPathResponse200")


@attr.s(auto_attribs=True)
class GetHubScriptByPathResponse200:
    """
    Attributes:
        content (str):
        language (GetHubScriptByPathResponse200Language):
        lockfile (Union[Unset, str]):
        schema (Union[Unset, Any]):
        summary (Union[Unset, str]):
    """

    content: str
    language: GetHubScriptByPathResponse200Language
    lockfile: Union[Unset, str] = UNSET
    schema: Union[Unset, Any] = UNSET
    summary: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content = self.content
        language = self.language.value

        lockfile = self.lockfile
        schema = self.schema
        summary = self.summary

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "language": language,
            }
        )
        if lockfile is not UNSET:
            field_dict["lockfile"] = lockfile
        if schema is not UNSET:
            field_dict["schema"] = schema
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content = d.pop("content")

        language = GetHubScriptByPathResponse200Language(d.pop("language"))

        lockfile = d.pop("lockfile", UNSET)

        schema = d.pop("schema", UNSET)

        summary = d.pop("summary", UNSET)

        get_hub_script_by_path_response_200 = cls(
            content=content,
            language=language,
            lockfile=lockfile,
            schema=schema,
            summary=summary,
        )

        get_hub_script_by_path_response_200.additional_properties = d
        return get_hub_script_by_path_response_200

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
