#!/usr/bin/env python
# -*- coding:utf-8 -*-
import abc
import inspect
import json
from locale import getpreferredencoding
from pathlib import Path
from subprocess import PIPE, Popen, run
from time import time
from typing import Any, IO, Dict

from ..char import String, StringBuilder
from ..classes import StaticClass
from ..exceptions import TimeoutExpiredException, raise_exception
from ..log import LoggerFactory
from ..utils import StringUtils, ObjectsUtils

_logger = LoggerFactory.get_logger("command")

_encoding = getpreferredencoding(False)

_stack = inspect.stack()


class Command(metaclass=StaticClass):
    """
    Command-line utility classes.
    Two execution methods are provided, one is runtime (native subprocess.run).
    The other is the exec execution method of this tool extension, which supports the input of interactive instructions.
    """

    @staticmethod
    def exec(cmd, cwd: str or Path = None, timeout: int = None, encoding: str = None, **kwargs) -> '_Executor':
        """
        Execute the command
        :param encoding: encode
        :param cmd: commandline
        :param cwd: working directory
        :param timeout: timeout, default block thread
        """
        return _Executor(cmd, cwd=cwd, timeout=timeout, encoding=encoding, **kwargs)

    @staticmethod
    def run(*popenargs, cwd: str or Path = None, input_=None, capture_output=False, timeout=None, check=False,
            encoding: str = None, **kwargs) -> '_Runner':
        """
        subprocess run method
        """
        return _Runner(*popenargs, cwd=cwd, input=input_, capture_output=capture_output, timeout=timeout, check=check,
                       encoding=encoding, **kwargs)


class _AbstractCommand(metaclass=abc.ABCMeta):

    def __setattr__(self, key, value):
        if __file__ != _stack[0].filename:
            raise_exception(RuntimeError("can't set"))
        self.__dict__[key] = value

    def __init__(self, kwargs: Dict):
        self.__out = ""
        self.__err = ""
        if "stdin" not in kwargs:
            kwargs["stdin"] = PIPE
        if "stdout" not in kwargs:
            kwargs["stdout"] = PIPE
        if "stderr" not in kwargs:
            kwargs["stderr"] = PIPE
        self.__input_log_builder: StringBuilder = StringBuilder(start="\n")

    def __show_log(self):
        input_msg = self.__input_log_builder.string(lambda i, v: f'\t({i}) interactive input => {v}\n')
        log_content = f"""
{'Command START'.center(81, '*')}
Command line              => {self.__args}
{'' if StringUtils.is_empty(input_msg) else input_msg}
Command exit code         => {self.__code}\n
Command Out               => \n{self.__out}\n
Command err               => \n{self.__err}
{'Command END'.center(83, '*')}
"""
        _logger.info(log_content)

    @abc.abstractmethod
    def finish(self):
        self.__show_log()

    def __build(self, args, code: int, out: str, err: str):
        self.__args = args
        self.__code: int = code
        self.__out: str = ObjectsUtils.none_of_default(out, "")
        self.__err: str = ObjectsUtils.none_of_default(err, "")
        # noinspection PyBroadException
        try:
            self.__out_dict = json.loads(self.__out)
        except BaseException:
            self.__out_dict = {}
        # noinspection PyBroadException
        try:
            self.__err_dict = json.loads(self.__err)
        except BaseException:
            self.__err_dict = {}

    @property
    def args(self):
        return self.__args

    @property
    def code(self) -> int:
        """
        Returns the exit code after executing the command
        """
        return self.__code

    @property
    def out(self) -> String:
        """
        Returns standard output
        """
        return String(self.__out)

    @property
    def out_to_dict(self) -> Dict:
        """
        Converts command-line standard output to dict
        """
        return self.__out_dict

    @property
    def err(self) -> String:
        """
        Returns standard error
        """
        return String(self.__err)

    @property
    def err_to_dict(self) -> Dict:
        """
        Convert command-line standard error to dict
        """
        return self.__out_dict

    @property
    def is_success(self) -> bool:
        """
        Determine whether the command line is executed successfully
        """
        return self.__code == 0

    @property
    def is_fail(self) -> bool:
        """
        Determine whether the command line is executed failed
        """
        return not self.is_success

    @property
    def out_is_empty(self) -> bool:
        """
        Determine whether the standard output is blank
        """
        return StringUtils.is_empty(self.__out)

    @property
    def out_is_not_empty(self) -> bool:
        """
        Judge that the standard output is not blank
        """
        return not self.out_is_empty

    def out_contain(self, value: Any) -> bool:
        """
        Judge that the standard output contains a value
        """
        return StringUtils.contains(self.__out, str(value))

    def out_not_contain(self, value: Any) -> bool:
        """
        The criterion output does not contain a value
        """
        return not self.out_contain(str(value))

    def out_trip_contain(self, value: Any) -> bool:
        """
        Judgment standard output contains values (after removing leading and trailing spaces)
        """
        return StringUtils.trip_contains(self.__out, str(value))

    def out_trip_not_contain(self, value: Any) -> bool:
        """
        Judgment standard output does not contain values (after removing leading and trailing spaces)
        """
        return not self.out_trip_contain(str(value))

    def out_equal(self, value: Any) -> bool:
        """
        Judge that the standard output is equal to the value
        """
        return str(value) == self.__out

    def out_not_equal(self, value: Any) -> bool:
        """
        Determine that the standard output is not equal to the value
        """
        return not self.out_equal(str(value))

    def out_trip_equal(self, value: Any) -> bool:
        """
        Judge that the standard output is equal to the value (after removing the leading and trailing spaces)
        """
        return str(value).strip() == self.__out.strip()

    def out_trip_not_equal(self, value: Any) -> bool:
        """
        Judge that the standard output is not equal to the value (after removing the leading and trailing spaces)
        """
        return not self.out_trip_equal(str(value))

    @property
    def err_is_empty(self) -> bool:
        """
        The criterion error is blank
        """
        return StringUtils.is_empty(self.__err)

    @property
    def err_is_not_empty(self) -> bool:
        """
        Criterion errors are not blank
        """
        return not self.err_is_empty

    def err_contain(self, value: Any) -> bool:
        """
        The criterion error contains a value
        """
        return StringUtils.contains(self.__err, str(value))

    def err_not_contain(self, value: Any) -> bool:
        """
        The criterion error does not contain a value
        """
        return not self.err_contain(str(value))

    def err_trip_contain(self, value: Any) -> bool:
        """
        Judgment criterion error contains value (after removing leading and trailing spaces)
        """
        return StringUtils.trip_contains(self.__err, str(value))

    def err_trip_not_contain(self, value: Any) -> bool:
        """
        Criterion error does not contain a value (after removing leading and trailing spaces)
        """
        return not self.err_trip_contain(str(value))

    def err_equal(self, value: Any) -> bool:
        """
        The criterion error is equal to the value
        """
        return str(value) == self.__err

    def err_not_equal(self, value: Any) -> bool:
        """
        The criterion error is not equal to the value
        """
        return not self.err_equal(str(value))

    def err_trip_equal(self, value: Any) -> bool:
        """
        The criterion error is equal to the value (after removing the leading and trailing spaces)
        """
        return str(value).strip() == self.__err.strip()

    def err_trip_not_equal(self, value: Any) -> bool:
        """
        The criterion error is not equal to the value (after removing the leading and trailing spaces, it is judged)
        """
        return not self.err_trip_equal(str(value))


class _Executor(_AbstractCommand):
    def __init__(self, cmd, cwd: Path or str = None, timeout: int = None, encoding: str = None, **kwargs):
        super().__init__(kwargs)
        self.__process = Popen(cmd, cwd=ObjectsUtils.none_of_default(cwd, Path.cwd()),
                               shell=True, universal_newlines=True,
                               encoding=ObjectsUtils.none_of_default(encoding, _encoding), **kwargs)
        self.__timeout: int = timeout if issubclass(type(timeout), int) and timeout > 0 else None

    def input(self, content: str) -> '_Executor':
        if not isinstance(content, str):
            raise TypeError("need str type params")
        self._AbstractCommand__input_log_builder.append(content)
        self.__process.stdin.write(content)
        self.__process.stdin.write("\n")
        self.__process.stdin.flush()
        return self

    def finish(self) -> '_Executor':
        t1 = time()
        while self.__process.poll() is None:
            if self.__timeout and time() - t1 > self.__timeout:
                self.__process.kill()
                raise_exception(TimeoutExpiredException("exec commandline timeout!!!"))
        self._AbstractCommand__build(self.__process.args, self.__process.returncode,
                                     self.__read(self.__process.stdout),
                                     self.__read(self.__process.stderr))
        self.__process.stdin.close()
        super(_Executor, self).finish()
        return self

    @staticmethod
    def __read(stream: IO):
        result = stream.read()
        stream.close()
        return result


class _Runner(_AbstractCommand):
    def __init__(self, *popenargs, cwd: str or Path = None, input_=None, capture_output=False, timeout=None,
                 check=False, encoding: str = _encoding, **kwargs):
        super().__init__(kwargs)
        kwargs["shell"] = True
        kwargs["cwd"] = ObjectsUtils.none_of_default(cwd, Path.cwd())
        kwargs["input"] = input_
        kwargs["capture_output"] = capture_output
        kwargs["timeout"] = timeout
        kwargs["check"] = check
        encoding = ObjectsUtils.none_of_default(encoding, _encoding)
        self.__result = run(*popenargs, encoding=encoding, **kwargs)

    def finish(self) -> '_Runner':
        self._AbstractCommand__build(self.__result.args, self.__result.returncode, self.__result.stdout, self.__result.stderr)
        super(_Runner, self).finish()
        return self


__all__ = [Command]
