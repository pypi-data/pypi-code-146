from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Sequence


@dataclass
class UpsertFeatureIdGQL:
    fqn: str
    name: str
    namespace: str


@dataclass
class UpsertReferencePathComponentGQL:
    parent: UpsertFeatureIdGQL
    child: UpsertFeatureIdGQL
    parentToChildAttributeName: str


@dataclass
class UpsertFilterGQL:
    lhs: UpsertFeatureIdGQL
    op: str
    rhs: UpsertFeatureIdGQL


@dataclass
class UpsertDataFrameGQL:
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclass
class UpsertFeatureReferenceGQL:
    underlying: UpsertFeatureIdGQL
    path: Optional[List[UpsertReferencePathComponentGQL]] = None


@dataclass
class UpsertHasOneKindGQL:
    join: UpsertFilterGQL


@dataclass
class UpsertHasManyKindGQL:
    join: UpsertFilterGQL
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclass
class UpsertScalarKindGQL:
    scalarKind: str
    primary: bool
    baseClasses: List[str]
    version: Optional[int]
    hasEncoderAndDecoder: bool = False


@dataclass
class UpsertFeatureTimeKindGQL:
    format: Optional[str] = None


@dataclass
class UpsertFeatureGQL:
    id: UpsertFeatureIdGQL

    scalarKind: Optional[UpsertScalarKindGQL] = None
    hasManyKind: Optional[UpsertHasManyKindGQL] = None
    hasOneKind: Optional[UpsertHasOneKindGQL] = None
    featureTimeKind: Optional[UpsertFeatureTimeKindGQL] = None
    etlOfflineToOnline: bool = False
    windowBuckets: Optional[List[int]] = None

    tags: Optional[List[str]] = None
    maxStaleness: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None

    namespacePath: Optional[str] = None


@dataclass
class KafkaConsumerConfigGQL:
    broker: List[str]
    topic: List[str]
    sslKeystoreLocation: Optional[str]
    clientIdPrefix: Optional[str]
    groupIdPrefix: Optional[str]
    topicMetadataRefreshIntervalMs: Optional[int]
    securityProtocol: Optional[str]


@dataclass
class UpsertStreamResolverParamMessageGQL:
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None


@dataclass
class UpsertStreamResolverParamKeyedStateGQL:
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None
    defaultValue: Optional[Any] = None


@dataclass
class UpsertStreamResolverParamGQL:
    message: Optional[UpsertStreamResolverParamMessageGQL]
    state: Optional[UpsertStreamResolverParamKeyedStateGQL]


@dataclass
class UpsertStreamResolverGQL:
    fqn: str
    kind: str
    functionDefinition: str
    sourceClassName: Optional[str] = None
    sourceConfig: Optional[Any] = None
    machineType: Optional[str] = None
    environment: Optional[List[str]] = None
    output: Optional[List[UpsertFeatureIdGQL]] = None
    inputs: Optional[Sequence[UpsertStreamResolverParamGQL]] = None
    doc: Optional[str] = None


@dataclass
class UpsertResolverOutputGQL:
    features: Optional[List[UpsertFeatureIdGQL]] = None
    dataframes: Optional[List[UpsertDataFrameGQL]] = None


@dataclass
class UpsertResolverGQL:
    fqn: str
    kind: str
    functionDefinition: str
    output: UpsertResolverOutputGQL
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    cron: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machineType: Optional[str] = None


@dataclass
class UpsertSinkResolverGQL:
    fqn: str
    functionDefinition: str
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machineType: Optional[str] = None
    bufferSize: Optional[int] = None
    debounce: Optional[str] = None
    maxDelay: Optional[str] = None
    upsert: Optional[bool] = None


@dataclass
class MetadataSettings:
    name: str
    missing: str


@dataclass
class FeatureSettings:
    metadata: Optional[List[MetadataSettings]] = None


@dataclass
class ValidationSettings:
    feature: Optional[FeatureSettings] = None


@dataclass
class EnvironmentSettingsGQL:
    id: str
    runtime: Optional[str]
    requirements: Optional[str]
    dockerfile: Optional[str]
    requiresPackages: Optional[List[str]] = None


@dataclass
class ProjectSettingsGQL:
    project: str
    environments: Optional[List[EnvironmentSettingsGQL]]
    validation: Optional[ValidationSettings] = None


@dataclass
class FailedImport:
    filename: str
    module: str
    traceback: str


@dataclass
class ChalkPYInfo:
    version: str


class GraphLogSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class UpdateGraphError:
    header: str
    subheader: str
    severity: GraphLogSeverity


@dataclass
class UpsertGraphGQL:
    resolvers: Optional[List[UpsertResolverGQL]] = None
    features: Optional[List[UpsertFeatureGQL]] = None
    streams: Optional[List[UpsertStreamResolverGQL]] = None
    sinks: Optional[List[UpsertSinkResolverGQL]] = None
    config: Optional[ProjectSettingsGQL] = None
    failed: Optional[List[FailedImport]] = None
    chalkpy: Optional[ChalkPYInfo] = None
    validated: Optional[bool] = None
    errors: Optional[List[UpdateGraphError]] = None
