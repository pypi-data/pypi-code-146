from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.api._utils import read_nodejs_date
from vectice.api.json.workspace import WorkspaceOutput

if TYPE_CHECKING:
    from datetime import datetime


class ProjectInput(dict):
    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> str:
        return str(self["description"])


class ProjectOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "workspace" in self:
            self._workspace: WorkspaceOutput = WorkspaceOutput(**self["workspace"])

    def items(self):
        result = []
        for key in self:
            if self[key] is not None:
                result.append((key, self[key]))
        return result

    @property
    def workspace_id(self) -> int:
        return int(self["workspaceId"])

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> str | None:
        if "description" in self and self["description"] is not None:
            return str(self["description"])
        else:
            return None

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
    def workspace(self) -> WorkspaceOutput:
        return self._workspace
