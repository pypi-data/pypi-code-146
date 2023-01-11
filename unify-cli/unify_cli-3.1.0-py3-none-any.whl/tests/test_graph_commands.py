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
from source.graph.commands import list_graphs
from source.graph.commands import query_graphs

from tests.properties import Properties

from tests import test_org
from tests import test_pipeline
import re


class GraphV2TestCases(unittest.TestCase):

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

    def test_graph_list(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org
        ]

        graph_list_all = self.runner.invoke(list_graphs, params)

        self.assertEqual(graph_list_all.exit_code, 0, graph_list_all.output)

        self.assertEquals(len(json.loads(graph_list_all.output)), 0, graph_list_all.output)

    def test_query_graphs(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--graph", str(uuid.uuid4()),
            "MATCH (n)-[r]->(g) RETURN *"
        ]

        query_results = self.runner.invoke(query_graphs, params)

        self.assertEqual(query_results.exit_code, 0, query_results.output)
        self.assertTrue("code" in query_results.output, query_results.output)


    @classmethod
    def tearDownClass(cls):
        cls.runner.invoke(disconnect_cluster, ["--remote", cls.cluster_name, "-y"])
