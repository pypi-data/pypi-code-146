from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from vectice.api.http_error_handlers import VecticeException

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api.json.iteration import IterationStepArtifact
    from vectice.models import Iteration, Phase, Project, Workspace


_logger = logging.getLogger(__name__)


class Step:
    """Model a Vectice step.

    Steps define the logical sequence of steps required to complete
    the Phase along with their expected outcomes.

    """

    def __init__(
        self,
        id: int,
        iteration: Iteration,
        name: str,
        index: int,
        description: str | None = None,
        completed: bool = False,
        artifacts: list[IterationStepArtifact] | None = None,
    ):
        """
        :param id: the step identifier
        :param iteration: the iteration to which the step belongs
        :param name: the name of the step
        :param description: the description of the step
        """
        self._id = id
        self._iteration: Iteration = iteration
        self._name = name
        self._index = index
        self._description = description
        self._client = self._iteration._client
        self._completed = completed
        self._artifacts = artifacts

    def __repr__(self):
        return f"Step(name='{self.name}', id={self.id}, description='{self._description}', completed={self.completed})"

    def __eq__(self, other: object):
        if not isinstance(other, Step):
            return NotImplemented
        return self.id == other.id

    @property
    def name(self) -> str:
        """Return the step's name.

        :return: str
        """
        return self._name

    @property
    def id(self) -> int:
        """Return the step's id.

        :return: int
        """
        return self._id

    @id.setter
    def id(self, step_id: int):
        """Set the step's id.

        :param step_id: the id to set
        """
        self._id = step_id

    @property
    def index(self) -> int:
        """Return the step's index.

        :return: int
        """
        return self._index

    @property
    def properties(self) -> dict:
        """Return the step's name, id, and index.

        :return: Optional[Dict]
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def completed(self) -> bool:
        return self._completed

    @property
    def artifacts(self) -> list[IterationStepArtifact] | None:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts: list[IterationStepArtifact]):
        self._artifacts = artifacts

    def next_step(self, message: str | None = None) -> Step | None:
        """Advance to the next step.

        Close the current step (mark it completed) and return the next
        step to complete if another open step exists.  Otherwise
        return None.

        Note that steps are not currently ordered, and so the concept
        of "next" is rather arbitrary.

        :return: Optional[Step]

        """
        self.close(message)
        steps_output = self._client.list_steps(self._iteration.id)
        open_steps = sorted(
            [
                Step(item.id, self._iteration, item.name, item.index, item.description)
                for item in steps_output
                if not item.completed
            ],
            key=lambda x: x.index,
        )
        if not open_steps:
            _logger.info("There are no active steps.")
            return None
        next_step = open_steps[0]
        _logger.info(f"Next step : {repr(next_step)}")
        return next_step

    def close(self, message: str | None = None):
        """Close the current step, marking it completed."""
        try:
            self._client.close_step(self.id, message)
            _logger.info(f"'{self.name}' was successfully closed.")
            self._completed = True
        except VecticeException as e:
            raise e

    @property
    def connection(self) -> Connection:
        """Return the Connection to which this step belongs.

        :return: Connection
        """
        return self._iteration.connection

    @property
    def workspace(self) -> Workspace:
        """Return the Workspace to which this step belongs.

        :return: Workspace
        """
        return self._iteration.workspace

    @property
    def project(self) -> Project:
        """Return the Project to which this step belongs.

        :return: Project
        """
        return self._iteration.project

    @property
    def phase(self) -> Phase:
        """Return the Phase to which this step belongs.

        :return: Phase
        """
        return self._iteration.phase

    @property
    def iteration(self) -> Iteration:
        """Return the Iteration to which this step belongs.

        :return: Iteration
        """
        return self._iteration
