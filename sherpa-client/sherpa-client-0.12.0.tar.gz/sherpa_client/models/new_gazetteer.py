from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_gazetteer_parameters import NewGazetteerParameters


T = TypeVar("T", bound="NewGazetteer")


@attr.s(auto_attribs=True)
class NewGazetteer:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewGazetteerParameters):
        email_notification (Union[Unset, bool]):
        tags (Union[Unset, List[str]]):
    """

    engine: str
    label: str
    parameters: "NewGazetteerParameters"
    email_notification: Union[Unset, bool] = UNSET
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        engine = self.engine
        label = self.label
        parameters = self.parameters.to_dict()

        email_notification = self.email_notification
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "engine": engine,
                "label": label,
                "parameters": parameters,
            }
        )
        if email_notification is not UNSET:
            field_dict["emailNotification"] = email_notification
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_gazetteer_parameters import NewGazetteerParameters

        d = src_dict.copy()
        engine = d.pop("engine")

        label = d.pop("label")

        parameters = NewGazetteerParameters.from_dict(d.pop("parameters"))

        email_notification = d.pop("emailNotification", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        new_gazetteer = cls(
            engine=engine,
            label=label,
            parameters=parameters,
            email_notification=email_notification,
            tags=tags,
        )

        return new_gazetteer
