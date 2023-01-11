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
from source.org.commands import org_add
from source.cluster.commands import add_cluster
from source.cluster.commands import login
from tests.properties import Properties
import uuid
import re

def test_org_add():
    runner = CliRunner()

    props = Properties()

    cluster_name = "qa"
    org_name = "zQA-CLI-{}".format(uuid.uuid4())

    confi = '--remote "{}" --username "{}" --password "{}" --name "{}" --assetsync True'.format(
        props.api_url,
        props.user_name,
        props.user_password,
        cluster_name
    )

    runner.invoke(add_cluster, confi)

    runner.invoke(login, '--remote "{}"'.format(cluster_name))

    org_add_results = runner.invoke(org_add, '--name "{}" --remote {}'.format(org_name, cluster_name))

    reg_number = re.compile(r'\d+')

    assert reg_number.match(org_add_results.output)
