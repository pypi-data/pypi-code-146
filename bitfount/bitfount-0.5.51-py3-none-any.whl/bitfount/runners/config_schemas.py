"""Dataclasses to hold the configuration details for the runners."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
import os
from pathlib import Path
import re
import typing
from typing import Callable, Dict, List, Mapping, MutableMapping, Optional, Tuple, Union

import desert
from marshmallow import ValidationError, fields, validate
from marshmallow.validate import OneOf
from marshmallow_union import Union as M_Union

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
    _get_environment,
)
from bitfount.data.types import (
    DataPathModifiers,
    SchemaOverrideMapping,
    _SemanticTypeValue,
)
from bitfount.federated.authorisation_checkers import (
    DEFAULT_IDENTITY_VERIFICATION_METHOD,
    IDENTITY_VERIFICATION_METHODS,
)
from bitfount.federated.privacy.differential import DPModellerConfig, DPPodConfig
from bitfount.federated.transport.config import (
    _DEV_MESSAGE_SERVICE_PORT,
    _DEV_MESSAGE_SERVICE_TLS,
    _DEV_MESSAGE_SERVICE_URL,
    _STAGING_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.hub.authentication_handlers import _DEFAULT_USERNAME
from bitfount.hub.types import (
    _DEV_AM_URL,
    _DEV_HUB_URL,
    _DEV_IDP_URL,
    _PRODUCTION_IDP_URL,
    _STAGING_AM_URL,
    _STAGING_HUB_URL,
    _STAGING_IDP_URL,
    PRODUCTION_AM_URL,
    PRODUCTION_HUB_URL,
)
from bitfount.models.base_models import (
    EarlyStopping,
    LoggerConfig,
    Optimizer,
    Scheduler,
)
from bitfount.types import _JSONDict

logger = logging.getLogger(__name__)

# POD_NAME_REGEX = re.compile(r"[a-z\d]+(-[a-z\d]+)*")
# USERNAME_REGEX = re.compile(r"[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}")
# TODO: [BIT-1493] revert to regex above to disallow underscores
POD_NAME_REGEX = re.compile(r"[a-z\d]+((-|_)[a-z\d]+)*")
USERNAME_REGEX = re.compile(r"[a-z\d](?:[a-z\d]|(-|_)(?=[a-z\d])){0,38}")


def _deserialize_path(
    path: Optional[str], context: Dict[str, typing.Any]
) -> Optional[Path]:
    """Converts a str into a Path.

    If the input is None, the output is None.

    If the path to the config file is supplied in the `context` dict (in the
    "config_path" key) then any relative paths will be resolved relative to the
    directory containing the config file.
    """
    if path is None:
        return None

    ppath = Path(path)

    # If relative path, use relative to config file if present
    if not ppath.is_absolute() and "config_path" in context:
        config_dir = Path(context["config_path"]).parent
        orig_ppath = ppath
        ppath = config_dir.joinpath(ppath).resolve()
        logger.debug(
            f"Making relative paths relative to {config_dir}: {orig_ppath} -> {ppath}"
        )

    return ppath.expanduser()


def _deserialize_model_ref(ref: str) -> Union[Path, str]:
    """Deserializes a model reference.

    If the reference is a path to a file (and that file exists), return a Path
    instance. Otherwise, returns the str reference unchanged.
    """
    path = Path(ref).expanduser()
    if path.is_file():  # also returns False if path doesn't exist
        return path
    else:
        return ref


# COMMON SCHEMAS
@dataclass
class AccessManagerConfig:
    """Configuration for the access manager."""

    url: str = desert.field(fields.URL(), default=PRODUCTION_AM_URL)


@dataclass
class HubConfig:
    """Configuration for the hub."""

    url: str = desert.field(fields.URL(), default=PRODUCTION_HUB_URL)


@dataclass
class APIKeys:
    """API keys for BitfountSession."""

    access_key_id: str = desert.field(fields.String())
    access_key: str = desert.field(fields.String())


@dataclass
class JWT:
    """Externally managed JWT for BitfountSession."""

    jwt: str = desert.field(fields.String())
    expires: datetime = desert.field(fields.DateTime())
    get_token: Callable[[], Tuple[str, datetime]] = desert.field(fields.Function())


# MODELLER SCHEMAS
@dataclass
class ModellerUserConfig:
    """Configuration for the modeller.

    Args:
        username: The username of the modeller. This can be picked up automatically
            from the session but can be overridden here.
        identity_verification_method: The method to use for identity verification.
            Accepts one of the values in `IDENTITY_VERIFICATION_METHODS`, i.e. one of
            `key-based`, `saml`, `oidc-auth-code` or `oidc-device-code`.
        private_key_file: The path to the private key file for key-based identity
            verification.
    """

    username: str = desert.field(
        fields.String(validate=validate.Regexp(USERNAME_REGEX)),
        default=_DEFAULT_USERNAME,
    )

    identity_verification_method: str = desert.field(
        fields.String(validate=OneOf(IDENTITY_VERIFICATION_METHODS)),
        default=DEFAULT_IDENTITY_VERIFICATION_METHOD,
    )
    private_key_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )

    def __post_init__(self) -> None:
        environment = _get_environment()
        self._identity_provider_url: str

        if environment == _STAGING_ENVIRONMENT:
            self._identity_provider_url = _STAGING_IDP_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self._identity_provider_url = _DEV_IDP_URL
        else:
            self._identity_provider_url = _PRODUCTION_IDP_URL


@dataclass
class ModellerConfig:
    """Full configuration for the modeller."""

    pods: PodsConfig
    task: TaskConfig
    secrets: Optional[Union[APIKeys, JWT]] = desert.field(
        M_Union(
            [
                fields.Nested(desert.schema_class(APIKeys)),
                fields.Nested(desert.schema_class(JWT)),
            ]
        ),
        default=None,
    )

    modeller: ModellerUserConfig = desert.field(
        fields.Nested(desert.schema_class(ModellerUserConfig)),
        default_factory=ModellerUserConfig,
    )
    hub: HubConfig = desert.field(
        fields.Nested(desert.schema_class(HubConfig)), default_factory=HubConfig
    )
    message_service: MessageServiceConfig = desert.field(
        fields.Nested(desert.schema_class(MessageServiceConfig)),
        default_factory=MessageServiceConfig,
    )
    project_id: Optional[str] = None
    run_on_new_data_only: bool = False

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            self.hub.url = _STAGING_HUB_URL
            self.message_service.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self.hub.url = _DEV_HUB_URL
            self.message_service.url = _DEV_MESSAGE_SERVICE_URL
            self.message_service.port = _DEV_MESSAGE_SERVICE_PORT
            self.message_service.tls = _DEV_MESSAGE_SERVICE_TLS


@dataclass
class ModelStructureConfig:
    """Configuration for the ModelStructure."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )


@dataclass
class BitfountModelReferenceConfig:
    """Configuration for BitfountModelReference."""

    model_ref: Union[Path, str] = desert.field(
        fields.Function(deserialize=_deserialize_model_ref)
    )
    model_version: Optional[int] = None
    username: Optional[str] = None


@dataclass
class ModelConfig:
    """Configuration for the model."""

    # For existing models
    name: Optional[str] = None
    structure: Optional[ModelStructureConfig] = None

    # For custom models
    bitfount_model: Optional[BitfountModelReferenceConfig] = None

    # Other
    hyperparameters: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )
    logger_config: Optional[LoggerConfig] = None
    dp_config: Optional[DPModellerConfig] = None

    def __post_init__(self) -> None:
        # Validate either name or bitfount_model reference provided
        self._name_or_bitfount_model()
        try:
            self.hyperparameters["optimizer"] = Optimizer(
                **self.hyperparameters["optimizer"]
            )
        except KeyError:
            pass
        try:
            self.hyperparameters["early_stopping"] = EarlyStopping(
                **self.hyperparameters["early_stopping"]
            )
        except KeyError:
            pass
        try:
            self.hyperparameters["scheduler"] = Scheduler(
                **self.hyperparameters["scheduler"]
            )
        except KeyError:
            pass

    def _name_or_bitfount_model(self) -> None:
        """Ensures that both `name` and `bitfount_model` can't be set.

        Raises:
            ValidationError: if both `name` and `bitfount_model` are set
        """
        if self.name and self.bitfount_model:
            raise ValidationError("Cannot specify both name and bitfount_model.")
        if not self.name and not self.bitfount_model:
            raise ValidationError("Must specify either name or bitfount_model.")


@dataclass
class PodsConfig:
    """Configuration for the pods to use for the modeller."""

    identifiers: List[str]


@dataclass
class ProtocolConfig:
    """Configuration for the Protocol."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )


@dataclass
class AggregatorConfig:
    """Configuration for the Aggregator."""

    secure: bool
    weights: Optional[Dict[str, Union[int, float]]] = None

    def __post_init__(self) -> None:
        if self.secure and self.weights:
            # TODO: [BIT-1486] Remove this constraint
            raise NotImplementedError(
                "SecureAggregation does not support update weighting"
            )


@dataclass
class AlgorithmConfig:
    """Configuration for the Algorithm."""

    name: str
    arguments: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )
    pretrained_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )
    model: Optional[ModelConfig] = None


@dataclass
class TaskConfig:
    """Configuration for the task."""

    protocol: ProtocolConfig
    algorithm: Union[AlgorithmConfig, List[AlgorithmConfig]]
    data_structure: Optional[DataStructureConfig] = None
    aggregator: Optional[AggregatorConfig] = None
    transformation_file: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )


# POD SCHEMAS
@dataclass
class PodConfig:
    """Full configuration for the pod.

    Raises:
        ValueError: If a username is not provided alongside API keys.
    """

    datasource: str
    data_config: PodDataConfig
    name: str = desert.field(fields.String(validate=validate.Regexp(POD_NAME_REGEX)))
    secrets: Optional[Union[APIKeys, JWT]] = desert.field(
        M_Union(
            [
                fields.Nested(desert.schema_class(APIKeys)),
                fields.Nested(desert.schema_class(JWT)),
            ]
        ),
        default=None,
    )
    pod_details_config: Optional[PodDetailsConfig] = None
    schema: Optional[Path] = desert.field(
        fields.Function(deserialize=_deserialize_path), default=None
    )
    access_manager: AccessManagerConfig = desert.field(
        fields.Nested(desert.schema_class(AccessManagerConfig)),
        default_factory=AccessManagerConfig,
    )
    hub: HubConfig = desert.field(
        fields.Nested(desert.schema_class(HubConfig)), default_factory=HubConfig
    )
    message_service: MessageServiceConfig = desert.field(
        fields.Nested(desert.schema_class(MessageServiceConfig)),
        default_factory=MessageServiceConfig,
    )
    differential_privacy: Optional[DPPodConfig] = None
    approved_pods: Optional[List[str]] = None
    username: str = desert.field(
        fields.String(validate=validate.Regexp(USERNAME_REGEX)),
        default=_DEFAULT_USERNAME,
    )
    update_schema: bool = False
    pod_db: bool = False
    show_datapoints_with_results_in_db: bool = True

    def __post_init__(self) -> None:
        environment = _get_environment()
        if environment == _STAGING_ENVIRONMENT:
            self.hub.url = _STAGING_HUB_URL
            self.access_manager.url = _STAGING_AM_URL
            self.message_service.url = _STAGING_MESSAGE_SERVICE_URL
        elif environment == _DEVELOPMENT_ENVIRONMENT:
            self.hub.url = _DEV_HUB_URL
            self.access_manager.url = _DEV_AM_URL
            self.message_service.url = _DEV_MESSAGE_SERVICE_URL
            self.message_service.port = _DEV_MESSAGE_SERVICE_PORT
            self.message_service.tls = _DEV_MESSAGE_SERVICE_TLS

        # Use API Keys for authentication if provided
        if isinstance(self.secrets, APIKeys):
            if self.username == _DEFAULT_USERNAME:
                raise ValueError("Must specify a username when using API Keys.")

            logger.info("Setting API Keys as environment variables.")

            if os.environ.get("BITFOUNT_API_KEY_ID") or os.environ.get(
                "BITFOUNT_API_KEY"
            ):
                logger.warning(
                    "Existing environment variable API keys detected. Overriding with "
                    "those provided in the pod config."
                )
            os.environ["BITFOUNT_API_KEY_ID"] = self.secrets.access_key_id
            os.environ["BITFOUNT_API_KEY"] = self.secrets.access_key

    @property
    def pod_id(self) -> str:
        """The pod ID of the pod specified."""
        return f"{self.username}/{self.name}"


@dataclass
class PathConfig:
    """Configuration for the path."""

    path: Path = desert.field(fields.Function(deserialize=_deserialize_path))


@dataclass
class DataSplitConfig:
    """Configuration for the data splitter."""

    data_splitter: str = desert.field(
        fields.String(validate=OneOf(["percentage", "predefined"])),
        default="percentage",
    )
    args: _JSONDict = desert.field(fields.Dict(keys=fields.Str), default_factory=dict)


@dataclass
class PodDataConfig:
    """Configuration for the Schema, BaseSource and Pod.

    Args:
        force_stypes: The semantic types to force for the data. This is passed to the
            `BitfountSchema`. This should be a mapping from pod name to a mapping from
            the type to a list of column names (e.g. {"pod_name": {categorical:
            ["col1", "col2"]}}, or a mappping from each table name in a multitable
            datasource to a mapping from the type to a list of column names (e.g.
            {"table1": {categorical: ["col1", "col2"]}, "table2":  {continuous:
            ["col3", "col4"]}}.
        ignore_cols: The columns to ignore. This is passed to the data source.
        modifiers: The modifiers to apply to the data. This is passed to the
            `BaseSource`.
        datasource_args: Key-value pairs of arguments to pass to the data source
            constructor.
        data_split: The data split configuration. This is passed to the data source.
        auto_tidy: Whether to automatically tidy the data. This is used by the
            `Pod` and will result in removal of NaNs and normalisation of numeric
            values. Defaults to False.
    """

    force_stypes: Optional[
        Mapping[str, MutableMapping[_SemanticTypeValue, List[str]]]
    ] = desert.field(
        fields.Dict(
            keys=fields.String(),
            values=fields.Dict(
                keys=fields.String(validate=OneOf(typing.get_args(_SemanticTypeValue))),
                values=fields.List(fields.String()),
            ),
        ),
        default=None,
    )

    ignore_cols: Optional[Mapping[str, List[str]]] = desert.field(
        fields.Dict(keys=fields.String(), values=fields.List(fields.String())),
        default=None,
    )

    modifiers: Optional[Dict[str, DataPathModifiers]] = desert.field(
        fields.Dict(
            keys=fields.Str,
            values=fields.Dict(
                keys=fields.String(
                    validate=OneOf(DataPathModifiers.__annotations__.keys())
                )
            ),
            default=None,
        ),
        default=None,
    )
    datasource_args: _JSONDict = desert.field(
        fields.Dict(keys=fields.Str), default_factory=dict
    )
    data_split: DataSplitConfig = desert.field(
        fields.Nested(desert.schema_class(DataSplitConfig)),
        default_factory=DataSplitConfig,
    )
    auto_tidy: bool = False


@dataclass
class PodDetailsConfig:
    """Configuration for the pod details.

    Args:
        display_name: The display name of the pod.
        description: The description of the pod.
    """

    display_name: str
    description: str


@dataclass
class DataStructureSelectConfig:
    """Configuration for the datastructure select argument."""

    include: List[str] = desert.field(
        fields.List(fields.String()), default_factory=list
    )
    exclude: List[str] = desert.field(
        fields.List(fields.String()), default_factory=list
    )


@dataclass
class DataStructureAssignConfig:
    """Configuration for the datastructure assign argument."""

    target: Optional[Union[str, List[str]]] = desert.field(
        M_Union([fields.String(), fields.List(fields.String())]), default=None
    )
    image_cols: Optional[List[str]] = None
    loss_weights_col: Optional[str] = None
    multihead_col: Optional[str] = None
    ignore_classes_col: Optional[str] = None


@dataclass
class DataStructureTransformConfig:
    """Configuration for the datastructure transform argument."""

    dataset: Optional[List[Dict[str, _JSONDict]]] = None
    batch: Optional[List[Dict[str, _JSONDict]]] = None
    auto_convert_grayscale_images: bool = True


@dataclass
class DataStructureTableConfig:
    """Configuration for the datastructure table arguments."""

    table: Optional[Union[str, Dict[str, str]]] = desert.field(
        M_Union(
            [
                fields.String(),
                fields.Dict(keys=fields.String(), values=fields.String(), default=None),
            ],
            default=None,
        ),
        default=None,
    )
    query: Optional[Union[str, Dict[str, str]]] = desert.field(
        M_Union(
            [
                fields.String(),
                fields.Dict(keys=fields.String(), values=fields.String(), default=None),
            ],
            default=None,
        ),
        default=None,
    )
    schema_types_override: Optional[
        Union[SchemaOverrideMapping, Mapping[str, SchemaOverrideMapping]]
    ] = desert.field(
        fields.Dict(
            keys=fields.String(),
            values=fields.List(
                M_Union([fields.String(default=None), fields.Dict(default=None)])
            ),
            default=None,
        ),
        default=None,
    )


@dataclass
class DataStructureConfig:
    """Configuration for the modeller schema and dataset options."""

    table_config: DataStructureTableConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureTableConfig)),
    )
    assign: DataStructureAssignConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureAssignConfig)),
    )
    select: DataStructureSelectConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureSelectConfig)),
        default_factory=DataStructureSelectConfig,
    )
    transform: DataStructureTransformConfig = desert.field(
        fields.Nested(desert.schema_class(DataStructureTransformConfig)),
        default_factory=DataStructureTransformConfig,
    )
