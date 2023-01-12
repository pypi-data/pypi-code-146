from __future__ import annotations

from enum import Enum


class ActivityTargetType(Enum):
    Code = "Code"
    CodeVersion = "CodeVersion"
    DataResource = "DataResource"
    DataSet = "DataSet"
    DataSetVersion = "DataSetVersion"
    Datasheet = "Datasheet"
    Iteration = "Iteration"
    Review = "Review"
    ReviewComment = "ReviewComment"
    IterationStep = "IterationStep"
    Model = "Model"
    ModelCard = "ModelCard"
    ModelVersion = "ModelVersion"
    Phase = "Phase"
    Project = "Project"
    StepDefinition = "StepDefinition"
    Workspace = "Workspace"
    WorkspaceUser = "WorkspaceUser"


class UserActivity(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def id(self) -> int:
        return int(self["targetId"])

    @property
    def name(self) -> str:
        return str(self["targetName"])

    @property
    def target_type(self) -> ActivityTargetType:
        return ActivityTargetType(self["targetType"])
