import abc
import collections
import dataclasses
import logging
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
)

from typing_extensions import final

from .data import ConstructionConfig, Context, Value
from .errors import ContextTypeError, FactoryError, InternalError, TerramareError
from .pretty_printer import (
    LoggablePrimitive,
    LoggableTarget,
    print_object,
    print_table,
    print_type_name,
)
from .safe_mapping import SafeMutableMapping
from .types import Primitive, Target

if TYPE_CHECKING:  # pragma: no cover
    from .metadata import TargetMetadata

_log = logging.getLogger(__name__)

_T_co = TypeVar("_T_co", covariant=True)


@dataclass(frozen=True)
class InternalFactoryError(TerramareError):
    """Internal exception raised when failing to create a constructor."""

    summary: str
    detail: str


@dataclass(frozen=True)
class ContextParameter:
    key: str
    type_: Target[Any]
    parameter: str
    required: bool


class ConstructorCore(Generic[_T_co], abc.ABC):
    """
    Interface for constructor implementations.

    This should not be used directly - instead, use:
    - the InternalConstructor wrapper class, if constructing a sub-object from
      another constructor;
    - the public Constructor class, if constructing a top-level object.
    """

    @abc.abstractmethod
    def __call__(self, data: Value) -> _T_co:
        """
        Create an instance of the target type.

        :param data: Primitive value from which to construct an instance of the
            target type.

        :returns: Instance of the target type.

        :raises terramare.errors.ConstructorError: If the primitive value has
            an incorrect type or structure.
        :raises terramare.errors.ValidationException: If the primitive value has
            the correct type and structure but fails value-level validation.
        """

    @abc.abstractmethod
    def get_children(self) -> Iterator["InternalConstructor[Any]"]:
        """
        Retrieve all constructors owned by this constructor.

        Used to iterate over the constructor tree.
        """

    def requires_context(self) -> Iterable[ContextParameter]:
        """Return the Context fields required by this constructor."""
        return ()

    def __str__(self) -> str:  # pragma: no cover
        return print_object(self)


@final
@dataclass
class ForwardRef(ConstructorCore[_T_co]):
    """
    Forward reference to a ConstructorCore.

    This is necessary to create constructors for recursive types. For example,
    consider:

    @dataclass
    class LinkedList:
        next: Optional["LinkedList"] = None

    With a naive implementation we would not be able to create a LinkedList
    constructor without already having a LinkedList constructor!

    A ForwardRef can be returned in place of a constructor from
    `create_constructor` when it is called with a target type from within a
    call to `create_constructor` for that type.

    All instances of the ForwardRef are then resolved to a real constructor
    before returning from the earlier call to `create_constructor`.

    For example, calling `create_constructor(LinkedList)` as part of creating a
    constructor for the `next` field of LinkedList will return a ForwardRef,
    preventing infinite recursion.

    By the time a constructor is returned from the top-level `create_constructor`
    call this ForwardRef has been resolved - the same constructor is used for
    constructing a top-level LinkedList instance _and_ its `next` member.
    """

    _impl: Optional[ConstructorCore[_T_co]] = None

    def __call__(self, data: Value) -> _T_co:
        """
        Call the referenced constructor.

        See `ConstructorCore.__call__`.

        :raises InternalError: If the ForwardRef has not been resolved.
        """
        return self.deref()(data)

    def get_children(self) -> Iterator["InternalConstructor[Any]"]:
        return self.deref().get_children()

    def requires_context(self) -> Iterable[ContextParameter]:
        return self.deref().requires_context()

    def resolve_to(self, impl: ConstructorCore[_T_co]) -> None:
        """Resolve the forward reference to the given real constructor."""
        self._impl = impl

    def deref(self) -> ConstructorCore[_T_co]:
        """
        Retrieve the referenced constructor.

        :raises InternalError: If the ForwardRef has not been resolved.
        """
        if self._impl is None:  # pragma: no cover
            raise InternalError(
                f"attempted to dereference unresolved forward reference {id(self):x}"
            )
        return self._impl


@final
@dataclass(frozen=True)
class _Stack:
    _inner: Sequence[Tuple[str, str]] = field(default_factory=list)

    def __str__(self) -> str:
        return print_table([("path", "type"), *self._inner])

    def push(self, frame: str, target: Union[str, Target[Any]]) -> "_Stack":
        if not isinstance(target, str):  # pragma: no branch
            target = print_type_name(target)
        return _Stack([*self._inner, (frame, target)])


@final
@dataclass
class InternalConstructor(Generic[_T_co]):
    """
    Internal-only wrapper class for constructor implementations.

    Provides logging, error context, and forward reference handling.
    """

    _impl: ConstructorCore[_T_co]
    _target: Target[_T_co]
    _stack: _Stack = field(compare=False)

    def __call__(self, data: Value) -> _T_co:
        """
        Create an instance of the target type.

        See `ConstructorCore.__call__`.
        """
        if isinstance(self._impl, ForwardRef):
            self._impl = self._impl.deref()
        _log.debug(
            "Attempting to construct %s from data: %s",
            LoggableTarget(self._target),
            LoggablePrimitive(data.raw),
        )
        value = self._impl(data.clone().push_stack(print_type_name(self.target)))
        _log.debug(
            "Constructed %s: %s",
            LoggableTarget(self._target),
            value,
        )
        return value

    def __str__(self) -> str:  # pragma: no cover
        """Return a human-readable representation of the constructor."""
        return f"Constructor[{print_type_name(self.target)}]"

    def walk(
        self, *, _seen: Optional[List["InternalConstructor[Any]"]] = None
    ) -> Iterator["InternalConstructor[Any]"]:
        if _seen is None:
            _seen = []
        yield self
        for child in self._impl.get_children():
            if child in _seen:
                continue
            _seen.append(child)
            for constructor in child.walk(_seen=_seen):
                yield constructor

    def requires_context(self) -> Iterable[ContextParameter]:
        return self._impl.requires_context()

    def unwrap(self) -> ConstructorCore[_T_co]:
        """Retrieve the wrapped ConstructorCore."""
        return self._impl

    @property
    def stack(self) -> _Stack:
        return self._stack

    @property
    def target(self) -> Target[_T_co]:
        return self._target


class FactoryCore(abc.ABC):
    """
    Interface for constructor factory implementations.

    This should not be used directly - instead, use:
    - the InternalFactory wrapper class, if creating a sub-constructor from
      another constructor factory;
    - the public Factory class, if creating a top-level constructor.
    """

    @abc.abstractmethod
    def create_constructor(
        self, factory: "InternalFactory", target: Target[_T_co]
    ) -> ConstructorCore[_T_co]:
        """
        Create a constructor for the given target type.

        :param factory: Constructor factory used when recursively creating sub-
            constructors.
        :param target: Target type.

        :returns: A `ConstructorCore` targeting the given type.

        :raises InternalFactoryError: If a constructor for the given target type
            cannot be created due to fundamental problems with the target type.
        :raises UnsupportedTargetTypeError: If a constructor for the given
            target type cannot be created by this factory, but another factory
            may be able to create such a constructor.
        """

    def __str__(self) -> str:  # pragma: no cover
        return print_object(self)


@final
@dataclass(frozen=True)
class InternalFactory:
    """
    Internal-only wrapper class for constructor factory implementations.

    Provides logging, error context, caching and forward reference handling.

    A new instance of this class is created with each `create_constructor` call,
    including recursive calls. New instances share the persistent data of the
    parent instance.
    """

    _persistent_data: "PersistentData"
    _stack: _Stack = field(default_factory=_Stack)

    @dataclass(frozen=True)
    class PersistentData:
        """Persistent data shared between recursive `create_constructor` calls."""

        impl: FactoryCore
        cache: SafeMutableMapping[Target[Any], InternalConstructor[Any]] = field(
            default_factory=SafeMutableMapping
        )

    def create_constructor(
        self, target: Target[_T_co], *, frame: str = ""
    ) -> InternalConstructor[_T_co]:
        """
        Create a constructor for the given target type.

        :param target: Target type.
        :param context: Additional context for the constructor, such as an enum
            variant index.

        :returns: An `InternalConstructor` targeting the given type.

        :raises InternalFactoryError: If a constructor for the given target type
            cannot be created due to fundamental problems with the target type.
        :raises UnsupportedTargetTypeError: If a constructor for the given
            target type cannot be created by this factory, but another factory
            may be able to create such a constructor.
        """
        _log.debug(
            "Attempting to create constructor for target %s",
            LoggableTarget(target),
        )

        def create() -> ConstructorCore[_T_co]:
            return self._persistent_data.impl.create_constructor(
                self.push_stack(target, frame=frame), target
            )

        if target not in self._persistent_data.cache:
            _log.debug("Cache miss for target %s", LoggableTarget(target))
            forward_ref: ForwardRef[_T_co] = ForwardRef()
            _log.debug(
                "Created ForwardRef %x for target %s",
                id(forward_ref),
                LoggableTarget(target),
            )
            self._persistent_data.cache[target] = self.wrap(target, forward_ref)
            try:
                constructor = create()
            except BaseException:
                # Remove the unresolved forward reference.
                del self._persistent_data.cache[target]
                raise
            forward_ref.resolve_to(constructor)
            _log.debug(
                "ForwardRef %x for target %s resolved to %s",
                id(forward_ref),
                LoggableTarget(target),
                constructor,
            )
            _log.debug("Cached constructor for target %s", LoggableTarget(target))
        _log.debug(
            "Retrieved constructor from cache for target %s",
            LoggableTarget(target),
        )
        return self._persistent_data.cache[target]

    def make_error(self, msg: str) -> InternalFactoryError:
        """
        Create an `InternalFactoryError` with the given message.

        The error will contain additional context including the stack of target
        types.
        """
        return InternalFactoryError(msg, self.stack)

    def push_stack(
        self, target: Target[_T_co], *, frame: str = ""
    ) -> "InternalFactory":
        return dataclasses.replace(self, _stack=self._stack.push(frame, target))

    def wrap(
        self, target: Target[_T_co], core: ConstructorCore[_T_co]
    ) -> InternalConstructor[_T_co]:
        return InternalConstructor(core, target, self._stack)

    @property
    def stack(self) -> str:
        return str(self._stack)

    def __str__(self) -> str:  # pragma: no cover
        return print_object(self)


@final
@dataclass(frozen=True)
class Factory:
    _persistent_data: InternalFactory.PersistentData = field(
        # pylint: disable=unnecessary-lambda
        default_factory=lambda: Factory._make_persistent_data()
    )

    @classmethod
    def new(
        cls,
        *,
        _experimental_metadata: Optional[Mapping[Target[Any], "TargetMetadata"]] = None,
    ) -> "Factory":
        return cls(
            cls._make_persistent_data(_experimental_metadata=_experimental_metadata)
        )

    @overload
    def create_constructor(self, target: Target[_T_co]) -> "Constructor[_T_co]":
        # See terramare.py for an explanation of the overloads here.
        ...  # pragma: no cover

    @overload
    def create_constructor(self, target: Any) -> "Constructor[Any]":
        ...  # pragma: no cover

    def create_constructor(self, target: Any) -> "Constructor[_T_co]":
        factory = InternalFactory(self._persistent_data)
        try:
            return Constructor.new(factory.create_constructor(target))
        except InternalFactoryError as e:
            raise FactoryError(
                f"failed to create constructor for type '{print_type_name(target)}': "
                f"{e.summary}\n{e.detail}"
            ) from e

    @overload
    def structure(
        self,
        data: Primitive,
        *,
        into: Target[_T_co],
        coerce_strings: bool = False,
        context: Optional[Mapping[str, object]] = None,
    ) -> _T_co:
        # See terramare.py for an explanation of the overloads here.
        ...  # pragma: no cover

    @overload
    def structure(
        self,
        data: Primitive,
        *,
        into: Any,
        coerce_strings: bool = False,
        context: Optional[Mapping[str, object]] = None,
    ) -> Any:
        ...  # pragma: no cover

    def structure(
        self,
        data: Primitive,
        *,
        into: Any,
        coerce_strings: bool = False,
        context: Optional[Mapping[str, object]] = None,
    ) -> Any:
        return self.create_constructor(into)(
            data, coerce_strings=coerce_strings, context=context
        )

    @staticmethod
    def _make_persistent_data(
        *,
        _experimental_metadata: Optional[Mapping[Target[Any], "TargetMetadata"]] = None,
    ) -> InternalFactory.PersistentData:
        # pylint: disable=import-outside-toplevel, cyclic-import
        from .classes import ClassFactory
        from .composite import CompositeFactory
        from .context_factory import ContextFactory
        from .enums import EnumFactory, LiteralFactory
        from .mappings import MappingFactory, TypedDictFactory
        from .metadata import MetadataCollection, MetadataFactory
        from .newtypes import NewTypeFactory
        from .primitives import (
            AnyFactory,
            BoolFactory,
            FloatFactory,
            IntFactory,
            NoneFactory,
            PrimitiveDictFactory,
            PrimitiveListFactory,
            StrFactory,
        )
        from .sequences import SequenceFactory, TupleFactory
        from .stdlib_metadata import DEFAULT_METADATA
        from .tagged_constructors import TaggedFactory
        from .unions import UnionFactory

        metadata = MetadataCollection.new(
            {**DEFAULT_METADATA, **(_experimental_metadata or {})}
        )

        return InternalFactory.PersistentData(
            CompositeFactory(
                [
                    ContextFactory(),
                    MetadataFactory(metadata),
                    TaggedFactory(metadata),
                    NewTypeFactory(),
                    NoneFactory(),
                    BoolFactory(),
                    IntFactory(),
                    FloatFactory(),
                    StrFactory(),
                    PrimitiveListFactory(),
                    PrimitiveDictFactory(),
                    AnyFactory(),
                    EnumFactory(),
                    LiteralFactory(),
                    SequenceFactory(),
                    TupleFactory(),
                    MappingFactory(),
                    TypedDictFactory(),
                    UnionFactory(),
                    ClassFactory(metadata),
                ]
            )
        )


@dataclass(frozen=True)
class _ContextParameter:
    constructors: Sequence[Tuple[Target[Any], _Stack]]
    required: bool

    def __post_init__(self) -> None:
        assert self.constructors

    def to_stack_str(self) -> str:
        required_str = "required" if self.required else "used"
        return "\n".join(
            f"{required_str} to construct target '{print_type_name(target)}'\n{stack}"
            for target, stack in self.constructors
        )


@final
@dataclass(frozen=True)
class Constructor(Generic[_T_co]):
    _impl: InternalConstructor[_T_co]
    _context_parameters: Mapping[str, _ContextParameter]

    @staticmethod
    def new(impl: InternalConstructor[_T_co]) -> "Constructor[_T_co]":
        return Constructor(_impl=impl, _context_parameters=_gather_context(impl))

    def __call__(
        self,
        data: Primitive,
        *,
        coerce_strings: bool = False,
        context: Optional[Mapping[str, object]] = None,
    ) -> _T_co:
        context = context or {}
        if not _is_primitive(data):
            raise TypeError("unsupported type for 'data': expected Primitive")
        if not isinstance(coerce_strings, bool):
            raise TypeError("unsupported type for 'coerce_strings': expected bool")
        self._check_context(context)

        return self._impl(
            Value.new(
                data,
                config=ConstructionConfig(coerce_strings=coerce_strings),
                context=Context(context or {}),
            )
        )

    def __str__(self) -> str:  # pragma: no cover
        return str(self._impl)

    def _check_context(self, context: Mapping[str, object]) -> None:
        for name, req_ctx in self._context_parameters.items():
            if name not in context and req_ctx.required:
                raise ContextTypeError(
                    f"missing context parameter '{name}' {req_ctx.to_stack_str()}"
                )


def _gather_context(impl: InternalConstructor[Any]) -> Mapping[str, _ContextParameter]:
    @dataclass(frozen=True)
    class ContextData:
        t: Target[Any]
        s: _Stack
        p: ContextParameter

    context: Dict[str, List[ContextData]] = collections.defaultdict(list)

    for constructor in impl.walk():
        for required_context in constructor.requires_context():
            _log.debug(
                "Found context parameter '%s' of type %s on constructor %r",
                required_context.key,
                LoggableTarget(required_context.type_),
                constructor,
            )
            context[required_context.key].append(
                ContextData(
                    constructor.target,
                    constructor.stack.push(
                        f"field {required_context.parameter}", required_context.type_
                    ),
                    required_context,
                )
            )

    requires_context: Dict[str, _ContextParameter] = {}
    for key, cds in context.items():
        requires_context[key] = _ContextParameter(
            [(cd.t, cd.s) for cd in cds],
            any(cd.p.required for cd in cds),
        )
    return requires_context


def _is_primitive(data: Any) -> bool:
    if data is None:
        return True
    if isinstance(data, (bool, int, float, str)):
        return True
    if isinstance(data, list):
        return all(_is_primitive(element) for element in data)
    if isinstance(data, dict):
        return all(
            isinstance(key, str) and _is_primitive(value) for key, value in data.items()
        )
    return False
