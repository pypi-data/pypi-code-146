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
from unify.helpers.Permissions import Verbs, Domains, Effects, DisplayNames

from source.utils.util_methods import get_piped_param
from source.common.commands import org_cluster_options


@click.group()
def rules():
    """

    Group for Element Unify Rules Permissions related commands
    :return: None
    """


@rules.command('list')
@org_cluster_options
@click.option('--table', '-t', is_flag=True, help="Print in table")
def list_rules(remote, org, table):
    try:
        response = ApiManager(cluster=remote).get_rules_list(org_id=org)
        if table:
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@rules.command('pipeline')
@org_cluster_options
@click.option('--pipeline_id', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
def org_config(remote, org, pipeline_id):
    try:
        response = ApiManager(cluster=remote).get_pipeline_rules(org_id=org, pipeline_id=pipeline_id)
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@rules.command('dataset')
@org_cluster_options
@click.option('--dataset_id', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
def org_config(remote, org, dataset_id):
    try:
        response = ApiManager(cluster=remote).get_dataset_rules(org_id=org, dataset_id=dataset_id)
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@rules.command('delete')
@org_cluster_options
@click.option('--rule_id', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
def delete_rule(remote, org, rule_id):
    try:
        response = ApiManager(cluster=remote).delete_rule(
            org_id=org,
            rule_id=rule_id
        )

        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@rules.command('add')
@org_cluster_options
@click.option('--domain', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.Choice([v for v, m in vars(Domains).items() if not (v.startswith('_') or callable(m))]))
@click.option('--effect', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.Choice([v for v, m in vars(Effects).items() if not (v.startswith('_') or callable(m))]))
@click.option('--verb', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.Choice([v for v, m in vars(Verbs).items() if not (v.startswith('_') or callable(m))]))
@click.option('--user_selector', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.INT)
@click.option('--resource_selector', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.INT)
def add_rule(remote, org, domain, effect, verb, user_selector, resource_selector):
    try:
        response = ApiManager(cluster=remote).add_rule(
            org_id=org,
            domain=domain,
            verb=verb,
            effect=effect,
            userSelector=user_selector,
            resourceSelector=resource_selector
        )

        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
