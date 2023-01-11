from __future__ import annotations

from continual.python.sdk.exceptions import InvalidArgumentError


class ProjectEnvironmentIdentifer:
    """Utility class to handle project and environment names and identifers."""

    production_environment_ids = ["production"]
    default_environment_id = "production"

    def __init__(self, project_name_or_id="", environment_name_or_id=""):
        self.__project_name = ""
        self.__project_id = ""
        self.__environment_name = ""
        self.__environment_id = ""
        self.__parse(project_name_or_id, environment_name_or_id)

    def __parse(self, project_name_or_id: str, environment_name_or_id: str):
        project_part = ""
        environment_part = ""

        if project_name_or_id:
            project_part = project_name_or_id

        if environment_name_or_id:
            environment_part = environment_name_or_id
            if not project_part:
                splits = environment_part.split("/")
                if len(splits) == 4:
                    project_part = "/".join(splits[:-2])

        if not project_part:
            raise InvalidArgumentError(
                f"A project name or ID is required. Received: '{project_name_or_id}', '{environment_name_or_id}'"
            )
        elif project_part.startswith("projects/"):
            self.__project_id = project_part.split("projects/")[1]
            self.__project_name = project_part
        else:
            self.__project_id = project_part
            self.__project_name = f"projects/{self.__project_id}"

        if not environment_part:
            if self.__project_name:
                # set default as production but potentially remove
                self.__environment_id = self.default_environment_id
                self.__environment_name = (
                    f"{self.__project_name}/environments/{self.__environment_id}"
                )
            else:
                raise InvalidArgumentError(
                    f"A project name or ID is required. Received: '{project_name_or_id}', '{environment_name_or_id}'"
                )
        elif environment_part.startswith("projects/"):
            if environment_part == self.__project_name:
                self.__environment_id = self.default_environment_id
                self.__environment_name = (
                    f"{environment_part}/environments/{self.__environment_id}"
                )
            else:
                self.__environment_name = environment_part
                splits = environment_part.split("/")
                if len(splits) == 4:
                    self.__environment_id = splits[-1]
                    self.__project_name = "/".join(splits[:2])
                    self.__project_id = splits[1]
        elif environment_part in self.production_environment_ids:
            if self.__project_name:
                self.__environment_id = self.default_environment_id
                self.__environment_name = (
                    f"{self.__project_name}/environments/{self.__environment_id}"
                )
            else:
                raise InvalidArgumentError(
                    f"A project name or ID is required. Received: '{project_name_or_id}', '{environment_name_or_id}'"
                )
        else:
            self.__environment_id = environment_part
            self.__environment_name = (
                f"{self.__project_name}/environments/{self.__environment_id}"
            )

    @property
    def project_name(self) -> str:
        """Project name `projects/[project_id]`."""
        return self.__project_name

    @property
    def project_id(self) -> str:
        """Project ID `[project_id]`."""
        return self.__project_id

    @property
    def environment_name(self) -> str:
        """Environment name `projects/[project_id]/environments/[environment_id]`."""
        return self.__environment_name

    @property
    def environment_id(self) -> str:
        """Environment ID: `[environment_id]` when non-default, `[project_name]` when default."""
        return self.__environment_id

    def __getitem__(self, key):
        return getattr(self, key)
