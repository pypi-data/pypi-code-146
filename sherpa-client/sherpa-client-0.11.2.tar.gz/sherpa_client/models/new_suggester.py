from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_suggester_parameters import NewSuggesterParameters


T = TypeVar("T", bound="NewSuggester")


@attr.s(auto_attribs=True)
class NewSuggester:
    """
    Attributes:
        engine (str):
        label (str):
        parameters (NewSuggesterParameters):
        tags (Union[Unset, List[str]]):
    """

    engine: str
    label: str
    parameters: "NewSuggesterParameters"
    tags: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        engine = self.engine
        label = self.label
        parameters = self.parameters.to_dict()

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
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_suggester_parameters import NewSuggesterParameters

        d = src_dict.copy()
        engine = d.pop("engine")

        label = d.pop("label")

        parameters = NewSuggesterParameters.from_dict(d.pop("parameters"))

        tags = cast(List[str], d.pop("tags", UNSET))

        new_suggester = cls(
            engine=engine,
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return new_suggester
