from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_0_input_transforms import FlowModuleValue2Type0InputTransforms
from ..models.flow_module_value_2_type_0_language import FlowModuleValue2Type0Language
from ..models.flow_module_value_2_type_0_type import FlowModuleValue2Type0Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type0")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type0:
    """
    Attributes:
        input_transforms (FlowModuleValue2Type0InputTransforms):
        content (str):
        language (FlowModuleValue2Type0Language):
        type (FlowModuleValue2Type0Type):
        path (Union[Unset, str]):
        lock (Union[Unset, str]):
    """

    input_transforms: FlowModuleValue2Type0InputTransforms
    content: str
    language: FlowModuleValue2Type0Language
    type: FlowModuleValue2Type0Type
    path: Union[Unset, str] = UNSET
    lock: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms = self.input_transforms.to_dict()

        content = self.content
        language = self.language.value

        type = self.type.value

        path = self.path
        lock = self.lock

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_transforms": input_transforms,
                "content": content,
                "language": language,
                "type": type,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if lock is not UNSET:
            field_dict["lock"] = lock

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_transforms = FlowModuleValue2Type0InputTransforms.from_dict(d.pop("input_transforms"))

        content = d.pop("content")

        language = FlowModuleValue2Type0Language(d.pop("language"))

        type = FlowModuleValue2Type0Type(d.pop("type"))

        path = d.pop("path", UNSET)

        lock = d.pop("lock", UNSET)

        flow_module_value_2_type_0 = cls(
            input_transforms=input_transforms,
            content=content,
            language=language,
            type=type,
            path=path,
            lock=lock,
        )

        flow_module_value_2_type_0.additional_properties = d
        return flow_module_value_2_type_0

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
