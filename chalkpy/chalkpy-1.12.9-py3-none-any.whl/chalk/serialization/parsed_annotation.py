from __future__ import annotations

import types
from typing import TYPE_CHECKING, List, Optional, Set, Type, TypeVar, Union, cast, get_type_hints

from typing_extensions import Annotated, get_args, get_origin

from chalk.utils.collection_type import GenericAlias
from chalk.utils.metaprogramming import _MISSING_TYPE, MISSING

if TYPE_CHECKING:
    from chalk.features import Features
    from chalk.streams import Windowed

T = TypeVar("T")
U = TypeVar("U")
JsonValue = TypeVar("JsonValue")


class ParsedAnnotation:
    def __init__(
        self,
        features_cls: Optional[Type[Features]] = None,
        attribute_name: Optional[str] = None,
        *,
        underlying: Optional[Union[type, Annotated, Windowed]] = None,
    ) -> None:
        # Either pass in the underlying -- if it is already parsed -- or pass in the feature cls and attribute name
        self._features_cls = features_cls
        self._attribute_name = attribute_name
        self._is_nullable: Optional[bool] = None
        self._is_dataframe: Optional[bool] = None
        self._collection_type: Optional[GenericAlias] = None
        self._is_scalar: Optional[bool] = None
        self._is_feature_time: Union[Optional[bool], _MISSING_TYPE] = MISSING
        self._is_primary: Union[Optional[bool], _MISSING_TYPE] = MISSING
        self._underlying = None
        self._parsed_annotation = None
        if underlying is not None:
            if features_cls is not None and attribute_name is not None:
                raise ValueError("If specifying the underlying, do not specify (features_cls, attribute_name)")
            self._parse_type(underlying)
        elif features_cls is None or attribute_name is None:
            raise ValueError(
                "If not specifying the underlying, then both the (features_cls, attribute_name) must be provided"
            )
        # Store the class and attribute name to later use typing.get_type_hints to
        # resolve any forward references in the type annotations
        # Resolution happens lazily -- after everything is imported -- to avoid circular imports

    @property
    def is_parsed(self) -> bool:
        return self._underlying is not None

    @property
    def annotation(self) -> Union[str, type, Windowed, Annotated]:
        """Return the type annotation, without parsing the underlying type if it is not yet already parsed."""
        if self._parsed_annotation is not None:
            # It is already parsed. Return it.
            return self._parsed_annotation
        assert self._features_cls is not None
        assert self._attribute_name is not None
        return self._features_cls.__annotations__[self._attribute_name]

    @property
    def parsed_annotation(self) -> Union[type, Windowed]:
        """The parsed type annotation. It will be parsed if needed.

        Unlike :attr:`underlying`, parsed annotation contains any container or optional types, such as
        list, dataframe, or Optional.
        """
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._parsed_annotation is not None
        return self._parsed_annotation

    def __str__(self):
        if isinstance(self.annotation, type):
            return self.annotation.__name__
        return str(self.annotation)

    def _parse_annotation(self):
        assert self._features_cls is not None
        assert self._attribute_name is not None
        hints = get_type_hints(self._features_cls)
        parsed_annotation = hints[self._attribute_name]
        self._parse_type(parsed_annotation)

    def _parse_type(self, annotation: Optional[Union[type, Windowed, Annotated]]):
        from chalk.features import DataFrame, Features

        assert self._parsed_annotation is None, "The annotation was already parsed"
        self._parsed_annotation = annotation
        self._is_nullable = False
        if self._features_cls is not None and self._attribute_name is not None:
            # Return a more helpful error message, since we have context
            error_ctx = f" {self._features_cls.__name__}.{self._attribute_name}"
        else:
            error_ctx = ""
        origin = get_origin(annotation)
        if origin is Annotated:
            annotation = get_args(annotation)[0]
            origin = get_origin(annotation)
        if origin in (
            Union,
            getattr(types, "UnionType", Union),
        ):  # using getattr as UnionType was introduced in python 3.10
            args = get_args(annotation)
            # If it's a union, then the only supported union is for nullable features. Validate this
            if len(args) != 2 or (None not in args and type(None) not in args):
                raise TypeError(
                    f"Invalid annotation for feature{error_ctx}: Unions with non-None types are not allowed"
                )
            annotation = args[0] if args[1] in (None, type(None)) else args[1]
            self._is_nullable = True

        # The only allowed collections here are Set, List, or DataFrame
        if origin in (set, Set):
            args = get_args(annotation)
            assert len(args) == 1, "typing.Set takes just one arg"
            annotation = args[0]
            self._collection_type = Set[cast(Type, annotation)]

        if origin in (list, List):
            args = get_args(annotation)
            assert len(args) == 1, "typing.List takes just one arg"
            annotation = args[0]
            self._collection_type = List[cast(Type, annotation)]

        self._is_dataframe = False

        if annotation is not None and isinstance(annotation, type) and issubclass(annotation, DataFrame):
            self._is_dataframe = True
            # For features, annotations like DataFrame[User.id] are not allowed
            # Annotations like these are only allowed in resolvers
            # So, error here.
            # if annotation.references_feature_set is None:
            #     raise TypeError("DF has no underlying type")
            annotation = annotation.references_feature_set

        self._is_scalar = annotation is not None and not (
            isinstance(annotation, type) and issubclass(annotation, (Features, DataFrame))
        )

        if self._collection_type is not None and not self._is_scalar:
            raise TypeError(
                (
                    f"Invalid type annotation for feature {error_ctx}: "
                    f"{str(self._collection_type)} must be of scalar types, "
                    f"not {self._parsed_annotation}"
                )
            )
        if self._is_dataframe and self._is_scalar:
            raise TypeError(
                f"Invalid type annotation for feature{error_ctx}: Dataframes must be of Features types, not {self._parsed_annotation}"
            )

        self._underlying = annotation

    @property
    def is_nullable(self) -> bool:
        """Whether the type annotation is nullable."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_nullable is not None
        return self._is_nullable

    @property
    def underlying(self) -> Union[type, Windowed]:
        """The underlying type annotation from the annotation."""
        if self.parsed_annotation is None:
            self._parse_annotation()
        if self._underlying is None:
            raise TypeError("There is no underlying type")
        return self._underlying

    @underlying.setter
    def underlying(self, underlying: Optional[type]):
        self._underlying = underlying

    @property
    def is_dataframe(self) -> bool:
        """Whether the type annotation is a dataframe."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_dataframe is not None
        return self._is_dataframe

    @property
    def collection_type(self) -> Optional[GenericAlias]:
        if self._parsed_annotation is None:
            self._parse_annotation()
        return self._collection_type

    @property
    def is_scalar(self) -> bool:
        """Whether the type annotation is a scalar type (i.e. not a Features type)."""
        if self._parsed_annotation is None:
            self._parse_annotation()
        assert self._is_scalar is not None
        return self._is_scalar

    @property
    def is_primary(self) -> Optional[bool]:
        if self._is_primary is not MISSING:
            assert not isinstance(self._is_primary, _MISSING_TYPE)
            return self._is_primary
        self._is_primary = None
        annotation = self.annotation
        origin = get_origin(annotation)
        if origin is not None:
            args = get_args(annotation)
            if "__chalk_primary__" in args:
                self._is_primary = True

        return self._is_primary

    @property
    def is_feature_time(self) -> Optional[bool]:
        if self._is_feature_time is not MISSING:
            assert not isinstance(self._is_feature_time, _MISSING_TYPE)
            return self._is_feature_time
        self._is_feature_time = None
        annotation = self.annotation
        origin = get_origin(annotation)
        if origin is not None:
            args = get_args(annotation)
            if "__chalk_ts__" in args:
                self._is_feature_time = True

        return self._is_feature_time
