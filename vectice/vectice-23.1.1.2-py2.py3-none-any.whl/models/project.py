from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.json.iteration import IterationStepArtifactInput
from vectice.models.datasource.datawrapper.metadata import SourceUsage
from vectice.models.phase import Phase
from vectice.utils.automatic_link_utils import existing_dataset_logger, link_dataset_to_step
from vectice.utils.common_utils import _check_code_source

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.models import Workspace
    from vectice.models.datasource.datawrapper import DataWrapper


_logger = logging.getLogger(__name__)


class Project:
    """Represent a Vectice project.

    A project reflects a typical Data Science project, including
    phases and the associated assets like code, datasets, models, and
    documentation. Multiple projects may be defined within each
    workspace.

    """

    __slots__ = ["_id", "_workspace", "_name", "_description", "_phase", "_origin_dataset", "_client", "_pointers"]

    def __init__(
        self,
        id: int,
        workspace: Workspace,
        name: str,
        description: str | None = None,
    ):
        """
        :param id: Project identifier
        :param workspace: The workspace reference this project belongs to
        :param name: Name of the project
        :param description: Brief description of the project
        """
        self._id = id
        self._workspace = workspace
        self._name = name
        self._description = description
        self._phase: Phase | None = None
        self._origin_dataset: DataWrapper | None = None
        self._client = workspace._client

    def __repr__(self):
        return (
            f"Project(name='{self.name}', id={self._id}, description='{self.description}', workspace={self._workspace})"
        )

    def __eq__(self, other: object):
        if not isinstance(other, Project):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """Return the project's id.

        :return: int
        """
        return self._id

    @property
    def workspace(self) -> Workspace:
        """Return the workspace to which this project belongs.

        :return: Workspace
        """
        return self._workspace

    @property
    def connection(self) -> Connection:
        """Return the Connection to which this project belongs.

        :return: Connection
        """
        return self._workspace.connection

    @property
    def name(self) -> str:
        """Return this project's name.

        :return: str
        """
        return self._name

    @property
    def description(self) -> str | None:
        """Return this project's description.

        :return: Optional[str]
        """
        return self._description

    @property
    def properties(self) -> dict:
        """Return this project's identifiers.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id, "workspace": self.workspace.id}

    def phase(self, phase: str | int) -> Phase:
        """Return a phase.

        :return: Optional[Phase]
        """
        item = self._client.get_phase(phase, project_id=self._id)
        _logger.info(f"Phase with id: {item.id} successfully retrieved.")
        phase_object = Phase(item.id, self, item.name, item.index, item.status)
        self._phase = phase_object
        return phase_object

    @property
    def phases(self) -> list[Phase]:
        """Return phases.

        Return the phases associated with this project.

        :return: List[Phase]
        """
        outputs = self._client.list_phases(project=self._id)
        return sorted(
            [Phase(item.id, self, item.name, item.index, item.status) for item in outputs], key=lambda x: x.index
        )

    @property
    def origin_dataset(self) -> DataWrapper | None:
        """Return the wrapped origin dataset of the project.

        If none exists, return None.

        :return: Optional[DataWrapper]
        """
        return self._origin_dataset

    @origin_dataset.setter
    def origin_dataset(self, data_source: DataWrapper):
        """Set the wrapped origin dataset of the Project.

        :param data_source: the origin dataset

        """
        if data_source.capture_code:
            code_version_id = _check_code_source(self._client, self._id, _logger)
        else:
            code_version_id = None
        self._origin_dataset = data_source
        data = self._client.register_dataset_from_source(
            data_source, SourceUsage.ORIGIN, project_id=self._id, code_version_id=code_version_id
        )
        existing_dataset_logger(data, data_source.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        link_dataset_to_step(step_artifact, data_source, data, _logger, project=self)
