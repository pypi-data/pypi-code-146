# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import uuid
import unittest
from click.testing import CliRunner

from source.cluster.commands import add_cluster
from source.cluster.commands import login
from source.cluster.commands import disconnect_cluster
from source.template.commands import show_templates

from tests.properties import Properties

from tests import test_org
from tests import test_pipeline


class TemoplatesTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
        cls.cluster_name = str(uuid.uuid4())[:4]
        cls.props = Properties()

        params = [
            "--remote", cls.props.api_url,
            "--username", cls.props.user_name,
            "--password", cls.props.user_password,
            "--name", cls.cluster_name,
            "--assetsync", True
        ]

        cls.runner.invoke(add_cluster, params)

        cls.runner.invoke(login, ["--remote", cls.cluster_name])

    def test_show_templates(self):
        query_command = "--remote {} --org {}".format(self.cluster_name, test_org)

        templates_list = self.runner.invoke(show_templates, query_command)

        self.assertEqual(templates_list.exit_code, 0, templates_list.output)

    @classmethod
    def tearDownClass(cls):
        cls.runner.invoke(disconnect_cluster, ["--remote", cls.cluster_name, "-y"])
