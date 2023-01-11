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

from click.testing import CliRunner
from source.ah import cli
from source.workflow.commands import wf
from source.workflow.commands import import_pipeline
from source.cluster.commands import cluster


def test_command_help_cluster():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "cluster" in result.output
    assert "dataset" in result.output


def test_command_help_org():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "org" in result.output


def test_command_help_pipeline():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "pipeline" in result.output


def test_command_help_wf():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "wf" in result.output


def test_command_wf_export_pipeline():
    runner = CliRunner()
    result = runner.invoke(wf, ["--help"])
    assert result.exit_code == 0
    assert "export-pipeline" in result.output


def test_command_wf_import_pipeline():
    runner = CliRunner()
    result = runner.invoke(wf, ["--help"])
    assert result.exit_code == 0
    assert "import-pipeline" in result.output


def test_command_wf_import_pipeline_help_remote():
    runner = CliRunner()
    result = runner.invoke(import_pipeline, ["--help"])
    assert result.exit_code == 0
    assert "--remote" in result.output


def test_command_wf_import_pipeline_help_org():
    runner = CliRunner()
    result = runner.invoke(import_pipeline, ["--help"])
    assert result.exit_code == 0
    assert "--org" in result.output
