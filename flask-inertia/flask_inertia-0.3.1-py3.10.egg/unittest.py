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
Unit tests tools for flask-inertia
----------------------------------
"""

import json
from types import SimpleNamespace

from flask import Response


class InertiaTestResponse(Response):
    """Inertia test response wrapper.

    You can use it in your unit test cases as followed::

    .. code-block:: python

        from inertia.unittest import InertiaTestResponse

        class MyTestCase(unittest.TestCase):

            def setUp(self):
                self.app = create_app()  # if you use an application factory
                self.app.response_class = InertiaTestResponse
                self.client = self.app.test_client()

            def test_lambda(self):
                response = self.client.get("/")
                data = response.inertia("root-id")
    """

    def inertia(self, root_id: str) -> SimpleNamespace:
        """Access inertia data stored in html page.

        Parse flask html response to extract inertia data stored in the
        root component `data-page` attribute. It will parse the page JSON
        object and convert into a Python object using `SimpleNamespace`.

        :param root_id: Root component html id
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(self.data, features="html.parser")
            root = soup.find(id=root_id)
            return json.loads(
                root.get("data-page", "{}"),
                object_hook=lambda d: SimpleNamespace(**d),
            )
        except ImportError as err:
            err.msg = "\n".join(
                [
                    err.msg,
                    "flask-inertia needs BeautifulSoup to parse html messages in tests, ",
                    "please install it using `pip install flask-inertia[tests]`",
                ]
            )
            raise err
