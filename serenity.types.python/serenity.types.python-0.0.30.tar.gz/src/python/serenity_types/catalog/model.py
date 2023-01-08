from datetime import date
from enum import Enum
from typing import Dict
from uuid import UUID

from pydantic import Json

from serenity_types.utils.serialization import CamelModel


class ModelStatus(Enum):
    RECOMMENDED = 'RECOMMENDED'
    """
    Production-grade and recommended for use.
    """

    EXPERIMENTAL = 'EXPERIMENTAL'
    """
    Current experiment which may be promoted in a coming release; for testing only.
    """

    DEPRECATED = 'DEPRECATED'
    """
    No longer supported model kept in database for historical use only.
    """


class Model(CamelModel):
    """
    A risk model or other model built into Serenity. In general Models correspond to a single
    implementation in code, potentially with multiple parameterizations represented by several
    ModelConfiguration entries.
    """

    model_id: UUID
    """
    Unique ID for this particular model.
    """

    model_class_id: UUID
    """
    Unique ID for the parent ModelClass.
    """

    short_name: str
    """
    A structured name suitable for lookup keys, like risk.factor.regression.slm.
    """

    display_name: str
    """
    A human-readable name suitable for labels, like Serenity Factor Risk Model.
    """

    description: str
    """
    A longer, human-readable description suitable for tooltips and docs.
    """


class ModelClass(CamelModel):
    """
    A group of related models, like all VaR models.
    """

    model_class_id: UUID
    """
    Unique ID for this class of models.
    """

    short_name: str
    """
    A structured name suitable for lookup keys, like risk.market.
    """

    display_name: str
    """
    A human-readable name suitable for labels, like Market Risk.
    """

    description: str
    """
    A longer, human-readable description suitable for tooltips and docs.
    """


class ModelConfiguration(CamelModel):
    """
    A parameterizxation of a Model, e.g. the short, medium and long time horizon variations
    of a factor risk model.
    """

    model_config_id: UUID
    """
    Unique ID for this specific model version and parameterization.
    """

    model_id: UUID
    """
    Unique ID for the parent Model.
    """

    model_status: ModelStatus
    """
    Current status of this model, e.g. RECOMMENDED or EXPERIMENTAL.
    """

    short_name: str
    """
    A structured name suitable for lookup keys, like risk.var.parametric.normal.
    """

    display_name: str
    """
    A human-readable name suitable for labels, like Parametric VaR Model (Normal).
    """

    description: str
    """
    A longer, human-readable description suitable for tooltips and docs.
    """

    version: str
    """
    Version number, by convention following SemVer conventions.
    """

    deployment_date: date
    """
    UTC date when the config was last deployed.
    """

    training_date: date
    """
    UTC date for as-of date of training data used.
    """

    code_version: str
    """
    A GitHub commit ID, tag or other means to uniquely identify the code.
    """

    data_parameters: Dict[str, Json]
    """
    A set of name-value pairs characterizing input data.
    """

    model_parameters: Dict[str, Json]
    """
    A set of name-value pairs parameterizing the model.
    """


class ModelConfigurationSummary(CamelModel):
    """
    Summary of a particular available model configuration, suitable for external use.
    """

    model_config_id: UUID
    """
    Unique ID for this specific model version and parameterization.
    """

    model_id: UUID
    """
    Unique ID for the parent Model.
    """

    model_status: ModelStatus
    """
    Current status of this model, e.g. RECOMMENDED or EXPERIMENTAL.
    """

    short_name: str
    """
    A structured name suitable for lookup keys, like risk.var.parametric.normal.
    """

    display_name: str
    """
    A human-readable name suitable for labels, like Parametric VaR Model (Normal).
    """

    description: str
    """
    A longer, human-readable description suitable for tooltips and docs.
    """
