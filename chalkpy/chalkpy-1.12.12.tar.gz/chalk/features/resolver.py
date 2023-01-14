from __future__ import annotations

import dataclasses
import inspect
from dataclasses import dataclass
from inspect import Parameter, isclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    get_type_hints,
    overload,
)

import pyarrow
from pydantic import BaseModel
from typing_extensions import ParamSpec, get_args, get_origin

from chalk.features.dataframe import DataFrame
from chalk.features.feature_field import Feature
from chalk.features.feature_set import Features
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter
from chalk.features.tag import Environments, Tags
from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.state import StateWrapper
from chalk.streams import StreamSource, Windowed, get_name_with_duration
from chalk.streams.types import (
    StreamResolverParam,
    StreamResolverParamKeyedState,
    StreamResolverParamMessage,
    StreamResolverParamMessageWindow,
    StreamResolverSignature,
)
from chalk.utils import MachineType
from chalk.utils.annotation_parsing import ResolverAnnotationParser
from chalk.utils.collection_type import GenericAlias
from chalk.utils.collections import ensure_tuple
from chalk.utils.duration import Duration, ScheduleOptions
from chalk.utils.environment_parsing import env_var_bool

if TYPE_CHECKING:
    from chalk.sql import BaseSQLSourceProtocol


T = TypeVar("T")
P = ParamSpec("P")


@dataclasses.dataclass(frozen=True)
class ResolverArgErrorHandler:
    default_value: Any


@dataclass
class StateDescriptor(Generic[T]):
    kwarg: str
    pos: int
    initial: T
    typ: Type[T]


class FilterFunction(Protocol):
    def __call__(self, *args: Feature) -> bool:
        ...


class SampleFunction(Protocol):
    def __call__(self) -> DataFrame:
        ...


@dataclass
class Cron:
    schedule: Optional[ScheduleOptions] = None
    filter: Optional[FilterFunction] = None
    sample: Optional[SampleFunction] = None
    trigger_downstream: Optional[bool] = True


def _flatten_features(output: Optional[Type[Features]]) -> Sequence[Feature]:
    if output is None:
        return []
    features = output.features
    if len(features) == 1 and isinstance(features[0], type) and issubclass(features[0], DataFrame):
        return features[0].columns
    else:
        return features


class Resolver(Generic[P, T]):
    function_definition: str
    fqn: str
    filename: str
    inputs: List[Feature]
    output: Type[Features]
    fn: Callable[P, T]
    environment: Optional[List[str]]
    tags: Optional[List[str]]
    max_staleness: Optional[Duration]
    machine_type: Optional[MachineType]
    owner: Optional[str]
    state: Optional[StateDescriptor]
    default_args: List[Optional[ResolverArgErrorHandler]]

    registry: "ClassVar[List[Resolver]]" = []
    hook: "ClassVar[Optional[Callable[[Resolver], None]]]" = None

    def __hash__(self):
        return hash(self.fqn)

    def __call__(self, *args: P.args, **kwds: P.kwargs) -> T:
        ...

    @property
    def __name__(self):
        return self.fn.__name__


def _process_call(result: T, *, declared_output: Optional[Type[Features]]) -> T:
    # __call__ is defined to support userland code that invokes a resolver
    # as if it is a normal python function
    # If the user returns a ChalkQuery, then we'll want to automatically execute it
    from chalk.sql import FinalizedChalkQuery
    from chalk.sql._internal.chalk_query import ChalkQuery
    from chalk.sql._internal.string_chalk_query import StringChalkQuery

    if isinstance(result, (ChalkQuery, StringChalkQuery)):
        result = result.all()
    if isinstance(result, FinalizedChalkQuery):
        result = result.execute(_flatten_features(declared_output))
    return result


class SinkResolver(Resolver[P, T]):
    registry: "List[SinkResolver]" = []

    def __eq__(self, other):
        return isinstance(other, SinkResolver) and self.fqn == other.fqn

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return _process_call(self.fn(*args, **kwargs), declared_output=None)

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[Feature],
        output: Type[Features],
        fn: Callable[P, T],
        environment: Optional[List[str]],
        tags: Optional[List[str]],
        machine_type: Optional[MachineType],
        buffer_size: Optional[int],
        debounce: Optional[Duration],
        max_delay: Optional[Duration],
        upsert: Optional[bool],
        owner: Optional[str],
        integration: Optional[BaseSQLSourceProtocol] = None,
    ):
        self.owner = owner
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.__module__ = fn.__module__
        self.__doc__ = fn.__doc__
        self.__annotations__ = fn.__annotations__
        self.environment = environment
        self.tags = tags
        self.doc = doc
        self.machine_type = machine_type
        self.buffer_size = buffer_size
        self.debounce = debounce
        self.max_delay = max_delay
        self.upsert = upsert
        self.integration = integration
        self.default_args = []
        self.max_staleness = None
        self.state = None

    def __repr__(self):
        return f"SinkResolver(name={self.fqn})"


class OnlineResolver(Resolver[P, T]):
    cron: Union[ScheduleOptions, Cron]

    def __eq__(self, other):
        return isinstance(other, OnlineResolver) and self.fqn == other.fqn

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return _process_call(self.fn(*args, **kwargs), declared_output=self.output)

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[Feature],
        output: Type[Features],
        fn: Callable[P, T],
        environment: Optional[List[str]],
        tags: Optional[List[str]],
        max_staleness: Optional[Duration],
        cron: Optional[Union[ScheduleOptions, Cron]],
        machine_type: Optional[MachineType],
        when: Optional[Filter],
        state: Optional[StateDescriptor],
        default_args: List[Optional[ResolverArgErrorHandler]],
        owner: Optional[str],
    ):
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.__module__ = fn.__module__
        self.__doc__ = fn.__doc__
        self.__annotations__ = fn.__annotations__
        self.environment = environment
        self.tags = tags
        self.max_staleness = max_staleness
        self.cron = cron
        self.doc = doc
        self.machine_type = machine_type
        self.when = when
        self.state = state
        self.default_args = default_args
        self.owner = owner

    def __repr__(self):
        return f"OnlineResolver(name={self.fqn})"


class OfflineResolver(Resolver[P, T]):
    def __eq__(self, other):
        return isinstance(other, OfflineResolver) and self.fqn == other.fqn

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return _process_call(self.fn(*args, **kwargs), declared_output=self.output)

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        inputs: List[Feature],
        output: Type[Features],
        fn: Callable[P, T],
        environment: Optional[List[str]],
        tags: Optional[List[str]],
        max_staleness: Optional[Duration],
        cron: Union[ScheduleOptions, Cron],
        machine_type: Optional[MachineType],
        state: Optional[StateDescriptor],
        when: Optional[Filter],
        default_args: List[Optional[ResolverArgErrorHandler]],
        owner: Optional[str],
    ):
        self.when = when
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.doc = doc
        self.inputs = inputs
        self.output = output
        self.fn = fn
        self.__module__ = fn.__module__
        self.__doc__ = fn.__doc__
        self.__annotations__ = fn.__annotations__
        self.environment = environment
        self.tags = tags
        self.max_staleness = max_staleness
        self.cron = cron
        self.machine_type = machine_type
        self.state = state
        self.default_args = default_args
        self.owner = owner


def __repr__(self):
    return f"OfflineResolver(name={self.fqn})"


@dataclasses.dataclass(frozen=True)
class ResolverParseResult(Generic[P, T]):
    fqn: str
    inputs: List[Feature]
    state: Optional[StateDescriptor]
    output: Optional[Type[Features]]
    function: Callable[P, T]
    function_definition: str
    doc: Optional[str]
    default_args: List[Optional[ResolverArgErrorHandler]]


def get_resolver_fqn(function: Callable):
    return f"{function.__module__}.{function.__name__}"


def get_state_default_value(
    state_typ: Type[Any],
    declared_default: Any,
    parameter_name_for_errors: str,
    resolver_fqn_for_errors: str,
) -> Any:
    if not issubclass(state_typ, BaseModel) and not dataclasses.is_dataclass(state_typ):
        raise ValueError(
            (
                f"State value must be a pydantic model or dataclass, "
                f"but argument '{parameter_name_for_errors}' has type '{type(state_typ).__name__}'"
            )
        )

    default = declared_default
    if default is inspect.Signature.empty:
        try:
            default = state_typ()
        except Exception as e:
            cls_name = state_typ.__name__
            raise ValueError(
                (
                    "State parameter must have a default value, or be able to be instantiated "
                    f"with no arguments. For resolver '{resolver_fqn_for_errors}', no default found, and default "
                    f"construction failed with '{str(e)}'. Assign a default in the resolver's "
                    f"signature ({parameter_name_for_errors}: {cls_name} = {cls_name}(...)), or assign a default"
                    f" to each of the fields of '{cls_name}'."
                )
            )

    if not isinstance(default, state_typ):
        raise ValueError(
            f"Expected type '{state_typ.__name__}' for '{parameter_name_for_errors}', but default has type '{type(default).__name__}'"
        )

    return default


def parse_function(
    fn: Callable[P, T],
    glbs: Optional[Dict[str, Any]],
    lcls: Optional[Dict[str, Any]],
    ignore_return: bool = False,
    allow_custom_args: bool = False,
    is_streaming_resolver: bool = False,
) -> ResolverParseResult[P, T]:
    fqn = get_resolver_fqn(function=fn)
    sig = inspect.signature(fn)
    annotation_parser = ResolverAnnotationParser(fn, glbs, lcls)

    function_definition = inspect.getsource(fn)
    return_annotation = get_type_hints(fn).get("return")
    if return_annotation is None:
        raise TypeError(
            f"Resolver '{fqn}' must have a return annotation. See https://docs.chalk.ai/docs/resolver-outputs for more information."
        )

    ret_val = None

    if isinstance(return_annotation, FeatureWrapper):
        return_annotation = return_annotation._chalk_feature

    if isinstance(return_annotation, Feature):
        assert return_annotation.typ is not None

        if return_annotation.is_has_many:
            assert issubclass(return_annotation.typ.parsed_annotation, DataFrame)
            ret_val = Features[return_annotation.typ.parsed_annotation.columns]
        elif return_annotation.is_has_one:
            assert issubclass(return_annotation.typ.underlying, Features)
            ret_val = Features[return_annotation.typ.underlying.features]
        else:
            # function annotated like def get_account_id(user_id: User.id) -> User.account_id
            ret_val = Features[return_annotation]

    if ret_val is None:
        if not isinstance(return_annotation, type):
            raise TypeError(f"return_annotation {return_annotation} of type {type(return_annotation)} is not a type")
        if issubclass(return_annotation, Features):
            # function annotated like def get_account_id(user_id: User.id) -> Features[User.account_id]
            # or def get_account_id(user_id: User.id) -> User:
            ret_val = return_annotation
        elif issubclass(return_annotation, DataFrame):
            # function annotated like def get_transactions(account_id: Account.id) -> DataFrame[Transaction]
            ret_val = Features[return_annotation]

    if ret_val is None and not ignore_return:
        raise ValueError(f"Resolver {fqn} did not have a valid return type")

    inputs = [annotation_parser.parse_annotation(p) for p in sig.parameters.keys()]

    # Unwrap anything that is wrapped with FeatureWrapper
    inputs = [unwrap_feature(p) if isinstance(p, FeatureWrapper) else p for p in inputs]

    state = None
    default_args: List[Optional[ResolverArgErrorHandler]] = [None for _ in range(len(inputs))]

    for i, (arg_name, parameter) in enumerate(sig.parameters.items()):
        bad_input = lambda: ValueError(
            f"Resolver inputs must be Features or State. Received {str(inputs[i])} for argument '{arg_name}' for '{fqn}'.\n"
        )
        arg = inputs[i]

        if isinstance(arg, GenericAlias) and get_origin(arg) == Union:
            args = get_args(arg)
            if len(args) != 2:
                raise bad_input()
            if type(None) not in args:
                raise bad_input()
            real_arg = next((a for a in args if a is not type(None)), None)
            if real_arg is None:
                raise bad_input()
            default_args[i] = ResolverArgErrorHandler(None)
            arg = unwrap_feature(real_arg)
            inputs[i] = arg

        if parameter.empty != parameter.default:
            default_args[i] = ResolverArgErrorHandler(parameter.default)

        if not isinstance(arg, (StateWrapper, Feature)):
            if allow_custom_args:
                continue
            raise bad_input()

        if isinstance(arg.typ, ParsedAnnotation) and isinstance(arg.typ.underlying, Windowed):
            f = arg.typ.underlying
            raise ValueError(
                (
                    f"Resolver argument '{arg_name}' to '{fqn}' does not select a window. "
                    f"Add a selected window, like {arg.name}('{next(iter(f._buckets), '')}'). "
                    f"Available windows: {', '.join(f._buckets)}."
                )
            )

        if not isinstance(arg, StateWrapper):
            continue

        if state is not None:
            raise ValueError(
                f"Only one state argument is allowed. Two provided to '{fqn}': '{state.kwarg}' and '{arg_name}'"
            )

        arg_name = parameter.name

        state = StateDescriptor(
            kwarg=arg_name,
            pos=i,
            initial=get_state_default_value(
                state_typ=arg.typ,
                resolver_fqn_for_errors=fqn,
                parameter_name_for_errors=arg_name,
                declared_default=parameter.default,
            ),
            typ=arg.typ,
        )

    assert ret_val is None or issubclass(ret_val, Features)
    if not ignore_return and ret_val is not None and issubclass(ret_val, Features):
        # Streaming resolvers are themselves windowed, so the outputs must not specify a window explicitly.
        for f in _flatten_features(ret_val):
            if f.is_windowed and not is_streaming_resolver:
                raise TypeError(
                    (
                        "Windowed features need to specify a window "
                        f"period in the return type. The feature "
                        f"'{f.root_fqn}' returned from '{fn.__name__}' does not."
                    )
                )
            if f.is_windowed_pseudofeature and is_streaming_resolver:
                feature_name_without_duration = "__".join(f.root_fqn.split("__")[:-1])  # A bit hacky, but should work
                raise TypeError(
                    (
                        "Streaming resolvers should not resolve features of a particular window period in the return type"
                        f"Resolver '{fn.__name__}' returned feature '{f.root_fqn}'. Instead, return {feature_name_without_duration}"
                    )
                )
    state_index = state.pos if state is not None else None
    return ResolverParseResult(
        fqn=fqn,
        inputs=[v for i, v in enumerate(inputs) if i != state_index],
        output=ret_val,
        function=fn,
        function_definition=function_definition,
        doc=fn.__doc__,
        state=state,
        default_args=default_args,
    )


@overload
def online(
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Optional[Union[ScheduleOptions, Cron]] = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
    owner: Optional[str] = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    ...


@overload
def online(
    fn: Callable[P, T],
    /,
) -> Callable[P, T]:
    ...


def online(
    fn: Optional[Callable[P, T]] = None,
    /,
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Optional[Union[ScheduleOptions, Cron]] = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
    owner: Optional[str] = None,
) -> Union[Callable[[Callable[P, T]], Callable[P, T]], Callable[P, T]]:
    """
    :param fn: The function that you're decorating as a resolver.

    :param environment: Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:

            - None (default) - candidate to run in every environment
            - str - run only in this environment
            - list[str] - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments

    :param owner: Owner allows you to specify an individual or team
        who is responsible for this resolver. The Chalk Dashboard
        will display this field, and alerts can be routed to owners.

    :param tags: Tags allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags

    :param cron: You can schedule resolvers to run on a
        pre-determined schedule via the cron argument to resolver
        decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron

    :param machine_type: You can optionally specify that resolvers
        need to run on a machine other than the default. Must be
        configured in your deployment.

    :param when: Like tags, `when` can filter when a resolver
        is eligible to run. Unlike tags, `when` can use feature values,
        so that you can write resolvers like:

            @batch(when=User.risk_profile == "low" or User.is_employee)
            def resolver_fn(...) -> ...:
                ...

    :return: A callable function! You can unit test resolvers
        as you would unit test any other code.

    Read more at https://docs.chalk.ai/docs/unit-tests
    """
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_globals = caller_frame.frame.f_globals
    caller_locals = caller_frame.frame.f_locals

    def decorator(fn: Callable[P, T]):
        parsed = parse_function(fn, caller_globals, caller_locals)
        if not env_var_bool("CHALK_ALLOW_REGISTRY_UPDATES") and parsed.fqn in {s.fqn for s in Resolver.registry}:
            raise ValueError(f"Duplicate resolver {parsed.fqn}")
        if parsed.output is None:
            raise ValueError(f"Online resolvers must return features; '{parsed.fqn}' returns None")

        resolver = OnlineResolver(
            filename=caller_filename,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.inputs,
            output=parsed.output,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            max_staleness=None,
            cron=cron,
            machine_type=machine_type,
            when=when,
            owner=owner,
            state=parsed.state,
            default_args=parsed.default_args,
        )

        Resolver.registry.append(resolver)
        if Resolver.hook:
            Resolver.hook(resolver)

        # Return the decorated resolver, which notably implements __call__() so it acts the same as
        # the underlying function if called directly, e.g. from test code
        return resolver

    return decorator(fn) if fn else decorator


@overload
def offline(
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Optional[Union[ScheduleOptions, Cron]] = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
    owner: Optional[str] = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    ...


@overload
def offline(
    fn: Callable[P, T],
    /,
) -> Callable[P, T]:
    ...


def offline(
    fn: Optional[Callable[P, T]] = None,
    /,
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    cron: Union[ScheduleOptions, Cron] = None,
    machine_type: Optional[MachineType] = None,
    when: Optional[Any] = None,
    owner: Optional[str] = None,
) -> Union[Callable[[Callable[P, T]], Callable[P, T]], Callable[P, T]]:
    """
    :param fn: The function that you're decorating as a resolver.

    :param environment: Environments are used to trigger behavior
        in different deployments such as staging, production, and
        local development. For example, you may wish to interact with
        a vendor via an API call in the production environment, and
        opt to return a constant value in a staging environment.

        Environment can take one of three types:

            - None (default) - candidate to run in every environment
            - str - run only in this environment
            - list[str] - run in any of the specified environment and no others

        Read more at https://docs.chalk.ai/docs/resolver-environments

    :param owner: Owner allows you to specify an individual or team
        who is responsible for this resolver. The Chalk Dashboard
        will display this field, and alerts can be routed to owners.

    :param tags: Tags allow you to scope requests within an
        environment. Both tags and environment need to match for a
        resolver to be a candidate to execute.

        You might consider using tags, for example, to change out
        whether you want to use a sandbox environment for a vendor,
        or to bypass the vendor and return constant values in a
        staging environment.

        Read more at https://docs.chalk.ai/docs/resolver-tags

    :param cron: You can schedule resolvers to run on a
        pre-determined schedule via the cron argument to resolver
        decorators.

        Cron can sample all examples, a subset of all examples,
        or a custom provided set of examples.

        Read more at https://docs.chalk.ai/docs/resolver-cron

    :param machine_type: You can optionally specify that resolvers
        need to run on a machine other than the default. Must be
        configured in your deployment.

    :param when: Like tags, `when` can filter when a resolver
        is eligible to run. Unlike tags, `when` can use feature values,
        so that you can write resolvers like:

            @batch(when=User.risk_profile == "low" or User.is_employee)
            def resolver_fn(...) -> ...:
                ...

    :return: A callable function! You can unit test resolvers
        as you would unit test any other code.

    Read more at https://docs.chalk.ai/docs/unit-tests
    """
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_globals = caller_frame.frame.f_globals
    caller_locals = caller_frame.frame.f_locals

    def decorator(fn: Callable[P, T], cf: str = caller_filename):
        parsed = parse_function(fn, caller_globals, caller_locals)
        if not env_var_bool("CHALK_ALLOW_REGISTRY_UPDATES") and parsed.fqn in {s.fqn for s in Resolver.registry}:
            raise ValueError(f"Duplicate resolver {parsed.fqn}")
        if parsed.output is None:
            raise ValueError(f"Offline resolvers must return features; '{parsed.fqn}' returns None")
        resolver = OfflineResolver(
            filename=cf,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.inputs,
            output=parsed.output,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            max_staleness=None,
            cron=cron,
            machine_type=machine_type,
            state=parsed.state,
            when=when,
            owner=owner,
            default_args=parsed.default_args,
        )
        Resolver.registry.append(resolver)
        if Resolver.hook:
            Resolver.hook(resolver)
        return resolver

    return decorator(fn) if fn else decorator


@overload
def sink(
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    machine_type: Optional[MachineType] = None,
    buffer_size: Optional[int] = None,
    debounce: Optional[Duration] = None,
    max_delay: Optional[Duration] = None,
    upsert: Optional[bool] = None,
    integration: Optional[BaseSQLSourceProtocol] = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    ...


@overload
def sink(
    fn: Callable[P, T],
    /,
) -> Callable[P, T]:
    ...


def sink(
    fn: Optional[Callable[P, T]] = None,
    /,
    *,
    environment: Optional[Environments] = None,
    tags: Optional[Tags] = None,
    machine_type: Optional[MachineType] = None,
    buffer_size: Optional[int] = None,
    debounce: Optional[Duration] = None,
    max_delay: Optional[Duration] = None,
    upsert: Optional[bool] = None,
    integration: Optional[BaseSQLSourceProtocol] = None,
) -> Union[Callable[[Callable[P, T]], Callable[P, T]], Callable[P, T]]:
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_globals = caller_frame.frame.f_globals
    caller_locals = caller_frame.frame.f_locals

    def decorator(fn: Callable[P, T], cf: str = caller_filename):
        parsed = parse_function(fn, caller_globals, caller_locals, ignore_return=True)
        assert parsed.output is not None
        resolver = SinkResolver(
            filename=cf,
            function_definition=parsed.function_definition,
            fqn=parsed.fqn,
            doc=parsed.doc,
            inputs=parsed.inputs,
            output=parsed.output,
            fn=fn,
            environment=None if environment is None else list(ensure_tuple(environment)),
            tags=None if tags is None else list(ensure_tuple(tags)),
            machine_type=machine_type,
            buffer_size=buffer_size,
            debounce=debounce,
            max_delay=max_delay,
            upsert=upsert,
            integration=integration,
        )
        SinkResolver.registry.append(resolver)
        return resolver

    return decorator(fn) if fn else decorator


class StreamResolver(Resolver[P, T]):
    registry: "List[StreamResolver]" = []

    def __init__(
        self,
        caller_globals: Optional[Dict[str, Any]],
        caller_locals: Optional[Dict[str, Any]],
        caller_filename: str,
        source: StreamSource,
        fn: Callable[P, T],
        mode: Optional[str],
        signature: StreamResolverSignature,
        environment: Optional[List[str]],
        machine_type: Optional[str],
        output: Type[Features],
        message: Optional[Type[Any]],
    ):
        parsed = parse_function(fn, caller_globals, caller_locals, allow_custom_args=True, is_streaming_resolver=True)
        self.function_definition = parsed.function_definition
        self.fqn = parsed.fqn
        self.filename = caller_filename
        self.source = source
        self.mode = mode
        self.fn = fn
        self.environment = environment
        self.doc = parsed.doc
        self.inputs = []
        self.__doc__ = parsed.doc
        self.__module__ = fn.__module__
        self.machine_type = machine_type
        self.max_staleness = None
        self.state = parsed.state
        self.tags = None  # TODO -- should there be tags?
        self.signature = signature
        self.output = output
        self.message = message
        self.default_args = []
        fqn_to_windows = {o.fqn: o.window_durations for o in _flatten_features(self.output) if o.is_windowed}
        if len(set(tuple(v) for v in fqn_to_windows.values())) > 1:
            fqn_to_declared_windows = {
                o.fqn: sorted(o.window_durations) for o in _flatten_features(self.output) if o.is_windowed
            }
            periods = [f'{fqn}[{", ".join(f"{window}s")}]' for fqn, window in fqn_to_declared_windows.items()]
            raise ValueError((f"All features must have the same window periods. Found " f"{', '.join(periods)}"))
        self.window_periods_seconds = next(iter(fqn_to_windows.values()), ())
        # Mapping of window (in secs) to mapping of (original feature, windowed pseudofeature)
        self.windowed_pseudofeatures: Dict[int, Dict[Feature, Feature]] = {}
        self.window_index = None
        for i, w in enumerate(signature.params):
            if isinstance(w, StreamResolverParamMessageWindow):
                self.window_index = i
                break

        for window_period in self.window_periods_seconds:
            self.windowed_pseudofeatures[window_period] = {}
            for o in _flatten_features(self.output):
                if o.is_windowed:
                    windowed_fqn = get_name_with_duration(o.root_fqn, window_period)
                    windowed_feature = Feature.from_root_fqn(windowed_fqn)
                    self.windowed_pseudofeatures[window_period][o] = windowed_feature

    @property
    def output_features(self) -> Sequence[Feature]:
        return _flatten_features(self.output)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        from chalk._autosql.autosql import query_as_feature_formatted

        raw_result = self.fn(*args, **kwargs)
        if self.window_index is not None and isinstance(raw_result, str) and str(args[self.window_index]) in raw_result:
            raw_result = DataFrame(
                query_as_feature_formatted(
                    formatted_query=raw_result,
                    fqn_to_name={s.root_fqn: s.name for s in self.output_features},
                    table=args[self.window_index],
                )
            )

        return raw_result

    def __repr__(self):
        return f"StreamResolver(name={self.fqn})"


def _is_stream_resolver_body_type(annotation: Type):
    origin = get_origin(annotation)
    if origin is not None:
        return False
    return (
        isinstance(annotation, type) and issubclass(annotation, (str, bytes, BaseModel))
    ) or dataclasses.is_dataclass(annotation)


def _parse_stream_resolver_param(
    param: Parameter,
    annotation_parser: ResolverAnnotationParser,
    resolver_fqn_for_errors: str,
    is_windowed_resolver: bool,
) -> StreamResolverParam:
    if param.kind not in {Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' includes unsupported keyword or variadic arg '{param.name}'"
        )

    annotation = annotation_parser.parse_annotation(param.name)
    if isinstance(annotation, StateWrapper):
        if is_windowed_resolver:
            raise ValueError(
                f"Windowed stream resolvers cannot have state, but '{resolver_fqn_for_errors}' requires state."
            )
        default_value = get_state_default_value(
            state_typ=annotation.typ,
            declared_default=param.default,
            resolver_fqn_for_errors=resolver_fqn_for_errors,
            parameter_name_for_errors=param.name,
        )
        return StreamResolverParamKeyedState(
            name=param.name,
            typ=annotation.typ,
            default_value=default_value,
        )

    if not is_windowed_resolver and _is_stream_resolver_body_type(annotation):
        return StreamResolverParamMessage(name=param.name, typ=annotation)

    if is_windowed_resolver and get_origin(annotation) in (list, List):
        item_typ = get_args(annotation)[0]
        if _is_stream_resolver_body_type(item_typ):
            return StreamResolverParamMessageWindow(name=param.name, typ=annotation)

    if (
        is_windowed_resolver
        and isclass(annotation)
        and (
            issubclass(annotation, pyarrow.Table)
            or annotation.__name__ in ("DataFrame", "DataFrameImpl", "SubclassedDataFrame")
        )
    ):
        # Using string comparison as polars may not be installed
        return StreamResolverParamMessageWindow(name=param.name, typ=annotation)

    raise ValueError(
        (
            f"Stream resolver parameter '{param.name}' of resolver '{resolver_fqn_for_errors}' is not recognized. "
            f"Message payloads must be one of `str`, `bytes`, or pydantic model class. "
            f"Keyed state parameters must be chalk.KeyedState[T]. "
            f"Received: {annotation}"
        )
    )


def parse_stream_resolver_params(
    user_func: Callable,
    *,
    resolver_fqn_for_errors: str,
    annotation_parser: ResolverAnnotationParser,
    is_windowed_resolver: bool,
) -> Sequence[StreamResolverParam]:
    sig = inspect.signature(user_func)
    params = [
        _parse_stream_resolver_param(p, annotation_parser, resolver_fqn_for_errors, is_windowed_resolver)
        for p in sig.parameters.values()
    ]

    uses_message_body = any(
        p for p in params if isinstance(p, (StreamResolverParamMessage, StreamResolverParamMessageWindow))
    )

    if not uses_message_body:
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' must take as input "
            + f"a pydantic model, `str`, or `bytes` representing the message body"
        )

    keyed_state_params = [p.name for p in params if isinstance(p, StreamResolverParamKeyedState)]
    if len(keyed_state_params) > 1:
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' includes more than one KeyedState parameter: {keyed_state_params}"
        )

    return params


def parse_stream_resolver_output_features(
    user_func: Callable,
    *,
    resolver_fqn_for_errors: str,
) -> Type[Features]:
    return_annotation = get_type_hints(user_func).get("return")
    if return_annotation is None:
        raise TypeError(
            (
                f"Resolver '{user_func.__name__}' must have a return annotation. See "
                f"https://docs.chalk.ai/docs/resolver-outputs for "
                f"more information."
            )
        )

    if not isinstance(return_annotation, type):
        raise TypeError(f"return_annotation {return_annotation} of type {type(return_annotation)} is not a type")

    if issubclass(return_annotation, DataFrame):
        return Features[return_annotation]

    if not issubclass(return_annotation, Features):
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' did not have a valid return type: "
            + f"must be a features class or chalk.features.Features[]"
        )

    # TODO: validate that these features are in the same namespace and include a pkey
    output_features = cast(Type[Features], return_annotation)

    return output_features


def parse_and_register_stream_resolver(
    *,
    caller_globals: Optional[Dict[str, Any]],
    caller_locals: Optional[Dict[str, Any]],
    fn: Callable[P, T],
    source: StreamSource,
    caller_filename: str,
    mode: Optional[str] = None,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
    message: Optional[Type[Any]] = None,
) -> StreamResolver[P, T]:
    fqn = f"{fn.__module__}.{fn.__name__}"
    annotation_parser = ResolverAnnotationParser(fn, caller_globals, caller_locals)
    output_features = parse_stream_resolver_output_features(
        fn,
        resolver_fqn_for_errors=fqn,
    )
    flattened_output_features = (
        df.columns
        if len(output_features.features) == 1
        and isinstance(output_features.features[0], type)
        and issubclass(df := output_features.features[0], DataFrame)
        else output_features.features
    )
    is_windowed_resolver = any(x.is_windowed for x in flattened_output_features)
    params = parse_stream_resolver_params(
        fn,
        resolver_fqn_for_errors=fqn,
        annotation_parser=annotation_parser,
        is_windowed_resolver=is_windowed_resolver,
    )

    if isinstance(output_features.features[0], type) and issubclass(output_features.features[0], DataFrame):
        output_feature_fqns = set(f.fqn for f in cast(Type[DataFrame], output_features.features[0]).columns)
    else:
        output_feature_fqns = set(f.fqn for f in output_features.features)

    signature = StreamResolverSignature(
        params=params,
        output_feature_fqns=output_feature_fqns,
    )

    resolver = StreamResolver(
        caller_globals=caller_globals,
        caller_locals=caller_locals,
        caller_filename=caller_filename,
        source=source,
        mode=mode,
        fn=fn,
        environment=None if environment is None else list(ensure_tuple(environment)),
        machine_type=machine_type,
        signature=signature,
        output=output_features,
        message=message,
    )

    StreamResolver.registry.append(resolver)
    return resolver
