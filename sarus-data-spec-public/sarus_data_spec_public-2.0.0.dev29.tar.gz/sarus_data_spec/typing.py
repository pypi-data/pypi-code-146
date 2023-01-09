"""Protocols describing common object behaviors.
"""
from __future__ import annotations

from abc import abstractmethod
import typing as t
import warnings

import pandas as pd
import pyarrow as pa

try:
    import tensorflow as tf
except ModuleNotFoundError:
    warnings.warn('tensorflow not found, tensorflow datasets not available')

try:
    import sklearn  # noqa: F401
except ModuleNotFoundError:
    warnings.warn('sklearn not found, sklearn models not available')

try:
    import pandas_profiling  # noqa: F401
except ModuleNotFoundError:
    warnings.warn('pandas_profiling not found, ProfileReport not available')

try:
    from sarus_differential_privacy.protobuf.private_query_pb2 import (
        PrivateQuery,
    )
except ModuleNotFoundError:
    warnings.warn(
        'sarus_differential_privacy not found, private_query not available'
    )

from enum import Enum
import datetime as dt

import numpy as np

from sarus_data_spec.protobuf.typing import Protobuf, ProtobufWithUUID
import sarus_data_spec.manager.typing as manager_typing
import sarus_data_spec.protobuf as sp
import sarus_data_spec.storage.typing as storage_typing

if t.TYPE_CHECKING:
    from sklearn import svm

    DataSpecValue = t.Union[pd.DataFrame, np.ndarray, svm.SVC]
else:
    DataSpecValue = t.Any
P = t.TypeVar('P', bound=Protobuf, covariant=True)


@t.runtime_checkable
class HasProtobuf(t.Protocol[P]):
    """An object backed by a protocol buffer message."""

    def protobuf(self) -> P:
        """Returns the underlying protobuf object."""
        ...

    def prototype(self) -> t.Type[P]:
        """Returns the type of protobuf."""
        ...

    def type_name(self) -> str:
        """Returns the name of the type."""
        ...

    def __getitem__(self, key: str) -> str:
        """Returns the property referred by key"""
        ...

    def properties(self) -> t.Mapping[str, str]:
        """Returns the properties"""
        ...


@t.runtime_checkable
class Value(t.Protocol):
    """An object with value semantics."""

    def __bytes__(self) -> bytes:
        ...

    def __repr__(self) -> str:
        ...

    def __str__(self) -> str:
        ...

    def __eq__(self, value: object) -> bool:
        ...

    def __hash__(self) -> int:
        ...


@t.runtime_checkable
class Frozen(t.Protocol):
    """An immutable object."""

    def _freeze(self) -> None:
        """Freeze the state of the object"""
        ...

    def _frozen(self) -> bool:
        """Check if the frozen object was left unchanged"""
        ...


PU = t.TypeVar('PU', bound=ProtobufWithUUID, covariant=True)


@t.runtime_checkable
class Referrable(HasProtobuf[PU], Frozen, t.Protocol[PU]):
    """Can be referred to by uuid."""

    def uuid(self) -> str:
        """Reference to use to refer to this object."""
        ...

    def referring(
        self, type_name: t.Optional[str] = None
    ) -> t.Collection[Referring[ProtobufWithUUID]]:
        """Referring objects pointing to this one."""
        ...

    def storage(self) -> storage_typing.Storage:
        ...

    def manager(self) -> manager_typing.Manager:
        ...


@t.runtime_checkable
class Referring(Referrable[PU], Frozen, t.Protocol[PU]):
    """Is referring to other Referrables"""

    _referred: t.MutableSet[str] = set()

    def referred(self) -> t.Collection[Referrable[ProtobufWithUUID]]:
        """Referred by this object."""
        ...


FM = t.TypeVar('FM', bound=Protobuf)


@t.runtime_checkable
class Factory(t.Protocol):
    """Can produce objects from protobuf messages"""

    def register(self, name: str, type: t.Type[HasProtobuf[Protobuf]]) -> None:
        """Registers a class"""
        ...

    def create(self, message: FM, store: bool) -> HasProtobuf[FM]:
        """Returns a wrapped protobuf"""
        ...


class VariantConstraint(Referrable[sp.VariantConstraint]):
    def constraint_kind(self) -> ConstraintKind:
        ...

    def required_context(self) -> t.List[str]:
        ...

    def privacy_limit(self) -> t.Optional[PrivacyLimit]:
        ...

    def accept(self, visitor: TransformVisitor) -> None:
        ...


# Type alias
DS = t.TypeVar('DS', bound=t.Union[sp.Scalar, sp.Dataset])


class Attribute(Referring[sp.Attribute]):
    def prototype(self) -> t.Type[sp.Attribute]:
        ...

    def name(self) -> str:
        ...


@t.runtime_checkable
class DataSpec(Referring[DS], t.Protocol):
    def parents(
        self,
    ) -> t.Tuple[t.List[DataSpec[DS]], t.Dict[str, DataSpec[DS]]]:
        ...

    def variant(
        self,
        kind: ConstraintKind,
        public_context: t.List[str],
        privacy_limit: t.Optional[PrivacyLimit] = None,
    ) -> t.Optional[DataSpec[DS]]:
        ...

    def variants(self) -> t.Collection[DataSpec]:
        ...

    def private_queries(self) -> t.List[PrivateQuery]:
        """Return the list of PrivateQueries used in a Dataspec's transform.

        It represents the privacy loss associated with the current computation.

        It can be used by Sarus when a user (Access object) reads a DP dataspec
        to update its accountant. Note that Private Query objects are generated
        with a random uuid so that even if they are submitted multiple times to
        an account, they are only accounted once (ask @cgastaud for more on
        accounting)."""
        ...

    def name(self) -> str:
        ...

    def doc(self) -> str:
        ...

    def is_pep(self) -> bool:
        ...

    def pep_token(self) -> t.Optional[str]:
        """Returns a PEP token if the dataset is PEP and None otherwise.

        The PEP token is stored in the properties of the VariantConstraint. It
        is a hash initialized with a value when the Dataset is protected.

        If a transform does not preserve the PEID then the token is set to None
        If a transform preserves the PEID assignment but changes the rows (e.g.
        sample, shuffle, filter,...) then the token's value is changed If a
        transform does not change the rows (e.g. selecting a column, adding a
        scalar,...) then the token is passed without change

        A Dataspec is PEP if its PEP token is not None. Two PEP Dataspecs are
        aligned (i.e. they have the same number of rows and all their rows have
        the same PEID) if their tokens are equal.
        """
        ...

    def is_public(self) -> bool:
        ...

    def is_transformed(self) -> bool:
        """Is the dataset composed."""
        ...

    def is_remote(self) -> bool:
        """Is the dataspec a remotely defined dataset."""
        ...

    def transform(self) -> Transform:
        ...

    def status(self, task_name: str) -> t.Optional[Status]:
        ...

    def accept(self, visitor: Visitor) -> None:
        ...

    def attribute(self, name: str) -> t.Optional[Attribute]:
        ...


class Dataset(DataSpec[sp.Dataset], t.Protocol):
    def prototype(self) -> t.Type[sp.Dataset]:
        ...

    def is_synthetic(self) -> bool:
        ...

    def is_protected(self) -> bool:
        ...

    def is_source(self) -> bool:
        ...

    def is_file(self) -> bool:
        ...

    def sources(self) -> t.Set[Dataset]:
        ...

    def schema(self) -> Schema:
        ...

    def size(self) -> t.Optional[Size]:
        ...

    def bounds(self) -> t.Optional[Bounds]:
        ...

    def marginals(self) -> t.Optional[Marginals]:
        ...

    def to_arrow(self, batch_size: int = 10000) -> t.Iterator[pa.RecordBatch]:
        ...

    async def async_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        ...

    def spec(self) -> str:
        ...

    def __iter__(self) -> t.Iterator[pa.RecordBatch]:
        ...

    def to_pandas(self) -> pd.DataFrame:
        ...

    async def async_to_pandas(self) -> pd.DataFrame:
        ...

    def to_tensorflow(self) -> tf.data.Dataset:
        ...

    async def async_to_tensorflow(self) -> tf.data.Dataset:
        ...

    def dot(self) -> str:
        """return a graphviz representation of the dataset"""
        ...

    def sql(
        self, query: str, dialect: t.Optional[SQLDialect] = None
    ) -> t.List[t.Dict[str, t.Any]]:
        """Executes the sql method on the dataset"""
        ...

    def foreign_keys(self) -> t.Dict[Path, Path]:
        """returns foreign keys of the dataset"""
        ...

    def primary_keys(self) -> t.List[Path]:
        """Returns a list of the paths to all primary keys"""
        ...

    def links(self) -> Links:
        """Returns the foreign keys
        distributions of the dataset computed
        with dp"""
        ...


class Scalar(DataSpec[sp.Scalar], t.Protocol):
    def prototype(self) -> t.Type[sp.Scalar]:
        """Return the type of the underlying protobuf."""
        ...

    def is_model(self) -> bool:
        ...

    def is_privacy_params(self) -> bool:
        """Is the scalar privacy parameters."""

    def is_random_seed(self) -> bool:
        """Is the scalar a random seed."""

    def value(self) -> DataSpecValue:
        ...

    async def async_value(self) -> DataSpecValue:
        ...

    def spec(self) -> str:
        ...


class Visitor(t.Protocol):
    """A visitor class for Dataset"""

    def all(self, visited: DataSpec) -> None:
        ...

    def transformed(
        self,
        visited: DataSpec,
        transform: Transform,
        *arguments: DataSpec,
        **named_arguments: DataSpec,
    ) -> None:
        ...

    def other(self, visited: DataSpec) -> None:
        ...


class Bounds(Referring[sp.Bounds], t.Protocol):
    """A python abstract class to describe bounds"""

    def prototype(self) -> t.Type[sp.Bounds]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset:
        ...

    def statistics(self) -> Statistics:
        ...


class Marginals(Referring[sp.Marginals], t.Protocol):
    """A python abstract class to describe marginals"""

    def prototype(self) -> t.Type[sp.Marginals]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset:
        ...

    def statistics(self) -> Statistics:
        ...


class Size(Referring[sp.Size], t.Protocol):
    """A python abstract class to describe size"""

    def prototype(self) -> t.Type[sp.Size]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset:
        ...

    def statistics(self) -> Statistics:
        ...


class Schema(Referring[sp.Schema], t.Protocol):
    """A python abstract class to describe schemas"""

    def prototype(self) -> t.Type[sp.Schema]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str:
        ...

    def dataset(self) -> Dataset:
        ...

    def to_arrow(self) -> pa.Schema:
        ...

    def type(self) -> Type:
        ...

    def is_protected(self) -> bool:
        ...

    def tables(self) -> t.List[Path]:
        ...

    def protected_path(self) -> Path:
        ...

    def data_type(self) -> Type:
        ...


class Status(Referring[sp.Status], t.Protocol):
    """A python abstract class to describe status"""

    def prototype(self) -> t.Type[sp.Status]:
        """Return the type of the underlying protobuf."""
        ...

    def dataspec(self) -> DataSpec:
        ...

    def datetime(self) -> dt.datetime:
        ...

    def update(
        self,
        task_stages: t.Optional[t.Mapping[str, Stage]],
        properties: t.Optional[t.Mapping[str, str]],
    ) -> Status:
        ...

    def task(self, task: str) -> t.Optional[Stage]:
        ...

    def pending(self) -> bool:
        ...

    def processing(self) -> bool:
        ...

    def ready(self) -> bool:
        ...

    def error(self) -> bool:
        ...

    def owner(
        self,
    ) -> manager_typing.Manager:  # TODO: Maybe find a better name, but this was shadowing the actual manager of this object.  # noqa: E501
        ...

    def clear_task(self, task: str) -> t.Optional[Status]:
        """Creates a new status removing the task specified.
        If the task does not exist, nothing is created"""


class Stage(HasProtobuf[sp.Status.Stage], t.Protocol):
    def accept(self, visitor: StageVisitor) -> None:
        ...

    def stage(self) -> str:
        ...

    def ready(self) -> bool:
        ...

    def processing(self) -> bool:
        ...

    def pending(self) -> bool:
        ...

    def error(self) -> bool:
        ...


class StageVisitor(t.Protocol):
    """A visitor class for Status/Stage"""

    def pending(self) -> None:
        ...

    def processing(self) -> None:
        ...

    def ready(self) -> None:
        ...

    def error(self) -> None:
        ...


class Transform(Referrable[sp.Transform], t.Protocol):
    """A python abstract class to describe transforms"""

    def prototype(self) -> t.Type[sp.Transform]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str:
        ...

    def doc(self) -> str:
        ...

    def spec(self) -> str:
        ...

    def is_composed(self) -> bool:
        """Is the transform composed."""
        ...

    def is_variable(self) -> bool:
        """Is the transform a variable."""
        ...

    def is_external(self) -> bool:
        """Is the transform an external operation."""
        ...

    def infer_output_type(
        self, *arguments: DataSpec, **named_arguments: DataSpec
    ) -> t.Tuple[str, t.Callable[[DataSpec], None]]:
        """Guess if the external transform output is a Dataset or a Scalar.

        Registers schema if it is a Dataset and returns the value type.
        """
        ...

    def transforms(self) -> t.Set[Transform]:
        """return all transforms (and avoid infinite recursions/loops)"""
        ...

    def variables(self) -> t.Set[Transform]:
        """Return all the variables from a composed transform"""
        ...

    def compose(
        self,
        *compose_arguments: Transform,
        **compose_named_arguments: Transform,
    ) -> Transform:
        ...

    def apply(
        self,
        *apply_arguments: DataSpec,
        **apply_named_arguments: DataSpec,
    ) -> DataSpec:
        ...

    def abstract(
        self,
        *arguments: t.Union[int, str],
        **named_arguments: t.Union[int, str],
    ) -> Transform:
        ...

    def __call__(
        self,
        *arguments: t.Union[Transform, DataSpec, int, str],
        **named_arguments: t.Union[Transform, DataSpec, int, str],
    ) -> t.Union[Transform, DataSpec]:
        """Applies the transform to another element"""
        ...

    def __mul__(self, argument: Transform) -> Transform:
        ...

    def accept(self, visitor: TransformVisitor) -> None:
        ...


class TransformVisitor(t.Protocol):
    """A visitor class for Transform"""

    def all(self, visited: Transform) -> None:
        ...

    def composed(
        self,
        visited: Transform,
        transform: Transform,
        *arguments: Transform,
        **named_arguments: Transform,
    ) -> None:
        ...

    def variable(
        self,
        visited: Transform,
        position_name: t.Union[int, str] = 0,
    ) -> None:
        ...

    def other(self, visited: Transform) -> None:
        ...


class Path(HasProtobuf[sp.Path], Frozen, Value, t.Protocol):
    """A python class to describe Paths"""

    def prototype(self) -> t.Type[sp.Path]:
        """Return the type of the underlying protobuf."""
        ...

    def to_strings_list(self) -> t.List[t.List[str]]:
        ...

    def to_dict(self) -> t.Dict[str, str]:
        ...

    def label(self) -> str:
        ...

    def sub_paths(self) -> t.List[Path]:
        ...

    def select(self, select_path: Path) -> t.List[Path]:
        ...


class Type(HasProtobuf[sp.Type], Frozen, Value, t.Protocol):
    def prototype(self) -> t.Type[sp.Type]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str:
        """Returns the name of the underlying protobuf."""
        ...

    def latex(self: Type, parenthesized: bool = False) -> str:
        """return a latex representation of the type"""
        ...

    def compact(self: Type, parenthesized: bool = False) -> str:
        """return a compact representation of the type"""
        ...

    def structs(self: Type) -> t.Optional[t.List[Path]]:
        """Returns the path to the first level structs encountered in the
        type.
        For example, Union[Struct1,Union[Struct2[Struct3]] will return only a
        path that brings to Struct1 and Struct2.
        """
        ...

    def get(self, item: Path) -> Type:
        """Return a subtype of the considered type defined by the path."""
        ...

    def leaves(self) -> t.List[Type]:
        """Returns the leaves contained in the type tree structure"""
        ...

    def children(self) -> t.Dict[str, Type]:
        """Returns the children contained in the type tree structure"""
        ...

    # A Visitor acceptor
    def accept(self, visitor: TypeVisitor) -> None:
        ...

    def sub_types(self: Type, item: Path) -> t.List[Type]:
        """Returns the terminal nodes contained in the path"""
        ...

    def default(self: Type) -> pa.Array:
        """Returns an example of arrow array matching the type.
        For an optional type, it sets the default missing value.
        """

    def numpy_default(self: Type) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it sets the default missing value
        """

    def tensorflow_default(self, is_optional: bool = False) -> t.Any:
        """This methods returns a dictionary with tensors as leaves
        that match the type. For an optional type, we consider
        the case where the field is missing, and set the default value
        for each missing type.
        """

    def example(self: Type) -> pa.Array:
        """Returns an example of arrow array matching the type.
        For an optional type, it returns a non missing
        value of the type.
        """

    def numpy_example(self: Type) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it returns a non
        missing value of the type.
        """

    def tensorflow_example(self: Type) -> t.Any:
        """Returns an example of a dictionary with tensors as leaves
        that match the type..
        For an optional type, it returns a non missing value of the type.
        """


class IdBase(Enum):
    INT64 = sp.Type.Id.INT64
    INT32 = sp.Type.Id.INT32
    INT16 = sp.Type.Id.INT16
    INT8 = sp.Type.Id.INT8
    STRING = sp.Type.Id.STRING
    BYTES = sp.Type.Id.BYTES


class DatetimeBase(Enum):
    INT64_NS = sp.Type.Datetime.INT64_NS
    INT64_MS = sp.Type.Datetime.INT64_MS
    STRING = sp.Type.Datetime.STRING


class DateBase(Enum):
    INT32 = sp.Type.Date.INT32
    STRING = sp.Type.Date.STRING


class TimeBase(Enum):
    INT64_NS = sp.Type.Time.INT64_NS
    INT64_US = sp.Type.Time.INT64_US
    INT32_MS = sp.Type.Time.INT32_MS
    STRING = sp.Type.Time.STRING


class IntegerBase(Enum):
    INT64 = sp.Type.Integer.INT64
    INT32 = sp.Type.Integer.INT32
    INT16 = sp.Type.Integer.INT16
    INT8 = sp.Type.Integer.INT8


class FloatBase(Enum):
    FLOAT64 = sp.Type.Float.FLOAT64
    FLOAT32 = sp.Type.Float.FLOAT32
    FLOAT16 = sp.Type.Float.FLOAT16


class ConstraintKind(Enum):
    SYNTHETIC = sp.ConstraintKind.SYNTHETIC
    PEP = sp.ConstraintKind.PEP
    DP = sp.ConstraintKind.DP
    PUBLIC = sp.ConstraintKind.PUBLIC


class SQLDialect(Enum):
    """SQL Dialects"""

    POSTGRES = 1
    SQL_SERVER = 2
    MY_SQL = 3
    SQLLITE = 4
    ORACLE = 5
    BIG_QUERY = 6
    REDSHIFT = 7


class InferredDistributionName(Enum):
    UNIFORM = "Uniform"
    NORMAL = "Normal"
    EXPONENTIAL = "Exponential"
    GAMMA = "Gamma"
    BETA = "Beta"
    PARETO = "Pareto"


class TypeVisitor(t.Protocol):
    """A visitor class for Type"""

    @abstractmethod
    def Null(self, properties: t.Optional[t.Mapping[str, str]] = None) -> None:
        ...

    @abstractmethod
    def Unit(self, properties: t.Optional[t.Mapping[str, str]] = None) -> None:
        ...

    @abstractmethod
    def Boolean(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None:
        ...

    @abstractmethod
    def Id(
        self,
        unique: bool,
        reference: t.Optional[Path] = None,
        base: t.Optional[IdBase] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Integer(
        self,
        min: int,
        max: int,
        base: IntegerBase,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Enum(
        self,
        name: str,
        name_values: t.Sequence[t.Tuple[str, int]],
        ordered: bool,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Float(
        self,
        min: float,
        max: float,
        base: FloatBase,
        possible_values: t.Iterable[float],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Text(
        self,
        encoding: str,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Bytes(
        self, properties: t.Optional[t.Mapping[str, str]] = None
    ) -> None:
        ...

    @abstractmethod
    def Struct(
        self,
        fields: t.Mapping[str, Type],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Union(
        self,
        fields: t.Mapping[str, Type],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Optional(
        self,
        type: Type,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def List(
        self,
        type: Type,
        max_size: int,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Array(
        self,
        type: Type,
        shape: t.Tuple[int, ...],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Datetime(
        self,
        format: str,
        min: str,
        max: str,
        base: DatetimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Time(
        self,
        format: str,
        min: str,
        max: str,
        base: TimeBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Date(
        self,
        format: str,
        min: str,
        max: str,
        base: DateBase,
        possible_values: t.Iterable[str],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Duration(
        self,
        unit: str,
        min: int,
        max: int,
        possible_values: t.Iterable[int],
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Constrained(
        self,
        type: Type,
        constraint: Predicate,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Hypothesis(
        self,
        *types: t.Tuple[Type, float],
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...


class Predicate(HasProtobuf[sp.Predicate], Frozen, Value, t.Protocol):
    """A python class to describe types"""

    def prototype(self) -> t.Type[sp.Predicate]:
        """Return the type of the underlying protobuf."""

    # A bunch of operators
    def __or__(self, predicate: Predicate) -> Predicate:
        """Union operator"""

    def __and__(self, predicate: Predicate) -> Predicate:
        """Inter operator"""

    def __invert__(self) -> Predicate:
        """Complement"""


class Statistics(HasProtobuf[sp.Statistics], Frozen, Value, t.Protocol):
    """A python class to describe statistics"""

    def prototype(self) -> t.Type[sp.Statistics]:
        """Return the type of the underlying protobuf."""
        ...

    def name(self) -> str:
        ...

    def distribution(self) -> Distribution:
        ...

    def size(self) -> int:
        ...

    def multiplicity(self) -> float:
        ...

    def accept(self, visitor: StatisticsVisitor) -> None:
        ...

    def nodes_statistics(self, path: Path) -> t.List[Statistics]:
        """Returns the List of each statistics corresponding at the leaves
        of path"""
        ...

    def children(self) -> t.Dict[str, Statistics]:
        """Returns the children contained in the type tree structure"""
        ...


class Distribution(HasProtobuf[sp.Distribution], Frozen, Value, t.Protocol):
    """A python class to describe distributions"""

    def prototype(self) -> t.Type[sp.Distribution]:
        """Return the type of the underlying protobuf."""
        ...

    def values(self) -> t.Union[t.List[float], t.List[int]]:
        ...

    def probabilities(self) -> t.List[float]:
        ...

    def names(self) -> t.Union[t.List[bool], t.List[str]]:
        ...

    def min_value(self) -> t.Union[int, float]:
        ...

    def max_value(self) -> t.Union[int, float]:
        ...


class StatisticsVisitor(t.Protocol):
    """A visitor class for Statistics"""

    @abstractmethod
    def Null(self, size: int, multiplicity: float) -> None:
        ...

    @abstractmethod
    def Unit(self, size: int, multiplicity: float) -> None:
        ...

    def Boolean(
        self,
        size: int,
        multiplicity: float,
        probabilities: t.Optional[t.List[float]] = None,
        names: t.Optional[t.List[bool]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Id(self, size: int, multiplicity: float) -> None:
        ...

    @abstractmethod
    def Integer(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Enum(
        self,
        size: int,
        multiplicity: float,
        probabilities: t.Optional[t.List[float]] = None,
        names: t.Optional[t.List[str]] = None,
        values: t.Optional[t.List[float]] = None,
        name: str = 'Enum',
    ) -> None:
        ...

    @abstractmethod
    def Float(
        self,
        size: int,
        multiplicity: float,
        min_value: float,
        max_value: float,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[float]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Text(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        example: str = '',
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Bytes(self, size: int, multiplicity: float) -> None:
        ...

    @abstractmethod
    def Struct(
        self,
        fields: t.Mapping[str, Statistics],
        size: int,
        multiplicity: float,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Union(
        self,
        fields: t.Mapping[str, Statistics],
        size: int,
        multiplicity: float,
        name: t.Optional[str] = None,
        properties: t.Optional[t.Mapping[str, str]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Optional(
        self, statistics: Statistics, size: int, multiplicity: float
    ) -> None:
        ...

    @abstractmethod
    def List(
        self,
        statistics: Statistics,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        name: str = 'List',
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Array(
        self,
        statistics: Statistics,
        size: int,
        multiplicity: float,
        min_values: t.Optional[t.List[float]] = None,
        max_values: t.Optional[t.List[float]] = None,
        name: str = 'Array',
        probabilities: t.Optional[t.List[t.List[float]]] = None,
        values: t.Optional[t.List[t.List[float]]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Datetime(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Date(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Time(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Duration(
        self,
        size: int,
        multiplicity: float,
        min_value: int,
        max_value: int,
        probabilities: t.Optional[t.List[float]] = None,
        values: t.Optional[t.List[int]] = None,
    ) -> None:
        ...

    @abstractmethod
    def Constrained(
        self, statistics: Statistics, size: int, multiplicity: float
    ) -> None:
        ...


class InferredDistribution(t.Protocol):
    """A python class to to infer user input distribution

    Attributes:
        nparams: number of parameters
    """

    nparams: int

    def estimate_params(self, x: np.ndarray) -> None:
        """estimate distribution parameters (non-DP) from data column"""
        ...

    def log_likelihood(self, x: np.ndarray) -> float:
        """compute log-likelihood of the distribution on data column"""
        ...

    def preprocess(self, x: np.ndarray) -> np.ndarray:
        """Shift/scale data to be able to estimate distribution parameters"""
        ...

    def params(self) -> t.Mapping[str, float]:
        """return distribution parameters"""
        ...


class InferredAlphabet(t.Protocol):
    """A python class to to infer user input charset

    Attributes:
        charset (t.List[int]): list with int representation of unique chars
        complexity (int): charset intervals used to generate the alphabet
            e.g. if alphabet (ascii) is [1,2,3, ..., 126] has complexity=1
            if alphabet is [1,2,3] U [10] = [1,2,3,10] has complexity=2
    """

    charset: t.List[int]
    complexity: int


T = t.TypeVar('T', covariant=True)


class ContextManagerIterator(t.Iterator[T], t.ContextManager, t.Protocol):
    ...


class Links(Referring[sp.Links], t.Protocol):
    """A python abstract class to describe all
    the links statistics in a dataset"""

    def prototype(self) -> t.Type[sp.Links]:
        """Return the type of the underlying protobuf."""
        ...

    def dataset(self) -> Dataset:
        ...

    def links_statistics(self) -> t.List[LinkStatistics]:
        ...


class LinkStatistics(HasProtobuf[sp.Links.LinkStat], t.Protocol):
    """A python class to describe the statistics of a link
    for a foreign key"""

    def prototype(self) -> t.Type[sp.Links.LinkStat]:
        """Return the type of the underlying protobuf."""
        ...

    def pointing(self) -> Path:
        """returns the path of the foreign key column"""
        ...

    def pointed(self) -> Path:
        """returns the path of the column pointed by a foreign_key"""
        ...

    def distribution(self) -> Distribution:
        """Returns the distribution of counts
        for the given pointing/pointed"""
        ...


class PrivacyLimit:
    """An abstract Privacy Limit class."""

    def delta_epsilon_dict(self) -> t.Dict[float, float]:
        """Returns the limit as a dictionnary {delta: epsilon}"""
        pass
