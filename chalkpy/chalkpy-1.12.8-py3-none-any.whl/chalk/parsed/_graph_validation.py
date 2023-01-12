import collections
from collections import defaultdict
from enum import Enum
from typing import Dict, List, Mapping, NewType

from chalk.parsed.duplicate_input_gql import (
    ProjectSettingsGQL,
    UpdateGraphError,
    UpsertFeatureGQL,
    UpsertGraphGQL,
    UpsertResolverGQL,
)
from chalk.utils.duration import parse_chalk_duration
from chalk.utils.string import oxford_comma_list, to_camel_case


class GraphLogSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class _LogBuilder:
    def __init__(self):
        self._logs: List[UpdateGraphError] = []

    def add_log(self, header: str, subheader: str, severity: GraphLogSeverity):
        self._logs.append(UpdateGraphError(header=header, subheader=subheader, severity=severity))

    def add_error(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.ERROR)

    def add_warning(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.WARNING)

    def add_info(self, header: str, subheader: str):
        self.add_log(header=header, subheader=subheader, severity=GraphLogSeverity.INFO)

    def get_logs(self) -> List[UpdateGraphError]:
        return self._logs


def _validate_primary_key(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if (
        feature.scalarKind is not None
        and feature.scalarKind.primary
        and feature.scalarKind.scalarKind
        not in [
            "str",
            "int",
        ]
    ):
        builder.add_error(
            header=f'Invalid primary key type "{feature.id.fqn}"',
            subheader=f"Primary keys must be integers or strings. "
            f'Feature "{feature.id.fqn}" has a type of {feature.scalarKind.scalarKind}',
        )


def _validate_max_staleness(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.maxStaleness is not None and feature.maxStaleness != "infinity":
        try:
            parse_chalk_duration(feature.maxStaleness)
        except:
            builder.add_error(
                header=f'Could not parse max_staleness for feature "{feature.id.fqn}"',
                subheader=f'Received "{feature.maxStaleness}". See https://docs.chalk.ai/docs/duration for valid formats.',
            )


def _validate_etl_to_online(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.etlOfflineToOnline and feature.maxStaleness is None:
        builder.add_error(
            header=f'Missing max staleness for "{feature.id.fqn}"',
            subheader=f'The feature "{feature.id.fqn}" is set to ETL to online, but doesn\'t specify a max staleness. Any ETL to online would be immediately invalidated.',
        )


def _validate_no_feature_times_as_input(
    fqn_to_feature: Mapping[str, UpsertFeatureGQL],
    resolver: UpsertResolverGQL,
    builder: _LogBuilder,
):
    for i in resolver.inputs or []:
        if i.underlying.fqn not in fqn_to_feature:
            builder.add_error(
                header=f'Resolver "{resolver.fqn}" an unknown feature {i.underlying.fqn}',
                subheader=f"""Please check the inputs to this resolver, and make sure they are all features.""",
            )
        elif fqn_to_feature[i.underlying.fqn].featureTimeKind is not None and resolver.kind != "offline":
            builder.add_error(
                header=f"Feature times cannot be accepted as input to {resolver.kind} resolvers.",
                subheader=f'The resolver "{resolver.fqn}" takes as input the\n'
                f'feature "{i.underlying.fqn}", a feature_time() type.\n'
                f"Feature times can be returned from {resolver.kind} resolvers to\n"
                "indicate data from the past, but cannot be accepted\n"
                "as inputs.",
            )


def _validate_feature_names_unique(features: List[UpsertFeatureGQL], builder: _LogBuilder):
    counter: dict[str, int] = defaultdict(lambda: 0)
    for r in features:
        counter[r.id.fqn] += 1

    for fqn, count in counter.items():
        if count > 1:
            builder.add_error(
                header="Duplicate feature names",
                subheader=f'There are {count} features with the same name of "{fqn}". All features require a '
                f"distinct name",
            )


def _validate_resolver_names_unique(resolvers: List[UpsertResolverGQL], builder: _LogBuilder):
    counter: dict[str, int] = defaultdict(lambda: 0)
    for r in resolvers:
        counter[r.fqn.split(".")[-1]] += 1

    for name, count in counter.items():
        if count > 1:
            builder.add_error(
                header="Duplicate resolver names",
                subheader=f'There are {count} resolvers with the same name of "{name}". All resolvers require a '
                f"distinct name",
            )


def _validate_offline_resolver_has_one(resolver: UpsertResolverGQL, builder: _LogBuilder):
    if resolver.kind != "offline":
        return

    for i in resolver.inputs or []:
        if i.path is not None and len(i.path) > 1:
            full_path = [i.path[0].parent.fqn]
            for p in i.path[1:]:
                full_path.append(p.child.namespace)
            full_path.append(i.path[-1].parentToChildAttributeName)
            pathname = ".".join(full_path)
            builder.add_error(
                header=f"Invalid offline resolver input",
                subheader=f"Offline resolvers cannot require nested of more than one level. "
                + f'The resolver "{resolver.fqn}" takes as input the feature "{pathname}"',
            )


def _validate_resolver_input(resolver: UpsertResolverGQL, builder: _LogBuilder):
    namespaces = set()

    for i in resolver.inputs or []:
        if i.path is not None and len(i.path) > 0:
            namespaces.add(i.path[0].parent.namespace)
        else:
            namespaces.add(i.underlying.namespace)
    namespaces = list(namespaces)
    if len(namespaces) > 1:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" requires features from multiple namespaces.',
            subheader=f"""All inputs to a resolver should be rooted in the same namespace.
The resolver "{resolver.fqn}" takes inputs in the namespaces {oxford_comma_list(namespaces)}.

If you require features from many feature classes, reference them via their relationships, such as:
  User.bank_account.title,
  User.full_name

{resolver.functionDefinition}
""",
        )


def _validate_resolver_output(resolver: UpsertResolverGQL, builder: _LogBuilder):
    output = resolver.output
    features = output.features or []
    dataframes = output.dataframes or []
    if len(features) == 0 and len(dataframes) == 0:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" does not define outputs.',
            subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
        )

    if len(dataframes) > 1:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" defines multiple DataFrames as output.',
            subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
        )

    if len(features) > 0 and len(dataframes) > 0:
        builder.add_error(
            header=f'Resolver "{resolver.fqn}" returns both relationships and scalar features.',
            subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
        )

    # Want to validate this but only have feature id instead of feature
    # if len(resolver.inputs) == 0 and len(dataframes) == 1 and len([pkey for pkey in dataframes[0].columns if pkey.primary]) != 1:
    #     builder.add_error(
    #         header=f'Resolver "{resolver.fqn}" must return a primary feature',
    #         subheader="See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.",
    #     )

    if len(features) > 0:
        namespaces = list(set(f.namespace for f in features))
        if len(namespaces) > 1:
            builder.add_error(
                header=f'Resolver "{resolver.fqn}" outputs features from multiple namespaces.',
                subheader=f"""All outputs of a resolver should be rooted in the same namespace.
The resolver "{resolver.fqn}" outputs features in the namespaces {oxford_comma_list(namespaces)}.
See https://docs.chalk.ai/docs/resolver-outputs for information about valid resolver outputs.

{resolver.functionDefinition}
""",
            )


# FIXME CHA-66 we should validate that joins are all pkey on pkey joins. no non-primary keys, no self-joins, no constants
def _validate_joins(feature: UpsertFeatureGQL, builder: _LogBuilder):
    pass


def _validate_feature_names(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.id.name.startswith("__") or feature.id.name.startswith("_chalk"):
        builder.add_error(
            header="Feature uses protected name",
            subheader=f'The feature "{feature.id.fqn}" uses the protected name "{feature.id.name}". '
            'Feature names cannot begin with "_chalk" or "__". Please rename this feature.',
        )
    if feature.id.namespace.startswith("__") or feature.id.name.startswith("_chalk"):
        builder.add_error(
            header="Feature class uses protected namespace",
            subheader=f'The feature "{feature.id.fqn}" belongs to the protected namespace "{feature.id.namespace}". '
            f'Feature namespaces cannot begin with "_chalk" or "__". Please rename this feature set.',
        )


# FIXME: This needs to check for cycles. In particular:
#   def resolve_x(id: User.id) -> DataFrame[User]
# is bogus

_BUILT_IN_SUPPORTED_TYPES = {
    "datetime",
    "date",
    "int",
    "float",
    "str",
    "bool",
    "Enum",
    "__dataclass__",
    "__attrs__",
    "__pydantic__",
}


def _validate_custom_types_have_encoders(feature: UpsertFeatureGQL, builder: _LogBuilder):
    if feature.scalarKind is None:
        return

    # FIXME: need to validate that the underlying windowed type is supported
    # i.e. right now Windowed[Foobarbaz] counts even if foobarbaz can't work
    base_classes = set(feature.scalarKind.baseClasses)
    if (
        len(base_classes & _BUILT_IN_SUPPORTED_TYPES) == 0
        and not feature.scalarKind.hasEncoderAndDecoder
        and not "CHALK_WINDOWED" in feature.scalarKind.baseClasses
    ):
        allowed = ", ".join([z.strip("_") for z in _BUILT_IN_SUPPORTED_TYPES])
        builder.add_error(
            header=f'Encoder and decoder needed for feature type "{feature.scalarKind.scalarKind}"',
            subheader=(
                f"Custom types require an encoder and decoder to be explicitly specified. At present, the following types are automatically supported: "
                f'{allowed}. The feature "{feature.id.fqn}" has unsupported type "{feature.scalarKind.scalarKind}".'
            ),
        )


def _validate_feature_metadata(
    features: List[UpsertFeatureGQL],
    builder: _LogBuilder,
    request_config: ProjectSettingsGQL,
):
    MissingMetadata = NewType("MissingMetadata", Dict[GraphLogSeverity, List[str]])

    class WrappedFeature:
        def __init__(self, feature: UpsertFeatureGQL, missing_metadata: MissingMetadata):
            self.feature = feature
            self.missing_metadata = missing_metadata

    def get_missing_metadata(feature: UpsertFeatureGQL) -> MissingMetadata:
        res = collections.defaultdict(list)
        for setting in request_config.validation.feature.metadata:
            metadata_name = setting.name
            severity = setting.missing.lower()
            if hasattr(feature, metadata_name):
                value = getattr(feature, metadata_name)
                is_missing = value is None or (isinstance(value, list) and len(value) == 0)
                if is_missing:
                    res[severity].append(metadata_name)

        return res

    def get_missing_metadata_log(wrapped_features: List[WrappedFeature], severity: GraphLogSeverity):
        if not wrapped_features:
            return None, None

        missing_messages = []
        feature_str = "feature"
        missing_metadata_str = "missing metadata"
        max_name_len = max([len(w.feature.id.name) for w in wrapped_features])
        feature_column_width = max(max_name_len, len(feature_str)) + 1
        get_padding = lambda s: feature_column_width - len(s)

        first_feature = wrapped_features[0].feature
        header = f'"{to_camel_case(first_feature.id.namespace)}" features have missing metadata'
        subheader = f"  Filepath: {first_feature.namespacePath}\n\n"

        for wrapper in wrapped_features:
            missing_metadata = wrapper.missing_metadata.get(severity)
            if not missing_metadata:
                continue
            padding_1 = get_padding(wrapper.feature.id.name)
            missing_metadata_str = ", ".join(missing_metadata)
            missing_messages.append(f"      {wrapper.feature.id.name}{' ' * padding_1}: {missing_metadata_str}")

        if not missing_messages:
            return None, None

        padding_2 = get_padding(feature_str)
        subheader += f"      {'-' * len(feature_str)}{' ' * padding_2}  {'-' * len(missing_metadata_str)}\n"
        subheader += f"      {feature_str}{' ' * padding_2}  {missing_metadata_str}\n"
        subheader += f"      {'-' * len(feature_str)}{' ' * padding_2}  {'-' * len(missing_metadata_str)}\n"
        subheader += "\n".join(missing_messages)

        return header, subheader

    def build_log_for_each_severity(wrapped_features: List[WrappedFeature]):
        if not wrapped_features:
            return

        severities = [v.value for k, v in GraphLogSeverity.__dict__.items() if not k.startswith("_")]
        for severity in severities:
            header, subheader = get_missing_metadata_log(wrapped_features=wrapped_features, severity=severity)
            if header is None:
                continue
            builder.add_log(header=header, subheader=subheader, severity=severity)

    def get_wrapped_features(
        namespace_features: List[UpsertFeatureGQL],
    ) -> List[WrappedFeature]:
        wrapped_features = []
        for nf in namespace_features:
            missing_metadata = get_missing_metadata(nf)
            if not missing_metadata:
                continue
            wrapped_features.append(WrappedFeature(feature=nf, missing_metadata=missing_metadata))

        return wrapped_features

    if not (
        request_config
        and request_config.validation
        and request_config.validation.feature
        and request_config.validation.feature.metadata
    ):
        return

    namespace_to_features = collections.defaultdict(list)
    for f in features:
        namespace_to_features[f.id.namespace].append(f)

    for namespace, ns_features in namespace_to_features.items():
        wf = get_wrapped_features(namespace_features=ns_features)
        build_log_for_each_severity(wrapped_features=wf)


def _validate_feature_metadata_config(
    features: List[UpsertFeatureGQL],
    builder: _LogBuilder,
    request_config: ProjectSettingsGQL,
):
    if not (
        request_config
        and request_config.validation
        and request_config.validation.feature
        and request_config.validation.feature.metadata
    ):
        return

    severities = [v.value for k, v in GraphLogSeverity.__dict__.items() if not k.startswith("_")]
    first_feature = features and features[0]

    for missing_metadata in request_config.validation.feature.metadata:
        metadata_name = missing_metadata.name
        severity = missing_metadata.missing

        severity_lower = severity.lower()
        try:
            GraphLogSeverity(severity_lower)
        except ValueError:
            severity_choices = '" or "'.join(severities)
            builder.add_warning(
                header=f'Found invalid log severity "{severity}" config for missing metadata',
                subheader=(
                    f'The required feature metadata "{metadata_name}" is associated with an invalid log severity "{severity}".'
                    f' Please use "{severity_choices}" in chalk.yml'
                ),
            )

        if first_feature and not hasattr(first_feature, metadata_name):
            builder.add_warning(
                header=f'Found invalid feature metadata "{metadata_name}" in config',
                subheader=(
                    f'The required metadata "{metadata_name}" is not a valid feature metadata.'
                    f" Please consider removing it from chalk.yml"
                ),
            )


def _validate_namespace_primary_key(namespace: str, features: List[UpsertFeatureGQL], builder: _LogBuilder):
    primary_features = list(f for f in features if f.scalarKind and f.scalarKind.primary)

    if len(primary_features) == 0:
        builder.add_error(
            header=f"Feature set '{namespace}' is missing a primary feature",
            subheader=f"Please add an 'int' or 'str' feature to '{namespace}', annotated with '= feature(primary=True)'",
        )
    elif len(primary_features) > 1:
        names = ", ".join([f.id.name for f in primary_features])
        builder.add_error(
            header=f"Feature set '{namespace}' has too many primary features",
            subheader=f"Found primary features: {names}. Composite primary keys are not supported. Please mark only a single feature as primary.",
        )


def validate_graph(request: UpsertGraphGQL) -> List[UpdateGraphError]:
    builder = _LogBuilder()

    # Validate the features
    _validate_feature_names_unique(request.features or [], builder)
    _validate_feature_metadata(request.features or [], builder, request.config)
    _validate_feature_metadata_config(request.features or [], builder, request.config)

    namespaces: Dict[str, List[UpsertFeatureGQL]] = defaultdict(list)

    for feature in request.features or []:
        namespaces[feature.id.namespace].append(feature)

    for namespace, features in namespaces.items():
        _validate_namespace_primary_key(namespace, features, builder)

    for feature in request.features or []:
        _validate_primary_key(feature, builder)
        _validate_max_staleness(feature, builder)
        _validate_joins(feature, builder)
        _validate_etl_to_online(feature, builder)
        _validate_feature_names(feature, builder)
        _validate_custom_types_have_encoders(feature, builder)

    # Validate the resolvers
    fqn_to_feature = {f.id.fqn: f for f in request.features or []}
    _validate_resolver_names_unique(request.resolvers or [], builder)
    for resolver in request.resolvers or []:
        _validate_offline_resolver_has_one(resolver, builder)
        _validate_resolver_input(resolver, builder)
        _validate_resolver_output(resolver, builder)
        _validate_no_feature_times_as_input(
            fqn_to_feature=fqn_to_feature,
            resolver=resolver,
            builder=builder,
        )

    return builder.get_logs()
