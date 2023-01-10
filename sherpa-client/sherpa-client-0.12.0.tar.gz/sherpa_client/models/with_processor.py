from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.depends_on import DependsOn
    from ..models.next_step import NextStep
    from ..models.with_processor_condition import WithProcessorCondition
    from ..models.with_processor_parameters import WithProcessorParameters


T = TypeVar("T", bound="WithProcessor")


@attr.s(auto_attribs=True)
class WithProcessor:
    """
    Attributes:
        processor (str):
        condition (Union[Unset, WithProcessorCondition]):
        depends_on (Union[Unset, DependsOn]):
        disabled (Union[Unset, bool]):
        group (Union[Unset, str]):
        id (Union[Unset, str]):
        next_steps (Union[Unset, List['NextStep']]):
        parameters (Union[Unset, WithProcessorParameters]):
    """

    processor: str
    condition: Union[Unset, "WithProcessorCondition"] = UNSET
    depends_on: Union[Unset, "DependsOn"] = UNSET
    disabled: Union[Unset, bool] = UNSET
    group: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    next_steps: Union[Unset, List["NextStep"]] = UNSET
    parameters: Union[Unset, "WithProcessorParameters"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        processor = self.processor
        condition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.condition, Unset):
            condition = self.condition.to_dict()

        depends_on: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.depends_on, Unset):
            depends_on = self.depends_on.to_dict()

        disabled = self.disabled
        group = self.group
        id = self.id
        next_steps: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.next_steps, Unset):
            next_steps = []
            for next_steps_item_data in self.next_steps:
                next_steps_item = next_steps_item_data.to_dict()

                next_steps.append(next_steps_item)

        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "processor": processor,
            }
        )
        if condition is not UNSET:
            field_dict["condition"] = condition
        if depends_on is not UNSET:
            field_dict["dependsOn"] = depends_on
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if group is not UNSET:
            field_dict["group"] = group
        if id is not UNSET:
            field_dict["id"] = id
        if next_steps is not UNSET:
            field_dict["nextSteps"] = next_steps
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.depends_on import DependsOn
        from ..models.next_step import NextStep
        from ..models.with_processor_condition import WithProcessorCondition
        from ..models.with_processor_parameters import WithProcessorParameters

        d = src_dict.copy()
        processor = d.pop("processor")

        _condition = d.pop("condition", UNSET)
        condition: Union[Unset, WithProcessorCondition]
        if isinstance(_condition, Unset):
            condition = UNSET
        else:
            condition = WithProcessorCondition.from_dict(_condition)

        _depends_on = d.pop("dependsOn", UNSET)
        depends_on: Union[Unset, DependsOn]
        if isinstance(_depends_on, Unset):
            depends_on = UNSET
        else:
            depends_on = DependsOn.from_dict(_depends_on)

        disabled = d.pop("disabled", UNSET)

        group = d.pop("group", UNSET)

        id = d.pop("id", UNSET)

        next_steps = []
        _next_steps = d.pop("nextSteps", UNSET)
        for next_steps_item_data in _next_steps or []:
            next_steps_item = NextStep.from_dict(next_steps_item_data)

            next_steps.append(next_steps_item)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, WithProcessorParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = WithProcessorParameters.from_dict(_parameters)

        with_processor = cls(
            processor=processor,
            condition=condition,
            depends_on=depends_on,
            disabled=disabled,
            group=group,
            id=id,
            next_steps=next_steps,
            parameters=parameters,
        )

        return with_processor
