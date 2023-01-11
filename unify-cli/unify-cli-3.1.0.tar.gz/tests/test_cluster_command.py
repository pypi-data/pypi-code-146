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
from source.cluster.commands import list_cluster
from source.cluster.commands import add_cluster
from source.cluster.commands import login
from tests.properties import Properties
import json


def test_cluster_tags_correct():
    runner = CliRunner()
    r = runner.invoke(add_cluster,
                      '--remote "https://staging-qa-integration-001.ean.io/" --username "FAKE_USERNAME" --password "FAKE_PASSOWRD" --name "qa" --assetsync True')
    result = runner.invoke(list_cluster)
    assert "https://staging-qa-integration-001.ean.io/" in result.output


def test_cli_help():
    str_tags = "--help  Show this message and exit."
    runner = CliRunner()
    result = runner.invoke(cli, '--help')

    assert result.output.find(str_tags) != -1


def test_cluster_add_help():
    str_tags = "Store a new cluster information"
    runner = CliRunner()
    result = runner.invoke(add_cluster, '--help')
    assert result.output.find(str_tags) != -1


def test_cluster_list_help():
    str_tags = "List all the cluster the user has stored on this machine"
    runner = CliRunner()
    result = runner.invoke(list_cluster, '--help')
    assert result.output.find(str_tags) != -1


def test_cluster_add():
    props = Properties()
    runner = CliRunner()
    res = runner.invoke(add_cluster,
                        '--remote "{}" --username "{}" --password "{}" --name "qa" --assetsync True'.format(
                            props.api_url,
                            props.user_name,
                            props.user_password))
    result = runner.invoke(list_cluster)
    assert props.api_url in result.output


def test_cluster_not_empty():
    props = Properties()
    runner = CliRunner()
    res = runner.invoke(add_cluster,
                        '--remote "{}" --username "{}" --password "{}" --name "qa" --assetsync True'.format(
                            props.api_url,
                            props.user_name,
                            props.user_password))
    assert res is not None


def test_cluster_login_correct_credentials():

    runner = CliRunner()

    props = Properties()

    runner.invoke(
        add_cluster,
        '--remote "{}" --username "{}" --password "{}" --name "qa" --assetsync True'.format(
            props.api_url,
            props.user_name,
            props.user_password
        )
    )

    result = runner.invoke(login, '--remote qa ')
    assert result.output == ""


def test_cluster_login_incorrect_credentials():
    props = Properties()

    runner = CliRunner()

    cluster = "qa"

    runner.invoke(
        add_cluster,
        '--remote "{}" --username "{}" --password "{}" --name "{}" --assetsync True'.format(
            props.api_url,
            "FAKE_USERNAME",
            "FAKE_PASSWORD",
            cluster
        )
    )

    result = runner.invoke(login, '--remote "{}"'.format(cluster))

    assert "Authentication failed" in result.output
