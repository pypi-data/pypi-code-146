"""Deserializer to construct an instance of a class type from an object."""

import logging
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

from .. import type_utils
from ..core import (
    ConstructorCore,
    ContextParameter,
    InternalConstructor,
    InternalFactory,
)
from ..data import Value
from ..errors import InternalError
from ..metadata import MetadataCollection, from_context
from ..pretty_printer import LoggableArguments, LoggableTarget
from ..types import Target
from .metadata import disallow_unknown_fields
from .utils import (
    OMIT,
    ContextField,
    Field,
    FromContextField,
    PseudoField,
    SingleField,
    SkippedField,
    TypedParameter,
    VariadicField,
    add_type_hints,
    handle_keyword_pseudo_field,
    handle_positional_pseudo_field,
    skip,
)

_log = logging.getLogger(__name__)


_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True)
class FromObjectConstructor(ConstructorCore[_T_co]):
    _positional: Sequence[PseudoField]
    _keyword: Mapping[str, Field]
    _var_keyword: Optional[InternalConstructor[Any]]
    # Variadic positional parameters are not used by this constructor.

    _target: Target[_T_co]
    _disallow_unknown_fields: bool

    @staticmethod
    def new(
        metadata: MetadataCollection, factory: InternalFactory, target: Target[_T_co]
    ) -> InternalConstructor[_T_co]:
        parameters = add_type_hints(target, type_utils.get_parameters(target))

        positional: List[PseudoField] = []

        index = 0
        while (
            parameters
            and parameters[0].is_positional_only()
            and not parameters[0].is_variadic()
        ):  # pragma: no cover
            parameter = parameters.pop(0)
            positional_field = FromObjectConstructor._new_positional_field(
                metadata, factory, target, parameter
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

        positional_only_parameters = [
            p for p in parameters if p.is_positional_only() and not p.is_variadic()
        ]
        if positional_only_parameters:  # pragma: no cover
            raise InternalError(
                f"unexpected positional-only parameters remaining: {positional_only_parameters}"
            )

        keyword: Dict[str, Field] = {}
        var_keyword = None
        while parameters:
            parameter = parameters.pop(0)
            keyword_field = FromObjectConstructor._new_keyword_field(
                metadata, factory, target, parameter
            )
            if isinstance(keyword_field, VariadicField):
                _log.debug(
                    "Created variadic constructor for keyword parameter '%s': %s",
                    parameter.name,
                    keyword_field,
                )
                var_keyword = keyword_field.constructor
            elif keyword_field:
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
            FromObjectConstructor(
                _positional=positional,
                _keyword=keyword,
                _var_keyword=var_keyword,
                _target=target,
                _disallow_unknown_fields=disallow_unknown_fields.read(metadata, target),
            ),
        )

    @staticmethod
    def _new_positional_field(
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
        elif parameter.is_context():
            return ContextField()
        elif parameter.is_required():
            raise factory.make_error(
                "cannot create from-object constructor for target with required "
                f"positional-only parameter: {parameter.name}"
            )
        else:
            # Positional parameter is optional; omit it.
            return None

    @staticmethod
    def _new_keyword_field(
        metadata: MetadataCollection,
        factory: InternalFactory,
        target: Target[_T_co],
        parameter: TypedParameter,
    ) -> Union[Field, VariadicField, None]:
        from_context_ = from_context.read(metadata, target, parameter.name)
        if skip(metadata, factory, target, parameter):
            return SkippedField(parameter.default)
        elif from_context_ is not None:
            return FromContextField.from_parameter(from_context_, parameter)
        elif parameter.is_variadic():
            # The _FromObjectConstructor doesn't use variadic positional
            # parameters.
            if parameter.is_positional():
                return None
            # The _FromObjectConstructor doesn't use variadic context
            # parameters.
            if not parameter.is_context():
                return VariadicField(
                    factory.create_constructor(
                        parameter.type_hint, frame=f'field "{parameter.name}"'
                    )
                )
            return None
        elif parameter.is_context():
            return ContextField()
        else:
            return SingleField(
                factory.create_constructor(
                    parameter.type_hint, frame=f'field "{parameter.name}"'
                ),
                parameter.is_required(),
            )

    def __call__(self, data: Value) -> _T_co:
        object_data = data.as_object()
        field: Field

        positional: List[object] = []
        for index, field in enumerate(self._positional):
            positional.append(
                handle_positional_pseudo_field(index, field, data.context)
            )

        keyword: Dict[str, object] = {}
        for name, field in self._keyword.items():
            if isinstance(field, SingleField):
                try:
                    element = object_data.pop(name)
                except KeyError:
                    if field.required:
                        raise data.make_error(
                            f"missing required field: {name}"
                        ) from None
                    _log.debug("Keyword parameter '%s' field omitted", name)
                    continue
                value = field.constructor(element)
                _log.debug("Keyword parameter '%s' using value: %s", name, value)
                keyword[name] = value
            else:
                value = handle_keyword_pseudo_field(name, field, data.context)
                if value is not OMIT:
                    keyword[name] = value

        if self._var_keyword:
            while object_data:
                name = next(iter(object_data))
                data = object_data.pop(name)
                if name in self._keyword:
                    _log.debug("Skipped shadowed variadic argument '%s'", name)
                else:
                    value = self._var_keyword(data)
                    _log.debug("Variadic positional parameter using value: %s", value)
                    keyword[name] = value

        if self._disallow_unknown_fields and object_data:
            keys_str = ", ".join(f'"{key}"' for key in object_data)
            raise data.make_error(f"unknown field(s): {keys_str}")

        _log.debug(
            "Instantiating %s with arguments: %s",
            LoggableTarget(self._target),
            LoggableArguments(positional, keyword),
        )
        return self._target(*positional, **keyword)  # type: ignore[call-arg]

    def get_children(self) -> Iterator[InternalConstructor[Any]]:
        for field in self._keyword.values():
            if isinstance(field, SingleField):
                yield field.constructor
        if self._var_keyword:
            yield self._var_keyword

    def requires_context(self) -> Iterable[ContextParameter]:
        for i, pseudo_field in enumerate(self._positional):  # pragma: no cover
            if isinstance(pseudo_field, FromContextField):
                yield ContextParameter(
                    key=pseudo_field.key,
                    type_=pseudo_field.type_,
                    parameter=str(i),
                    required=pseudo_field.required,
                )
        for name, field in self._keyword.items():
            if isinstance(field, FromContextField):
                yield ContextParameter(
                    key=field.key,
                    type_=field.type_,
                    parameter=f"'{name}'",
                    required=field.required,
                )
