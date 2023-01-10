from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.project_annotators import ProjectAnnotators


T = TypeVar("T", bound="ProjectsAnnotators")


@attr.s(auto_attribs=True)
class ProjectsAnnotators:
    """
    Attributes:
        annotators (ProjectAnnotators):
        project_name (str):
    """

    annotators: "ProjectAnnotators"
    project_name: str

    def to_dict(self) -> Dict[str, Any]:
        annotators = self.annotators.to_dict()

        project_name = self.project_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "annotators": annotators,
                "projectName": project_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.project_annotators import ProjectAnnotators

        d = src_dict.copy()
        annotators = ProjectAnnotators.from_dict(d.pop("annotators"))

        project_name = d.pop("projectName")

        projects_annotators = cls(
            annotators=annotators,
            project_name=project_name,
        )

        return projects_annotators
