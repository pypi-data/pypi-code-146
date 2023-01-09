from __future__ import annotations

import datetime
import json
import typing as t

import numpy as np
import pandas as pd
import pyarrow as pa

from sarus_data_spec.base import Base
from sarus_data_spec.constants import (
    ARRAY_VALUES,
    DATA,
    LIST_VALUES,
    OPTIONAL_VALUE,
    PUBLIC,
    TEXT_CHARSET,
    TEXT_MAX_LENGTH,
    USER_COLUMN,
    WEIGHTS,
)
from sarus_data_spec.path import Path
from sarus_data_spec.predicate import Predicate
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

try:
    import tensorflow as tf
except ModuleNotFoundError:
    pass


DURATION_UNITS_TO_RANGE = {
    'us': (
        int(np.iinfo(np.int64).min / 1e3),
        int(np.iinfo(np.int64).max / 1e3),
    ),
    'ms': (
        int(np.iinfo(np.int64).min / 1e6),
        int(np.iinfo(np.int64).max / 1e6),
    ),
    's': (
        int(np.iinfo(np.int64).min / 1e9),
        int(np.iinfo(np.int64).max / 1e9),
    ),
}


class Type(Base[sp.Type]):
    """A python class to describe types"""

    def prototype(self) -> t.Type[sp.Type]:
        """Return the type of the underlying protobuf."""
        return sp.Type

    def name(self) -> str:
        """Returns the name of the underlying protobuf."""
        return self.protobuf().name

    def has_protected_format(self) -> bool:
        """Return True if the Type has the protected formalism."""
        protected_fields = {
            PUBLIC,
            USER_COLUMN,
            WEIGHTS,
            DATA,
        }

        type = self.protobuf()
        if type.HasField('struct'):
            field_names = {element.name for element in type.struct.fields}
            return field_names == protected_fields
        else:
            return False

    def data_type(self) -> Type:
        """Returns the first type level containing the data,
        hence skips the protected_entity struct if there is one"""
        if self.has_protected_format():
            data_type = next(
                iter(
                    [
                        field.type
                        for field in self.protobuf().struct.fields
                        if field.name == DATA
                    ]
                ),
                None,
            )
            assert data_type
            return Type(data_type)
        else:
            return self

    # A Visitor acceptor
    def accept(self, visitor: st.TypeVisitor) -> None:
        dispatch: t.Callable[[], None] = {
            'null': lambda: visitor.Null(properties=self._protobuf.properties),
            'unit': lambda: visitor.Unit(properties=self._protobuf.properties),
            'boolean': lambda: visitor.Boolean(
                properties=self._protobuf.properties
            ),
            'integer': lambda: visitor.Integer(
                min=self._protobuf.integer.min,
                max=self._protobuf.integer.max,
                base=st.IntegerBase(self._protobuf.integer.base),
                possible_values=self._protobuf.integer.possible_values,
                properties=self._protobuf.properties,
            ),
            'id': lambda: visitor.Id(
                base=st.IdBase(self._protobuf.id.base),
                unique=self._protobuf.id.unique,
                reference=Path(self._protobuf.id.reference)
                if self._protobuf.id.reference != sp.Path()
                else None,
                properties=self._protobuf.properties,
            ),
            'enum': lambda: visitor.Enum(
                self._protobuf.name,
                [
                    (name_value.name, name_value.value)
                    for name_value in self._protobuf.enum.name_values
                ],
                self._protobuf.enum.ordered,
                properties=self._protobuf.properties,
            ),
            'float': lambda: visitor.Float(
                min=self._protobuf.float.min,
                max=self._protobuf.float.max,
                base=st.FloatBase(self._protobuf.float.base),
                possible_values=self._protobuf.float.possible_values,
                properties=self._protobuf.properties,
            ),
            'text': lambda: visitor.Text(
                self._protobuf.text.encoding,
                possible_values=self._protobuf.text.possible_values,
                properties=self._protobuf.properties,
            ),
            'bytes': lambda: visitor.Bytes(
                properties=self._protobuf.properties
            ),
            'struct': lambda: visitor.Struct(
                {
                    field.name: Type(field.type)
                    for field in self._protobuf.struct.fields
                },
                name=None
                if self._protobuf.name == ''
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            'union': lambda: visitor.Union(
                {
                    field.name: Type(field.type)
                    for field in self._protobuf.union.fields
                },
                name=None
                if self._protobuf.name == ''
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            'optional': lambda: visitor.Optional(
                Type(self._protobuf.optional.type),
                None if self._protobuf.name == '' else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            'list': lambda: visitor.List(
                Type(self._protobuf.list.type),
                max_size=self._protobuf.list.max_size,
                name=None
                if self._protobuf.name == ''
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            'array': lambda: visitor.Array(
                Type(self._protobuf.array.type),
                tuple(self._protobuf.array.shape),
                None if self._protobuf.name == '' else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            'datetime': lambda: visitor.Datetime(
                self._protobuf.datetime.format,
                self._protobuf.datetime.min,
                self._protobuf.datetime.max,
                st.DatetimeBase(self._protobuf.datetime.base),
                possible_values=self._protobuf.datetime.possible_values,
                properties=self._protobuf.properties,
            ),
            'date': lambda: visitor.Date(
                self._protobuf.date.format,
                self._protobuf.date.min,
                self._protobuf.date.max,
                st.DateBase(self._protobuf.date.base),
                possible_values=self._protobuf.date.possible_values,
                properties=self._protobuf.properties,
            ),
            'time': lambda: visitor.Time(
                self._protobuf.time.format,
                self._protobuf.time.min,
                self._protobuf.time.max,
                st.TimeBase(self._protobuf.time.base),
                possible_values=self._protobuf.time.possible_values,
                properties=self._protobuf.properties,
            ),
            'duration': lambda: visitor.Duration(
                self._protobuf.duration.unit,
                self._protobuf.duration.min,
                self._protobuf.duration.max,
                possible_values=self._protobuf.duration.possible_values,
                properties=self._protobuf.properties,
            ),
            'constrained': lambda: visitor.Constrained(
                Type(self._protobuf.constrained.type),
                Predicate(self._protobuf.constrained.constraint),
                None if self._protobuf.name == '' else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            'hypothesis': lambda: visitor.Hypothesis(
                *[
                    (Type(scored.type), scored.score)
                    for scored in self._protobuf.hypothesis.types
                ],
                name=None
                if self._protobuf.name == ''
                else self._protobuf.name,
                properties=self._protobuf.properties,
            ),
            None: lambda: None,
        }[self._protobuf.WhichOneof('type')]
        dispatch()

    def latex(self: st.Type, parenthesized: bool = False) -> str:
        """return a latex representation of the type"""

        class Latex(st.TypeVisitor):
            result: str = ''

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'\emptyset'

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'\mathbb{1}'

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'\left\{0,1\right}'

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if (
                    min <= np.iinfo(np.int32).min
                    or max >= np.iinfo(np.int32).max
                ):
                    self.result = r'\mathbb{N}'
                else:
                    self.result = (
                        r'\left[' + str(min) + r'..' + str(max) + r'\right]'
                    )

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(name_values) > 3:
                    self.result = r'\left\{'
                    for name, _ in name_values[:2]:
                        self.result += r'\text{' + name + r'}, '
                    self.result += r',\ldots, '
                    for name, _ in name_values[-1:]:
                        self.result += r'\text{' + name + r'}, '
                    self.result = self.result[:-2] + r'\right\}'
                elif len(name_values) > 0:
                    self.result = r'\left\{'
                    for name, _ in name_values:
                        self.result += r'\text{' + name + r'}, '
                    self.result = self.result[:-2] + r'\right\}'
                else:
                    self.Unit()

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if (
                    min <= np.finfo(np.float32).min
                    or max >= np.finfo(np.float32).max
                ):
                    self.result = r'\mathbb{R}'
                else:
                    self.result = (
                        r'\left[' + str(min) + r', ' + str(max) + r'\right]'
                    )

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'\text{Text}'

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'\text{Bytes}'

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(fields) > 0:
                    if name is None:
                        self.result = r'\left\{'
                    else:
                        self.result = r'\text{' + name + r'}: \left\{'
                    for type_name, type in fields.items():
                        self.result = (
                            self.result
                            + r'\text{'
                            + type_name
                            + r'}:'
                            + Type.latex(type, parenthesized=True)
                            + r', '
                        )
                    self.result = self.result[:-2] + r'\right\}'
                else:
                    self.Unit()

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(fields) > 0:
                    for type in fields.values():
                        self.result = (
                            self.result
                            + Type.latex(type, parenthesized=True)
                            + r' | '
                        )
                    self.result = self.result[:-2]
                    if parenthesized:
                        self.result = r'\left(' + self.result + r'\right)'
                else:
                    self.Null()

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = Type.latex(type, parenthesized=True) + r'?'

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if max_size < 100:
                    self.result = (
                        Type.latex(type, parenthesized=True)
                        + r'^{'
                        + str(max_size)
                        + r'}'
                    )
                else:
                    self.result = Type.latex(type, parenthesized=True) + r'^*'

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = (
                    Type.latex(type)
                    + r'^{'
                    + r'\times '.join([str(i) for i in shape])
                    + r'}'
                )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'\text{Datetime}'

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'\text{Date}'

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'\text{Time}'

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'\text{Duration}'

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(types) > 0:
                    for type, score in types:
                        self.result = (
                            self.result
                            + Type.latex(type, parenthesized=True)
                            + f',{score}|'
                        )
                    self.result = self.result[:-2]
                    self.result = r'\langle' + self.result + r'\rangle'
                else:
                    self.Null()

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r''

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r''

        visitor = Latex()
        self.accept(visitor)
        return visitor.result

    def compact(self: st.Type, parenthesized: bool = False) -> str:
        """return a compact representation of the type"""

        class Compact(st.TypeVisitor):
            result: str = ''

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'∅'
                self.result = r'∅'

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'𝟙'

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'𝔹'

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if (
                    min <= np.iinfo(np.int32).min
                    or max >= np.iinfo(np.int32).max
                ):
                    self.result = r'ℕ'
                else:
                    self.result = r'[' + str(min) + r'..' + str(max) + r']'

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(name_values) > 3:
                    self.result = r'{'
                    for name, _ in name_values[:2]:
                        self.result += name
                    self.result += r',..., '
                    for name, _ in name_values[-1:]:
                        self.result += name + r', '
                    self.result = self.result[:-2] + r'}'
                elif len(name_values) > 0:
                    self.result = r'{'
                    for name, _ in name_values:
                        self.result += name + r', '
                    self.result = self.result[:-2] + r'}'
                else:
                    self.Unit()

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if (
                    min <= np.finfo(np.float32).min
                    or max >= np.finfo(np.float32).max
                ):
                    self.result = r'ℝ'
                else:
                    self.result = r'[' + str(min) + r', ' + str(max) + r']'

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'𝒯'

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = r'ℬ'

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(fields) > 0:
                    if name is None:
                        self.result = '{'
                    else:
                        self.result = name + r': {'
                    for type_name, type in fields.items():
                        self.result = (
                            self.result
                            + type_name
                            + r': '
                            + Type.compact(type, parenthesized=True)
                            + r', '
                        )
                    self.result = self.result[:-2] + r'}'
                else:
                    self.Unit()

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(fields) > 0:
                    for type in fields.values():
                        self.result = (
                            self.result
                            + Type.compact(type, parenthesized=True)
                            + r' | '
                        )
                    self.result = self.result[:-2]
                    if parenthesized:
                        self.result = r'(' + self.result + r')'
                else:
                    self.Null()

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = Type.compact(type, parenthesized=True) + r'?'

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = Type.compact(type, parenthesized=True) + r'*'

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = (
                    Type.compact(type)
                    + r'**('
                    + r'x'.join([str(i) for i in shape])
                    + r')'
                )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'𝒟𝓉'

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'𝒟𝒶'

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'𝒯𝓂'

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r'𝒟𝓊'

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if len(types) > 0:
                    self.result = r'<'
                    for type, score in types:
                        self.result = (
                            self.result
                            + Type.compact(type, parenthesized=False)
                            + f',{score}|'
                        )
                    self.result = self.result[:-1] + r'>'
                else:
                    self.Null()

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r''

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = r''

        visitor = Compact()
        self.accept(visitor)
        return visitor.result

    def get(self: Type, item: st.Path) -> st.Type:
        """Return a projection of the considered type defined by the path.
        The projection contains all the parents types of the leaves of
        the path. If the path stops at a Union, Struct or Optional,
        it also returns that type with everything it contains."""

        class Select(st.TypeVisitor):
            result = Type(sp.Type())

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Null()

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Id(base=base, unique=unique, reference=reference)

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Unit(properties=self.properties)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Boolean()

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Integer(
                    min=min,
                    max=max,
                    possible_values=possible_values,
                    properties=self.properties,
                )

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Enum(
                    name=name,
                    name_values=name_values,
                    ordered=ordered,
                    properties=self.properties,
                )

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Float(
                    min=min,
                    max=max,
                    possible_values=possible_values,
                    properties=self.properties,
                )

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Text(
                    encoding=encoding,
                    possible_values=possible_values,
                    properties=self.properties,
                )

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Bytes()

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                new_fields = {}
                for path in proto.paths:
                    # here struct each path must have a label
                    new_fields[path.label] = fields[path.label].get(Path(path))
                self.result = Struct(
                    fields=new_fields if len(new_fields) > 0 else fields,
                    name=name if name is not None else 'Struct',
                    properties=self.properties,
                )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                new_fields = {}
                for path in proto.paths:
                    new_fields[path.label] = fields[path.label].get(Path(path))
                self.result = Union(
                    fields=new_fields if len(new_fields) > 0 else fields,
                    name=name if name is not None else 'Union',
                    properties=self.properties,
                )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:

                proto = item.protobuf()
                assert len(proto.paths) <= 1
                self.result = Optional(
                    type.get(Path(proto.paths[0]))
                    if len(proto.paths) > 0
                    else type,
                    name=t.cast(str, name),
                    properties=self.properties,
                )

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) <= 1
                self.result = List(
                    type.get(Path(proto.paths[0]))
                    if len(proto.paths) > 0
                    else type,
                    name=t.cast(str, name),
                    max_size=max_size,
                    properties=self.properties,
                )

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) <= 1
                self.result = Array(
                    type.get(Path(proto.paths[0]))
                    if len(proto.paths) > 0
                    else type,
                    name=t.cast(str, name),
                    shape=shape,
                    properties=self.properties,
                )

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Datetime(
                    format=format,
                    min=min,
                    max=max,
                    properties=self.properties,
                    base=base,
                    possible_values=possible_values,
                )

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Date(
                    format=format,
                    min=min,
                    max=max,
                    properties=self.properties,
                    base=base,
                    possible_values=possible_values,
                )

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Time(
                    format=format,
                    min=min,
                    max=max,
                    properties=self.properties,
                    base=base,
                    possible_values=possible_values,
                )

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                proto = item.protobuf()
                assert len(proto.paths) == 0
                self.result = Duration(
                    unit=unit,
                    min=min,
                    max=max,
                    properties=self.properties,
                    possible_values=possible_values,
                )

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:

                # TODO
                pass

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

        visitor = Select(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def sub_types(self: Type, item: st.Path) -> t.List[st.Type]:
        """Returns a list of the subtypes corresponding to the
        leaves of the input path"""

        class Select(st.TypeVisitor):
            def __init__(self, type_item: st.Type):
                self.result = [type_item]

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for sub_path in item.sub_paths():
                    result.extend(fields[sub_path.label()].sub_types(sub_path))
                if len(result) > 0:
                    self.result = result
                    # otherwise struct is empty and it is a terminal node

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for sub_path in item.sub_paths():
                    result.extend(fields[sub_path.label()].sub_types(sub_path))
                if len(result) > 0:
                    self.result = result
                    # otherwise union is empty and it is a terminal node

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:

                result = []
                if len(item.sub_paths()) == 1:
                    result.extend(type.sub_types(item.sub_paths()[0]))
                    self.result = result

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                if len(item.sub_paths()) == 1:
                    result.extend(type.sub_types(item.sub_paths()[0]))
                    self.result = result

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                if len(item.sub_paths()) == 1:
                    result.extend(type.sub_types(item.sub_paths()[0]))
                    self.result = result

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

        visitor = Select(type_item=self)
        self.accept(visitor)
        return visitor.result

    def structs(self: Type) -> t.Optional[t.List[st.Path]]:
        """Returns the path to the first level structs encountered in the type.
        For example, Union[Struct1,Union[Struct2[Struct3]] will return only a
        path that brings to Struct1 and Struct2.
        """

        class AddPath(st.TypeVisitor):
            result: t.Optional[t.List[st.Path]] = None

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = []

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                paths = []
                for type_name, curr_type in fields.items():
                    if curr_type.protobuf().WhichOneof('type') == 'struct':
                        paths.append(Path(sp.Path(label=type_name)))
                    else:
                        sub_paths = curr_type.structs()
                        if sub_paths is not None:
                            paths.extend(
                                [
                                    Path(
                                        sp.Path(
                                            label=type_name,
                                            paths=[subpath.protobuf()],
                                        )
                                    )
                                    for subpath in sub_paths
                                ]
                            )
                if len(paths) > 0:
                    self.result = t.cast(t.List[st.Path], paths)

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if type.protobuf().WhichOneof('type') == 'struct':
                    self.result = [Path(sp.Path(label=OPTIONAL_VALUE))]
                else:
                    sub_paths = type.structs()
                    if sub_paths is not None:
                        self.result = [
                            Path(
                                sp.Path(
                                    label=OPTIONAL_VALUE,
                                    paths=[
                                        subpath.protobuf()
                                        for subpath in sub_paths
                                    ],
                                )
                            )
                        ]

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if type.protobuf().WhichOneof('type') == 'struct':
                    self.result = [Path(sp.Path(label=LIST_VALUES))]
                else:
                    sub_paths = type.structs()
                    if sub_paths is not None:
                        self.result = [
                            Path(
                                sp.Path(
                                    label=LIST_VALUES,
                                    paths=[
                                        subpath.protobuf()
                                        for subpath in sub_paths
                                    ],
                                )
                            )
                        ]

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if type.protobuf().WhichOneof('type') == 'struct':
                    self.result = [Path(sp.Path(label=ARRAY_VALUES))]
                else:
                    sub_paths = type.structs()
                    if sub_paths is not None:
                        self.result = [
                            Path(
                                sp.Path(
                                    label=ARRAY_VALUES,
                                    paths=[
                                        subpath.protobuf()
                                        for subpath in sub_paths
                                    ],
                                )
                            )
                        ]

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

        visitor = AddPath()
        self.accept(visitor)
        return visitor.result

    def leaves(self: st.Type) -> t.List[st.Type]:
        """Returns a list of the sub-types corresponding to
        the leaves of the type tree structure"""

        class AddLeaves(st.TypeVisitor):
            result: t.List[st.Type] = []

            def __init__(self, type_item: st.Type):
                self.result = [type_item]

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for item_name in fields.keys():
                    result.extend(fields[item_name].leaves())
                if len(result) > 0:
                    self.result = result

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                for item_name in fields.keys():
                    result.extend(fields[item_name].leaves())
                if len(result) > 0:
                    self.result = result

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:

                result = []
                result.extend(type.leaves())
                if len(result) > 0:
                    self.result = result

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                result.extend(type.leaves())
                if len(result) > 0:
                    self.result = result

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                result = []
                result.extend(type.leaves())
                if len(result) > 0:
                    self.result = result

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

        visitor = AddLeaves(type_item=self)
        self.accept(visitor)
        return visitor.result

    def children(self: st.Type) -> t.Dict[str, st.Type]:
        """Returns the children contained in the type tree structure"""

        class GetChildren(st.TypeVisitor):
            result: t.Dict[str, st.Type] = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = t.cast(t.Dict[str, st.Type], fields)

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = t.cast(t.Dict[str, st.Type], fields)

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {OPTIONAL_VALUE: type}

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {LIST_VALUES: type}

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {ARRAY_VALUES: type}

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                pass

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                pass

        visitor = GetChildren(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def example(self) -> pa.Array:
        """This methods returns a pyarrow scalar that matches the type.
        For an optional type, we consider the case where, the field
        is not missing.
        """

        class ToArrow(st.TypeVisitor):
            result = pa.nulls(0)

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                raise NotImplementedError

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.nulls(0)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array([True], type=pa.bool_())

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if base == st.IdBase.STRING:
                    self.result = pa.array(['1'], pa.string())
                elif base == st.IdBase.INT64:
                    self.result = pa.array([1], pa.int64())
                else:
                    raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([int((min + max) / 2)], type=pa.int64())

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([name_values[0][0]], pa.string())

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([(min + max) / 2], type=pa.float64())

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                try:
                    char_set = json.loads(self.properties[TEXT_CHARSET])
                except json.JSONDecodeError:
                    self.result = pa.array([""], pa.string())
                else:
                    max_length = int(self.properties[TEXT_MAX_LENGTH])
                    ex = ''.join(char_set)
                    if len(ex) > max_length:
                        ex = ex[:max_length]
                    self.result = pa.array([ex], pa.string())

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array(
                    [bytes('1', 'utf-8')], pa.binary(length=1)
                )

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.StructArray.from_arrays(
                    arrays=[
                        field_type.example() for field_type in fields.values()
                    ],
                    names=list(fields.keys()),
                )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                n_fields = len(fields)
                arrays = []
                for j, field_type in enumerate(fields.values()):
                    middle_arr = field_type.example()
                    early_arr = pa.nulls(j, type=middle_arr.type)
                    late_arr = pa.nulls(n_fields - j - 1, type=middle_arr.type)
                    arrays.append(
                        pa.concat_arrays([early_arr, middle_arr, late_arr])
                    )
                names = list(fields.keys())
                arrays.append(pa.array(names, pa.string()))
                names.append('field_selected')
                self.result = pa.StructArray.from_arrays(
                    arrays=arrays,
                    names=names,
                )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = type.example()

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                sub_type = type.example()
                # build ListArray with one single repeated value
                self.result = pa.ListArray.from_arrays(
                    offsets=[0, 1], values=pa.concat_arrays([sub_type])
                )

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array(
                    pd.to_datetime([max], format=format), pa.timestamp('ns')
                )

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

        visitor = ToArrow(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def numpy_example(self) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it returns a non missing value of the type.
        """
        return self.example().to_numpy(zero_copy_only=False)  # type:ignore

    def tensorflow_example(self) -> t.Any:
        """This methods returns a dictionary where the leaves are
        tf tensors. For optional types, we consider the case
        where the field is not missing.
        """

        class TensorflowExample(st.TypeVisitor):
            result = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                raise NotImplementedError

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant([np.NaN], dtype=tf.float64)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant([1], dtype=tf.int64)

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if base == st.IdBase.STRING:
                    self.result = tf.constant(['1'], tf.string)
                elif base == st.IdBase.INT64:
                    self.result = tf.constant([1], tf.int64)
                else:
                    raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([int((min + max) / 2)], tf.int64)

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([name_values[0][0]], tf.string)

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([(min + max) / 2], dtype=tf.float64)

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                try:
                    char_set = json.loads(self.properties[TEXT_CHARSET])
                except json.JSONDecodeError:
                    self.result = tf.constant([""], tf.string)
                else:
                    max_length = int(self.properties[TEXT_MAX_LENGTH])
                    ex = ''.join(char_set)
                    if len(ex) > max_length:
                        ex = ex[:max_length]
                    self.result = tf.constant([ex], tf.string)

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant(['1'], tf.string)

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_example()
                    for field_name, field_type in fields.items()
                }

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_example()
                    for field_name, field_type in fields.items()
                }

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    'input_mask': tf.constant([1], dtype=tf.int64),
                    'values': type.tensorflow_example(),
                }

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = tf.constant([min], dtype=tf.string)

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

        visitor = TensorflowExample(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def default(self) -> pa.Array:
        """This methods returns a pyarrow scalar that matches the type.
        For an optional type, we consider the case where, the field
        is missing.
        """

        class Default(st.TypeVisitor):
            result = pa.nulls(0)

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                raise NotImplementedError

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.nulls(0)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array([True], type=pa.bool_())

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if base == st.IdBase.STRING:
                    self.result = pa.array(['1'], pa.string())
                elif base == st.IdBase.INT64:
                    self.result = pa.array([1], pa.int64())
                else:
                    raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([int((min + max) / 2)], type=pa.int64())

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([name_values[0][0]], pa.string())

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([(min + max) / 2], type=pa.float64())

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                try:
                    char_set = json.loads(self.properties[TEXT_CHARSET])
                except json.JSONDecodeError:
                    self.result = pa.array([""], pa.string())
                else:
                    max_length = int(self.properties[TEXT_MAX_LENGTH])
                    ex = ''.join(char_set)
                    if len(ex) > max_length:
                        ex = ex[:max_length]
                    self.result = pa.array([ex], pa.string())

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = pa.array(
                    [bytes('1', 'utf-8')], pa.binary(length=1)
                )

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.StructArray.from_arrays(
                    arrays=[
                        field_type.default() for field_type in fields.values()
                    ],
                    names=list(fields.keys()),
                )

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                n_fields = len(fields)
                arrays = []
                for j, field_type in enumerate(fields.values()):
                    middle_arr = field_type.default()
                    early_arr = pa.nulls(j, type=middle_arr.type)
                    late_arr = pa.nulls(n_fields - j - 1, type=middle_arr.type)
                    arrays.append(
                        pa.concat_arrays([early_arr, middle_arr, late_arr])
                    )
                names = list(fields.keys())
                arrays.append(pa.array(names, pa.string()))
                names.append('field_selected')
                self.result = pa.StructArray.from_arrays(
                    arrays=arrays,
                    names=names,
                )

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array([None], type=type.default().type)

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = pa.array(
                    pd.to_datetime([max], format=format), pa.timestamp('ns')
                )

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

        visitor = Default(properties=self.properties())
        self.accept(visitor)
        return visitor.result

    def numpy_default(self) -> np.ndarray:
        """Returns an example of numpy array matching the type.
        For an optional type, it sets the default missing value
        """
        return self.default().to_numpy(zero_copy_only=False)  # type:ignore

    def tensorflow_default(self, is_optional: bool = False) -> t.Any:
        """This methods returns a dictionary with tensors as leaves
        that match the type.
        For an optional type, we consider the case where the field
        is missing, and set the default value for each missing type.
        """

        class ToTensorflow(st.TypeVisitor):
            result = {}

            def __init__(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ):
                self.properties = properties if properties is not None else {}

            def Null(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                raise NotImplementedError

            def Unit(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                self.result = tf.constant([np.NaN], dtype=tf.float64)

            def Boolean(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                if is_optional:
                    self.result = tf.constant(
                        [np.iinfo(np.int64).max], dtype=tf.int64
                    )
                else:
                    self.result = tf.constant([1], dtype=tf.int64)

            def Id(
                self,
                unique: bool,
                reference: t.Optional[st.Path] = None,
                base: t.Optional[st.IdBase] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                # TODO: we should clarify for Ids, user_input
                # and so on, to be consistent
                if is_optional:
                    if base == st.IdBase.STRING:
                        self.result = tf.constant([''], dtype=tf.string)
                    elif base == st.IdBase.INT64:
                        self.result = tf.constant(
                            [np.iinfo(np.int64).max], pa.string()
                        )
                    else:
                        raise NotImplementedError
                else:
                    if base == st.IdBase.STRING:
                        self.result = tf.constant(['1'], tf.string)
                    elif base == st.IdBase.INT64:
                        self.result = tf.constant([1], tf.int64)
                    else:
                        raise NotImplementedError

            def Integer(
                self,
                min: int,
                max: int,
                base: st.IntegerBase,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant(
                        [np.iinfo(np.int64).min], dtype=tf.int64
                    )
                else:
                    self.result = tf.constant(
                        [int((min + max) / 2)], type=tf.int64
                    )

            def Enum(
                self,
                name: str,
                name_values: t.Sequence[t.Tuple[str, int]],
                ordered: bool,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([''], dtype=tf.string)
                else:
                    self.result = tf.constant([name_values[0][0]], tf.string)

            def Float(
                self,
                min: float,
                max: float,
                base: st.FloatBase,
                possible_values: t.Iterable[float],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([np.NaN], dtype=tf.float64)
                else:
                    self.result = tf.constant(
                        [(min + max) / 2], dtype=tf.float64
                    )

            def Text(
                self,
                encoding: str,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([''], dtype=tf.string)
                else:
                    try:
                        char_set = json.loads(self.properties[TEXT_CHARSET])
                    except json.JSONDecodeError:
                        self.result = tf.constant([""], tf.string)
                    else:
                        max_length = int(self.properties[TEXT_MAX_LENGTH])
                        ex = ''.join(char_set)
                        if len(ex) > max_length:
                            ex = ex[:max_length]
                        self.result = tf.constant([ex], tf.string)

            def Bytes(
                self, properties: t.Optional[t.Mapping[str, str]] = None
            ) -> None:
                if is_optional:
                    self.result = tf.constant([''], dtype=tf.string)
                else:
                    self.result = tf.constant(['1'], tf.string)

            def Struct(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_default(
                        is_optional=is_optional
                    )
                    for field_name, field_type in fields.items()
                }

            def Union(
                self,
                fields: t.Mapping[str, st.Type],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    field_name: field_type.tensorflow_default(
                        is_optional=is_optional
                    )
                    for field_name, field_type in fields.items()
                }

            def Optional(
                self,
                type: st.Type,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                self.result = {
                    'input_mask': tf.constant([0], dtype=tf.int64),
                    'values': type.tensorflow_default(is_optional=True),
                }

            def List(
                self,
                type: st.Type,
                max_size: int,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Array(
                self,
                type: st.Type,
                shape: t.Tuple[int, ...],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Datetime(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DatetimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                if is_optional:
                    self.result = tf.constant([''], dtype=tf.string)
                else:
                    self.result = tf.constant([min], dtype=tf.string)

            def Date(
                self,
                format: str,
                min: str,
                max: str,
                base: st.DateBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Time(
                self,
                format: str,
                min: str,
                max: str,
                base: st.TimeBase,
                possible_values: t.Iterable[str],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Duration(
                self,
                unit: str,
                min: int,
                max: int,
                possible_values: t.Iterable[int],
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Constrained(
                self,
                type: st.Type,
                constraint: st.Predicate,
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

            def Hypothesis(
                self,
                *types: t.Tuple[st.Type, float],
                name: t.Optional[str] = None,
                properties: t.Optional[t.Mapping[str, str]] = None,
            ) -> None:
                raise NotImplementedError

        visitor = ToTensorflow(properties=self.properties())
        self.accept(visitor)
        return visitor.result


# A few builders
def Null() -> Type:
    return Type(sp.Type(name='Null', null=sp.Type.Null()))


def Unit(properties: t.Optional[t.Mapping[str, str]] = None) -> Type:
    return Type(
        sp.Type(name='Unit', unit=sp.Type.Unit(), properties=properties)
    )


def Id(
    unique: bool,
    base: t.Optional[st.IdBase] = None,
    reference: t.Optional[st.Path] = None,
) -> Type:
    if base is None:
        base = st.IdBase.STRING
    if reference is None:
        return Type(
            sp.Type(name='Id', id=sp.Type.Id(base=base.value, unique=unique))
        )
    return Type(
        sp.Type(
            name='Id',
            id=sp.Type.Id(
                base=base.value, unique=unique, reference=reference.protobuf()
            ),
        )
    )


def Boolean() -> Type:
    return Type(sp.Type(name='Boolean', boolean=sp.Type.Boolean()))


def Integer(
    min: t.Optional[int] = None,
    max: t.Optional[int] = None,
    base: t.Optional[st.IntegerBase] = None,
    possible_values: t.Optional[t.Iterable[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if base is None:
        base = st.IntegerBase.INT64
    if min is None:
        if base == st.IntegerBase.INT64:
            min = np.iinfo(np.int64).min
        elif base == st.IntegerBase.INT32:
            min = np.iinfo(np.int32).min
        elif base == st.IntegerBase.INT16:
            min = np.iinfo(np.int16).min
        else:
            min = np.iinfo(np.int8).min
    if max is None:
        if base == st.IntegerBase.INT64:
            max = np.iinfo(np.int64).max
        elif base == st.IntegerBase.INT32:
            max = np.iinfo(np.int32).max
        elif base == st.IntegerBase.INT16:
            max = np.iinfo(np.int16).max
        else:
            max = np.iinfo(np.int8).max
    return Type(
        sp.Type(
            name='Integer',
            integer=sp.Type.Integer(
                base=base.value,
                min=min,
                max=max,
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Enum(
    name: str,
    name_values: t.Union[
        t.Sequence[str], t.Sequence[int], t.Sequence[t.Tuple[str, int]]
    ],
    ordered: bool = False,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    enum_name_values: t.List[sp.Type.Enum.NameValue]
    if len(name_values) == 0:
        raise ValueError("No enum values")
    if isinstance(name_values[0], str):
        name_values = t.cast(t.Sequence[str], name_values)
        enum_name_values = [
            sp.Type.Enum.NameValue(name=n, value=v)
            for v, n in enumerate(sorted(name_values))
        ]
    elif isinstance(name_values[0], int):
        name_values = t.cast(t.Sequence[int], name_values)
        enum_name_values = [
            sp.Type.Enum.NameValue(name=str(v), value=v)
            for v in sorted(name_values)
        ]
    elif isinstance(name_values[0], tuple):
        name_values = t.cast(t.Sequence[t.Tuple[str, int]], name_values)
        enum_name_values = [
            sp.Type.Enum.NameValue(name=n, value=v)
            for n, v in sorted(name_values)
        ]
    return Type(
        sp.Type(
            name=name,
            enum=sp.Type.Enum(
                base=sp.Type.Enum.Base.INT64,
                ordered=ordered,
                name_values=enum_name_values,
            ),
            properties=properties,
        )
    )


def Float(
    min: t.Optional[float] = np.finfo(np.float64).min,
    max: t.Optional[float] = np.finfo(np.float64).max,
    base: t.Optional[st.FloatBase] = None,
    possible_values: t.Optional[t.Iterable[float]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if base is None:
        base = st.FloatBase.FLOAT64
    if min is None:
        if base == st.FloatBase.FLOAT64:
            min = np.finfo(np.float64).min
        elif base == st.FloatBase.FLOAT32:
            min = np.finfo(np.float32).min
        else:
            min = np.finfo(np.float16).min
    if max is None:
        if base == st.FloatBase.FLOAT64:
            max = np.finfo(np.float64).max
        elif base == st.FloatBase.FLOAT32:
            max = np.finfo(np.float32).max
        else:
            max = np.finfo(np.float16).max
    return Type(
        sp.Type(
            name='Float64',
            float=sp.Type.Float(
                base=base.value,
                min=min,
                max=max,
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Text(
    encoding: str = 'UTF-8',
    possible_values: t.Optional[t.Iterable[str]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=f'Text {encoding}',
            text=sp.Type.Text(
                encoding='UTF-8', possible_values=possible_values
            ),
            properties=properties,
        )
    )


def Bytes() -> Type:
    return Type(sp.Type(name='Bytes', bytes=sp.Type.Bytes()))


def Struct(
    fields: t.Mapping[str, st.Type],
    name: str = 'Struct',
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            struct=sp.Type.Struct(
                fields=[
                    sp.Type.Struct.Field(name=name, type=type.protobuf())
                    for name, type in fields.items()
                ]
            ),
            properties=properties,
        )
    )


def Union(
    fields: t.Mapping[str, st.Type],
    name: str = 'Union',
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            union=sp.Type.Union(
                fields=[
                    sp.Type.Union.Field(
                        name=field_name, type=field_type.protobuf()
                    )
                    for field_name, field_type in fields.items()
                ]
            ),
            properties=properties,
        )
    )


def Optional(
    type: st.Type,
    name: str = 'Optional',
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            optional=sp.Type.Optional(type=type.protobuf()),
            properties=properties,
        )
    )


def List(
    type: st.Type,
    max_size: int = np.iinfo(np.int64).max,
    name: str = 'List',
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            list=sp.Type.List(type=type.protobuf(), max_size=max_size),
            properties=properties,
        )
    )


def Array(
    type: st.Type,
    shape: t.Sequence[int],
    name: str = 'Array',
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            array=sp.Type.Array(type=type.protobuf(), shape=shape),
            properties=properties,
        )
    )


def Datetime(
    format: t.Optional[str] = None,
    min: t.Optional[str] = None,
    max: t.Optional[str] = None,
    base: t.Optional[st.DatetimeBase] = None,
    possible_values: t.Optional[t.Iterable[str]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    if format is None:
        format = '%Y-%m-%dT%H:%M:%S'
    if base is None:
        base = st.DatetimeBase.INT64_NS
    assert base == st.DatetimeBase.INT64_NS
    bounds = []
    iint64 = np.iinfo(np.int64)
    for i, bound in enumerate((min, max)):
        if bound is None:  # the bound is assumed to be sound otherwise
            # This starts with the true bounds for the type datetime64[ns]
            # However, storing dates as string implies an aliasing:
            # datetime.datetime cannot be more precise than µs.
            # So this would truncate the nanoseconds:
            # ```
            # min = (min + np.timedelta64(1, "us")).astype("datetime64[us]")
            # max = max.astype("datetime64[us]")
            # ```
            # More generally, the date format can only store a bound lower
            # than that bound, which is fine with the max but not for the
            # min, as it truncates some time units.
            if i == 0:
                bound = iint64.min + 1  # iint64.min maps to 'NaT'
                aliasing = np.timedelta64(0, 'ns')
                # This looks for the lowest offset for the format:
                # see:
                # https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-and-timedelta-arithmetic
                for unit, np_unit in [
                    ("%Y", "Y"),
                    ("%m", "M"),
                    ("%d", "D"),
                    ("%H", "h"),
                    ("%M", "m"),
                    ("%S", "s"),
                    ("%f", "us"),
                ]:
                    if unit not in format:
                        break
                    elif unit in ["%m", "%Y"]:
                        # months and years have variable length
                        as_unit = np.datetime64(bound, np_unit)
                        aliasing = np.timedelta64(1, np_unit)
                        aliasing = as_unit + aliasing - as_unit
                        aliasing = aliasing.astype("timedelta64[ns]")
                    else:
                        aliasing = np.timedelta64(1, np_unit)
            elif i == 1:
                bound = iint64.max
                aliasing = np.timedelta64(0, 'ns')
            bound = str(
                (np.datetime64(bound, "ns") + aliasing).astype(
                    "datetime64[us]"
                )
            )
            bound = datetime.datetime.strptime(
                bound, '%Y-%m-%dT%H:%M:%S.%f'
            ).strftime(format)
        bounds.append(bound)

    return Type(
        sp.Type(
            name='Datetime',
            datetime=sp.Type.Datetime(
                format=format,
                min=bounds[0],
                max=bounds[1],
                base=base.value,
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Date(
    format: t.Optional[str] = None,
    min: t.Optional[str] = None,
    max: t.Optional[str] = None,
    possible_values: t.Optional[t.Iterable[str]] = None,
    base: t.Optional[st.DateBase] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    """Inspired by pyarrow.date32() type. This is compatible with
    pyarrow-pandas integration:
    https://arrow.apache.org/docs/python/pandas.html#pandas-arrow-conversion

    pyarrow.date32() and not pyarrow.date64() because the later isndefined as:
    "milliseconds since UNIX epoch 1970-01-01"
    which is a bit bizarre since there are multiple integers representing
    a single date.

    Default ranges are defined by datetime.date lowest and highest year:
    0001-01-01 and 9999-12-31. Note that if the SQL database has a date outside
    of this range the table reflection would fail since also sql alchemy is
    using datetime.date as an underlying python type.
    """

    if format is None:
        format = '%Y-%m-%d'

    if base is None:
        base = st.DateBase.INT32

    if min is None:
        min = datetime.datetime.strptime(
            str(datetime.date(datetime.MINYEAR, 1, 1)), '%Y-%m-%d'
        ).strftime(format)
    if max is None:
        max = datetime.datetime.strptime(
            str(datetime.date(datetime.MAXYEAR, 12, 31)), '%Y-%m-%d'
        ).strftime(format)

    return Type(
        sp.Type(
            name='Date',
            date=sp.Type.Date(
                format=format,
                min=min,
                max=max,
                base=base.value,
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Time(
    format: t.Optional[str] = None,
    min: t.Optional[str] = None,
    max: t.Optional[str] = None,
    possible_values: t.Optional[t.Iterable[str]] = None,
    base: t.Optional[st.TimeBase] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    """Very similar to Datetime. The difference here is that the
    range is simpler.
    """
    if format is None:
        format = '%H:%M:%S.%f'
    if base is None:
        base = st.TimeBase.INT64_US
    if base == st.TimeBase.INT64_NS:
        raise NotImplementedError(
            'time with nanoseconds resolution not supported'
        )
    if min is None:
        if base == st.TimeBase.INT64_US:
            min = '00:00:00.000000'
        else:
            min = '00:00:00.000'
    if max is None:
        if base == st.TimeBase.INT64_US:
            max = '23:59:59.999999'
        else:
            max = '23:59:59.999'

    return Type(
        sp.Type(
            name='Time',
            time=sp.Type.Time(
                format=format,
                min=min,
                max=max,
                base=base.value,
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Duration(
    unit: t.Optional[str] = None,
    min: t.Optional[int] = None,
    max: t.Optional[int] = None,
    possible_values: t.Optional[t.Iterable[int]] = None,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    """Inspired by pythons datetime.timedelta,
    It stores duration as int64 with microseconds resolution.
    If unit is provided the range is adjusted accodingly.
    Compatible with pyarrow.duration(unit). All pyarrow units are valid:
    https://arrow.apache.org/docs/python/generated/pyarrow.duration.html
    except for 'ns' because it is incompatible with SQLAlchemy types
    (backed by python's datetime.timedelta which has up to 'us' resolution)
    and it would cause problems when pushing to sql (also SQL duration
    types have up to 'us' resolution).

    It raises an error if the unit provided is not among:
    ('us','ms', 's'). Default value 'us'
    """
    if unit is None:
        unit = 'us'

    default_bounds = DURATION_UNITS_TO_RANGE.get(unit)
    if default_bounds is None:
        raise ValueError(
            f'Duration unit {unit} not recongnized'
            f'Only values in {DURATION_UNITS_TO_RANGE.keys()} are allowed'
        )

    bounds = [
        default_bounds[0] if min is None else min,
        default_bounds[1] if max is None else max,
    ]

    return Type(
        sp.Type(
            name='Duration',
            duration=sp.Type.Duration(
                unit=unit,
                min=bounds[0],
                max=bounds[1],
                possible_values=possible_values,
            ),
            properties=properties,
        )
    )


def Constrained(
    type: st.Type,
    constraint: Predicate,
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name='Constrained',
            constrained=sp.Type.Constrained(
                type=type.protobuf(), constraint=constraint._protobuf
            ),
            properties=properties,
        )
    )


def Hypothesis(
    *types: t.Tuple[st.Type, float],
    name: str = 'Hypothesis',
    properties: t.Optional[t.Mapping[str, str]] = None,
) -> Type:
    return Type(
        sp.Type(
            name=name,
            hypothesis=sp.Type.Hypothesis(
                types=(
                    sp.Type.Hypothesis.Scored(type=v.protobuf(), score=s)
                    for v, s in types
                )
            ),
            properties=properties,
        )
    )


def extract_filter_from_types(
    initial_type: st.Type, goal_type: st.Type
) -> st.Type:
    class FilterVisitor(st.TypeVisitor):
        """Visitor that select type for filtering, it only takes
        the Union types of the goal type and the rest is taken from
        the initial type
        """

        filter_type = initial_type

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the goal type
            self.filter_type = Union(
                fields={
                    field_name: extract_filter_from_types(
                        initial_type=initial_type.children()[field_name],
                        goal_type=field_type,
                    )
                    for field_name, field_type in fields.items()
                }
            )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the initial type
            self.filter_type = Struct(
                fields={
                    field_name: (
                        extract_filter_from_types(
                            initial_type=field_type,
                            goal_type=fields[field_name],
                        )
                        if fields.get(field_name) is not None
                        else field_type
                    )
                    for field_name, field_type in initial_type.children().items()  # noqa: E501
                }
            )

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here it does not change
            self.filter_type = Optional(
                type=extract_filter_from_types(
                    initial_type=initial_type.children()[OPTIONAL_VALUE],
                    goal_type=type,
                )
            )

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

    visitor = FilterVisitor()
    goal_type.accept(visitor)
    return visitor.filter_type


def extract_project_from_types(
    initial_type: st.Type, goal_type: st.Type
) -> st.Type:
    class ProjectVisitor(st.TypeVisitor):
        """Visitor that select type for projecting, it only takes
        the Project types of the goal type and the rest is taken from
        the initial type
        """

        project_type = initial_type

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the initial type
            self.project_type = Union(
                fields={
                    field_name: (
                        extract_filter_from_types(
                            initial_type=field_type,
                            goal_type=fields[field_name],
                        )
                        if fields.get(field_name) is not None
                        else field_type
                    )
                    for field_name, field_type in initial_type.children().items()  # noqa: E501
                }
            )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here select the fields in the goal type
            self.project_type = Struct(
                fields={
                    field_name: extract_project_from_types(
                        initial_type=initial_type.children()[field_name],
                        goal_type=field_type,
                    )
                    for field_name, field_type in fields.items()
                }
            )

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # here it does not change
            self.project_type = Optional(
                type=extract_filter_from_types(
                    initial_type=initial_type.children()[OPTIONAL_VALUE],
                    goal_type=type,
                )
            )

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = ProjectVisitor()
    goal_type.accept(visitor)
    return visitor.project_type


if t.TYPE_CHECKING:
    test_type: st.Type = Type(sp.Type())
