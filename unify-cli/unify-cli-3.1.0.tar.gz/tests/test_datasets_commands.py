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

from source.dataset.commands import add_dataset
from source.dataset.commands import add_big_dataset
from source.dataset.commands import append_dataset
from source.dataset.commands import list_dataset
from source.dataset.commands import split_bid_dataset

from tests.properties import Properties

from tests import test_org
from tests import test_dataset
import re


class DataSetsTestCases(unittest.TestCase):

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

    def test_add_dataset(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--name", str(uuid.uuid4()),
            open("tests/data_test.csv", "r+").read()
        ]

        add_dataset_result = self.runner.invoke(add_dataset, params)

        self.assertEqual(add_dataset_result.exit_code, 0, add_dataset_result.output)

        self.assertTrue("id" in add_dataset_result.output, add_dataset_result.output)

    def test_add_big_dataset(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--name", str(uuid.uuid4()),
            open("tests/data_test.csv", "r+").read()
        ]

        big_dataset_result = self.runner.invoke(add_big_dataset, params)

        self.assertEqual(big_dataset_result.exit_code, 0, big_dataset_result.output)

        self.assertTrue("id" in big_dataset_result.output, big_dataset_result.output)

    def test_append_dataset(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--datasetid", test_dataset["id"],
            open("tests/data_test.csv", "r+").read()
        ]

        append_dataset_result = self.runner.invoke(append_dataset, params)

        self.assertEqual(append_dataset_result.exit_code, 0, append_dataset_result.output)

        self.assertTrue("id" in append_dataset_result.output, append_dataset_result.output)

    def test_list_dataset(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org
        ]

        list_dataset_result = self.runner.invoke(list_dataset, params)

        self.assertEqual(list_dataset_result.exit_code, 0, list_dataset_result.output)

        self.assertTrue(test_dataset["id"] in list_dataset_result.output, list_dataset_result.output)

    def test_split_bid_dataset(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--name", str(uuid.uuid4()),
            "--chunks",10,
            open("tests/data_test.csv", "r+").read()
        ]

        split_bid_dataset_result = self.runner.invoke(split_bid_dataset, params)

        self.assertEqual(split_bid_dataset_result.exit_code, 0, split_bid_dataset_result.output)

        self.assertTrue("id" in split_bid_dataset_result.output, split_bid_dataset_result.output)

    @classmethod
    def tearDownClass(cls):
        cls.runner.invoke(disconnect_cluster, ["--remote", cls.cluster_name, "-y"])
