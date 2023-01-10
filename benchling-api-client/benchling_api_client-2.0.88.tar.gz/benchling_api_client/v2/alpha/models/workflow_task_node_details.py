from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_task_schema_summary import WorkflowTaskSchemaSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowTaskNodeDetails")


@attr.s(auto_attribs=True, repr=False)
class WorkflowTaskNodeDetails:
    """  """

    _id: Union[Unset, str] = UNSET
    _task_schema: Union[Unset, WorkflowTaskSchemaSummary] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("task_schema={}".format(repr(self._task_schema)))
        return "WorkflowTaskNodeDetails({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        task_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._task_schema, Unset):
            task_schema = self._task_schema.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if task_schema is not UNSET:
            field_dict["taskSchema"] = task_schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_task_schema() -> Union[Unset, WorkflowTaskSchemaSummary]:
            task_schema: Union[Unset, Union[Unset, WorkflowTaskSchemaSummary]] = UNSET
            _task_schema = d.pop("taskSchema")

            if not isinstance(_task_schema, Unset):
                task_schema = WorkflowTaskSchemaSummary.from_dict(_task_schema)

            return task_schema

        try:
            task_schema = get_task_schema()
        except KeyError:
            if strict:
                raise
            task_schema = cast(Union[Unset, WorkflowTaskSchemaSummary], UNSET)

        workflow_task_node_details = cls(
            id=id,
            task_schema=task_schema,
        )

        return workflow_task_node_details

    @property
    def id(self) -> str:
        """ The ID of the workflow task node config details """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def task_schema(self) -> WorkflowTaskSchemaSummary:
        if isinstance(self._task_schema, Unset):
            raise NotPresentError(self, "task_schema")
        return self._task_schema

    @task_schema.setter
    def task_schema(self, value: WorkflowTaskSchemaSummary) -> None:
        self._task_schema = value

    @task_schema.deleter
    def task_schema(self) -> None:
        self._task_schema = UNSET
