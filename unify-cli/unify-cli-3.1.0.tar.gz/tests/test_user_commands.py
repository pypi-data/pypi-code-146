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
from source.cluster.commands import disconnect_cluster
from source.cluster.commands import login
from source.user.commands import service_account_add

from tests.properties import Properties

from tests import test_org
from tests import test_pipeline


class UserTestCases(unittest.TestCase):

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

    def test_service_account_add_admin(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--service_account_name", str(uuid.uuid4()),
            "--service_account_id", str(uuid.uuid4()),
            "--service_account_password", str(uuid.uuid4()),
            "--role", 'Admin'
        ]
        add_user_result = self.runner.invoke(service_account_add, params)

        self.assertEqual(add_user_result.exit_code, 0, add_user_result.output)

    def test_service_account_add_contributor(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--service_account_name", str(uuid.uuid4()),
            "--service_account_id", str(uuid.uuid4()),
            "--service_account_password", str(uuid.uuid4()),
            "--role", 'Contributor'
        ]

        add_user_result = self.runner.invoke(service_account_add, params)

        self.assertEqual(add_user_result.exit_code, 0, add_user_result.output)

    def test_service_account_add_invalid(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--service_account_name", str(uuid.uuid4()),
            "--service_account_id", str(uuid.uuid4()),
            "--service_account_password", str(uuid.uuid4()),
            "--role", str(uuid.uuid4())
        ]

        add_user_result = self.runner.invoke(service_account_add, params)

        self.assertNotEquals(add_user_result.exit_code, 0, add_user_result.output)

    @classmethod
    def tearDownClass(cls):
        cls.runner.invoke(disconnect_cluster, ["--remote", cls.cluster_name, "-y"])
