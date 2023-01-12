"""Gordo client schemas."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class CrossValidationMetaData(BaseModel):
    """Cross validation metadata schema."""

    scores: Dict[str, Any] = Field(default_factory=dict)
    cv_duration_sec: Optional[float] = None
    splits: Dict[str, Any] = Field(default_factory=dict)


class ModelBuildMetadata(BaseModel):
    """Model build schema."""

    model_offset: int = 0
    model_creation_date: Optional[str] = None
    model_builder_version: Optional[str] = None
    cross_validation: CrossValidationMetaData = Field(default_factory=CrossValidationMetaData)
    model_training_duration_sec: Optional[float] = None
    model_meta: Dict[str, Any] = Field(default_factory=dict)


class DatasetBuildMetadata(BaseModel):
    """Dataset build metadata schema."""

    query_duration_sec: Optional[float] = None  # How long it took to get the data
    dataset_meta: Dict[str, Any] = Field(default_factory=dict)


class BuildMetadata(BaseModel):
    """Build metadata schema."""

    model: ModelBuildMetadata = Field(default_factory=ModelBuildMetadata)
    dataset: DatasetBuildMetadata = Field(default_factory=DatasetBuildMetadata)


class Metadata(BaseModel):
    """Metadata schema."""

    user_defined: Dict[str, Any] = Field(default_factory=dict)
    build_metadata: BuildMetadata = Field(default_factory=BuildMetadata)


class Machine(BaseModel):
    """Machine schema."""

    name: str
    project_name: str
    model: Dict[str, Any] = Field(...)
    dataset: Dict[str, Any] = Field(...)
    metadata: Metadata = Field(default_factory=Metadata)
    runtime: Dict[str, Any] = Field(default_factory=dict)
    evaluation: Optional[Dict[str, Any]] = Field(default={"cv_mode": "full_build"})
