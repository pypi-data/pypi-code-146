#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2021 TROUVERIE Joachim <jtrouverie@joakode.fr>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Flask-Inertia test case class
-----------------------------
"""

from typing import Any
from functools import partialmethod
from unittest import TestCase

from flask import Response
from flask_inertia.tests import get_response_data


class InertiaTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertInertiaEqual = partialmethod(cls._assertInertiaEquality, func=cls.assertEqual)
        cls.assertInertiaNotEqual = partialmethod(cls._assertInertiaEquality, func=cls.assertNotEqual)
        cls.assertInertiaTrue = partialmethod(cls._assertInertiaExpr, func=cls.assertTrue)
        cls.assertInertiaFalse = partialmethod(cls._assertInertiaExpr, func=cls.assertFalse)
        cls.assertInertiaIsNone = partialmethod(cls._assertInertiaExpr, func=cls.assertIsNone)
        cls.assertInertiaIsNotNone = partialmethod(cls._assertInertiaExpr, func=cls.assertIsNotNone)

    def _assertInertiaEquality(
        self,
        flask_response: Response,
        root_id: str,
        data_path: str,
        expected: Any,
        **kwargs,
    ):
        response_data = get_response_data(flask_response, root_id)
        comp_func = kwargs.pop("func")
        data = getattr(response_data, data_path)
        comp_func(data, expected, **kwargs)

    def _assertInertiaExpr(
        self,
        flask_response: Response,
        root_id: str,
        data_path: str,
        **kwargs
    ):
        response_data = get_response_data(flask_response, root_id)
        expr_func = kwargs.pop("func")
        expr = getattr(response_data, data_path)
        expr_func(expr, **kwargs)
