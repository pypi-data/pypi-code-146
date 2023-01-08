"""Deserializer to construct an instance of a class type from an array."""

import logging
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

from .. import iterator_utils, type_utils
from ..core import ConstructorCore, InternalConstructor, InternalFactory
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
class FromArrayConstructor(ConstructorCore[_T_co]):
    _positional: Sequence[Field]
    _var_positional: Optional[InternalConstructor[Any]]
    _keyword: Mapping[str, PseudoField]
    # Variadic keyword parameters are not used by this constructor.

    _target: Target[_T_co]
    _disallow_extra_elements: bool

    @staticmethod
    def new(
        metadata: MetadataCollection, factory: InternalFactory, target: Target[_T_co]
    ) -> InternalConstructor[_T_co]:
        parameters = add_type_hints(target, type_utils.get_parameters(target))

        positional: List[Field] = []
        var_positional = None

        index = 0
        while parameters and parameters[0].is_positional():
            parameter = parameters.pop(0)
            positional_field = FromArrayConstructor._new_positional_field(
                metadata, factory, target, parameter
            )
            if isinstance(positional_field, VariadicField):
                _log.debug(
                    "Created variadic constructor for positional parameter '%s' (%d): %s",
                    parameter.name,
                    index,
                    positional_field,
                )
                var_positional = positional_field.constructor
            elif positional_field:
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

        positional_parameters = [p for p in parameters if p.is_positional()]
        if positional_parameters:  # pragma: no cover
            raise InternalError(
                f"unexpected positional parameters remaining: {positional_parameters}"
            )

        keyword: Dict[str, PseudoField] = {}
        while parameters:
            parameter = parameters.pop(0)
            keyword_field = FromArrayConstructor._new_keyword_field(
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
            FromArrayConstructor(
                _positional=positional,
                _var_positional=var_positional,
                _keyword=keyword,
                _target=target,
                _disallow_extra_elements=disallow_unknown_fields.read(metadata, target),
            ),
        )

    @staticmethod
    def _new_positional_field(
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
            # The _FromArrayConstructor doesn't use variadic context
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
            # The _FromArrayConstructor doesn't use variadic keyword
            # parameters.
            return None
        elif parameter.is_context():
            return ContextField()
        elif parameter.is_required():
            raise factory.make_error(
                "cannot create from-array constructor for target with required "
                f"keyword-only parameter: {parameter.name}"
            )
        # Covered, despite what 'coverage' says.
        else:  # pragma: no cover
            # Keyword parameter is optional; omit it.
            return None

    def __call__(self, data: Value) -> _T_co:
        array_data = data.as_array()
        iter_data = iter(array_data)

        positional: List[object] = []
        for index, field in enumerate(self._positional):
            if isinstance(field, SingleField):
                try:
                    element = next(iter_data)
                except StopIteration:
                    if field.required:
                        raise data.make_error(
                            f"too few elements ({len(array_data)}) - "
                            f"expected at least {self.min_elements} "
                        ) from None
                    break
                value = field.constructor(element)
                _log.debug("Positional parameter %d using value: %s", index, value)
                positional.append(value)
            else:
                positional.append(
                    handle_positional_pseudo_field(index, field, data.context)
                )

        if self._var_positional:
            for element in iter_data:
                value = self._var_positional(element)
                _log.debug("Variadic positional parameter using value: %s", value)
                positional.append(value)

        if self._disallow_extra_elements and not iterator_utils.is_empty(iter_data):
            raise data.make_error(
                f"too many elements ({len(array_data)}) - "
                f"expected at most {self.max_elements}"
            )

        keyword: Dict[str, object] = {}
        for name, field in self._keyword.items():
            value = handle_keyword_pseudo_field(name, field, data.context)
            if value is not OMIT:
                keyword[name] = value

        _log.debug(
            "Instantiating %s with arguments: %s",
            LoggableTarget(self._target),
            LoggableArguments(positional, keyword),
        )
        return self._target(*positional, **keyword)  # type: ignore[call-arg]

    def get_children(self) -> Iterator[InternalConstructor[Any]]:
        for field in self._positional:
            if isinstance(field, SingleField):
                yield field.constructor
        if self._var_positional:
            yield self._var_positional

    @property
    def min_elements(self) -> int:
        return sum(
            1
            for field in self._positional
            if isinstance(field, SingleField) and field.required
        )

    @property
    def max_elements(self) -> int:
        if self._var_positional:  # pragma: no cover
            raise InternalError(
                "no maximum element count for constructor with variadic parameter"
            )
        return sum(
            1
            for field in self._positional
            if isinstance(field, SingleField) and field.required
        )
