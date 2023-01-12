from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from vectice.api._utils import read_nodejs_date

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class WorkspaceInput:
    name: str | None
    description: str | None


class WorkspaceOutput(dict):
    def items(self):
        result = []
        for key in self:
            if self[key] is not None:
                result.append((key, self[key]))
        return result

    @property
    def organization_id(self) -> int:
        return int(self["organizationId"])

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
