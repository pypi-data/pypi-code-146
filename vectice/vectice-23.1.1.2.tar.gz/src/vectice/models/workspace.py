from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.models.project import Project

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client


_logger = logging.getLogger(__name__)


class Workspace:
    """Represent a Vectice Workspace.

    Workspaces are containers used to organize projects, assets, and
    users.

    Vectice users have access to a personal workspace and other
    workspaces so they can learn and collaborate with other users. An
    organization will have many workspaces, each with an Admin and
    Members with different privileges.


    Note that only an Org Admin can create a new workspace in the
    organization.

    """

    def __init__(self, id: int, name: str, description: str | None = None):
        """
        :param id: the workspace identifier
        :param name: the name of the workspace
        :param description: the description of the workspace
        """
        self._id = id
        self._name = name
        self._description = description
        self._client: Client
        self._connection: Connection

    def __post_init__(self, client: Client, connection: Connection):
        self._client = client
        self._connection = connection

    def __eq__(self, other: object):
        if not isinstance(other, Workspace):
            return NotImplemented
        return self.id == other.id

    def __repr__(self):
        return f"Workspace(name={self.name}, id={self._id}, description={self.description})"

    @property
    def id(self) -> int:
        """Return the workspace's id.

        :return: int
        """
        return self._id

    @property
    def name(self) -> str:
        """Return the workspace's name.

        :return: str
        """
        return self._name

    @property
    def description(self) -> str | None:
        """Return the workspace's description.

        :return: Optional[str]
        """
        return self._description

    @property
    def properties(self) -> dict:
        """Return the workspace's name and id.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id}

    def project(self, project: str | int) -> Project:
        """Return a project.

        :param project: The project name or id to get.

        :return: Project
        """
        item = self._client.get_project(project, self.id)
        _logger.info(f"Your current project: {item.id}")
        project_object = Project(item.id, self, item.name, item.description)
        return project_object

    @property
    def projects(self) -> list[Project]:
        """List projects.

        Return the projects in this workspace.

        :return: List[Project]
        """
        response = self._client.list_projects(self.id)
        return [Project(item.id, self, item.name, item.description) for item in response.list]

    @property
    def connection(self) -> Connection:
        return self._connection
