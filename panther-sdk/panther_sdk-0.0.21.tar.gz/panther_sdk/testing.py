# Copyright (C) 2022 Panther Labs, Inc.
#
# The Panther SaaS is licensed under the terms of the Panther Enterprise Subscription
# Agreement available at https://panther.com/enterprise-subscription-agreement/.
# All intellectual property rights in and to the Panther SaaS, including any and all
# rights to access the Panther SaaS, are governed by the Panther Enterprise Subscription Agreement.

# coding=utf-8
# *** WARNING: generated file
import ast
import typing
import unittest
import inspect

from panther_core import PantherEvent
from panther_core.snapshots import snapshot_func
from . import detection

__all__ = ["PantherPythonFilterTestCase"]


class PantherPythonFilterTestCase(unittest.TestCase):
    def _parseFilterFunc(self, pfilter: detection.PythonFilter) -> typing.Any:
        func_src, errors = snapshot_func(pfilter.func)

        self.assertEqual(0, len(errors), errors)

        sourcefile = inspect.getsourcefile(pfilter.func) or ""
        root_ast = ast.parse(func_src, filename=sourcefile, mode="exec")

        ns = dict(typing=typing)
        exec(ast.unparse(root_ast), ns)
        func = typing.cast(
            typing.Callable[[PantherEvent], bool], ns[pfilter.func.__name__]
        )
        return func

    def _callParsedFilterFunc(
        self, pfilter: detection.PythonFilter, evt: PantherEvent
    ) -> typing.Any:
        func = self._parseFilterFunc(pfilter)
        return func(evt)

    def assertFilterIsValid(self, test_filter: detection.PythonFilter) -> None:
        self.assertIsInstance(
            test_filter,
            detection.PythonFilter,
            "filter is not an instance of PythonFilter",
        )

        try:
            func = self._parseFilterFunc(test_filter)
        except BaseException as err:
            self.fail(f"unable to parse func value: {err}")

        self.assertTrue(callable(func), "parsed filter is not callable")

    def assertFilterMatches(
        self, test_filter: detection.PythonFilter, obj: typing.Any
    ) -> None:
        evt = PantherEvent(obj, data_model=None)
        unparsed_result = test_filter.func(evt)
        self.assertTrue(unparsed_result)

        parsed_result = self._callParsedFilterFunc(test_filter, evt)
        self.assertEqual(
            unparsed_result,
            parsed_result,
            "result from parsed version of filter does not match unparsed result",
        )

    def assertFilterNotMatches(
        self, test_filter: detection.PythonFilter, obj: typing.Any
    ) -> None:
        evt = PantherEvent(obj, data_model=None)
        unparsed_result = test_filter.func(evt)
        self.assertFalse(unparsed_result)

        parsed_result = self._callParsedFilterFunc(test_filter, evt)
        self.assertEqual(
            unparsed_result,
            parsed_result,
            "result from parsed version of filter does not match unparsed result",
        )
