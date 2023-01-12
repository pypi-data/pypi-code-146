from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.api._utils import read_nodejs_date

if TYPE_CHECKING:
    from datetime import datetime

    from vectice.api.json import ProjectOutput


class ModelOutput(dict):
    def __init__(self, *args, **kwargs):
        from vectice.api.json import ProjectOutput

        super().__init__(*args, **kwargs)
        if "project" in self:
            self._project: ProjectOutput = ProjectOutput(**self["project"])

    @property
    def created_date(self) -> datetime | None:
        return read_nodejs_date(str(self["createdDate"]))

    @property
    def updated_date(self) -> datetime | None:
        return read_nodejs_date(str(self["updatedDate"]))

    @property
    def deleted_date(self) -> datetime | None:
        return read_nodejs_date(str(self["deletedDate"]))

    @property
    def version(self) -> int:
        return int(self["version"])

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def project(self) -> ProjectOutput:
        from vectice.api.json import ProjectOutput

        return ProjectOutput(**self["project"])

    @project.setter
    def project(self, value: ProjectOutput) -> None:
        self._project = value

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def description(self) -> str:
        return str(self["description"])

    @property
    def author_id(self) -> int:
        return int(self["authorId"])

    @property
    def project_id(self) -> int:
        return int(self["projectId"])
