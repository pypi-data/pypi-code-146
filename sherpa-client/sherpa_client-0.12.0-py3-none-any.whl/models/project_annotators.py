from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.annotator import Annotator


T = TypeVar("T", bound="ProjectAnnotators")


@attr.s(auto_attribs=True)
class ProjectAnnotators:
    """
    Attributes:
        gazetteer (List['Annotator']):
        learner (List['Annotator']):
        plan (List['Annotator']):
        suggester (List['Annotator']):
    """

    gazetteer: List["Annotator"]
    learner: List["Annotator"]
    plan: List["Annotator"]
    suggester: List["Annotator"]

    def to_dict(self) -> Dict[str, Any]:
        gazetteer = []
        for gazetteer_item_data in self.gazetteer:
            gazetteer_item = gazetteer_item_data.to_dict()

            gazetteer.append(gazetteer_item)

        learner = []
        for learner_item_data in self.learner:
            learner_item = learner_item_data.to_dict()

            learner.append(learner_item)

        plan = []
        for plan_item_data in self.plan:
            plan_item = plan_item_data.to_dict()

            plan.append(plan_item)

        suggester = []
        for suggester_item_data in self.suggester:
            suggester_item = suggester_item_data.to_dict()

            suggester.append(suggester_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "gazetteer": gazetteer,
                "learner": learner,
                "plan": plan,
                "suggester": suggester,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.annotator import Annotator

        d = src_dict.copy()
        gazetteer = []
        _gazetteer = d.pop("gazetteer")
        for gazetteer_item_data in _gazetteer:
            gazetteer_item = Annotator.from_dict(gazetteer_item_data)

            gazetteer.append(gazetteer_item)

        learner = []
        _learner = d.pop("learner")
        for learner_item_data in _learner:
            learner_item = Annotator.from_dict(learner_item_data)

            learner.append(learner_item)

        plan = []
        _plan = d.pop("plan")
        for plan_item_data in _plan:
            plan_item = Annotator.from_dict(plan_item_data)

            plan.append(plan_item)

        suggester = []
        _suggester = d.pop("suggester")
        for suggester_item_data in _suggester:
            suggester_item = Annotator.from_dict(suggester_item_data)

            suggester.append(suggester_item)

        project_annotators = cls(
            gazetteer=gazetteer,
            learner=learner,
            plan=plan,
            suggester=suggester,
        )

        return project_annotators
