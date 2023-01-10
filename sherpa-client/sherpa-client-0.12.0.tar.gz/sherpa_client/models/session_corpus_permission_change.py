from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="SessionCorpusPermissionChange")


@attr.s(auto_attribs=True)
class SessionCorpusPermissionChange:
    """
    Attributes:
        add (bool):
        project_name (str):
        session_label (str):
        usernames (List[Any]):
    """

    add: bool
    project_name: str
    session_label: str
    usernames: List[Any]

    def to_dict(self) -> Dict[str, Any]:
        add = self.add
        project_name = self.project_name
        session_label = self.session_label
        usernames = self.usernames

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "add": add,
                "projectName": project_name,
                "sessionLabel": session_label,
                "usernames": usernames,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        add = d.pop("add")

        project_name = d.pop("projectName")

        session_label = d.pop("sessionLabel")

        usernames = cast(List[Any], d.pop("usernames"))

        session_corpus_permission_change = cls(
            add=add,
            project_name=project_name,
            session_label=session_label,
            usernames=usernames,
        )

        return session_corpus_permission_change
