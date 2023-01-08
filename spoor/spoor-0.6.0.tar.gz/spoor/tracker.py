import operator
import types
import typing
from abc import ABC
from collections import deque
from functools import update_wrapper
from typing import Callable, List, Optional

from varname import varname

from spoor.exporter import Exporter
from spoor.statistics import FuncCall, TopCalls
from spoor.storage import MemoryStorage, Storage
from spoor.utils import logger


class CallableWrapper(ABC):
    pass


# NOTE: at runtime, isinstance(x, T) will raise TypeError
WrapperType = typing.TypeVar("WrapperType", bound=CallableWrapper)


class Spoor:
    def __init__(
        self,
        storage: Optional[Storage] = None,
        exporters: Optional[List[Exporter]] = None,
        attach: bool = False,
        distinct_instances: bool = False,
        skip_dunder: bool = True,
        disabled: bool = False,
    ):
        self.attach = attach
        self.distinct_instances = distinct_instances
        self.skip_dunder = skip_dunder
        self._disabled = disabled
        self.storage = storage or MemoryStorage()
        self.exporters = exporters or []

    @property
    def enabled(self) -> bool:
        return not self._disabled

    def enable(self):
        self._disabled = False

    def disable(self):
        self._disabled = True

    def track(self, target):
        if isinstance(target, types.FunctionType):
            return self._decorate_function(target)
        elif isinstance(target, type):
            if self.attach:
                raise NotImplementedError("Attach for methods does not work yet")

            if self.distinct_instances:

                def new(cls, *args, **kwargs):
                    instance = object.__new__(cls)
                    instance._spoor_name = varname()
                    return instance

                setattr(target, "__new__", new)
            return self._decorate_methods(target)
        else:
            # TODO: add track by import path
            raise ValueError(f"Cannot track instance of {type(target)}")

    def _export(self, target: WrapperType):
        for e in self.exporters:
            key = target.name
            e.send(key=key)

    def __getitem__(self, func_id: CallableWrapper) -> FuncCall:
        if not self._is_tracked(func_id=func_id):
            obj_name = getattr(func_id, "__name__", str(func_id))
            raise KeyError(f"{obj_name} is not tracked")

        key = self._get_key(func_id)
        call_count = self.storage.get_value(key)
        func_call = FuncCall(
            name=func_id.name,
            called=bool(call_count),
            call_count=call_count,
        )
        return func_call

    def __del__(self):
        """
        Flush all the exporters
        """
        logger.debug("Flusing all the exporters and garbage collection")
        deque(
            map(operator.methodcaller("flush"), self.exporters),
            maxlen=0,
        )

    def _get_func_wrapper_cls(self, is_method: bool = False) -> WrapperType:
        """
        NOTE: We cannot attach a property on a function object,
        so class-based callable wrapper is used instead
        """
        spoor = self

        class Wrapper(CallableWrapper):
            """
            NOTE: should be nested class to be able expose properties on some
            wrapped objects and hide on others
            """

            def __init__(self, func: Callable, instance=None):
                self._func = func
                self._bound_instance = instance
                update_wrapper(self, func)

            # TODO: override `__new__` to register name on object creation

            def __call__(self, *args, **kwargs):
                instance = self._bound_instance
                if spoor.enabled:
                    target = self
                    if is_method:
                        #  is set by `wraps` decorator
                        method_name = self.__name__
                        target = self._func
                        if spoor.distinct_instances and instance is not None:
                            target = getattr(instance, method_name)

                    logger.debug(f"Tracking {target}")
                    # TODO: set name on initial register step
                    key = spoor._get_key(target)
                    spoor.storage.set_name(key, self.name)
                    spoor.storage.inc(key)
                    spoor._export(target)

                if is_method and instance is not None:
                    return self._func(instance, *args, **kwargs)
                return self._func(*args, **kwargs)

            @property
            def name(self) -> str:
                instance = self._bound_instance
                # is set by `wraps` decorator
                func_name = self.__name__
                if is_method:
                    # NOTE: below would not work for unbound methods
                    # class_name = instance.__class__.__name__
                    class_name = self._func.__qualname__.split(".")[-2]
                    alias = f"{class_name}.{func_name}"
                    # NOTE: bound instance is not None, use variable name
                    if spoor.distinct_instances and instance is not None:
                        instance_name = instance._spoor_name
                        alias = f"{instance_name}.{func_name}"
                    return alias

                return func_name

            def __str__(self) -> str:
                return f"(S) {self.name}[{self.__hash__()}]"

            def __get__(self, instance, cls):
                """
                Handle method binding
                """
                if is_method:
                    # NOTE: return bound method
                    logger.debug(f"Bound to {instance}")
                    return Wrapper(self._func, instance=instance)

                # TODO: how to test this path
                return self

            def __hash__(self):
                if spoor.distinct_instances and self._bound_instance is not None:
                    return hash(self._bound_instance)

                return hash(self._func)

        return Wrapper

    def _decorate_function(self, func: Callable, is_method: bool = False) -> Callable:
        WrapperClass = self._get_func_wrapper_cls(is_method=is_method)
        inner = WrapperClass(func)
        # NOTE: add function to the registry
        if self.attach:
            setattr(inner.__class__, "called", property(self.called))
            setattr(inner.__class__, "call_count", property(self.call_count))

        return inner

    def _is_dunder(self, name: str) -> bool:
        return name.startswith("__") and name.endswith("__")

    def _is_tracked(self, func_id) -> bool:
        return isinstance(func_id, CallableWrapper) and issubclass(
            func_id.__class__, CallableWrapper
        )

    def _decorate_methods(self, klass):
        """
        These are not methods yet, there is no instance created to bound to
        """
        for key in klass.__dict__:
            method = klass.__dict__[key]
            skip_method = self.skip_dunder and self._is_dunder(key)
            if isinstance(method, types.FunctionType) and not skip_method:
                logger.debug(f"Wrapping method {method}")
                decorated = self._decorate_function(method, is_method=True)
                setattr(klass, key, decorated)

        return klass

    def _get_key(self, func_id: WrapperType):
        # NOTE: try just func_id
        return hash(func_id)

    def called(self, func_id) -> bool:
        return self.call_count(func_id) != 0

    def call_count(self, func_id) -> int:
        key = self._get_key(func_id)
        count = self.storage.get_value(key)
        logger.debug(f"Calls count {func_id} = {count}")
        return count

    def topn(self, n: int = 5) -> TopCalls:
        data = self.storage.most_common(top_n=n)
        return TopCalls(data)
