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
from source.access.commands import get_databases
from source.access.commands import execute_query
from tests.properties import Properties

from tests import test_org
from tests import test_dataset


class AssetAccessTestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
        cls.cluster_name = str(uuid.uuid4())[:10]
        cls.props = Properties()

        confi = '--remote "{}" --username "{}" --password "{}" --name "{}" --assetsync True'.format(
            cls.props.api_url,
            cls.props.user_name,
            cls.props.user_password,
            cls.cluster_name
        )

        cls.runner.invoke(add_cluster, confi)

    def test_get_databases(self):
        query_command = "--remote {} --org {}".format(self.cluster_name, test_org)

        data_bases = self.runner.invoke(get_databases, query_command)

        self.assertEqual(data_bases.exit_code, 0, data_bases.output)

    def test_sql_query(self):
        table_name = "{}_{}".format(test_dataset["name"], test_dataset["id"][:4])

        query_command = "--remote {} --org {} 'SELECT * FROM {}'".format(self.cluster_name, test_org, table_name)

        sql_results = self.runner.invoke(execute_query, query_command)

        self.assertEqual(sql_results.exit_code, 0, sql_results.output)
