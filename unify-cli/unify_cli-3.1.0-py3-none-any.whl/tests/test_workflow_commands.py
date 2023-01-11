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
from tests.properties import Properties

from source.workflow.commands import export_template
from source.workflow.commands import import_template
from source.workflow.commands import export_pipeline
from source.workflow.commands import import_pipeline

from tests import test_org
from tests import test_pipeline
import re


class WorkFlowTestCases(unittest.TestCase):

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

    def test_export_template(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org
        ]

        export_template_res = self.runner.invoke(export_template, params)

        self.assertEqual(export_template_res.exit_code, 0, export_template_res.output)

    def test_import_template(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org
        ]

        export_template_res = self.runner.invoke(export_template, params)

        self.assertEqual(export_template_res.exit_code, 0, export_template_res.output)

        params.append(export_template_res.output)

        import_template_res = self.runner.invoke(import_template, params)

        self.assertEqual(import_template_res.exit_code, 0, import_template_res.output)

    def test_export_pipeline(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--pipeline", test_pipeline["pipeline"]["id"],
        ]

        export_pipeline_res = self.runner.invoke(export_pipeline, params)

        self.assertEqual(export_pipeline_res.exit_code, 0, export_pipeline_res.output)

        self.assertTrue(str(test_pipeline["pipeline"]["id"]) in export_pipeline_res.output)

    def test_import_pipeline(self):
        params = [
            "--remote", self.cluster_name,
            "--org", test_org,
            "--pipeline", test_pipeline["pipeline"]["id"],
        ]

        export_pipeline_res = self.runner.invoke(export_pipeline, params)

        self.assertEqual(export_pipeline_res.exit_code, 0, export_pipeline_res.output)

        params_import = [
            "--remote", self.cluster_name,
            "--org", test_org,
            export_pipeline_res.output
        ]

        import_pipeline_res = self.runner.invoke(import_pipeline, params_import)

        self.assertEqual(import_pipeline_res.exit_code, 0, import_pipeline_res.output)

        self.assertTrue("pipeline_id" in import_pipeline_res.output, import_pipeline_res.output)
        self.assertTrue("org_id" in import_pipeline_res.output, import_pipeline_res.output)
        self.assertTrue("url" in import_pipeline_res.output, import_pipeline_res.output)

    @classmethod
    def tearDownClass(cls):
        cls.runner.invoke(disconnect_cluster, ["--remote", cls.cluster_name, "-y"])
