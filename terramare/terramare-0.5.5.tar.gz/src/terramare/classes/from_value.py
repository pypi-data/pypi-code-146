"""Deserializer to construct an instance of a class type from a value."""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, TypeVar

from .. import type_utils
from ..core import ConstructorCore, InternalConstructor, InternalFactory
from ..data import Value
from ..errors import InternalError
from ..metadata import MetadataCollection, from_context
from ..pretty_printer import LoggableArguments, LoggableTarget
from ..types import Target
from .utils import (
    OMIT,
    ContextField,
    Field,
    FromContextField,
    PseudoField,
    SingleField,
    SkippedField,
    TypedParameter,
    add_type_hints,
    handle_keyword_pseudo_field,
    handle_positional_pseudo_field,
    skip,
)

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True)
class FromValueConstructor(ConstructorCore[_T_co]):
    _positional: Sequence["Field"]
    _keyword: Mapping[str, "PseudoField"]
    # Variadic parameters are not used by this constructor.

    _target: Target[_T_co]

    def __post_init__(self) -> None:
        values = [f for f in self._positional if isinstance(f, SingleField)]
        if len(values) != 1:  # pragma: no cover
            raise InternalError(f"expected exactly one value field: {values}")

    @staticmethod
    def new(
        metadata: MetadataCollection,
        factory: InternalFactory,
        target: Target[_T_co],
    ) -> InternalConstructor[_T_co]:
        parameters = add_type_hints(target, type_utils.get_parameters(target))

        positional: List[Field] = []

        def have_value() -> bool:
            return any(isinstance(f, SingleField) for f in positional)

        index = 0
        while parameters and parameters[0].is_positional():
            parameter = parameters.pop(0)
            positional_field = FromValueConstructor._new_positional_field(
                metadata, factory, target, parameter, have_value()
            )
            if positional_field:
                _log.debug(
                    "Created field constructor for positional parameter '%s' (%d): %s",
                    parameter.name,
                    index,
                    positional_field,
                )
                positional.append(positional_field)
            else:
                _log.debug(
                    "No constructor created for positional parameter '%s' (%d): %s",
                    parameter.name,
                    index,
                    positional_field,
                )
            index += 1

        if not have_value():
            raise factory.make_error(
                "cannot create from-value constructor for "
                "target with no positional parameters"
            )

        positional_parameters = [p for p in parameters if p.is_positional()]
        if positional_parameters:  # pragma: no cover
            raise InternalError(
                f"unexpected positional parameters remaining: {positional_parameters}"
            )

        keyword: Dict[str, PseudoField] = {}
        while parameters:
            parameter = parameters.pop(0)
            keyword_field = FromValueConstructor._new_keyword_field(
                metadata, factory, target, parameter
            )
            if keyword_field:
                _log.debug(
                    "Created field constructor for keyword parameter '%s': %s",
                    parameter.name,
                    keyword_field,
                )
                keyword[parameter.name] = keyword_field
            else:
                _log.debug(
                    "No constructor created for keyword parameter '%s': %s",
                    parameter.name,
                    keyword_field,
                )

        if parameters:  # pragma: no cover
            raise InternalError(f"unexpected parameters remaining: {parameters}")

        return factory.wrap(
            target,
            FromValueConstructor(
                _positional=positional, _keyword=keyword, _target=target
            ),
        )

    @staticmethod
    def _new_positional_field(
        metadata: MetadataCollection,
        factory: InternalFactory,
        target: Target[_T_co],
        parameter: TypedParameter,
        have_value: bool,
    ) -> Optional[Field]:
        from_context_ = from_context.read(metadata, target, parameter.name)
        if skip(metadata, factory, target, parameter):
            return SkippedField(parameter.default)
        elif from_context_ is not None:
            return FromContextField.from_parameter(from_context_, parameter)
        elif parameter.is_context():
            if parameter.is_variadic():
                # The _FromValueConstructor doesn't use variadic context
                # parameters.
                return None
            return ContextField()
        elif not have_value:
            return SingleField(
                factory.create_constructor(
                    parameter.type_hint, frame=f'field "{parameter.name}"'
                ),
                parameter.is_required(),
            )
        elif parameter.is_required():
            raise factory.make_error(
                "cannot create from-value constructor for target "
                "with more than one required parameter"
            )
        # Covered, despite what 'coverage' says.
        else:  # pragma: no cover
            # Tail optional parameter; omit.
            return None

    @staticmethod
    def _new_keyword_field(
        metadata: MetadataCollection,
        factory: InternalFactory,
        target: Target[_T_co],
        parameter: TypedParameter,
    ) -> Optional[PseudoField]:
        from_context_ = from_context.read(metadata, target, parameter.name)
        if skip(metadata, factory, target, parameter):
            return SkippedField(parameter.default)
        elif from_context_ is not None:
            return FromContextField.from_parameter(from_context_, parameter)
        elif parameter.is_variadic():
            # The _FromValueConstructor doesn't use variadic parameters.
            return None
        elif parameter.is_context():
            return ContextField()
        elif parameter.is_required():
            raise factory.make_error(
                "cannot create from-value constructor for "
                "target with required keyword-only parameter"
            )
        else:
            # Keyword parameter is optional; omit it.
            return None

    def __call__(self, data: Value) -> _T_co:
        positional: List[object] = []
        for index, field in enumerate(self._positional):
            if isinstance(field, SingleField):
                value = field.constructor(data)
                _log.debug("Positional parameter %d using value: %s", index, value)
                positional.append(value)
            else:
                positional.append(
                    handle_positional_pseudo_field(index, field, data.context)
                )

        keyword: Dict[str, object] = {}
        for name, field in self._keyword.items():
            value = handle_keyword_pseudo_field(name, field, data.context)
            if value is not OMIT:
                keyword[name] = value

        _log.debug(
            "Instantiating %s with argument: %s",
            LoggableTarget(self._target),
            LoggableArguments(positional, keyword),
        )
        return self._target(*positional, **keyword)  # type: ignore[call-arg]

    def get_children(self) -> Iterator[InternalConstructor[Any]]:
        for field in self._positional:
            if isinstance(field, SingleField):
                yield field.constructor
