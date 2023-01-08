"""Terramare-specific metadata for attrs classes."""

import abc
import collections
import dataclasses
import logging
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import final

from .core import ConstructorCore, FactoryCore, InternalFactory
from .errors import InternalError, TerramareError, UnsupportedTargetTypeError
from .pretty_printer import LoggableTarget
from .safe_mapping import SafeMapping
from .types import Lazy, Target

METADATA_KEY = f"{__name__}.dataclass_metadata"
_METADATA_FIELD = "__terramare_terramare__"

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)
_T_in = TypeVar("_T_in")


@dataclass(frozen=True)
class MetadataError(TerramareError):
    message: str


_Metadata = TypeVar("_Metadata")
_Target = TypeVar("_Target", bound=Target[Any])


def write(target: _Target, key: str, value: Any) -> _Target:
    metadata = _read_from_target(target)
    if not metadata:
        metadata = {}
        setattr(target, _METADATA_FIELD, (metadata, target))
    metadata[key] = value
    return target


TargetMetadata = Sequence["Metadata[Any]"]


@dataclass(frozen=True)
class MetadataCollection:
    _metadata: SafeMapping[Target[Any], Mapping[str, Any]] = dataclasses.field(
        default_factory=SafeMapping
    )

    @classmethod
    def new(
        cls, metadata: Mapping[Target[Any], TargetMetadata]
    ) -> "MetadataCollection":
        return cls(
            SafeMapping(
                [
                    (
                        target,
                        {element.KEY: element.value for element in target_metadata},
                    )
                    for target, target_metadata in metadata.items()
                ]
            )
        )

    def read(
        self,
        target: Target[Any],
        key: str,
        default: _Metadata,
        *,
        field: Optional[str] = None,
    ) -> _Metadata:
        if field is not None:
            return self._read_field_metadata(target, key, default, field)
        return self._read_target_metadata(target, key, default)

    def _read_field_metadata(
        self, target: Target[Any], key: str, default: _Metadata, field: str
    ) -> _Metadata:
        field_metadata = fields.read(self, target).get(field, {})
        if key in field_metadata:
            value = cast(_Metadata, field_metadata[key].value)
            _log.debug(
                "Read metadata key '%s' for field '%s' of target %s "
                "from fields metadata: %s",
                key,
                field,
                LoggableTarget(target),
                value,
            )
            return value

        dataclass_metadata = _read_from_dataclass_field(target, field)
        if key in dataclass_metadata:
            value = cast(_Metadata, dataclass_metadata[key].value)
            _log.debug(
                "Read metadata key '%s' for field '%s' of target %s "
                "from dataclass field metadata: %s",
                key,
                field,
                LoggableTarget(target),
                value,
            )
            return value

        return default

    def _read_target_metadata(
        self, target: Target[Any], key: str, default: _Metadata
    ) -> _Metadata:
        if target in self._metadata:
            target_metadata = self._metadata[target]
            if key in target_metadata:
                value = cast(_Metadata, target_metadata[key])
                _log.debug(
                    "Read metadata key '%s' for target %s from metadata collection: %s",
                    key,
                    LoggableTarget(target),
                    value,
                )
                return value

        target_metadata = _read_from_target(target)
        if key in target_metadata:
            value = cast(_Metadata, target_metadata[key])
            _log.debug(
                "Read metadata key '%s' for target %s from target metadata: %s",
                key,
                LoggableTarget(target),
                value,
            )
            return value

        return default


class Metadata(Generic[_Metadata], abc.ABC):
    KEY: ClassVar[str]
    DEFAULT: ClassVar[_Metadata]

    @classmethod
    def read(cls, metadata: MetadataCollection, target: _Target) -> _Metadata:
        return metadata.read(target, cls.KEY, cls.DEFAULT)

    @property
    @abc.abstractmethod
    def value(self) -> _Metadata:
        ...  # pragma: no cover

    def __call__(self, target: _Target) -> _Target:
        return write(target, self.KEY, self.value)


# See https://mypy.readthedocs.io/en/latest/runtime_troubles.html#using-classes-that-are-generic-in-stubs-but-not-at-runtime.  # noqa
if TYPE_CHECKING:  # pragma: no cover
    _BaseFieldMetadata = collections.abc.Mapping[str, Any]
else:
    _BaseFieldMetadata = collections.abc.Mapping


class FieldMetadata(Generic[_Metadata], abc.ABC, _BaseFieldMetadata):
    KEY: ClassVar[str]
    DEFAULT: ClassVar[_Metadata]

    @classmethod
    def read(
        cls, metadata: MetadataCollection, target: _Target, field: str
    ) -> _Metadata:
        return metadata.read(target, cls.KEY, cls.DEFAULT, field=field)

    @property
    @abc.abstractmethod
    def value(self) -> _Metadata:
        ...  # pragma: no cover

    def __getitem__(self, key: str) -> Any:
        return self._as_dict()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._as_dict())

    def __len__(self) -> int:
        return len(self._as_dict())

    def _as_dict(self) -> Mapping[str, Any]:
        return {METADATA_KEY: self}


_FieldsMetadata = Mapping[str, Mapping[str, FieldMetadata[object]]]


@dataclass(frozen=True)
class fields(Metadata[_FieldsMetadata]):
    KEY: ClassVar[str] = f"{__name__}.fields"
    DEFAULT: ClassVar[_FieldsMetadata]

    _value: _FieldsMetadata

    def __init__(
        self,
        fields_metadata: Mapping[
            str, Union[FieldMetadata[Any], Sequence[FieldMetadata[Any]]]
        ],
    ) -> None:
        def normalize(
            field_metadata: Union[FieldMetadata[Any], Sequence[FieldMetadata[Any]]]
        ) -> Sequence[FieldMetadata[object]]:
            if isinstance(field_metadata, FieldMetadata):  # pragma: no branch TODO
                field_metadata = [field_metadata]
            return field_metadata

        value: _FieldsMetadata = {
            field: {element.KEY: element for element in normalize(field_metadata)}
            for field, field_metadata in fields_metadata.items()
        }
        object.__setattr__(self, "_value", value)

    @property
    def value(self) -> _FieldsMetadata:
        return self._value


fields.DEFAULT = {}


class _skip(FieldMetadata[bool]):
    KEY: ClassVar[str] = f"{__name__}._skip"
    DEFAULT: ClassVar[bool] = False

    @property
    def value(self) -> bool:
        return True


skip = _skip()


@dataclass(frozen=True)
class from_context(FieldMetadata[Optional[str]]):
    KEY: ClassVar[str] = f"{__name__}.from_context"
    DEFAULT: ClassVar[Optional[str]] = None

    _value: str

    @property
    def value(self) -> str:
        return self._value


@dataclass(frozen=True)
class with_(Metadata[Optional[Lazy[Callable[..., Any]]]]):
    """Construct the decorated class using the given function."""

    KEY: ClassVar[str] = f"{__name__}.with_"
    DEFAULT: ClassVar[Optional[Lazy[Callable[..., Any]]]] = None

    _value: Lazy[Callable[..., Any]]

    @property
    def value(self) -> Lazy[Callable[..., Any]]:
        return self._value


@final
@dataclass(frozen=True)
class MetadataFactory(FactoryCore):
    _metadata: MetadataCollection

    def create_constructor(
        self, factory: InternalFactory, target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        _with = with_.read(self._metadata, target)
        if _with:
            return factory.create_constructor(_with(), frame="metadata 'with'").unwrap()
        raise UnsupportedTargetTypeError


def _read_from_target(target: Target[_T_in]) -> Dict[str, Any]:
    if not hasattr(target, _METADATA_FIELD):
        return {}
    attr = getattr(target, _METADATA_FIELD)
    if not (isinstance(attr, tuple) and isinstance(attr[0], dict)):
        raise MetadataError("unexpected type metadata")
    meta, t = attr
    # Ensure that the metadata was applied to `t` itself, rather than a base
    # class of `t`.
    # This is important because the base class may define metadata that is
    # not appropriate for derived classes, such as tagged polymorphism.
    if target != t:
        return {}
    return meta


_DATACLASS_FIELDS = "__dataclass_fields__"


def _read_from_dataclass_field(
    target: Target[Any], field: str
) -> Mapping[str, FieldMetadata[Any]]:
    if not (dataclasses.is_dataclass(target) and isinstance(target, type)):
        return {}
    if not hasattr(target, _DATACLASS_FIELDS):  # pragma: no cover
        raise InternalError(f"dataclass missing '{_DATACLASS_FIELDS}' field")
    field_data: Optional[dataclasses.Field[Any]] = getattr(
        target, _DATACLASS_FIELDS
    ).get(field)
    if field_data is None:
        return {}
    if METADATA_KEY not in field_data.metadata:
        return {}
    metadata = field_data.metadata[METADATA_KEY]

    if isinstance(metadata, FieldMetadata):
        return {metadata.KEY: metadata}
    if not (
        isinstance(metadata, list)
        and all(isinstance(v, FieldMetadata) for v in metadata)
    ):
        raise MetadataError("unexpected type metadata")
    return {v.KEY: v for v in metadata}
