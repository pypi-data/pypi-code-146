from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from vectice.api.json.step import PhaseOutput

if TYPE_CHECKING:
    from vectice.api.json.step import StepOutput


class IterationStatus(Enum):
    NotStarted = "NotStarted"
    InProgress = "InProgress"
    InReview = "InReview"
    Abandoned = "Abandoned"
    Completed = "Completed"


class IterationStepArtifactType(Enum):
    ModelVersion = "ModelVersion"
    DataSetVersion = "DataSetVersion"
    EntityFile = "EntityFile"
    JobRun = "JobRun"


class IterationStepArtifact(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def dataset_version_id(self) -> int:
        return int(self["datasetVersionId"])

    @property
    def model_version_id(self) -> int:
        return int(self["modelVersionId"])

    @property
    def entity_file_id(self) -> int:
        return int(self["entityFileId"])

    @property
    def type(self) -> IterationStepArtifactType:
        return IterationStepArtifactType(self["type"])


class IterationStepArtifactInput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def entity_file_id(self) -> int:
        return int(self["entityFileId"])


class IterationInput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class IterationOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def index(self) -> int:
        return int(self["index"])

    @property
    def phase(self) -> PhaseOutput:
        return PhaseOutput(**self["phase"])

    @property
    def steps(self) -> list[StepOutput]:
        from vectice.api.json.step import StepOutput

        steps_json = self["steps"]
        steps = [StepOutput(step) for step in steps_json]
        return steps

    @property
    def alias(self) -> str:
        return str(self["alias"])

    @property
    def status(self) -> IterationStatus:
        return IterationStatus(self["status"])
