from functools import partial
from typing import Any, Callable, Optional, Tuple, Union
from logging import Logger



class SafeExecutor:

    def __init__(self, func=None, *args, **kwargs) -> None:
        self._args = args
        self._kwargs = kwargs
        self._func = func
        self._instance = None
        self.default = None
        self.logger: Optional[Logger] = None
        self.callback: Optional[Callable] = None
        self._read_class_kwargs()

    def _read_class_kwargs(self) -> None:
        if self._func:
            return
        for k,v in self._kwargs.items():
            conditions = (
                hasattr(self, k),
                not k.startswith('_'),
                k != 'args',
                k != 'kwargs',
                k != 'func'
            )
            if all(conditions):
                setattr(self, k, v)
        self._args = tuple()
        self._kwargs = dict()

    def _fix_args(self, args: Tuple[Any]) -> Tuple[Any]:
        if args:
            if args[0] != self._instance and self._instance:
                args = tuple([self._instance] + list(args))
        return args


    def __call__(self, *args, **kwargs) -> None:
        if args:
            if isinstance(args[0], Callable) and not self._instance:
                self._func = args[0]
                args = args[1:]
                def decorator(*a, **kw):
                    self._args, self._kwargs = a, kw
                    return self._run_func()
                return decorator
        self._args, self._kwargs = self._fix_args(args), kwargs
        return self._run_func()

    def __get__(self, instance:Union[object, type], owner:Optional[type]):
        self._instance = instance
        return partial(self, instance)

    def _process_error(self, err: str) -> None:
        if isinstance(self.logger, Logger):
            self.logger.error(f'Execute error: {err}')
        if isinstance(self.callback, Callable):
            try: self.callback(err)
            except:
                try: self.callback()
                except: self.callback()
        return self.default

    def _run_func(self):
        try: return self._func(*self._args, **self._kwargs)
        except Exception as err: return self._process_error(err)
