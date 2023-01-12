from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.json.iteration import IterationStepArtifactInput
from vectice.api.json.phase import PhaseStatus
from vectice.models.datasource.datawrapper.metadata import SourceUsage
from vectice.models.iteration import Iteration
from vectice.utils.automatic_link_utils import existing_dataset_logger, link_dataset_to_step
from vectice.utils.common_utils import _check_code_source

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client
    from vectice.models import Project, Workspace
    from vectice.models.datasource.datawrapper import DataWrapper


_logger = logging.getLogger(__name__)


class Phase:
    """Represent a Vectice phase.

    Phases reflect the real-life phases of the project lifecycle
    (i.e., Business Understanding, Data Preparation, Modeling,
    Deployment, etc.).  The Vectice admin creates the phases of a
    project.

    Phases let you document the goals, assets, and outcomes along with
    the status to organize the project, enforce best practices, allow
    consistency, and capture knowledge.

    """

    __slots__ = [
        "_id",
        "_project",
        "_name",
        "_index",
        "_status",
        "_clean_dataset",
        "_client",
        "_current_iteration",
        "_pointers",
    ]

    def __init__(
        self,
        id: int,
        project: Project,
        name: str,
        index: int,
        status: PhaseStatus = PhaseStatus.NotStarted,
    ):
        """
        :param id: the phase identifier
        :param project: the project to which the phase belongs
        :param name: the name of the phase
        :param index: the index of the phase
        :param status: the status of the phase
        """
        self._id = id
        self._project = project
        self._name = name
        self._index = index
        self._status = status
        self._client: Client = self._project._client
        self._clean_dataset: DataWrapper | None = None
        self._current_iteration: Iteration | None = None

    def __repr__(self):
        return f"Phase (name='{self.name}', id={self.id}, status='{self.status.name}')"

    def __eq__(self, other: object):
        if not isinstance(other, Phase):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """Return the phase's id.

        :return: int
        """
        return self._id

    @id.setter
    def id(self, phase_id: int):
        """Set the phase's id.

        :param phase_id: the phase identifier to set
        """
        self._id = phase_id

    @property
    def name(self) -> str:
        """Return the phase's name.

        :return: str
        """
        return self._name

    @property
    def index(self) -> int:
        """Return the phase's index.

        :return: int
        """
        return self._index

    @property
    def status(self) -> PhaseStatus:
        """Set the phase's status.

        :return: PhaseStatus
        """
        return self._status

    @property
    def properties(self) -> dict:
        """Return the phase's name, id, and index.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def iterations(self) -> list[Iteration]:
        """Return the phase's iterations.

        :return: List[Iteration]
        """
        iteration_outputs = self._client.list_iterations(self.id)
        return sorted(
            [Iteration(item.id, item.index, self, item.status) for item in iteration_outputs], key=lambda x: x.index
        )

    def iteration(self, index: int | None = None) -> Iteration:
        """Return a (possibly new) iteration.

        Fetch and return an iteration by index.  If no index is
        provided, return a new iteration.

        :return: Iteration

        """
        if index:
            iteration_output = self._client.get_iteration_by_index(self.id, index)
            _logger.info(f"Iteration with index: {iteration_output.index} successfully retrieved.")
        else:
            iteration_output = self._client.get_or_create_iteration(self.id)
            _logger.info(f"Iteration with id: {iteration_output.id} successfully retrieved.")
        iteration_object = Iteration(iteration_output.id, iteration_output.index, self, iteration_output.status)
        self._current_iteration = iteration_object
        return iteration_object

    @property
    def clean_dataset(self) -> DataWrapper | None:
        """Return the phase's wrapped clean dataset.

        If the phase has no assigned cleaned data set, return None.

        :return: Optional[DataWrapper]
        """
        return self._clean_dataset

    @clean_dataset.setter
    def clean_dataset(self, data_source: DataWrapper) -> None:
        """Set the phase's cleaned data set.

        :param data_source: the clean dataset

        """
        if data_source.capture_code:
            code_version_id = _check_code_source(self._client, self._project._id, _logger)
        else:
            code_version_id = None
        self._clean_dataset = data_source
        data = self._client.register_dataset_from_source(
            data_source,
            SourceUsage.CLEAN,
            project_id=self._project._id,
            phase_id=self._id,
            code_version_id=code_version_id,
        )
        existing_dataset_logger(data, data_source.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        logging.getLogger("vectice.models.project").propagate = False
        link_dataset_to_step(step_artifact, data_source, data, _logger, phase=self)

    @property
    def connection(self) -> Connection:
        """Return the Connection to which this phase belongs.

        :return: Connection
        """
        return self._project.connection

    @property
    def workspace(self) -> Workspace:
        """Return the Workspace to which this phase belongs.

        :return: Workspace
        """
        return self._project.workspace

    @property
    def project(self) -> Project:
        """Return the Project to which this phase belongs.

        :return: Project
        """
        return self._project
