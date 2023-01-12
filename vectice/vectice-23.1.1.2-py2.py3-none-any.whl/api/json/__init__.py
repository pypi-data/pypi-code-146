from __future__ import annotations

from vectice.api.json.artifact_version import ArtifactVersion, VersionStrategy
from vectice.api.json.attachment import AttachmentOutput
from vectice.api.json.code import CodeInput, CodeOutput
from vectice.api.json.code_version import (
    CodeVersionCreateBody,
    CodeVersionInput,
    CodeVersionOutput,
    GitVersionInput,
    GitVersionOutput,
)
from vectice.api.json.dataset_register import DatasetRegisterOutput
from vectice.api.json.files_metadata import FileMetadata, FileMetadataType
from vectice.api.json.iteration import (
    IterationInput,
    IterationOutput,
    IterationStatus,
    IterationStepArtifact,
    IterationStepArtifactInput,
    IterationStepArtifactType,
)
from vectice.api.json.last_assets import ActivityTargetType, UserActivity
from vectice.api.json.metric import MetricInput, MetricOutput
from vectice.api.json.model_register import ModelRegisterInput, ModelRegisterOutput, ModelType
from vectice.api.json.model_version import ModelVersionInput, ModelVersionOutput, ModelVersionStatus
from vectice.api.json.page import Page
from vectice.api.json.paged_response import PagedResponse
from vectice.api.json.phase import PhaseInput, PhaseOutput
from vectice.api.json.project import ProjectInput, ProjectOutput
from vectice.api.json.property import PropertyInput, PropertyOutput
from vectice.api.json.step import StepInput, StepOutput
from vectice.api.json.user_declared_version import UserDeclaredVersion
from vectice.api.json.workspace import WorkspaceInput, WorkspaceOutput
from vectice.api.json.public_config import PublicConfigOutput, ArtifactName

__all__ = [
    "ArtifactVersion",
    "VersionStrategy",
    "GitVersionInput",
    "GitVersionOutput",
    "AttachmentOutput",
    "CodeInput",
    "CodeOutput",
    "CodeVersionInput",
    "CodeVersionOutput",
    "MetricInput",
    "MetricOutput",
    "ModelRegisterInput",
    "ModelRegisterOutput",
    "ModelType",
    "ModelVersionInput",
    "ModelVersionOutput",
    "ModelVersionStatus",
    "UserDeclaredVersion",
    "PagedResponse",
    "ProjectInput",
    "ProjectOutput",
    "PropertyInput",
    "PropertyOutput",
    "FileMetadata",
    "FileMetadataType",
    "WorkspaceOutput",
    "WorkspaceInput",
    "Page",
    "PhaseInput",
    "PhaseOutput",
    "StepInput",
    "StepOutput",
    "IterationInput",
    "IterationOutput",
    "IterationStatus",
    "IterationStepArtifactInput",
    "IterationStepArtifact",
    "IterationStepArtifactType",
    "DatasetRegisterOutput",
    "ModelRegisterOutput",
    "ActivityTargetType",
    "UserActivity",
    "CodeVersionCreateBody",
    "ArtifactName",
    "PublicConfigOutput",
]
