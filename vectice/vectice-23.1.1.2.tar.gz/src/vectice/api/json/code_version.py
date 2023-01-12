from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from vectice.api._utils import read_nodejs_date
from vectice.api.json.code import CodeOutput

if TYPE_CHECKING:
    from datetime import datetime


class CodeVersionAction(Enum):
    CREATE_GIT_VERSION = "CREATE_GIT_VERSION"
    CREATE_USER_DECLARED_VERSION = "CREATE_USER_DECLARED_VERSION"


@dataclass
class GitVersion:
    repositoryName: str
    branchName: str
    commitHash: str
    isDirty: bool
    uri: str
    commitComment: str | None = ""
    commitAuthorName: str | None = ""
    commitAuthorEmail: str | None = ""
    entrypoint: str | None = ""


@dataclass
class GitVersionInput:
    repositoryName: str
    branchName: str
    commitHash: str
    isDirty: bool
    uri: str
    commitComment: str | None = None
    commitAuthorName: str | None = None
    commitAuthorEmail: str | None = None
    entrypoint: str | None = None


class userDeclaredVersion(dict):
    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> str:
        return str(self["description"])

    @property
    def uri(self) -> str:
        return str(self["uri"])

    @property
    def is_starred(self) -> bool:
        return bool(self["isStarred"])


class CodeVersionCreateBody(dict):
    @property
    def action(self) -> str:
        return str(self["action"])

    @property
    def git_version(self) -> str:
        return str(self["gitVersion"])

    @property
    def user_declared_version(self) -> str:
        return str(self["userDeclaredVersion"])


class CodeVersionInput(dict):
    @property
    def code_id(self) -> int:
        return int(self["codeId"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> str:
        return str(self["description"])

    @property
    def uri(self) -> str:
        return str(self["uri"])

    @property
    def is_starred(self) -> str:
        return str(self["isStarred"])

    @property
    def git_version_id(self) -> int:
        return int(self["gitVersionId"])

    @property
    def git_version(self) -> GitVersionInput:
        return GitVersionInput(**self["gitVersion"])


class GitVersionOutput(dict):
    @property
    def created_date(self) -> datetime | None:
        return read_nodejs_date(str(self["createdDate"]))

    @property
    def updated_date(self) -> datetime | None:
        return read_nodejs_date(str(self["updatedDate"]))

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def version(self) -> int:
        return int(self["version"])

    @property
    def author_id(self) -> int:
        return int(self["authorId"])

    @property
    def workspace_id(self) -> int:
        return int(self["workspaceId"])

    @property
    def deleted_date(self) -> datetime | None:
        return read_nodejs_date(str(self["deletedDate"]))

    @property
    def repository_name(self) -> str:
        return str(self["repositoryName"])

    @property
    def branch_name(self) -> str:
        return str(self["branchName"])

    @property
    def commit_hash(self) -> str:
        return str(self["commitHash"])

    @property
    def commit_comment(self) -> str:
        return str(self["commitComment"])

    @property
    def commit_author_email(self) -> str:
        return str(self["commitAuthorEmail"])

    @property
    def commit_author_name(self) -> str:
        return str(self["commitAuthorName"])

    @property
    def is_dirty(self) -> bool:
        return bool(self["isDirty"])

    @property
    def uri(self) -> str:
        return str(self["uri"])

    @property
    def entrypoint(self) -> str:
        return str(self["entrypoint"])


class CodeVersionOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "code" in self:
            self._code: CodeOutput = CodeOutput(**self["code"])
        else:
            self._code = None

    def items(self):
        result = []
        for key in self:
            if self[key] is not None:
                result.append((key, self[key]))
        return result

    @property
    def created_date(self) -> datetime | None:
        return read_nodejs_date(str(self["createdDate"]))

    @property
    def updated_date(self) -> datetime | None:
        return read_nodejs_date(str(self["updatedDate"]))

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def version(self) -> int:
        return int(self["version"])

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
    def uri(self) -> str:
        return str(self["uri"])

    @property
    def author_id(self) -> int:
        return int(self["authorId"])

    @property
    def deleted_date(self) -> datetime | None:
        return read_nodejs_date(str(self["deletedDate"]))

    @property
    def version_number(self) -> int:
        return int(self["versionNumber"])

    @property
    def code_id(self) -> int:
        return int(self["codeId"])

    @property
    def git_version_id(self) -> int:
        return int(self["gitVersionId"])

    @property
    def git_version(self) -> GitVersionOutput | None:
        if "gitVersion" in self:
            return GitVersionOutput(**self["gitVersion"])
        else:
            return None

    @property
    def is_starred(self) -> bool | None:
        if self.get("isStarred"):
            return bool(self["isStarred"])
        else:
            return None

    @property
    def code(self) -> CodeOutput:
        return self._code
