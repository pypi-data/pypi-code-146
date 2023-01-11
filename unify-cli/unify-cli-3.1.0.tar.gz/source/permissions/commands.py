#!/usr/bin/env python

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

import click
import json

from tabulate import tabulate

from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json
from unify.permissions import Permissions

from source.utils.util_methods import get_piped_param
from source.common.commands import org_cluster_options

from source.permissions.rules.commands import rules as rules_group
from source.permissions.selectors.commands import selectors as selectors_group


@click.group()
def permissions():
    """

    Group for Element Unify Permissions related commands
    :return: None
    """


permissions.add_command(rules_group)

permissions.add_command(selectors_group)


@permissions.command('org-config')
@org_cluster_options
def org_config(remote, org):
    try:
        response = ApiManager(cluster=remote).get_permissions_org_config(org_id=org)
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@permissions.command('check')
@org_cluster_options
@click.option('--artifact_id', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
@click.option('--artifact_type', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
@click.option('--user_id', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
@click.option('--verb', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
def check_permission(remote, org, artifact_id, artifact_type, user_id, verb):
    try:
        response = ApiManager(cluster=remote).check_permission(
            org_id=org,
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            user_id=user_id,
            verb=verb
        )
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
