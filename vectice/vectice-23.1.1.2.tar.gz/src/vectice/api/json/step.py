from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from vectice.api.json.phase import PhaseOutput

if TYPE_CHECKING:
    from vectice.api.json.iteration import IterationStepArtifact


class DocumentationPageStatus(Enum):
    """
    Indicates the Documentation Page Status.
    """

    NotStarted = "NotStarted"
    """
    """
    InProgress = "Draft"
    """
    """
    Completed = "Completed"
    """
    """


class StepInput(dict):
    pass


class StepOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "phase" in self:
            self._phase: PhaseOutput = PhaseOutput(**self["phase"])
        else:
            self._phase = None

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def index(self) -> int:
        return int(self["index"])

    @property
    def parent(self) -> PhaseOutput:
        return self._phase

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def completed(self) -> bool:
        return bool(self["completed"])

    @property
    def description(self) -> str | None:
        return str(self["description"])

    @property
    def artifacts(self) -> list[IterationStepArtifact]:
        # TODO: refactor to break cyclic import
        from vectice.api.json.iteration import IterationStepArtifact

        return [IterationStepArtifact(artifact) for artifact in self["artifacts"]]


class StepUpdateInput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def text(self) -> str:
        return str(self["text"])
