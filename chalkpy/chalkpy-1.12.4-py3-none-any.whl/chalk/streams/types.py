from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any, List, Sequence, Set, Type, Union

import pyarrow
from pydantic import BaseModel
from typing_extensions import TypeAlias

from chalk.features import DataFrame
from chalk.utils import AnyDataclass

if TYPE_CHECKING:
    import polars as pl


@dataclasses.dataclass
class StreamResolverParam:
    name: str


@dataclasses.dataclass
class StreamResolverParamMessage(StreamResolverParam):
    typ: Union[Type[str], Type[bytes], Type[BaseModel], AnyDataclass]


StreamResolverWindowType: TypeAlias = Union[
    Type[List[str]],
    Type[List[bytes]],
    Type[List[BaseModel]],
    Type[AnyDataclass],
    Type[pyarrow.Table],
    Type["pl.DataFrame"],
    Type[DataFrame],
    Any,  # The annotation value is likely going to be a GenericAlias, which messes with pydantic's validation
]


@dataclasses.dataclass
class StreamResolverParamMessageWindow(StreamResolverParam):
    typ: StreamResolverWindowType


@dataclasses.dataclass
class StreamResolverSignature:
    params: Sequence[StreamResolverParam]
    output_feature_fqns: Set[str]


@dataclasses.dataclass
class StreamResolverParamKeyedState(StreamResolverParam):
    typ: Union[Type[BaseModel], Type[AnyDataclass]]
    default_value: Any
