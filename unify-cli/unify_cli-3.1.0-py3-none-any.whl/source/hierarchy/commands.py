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

from tabulate import tabulate
from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json
from source.common.commands import org_cluster_options


@click.group()
def hierarchy():
    """Group for hierarchy commands"""


@hierarchy.command('list')
@org_cluster_options
def get_hierarchies(org, remote):
    try:
        response = ApiManager(cluster=remote).get_all_hierarchies_display(org=org)
        click.echo(click.style(tabulate(tabulate_from_json(response), "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@hierarchy.command('get')
@org_cluster_options
@click.option('--hierarchy', prompt=False, hide_input=False, required=True, confirmation_prompt=False,
              type=click.INT)
def get_hierarchy(org, remote, hierarchy):
    try:
        response = ApiManager(cluster=remote).get_single_hierarchy(org, hierarchy)
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@hierarchy.command('create')
@org_cluster_options
@click.option('--name', prompt=False, hide_input=False, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--level', multiple=True, required=False, default=[])
@click.option('--private', prompt=False, hide_input=False, default=False, required=False, confirmation_prompt=False,
              type=click.BOOL)
def get_hierarchies(org, remote, name, level, private):
    try:
        response = ApiManager(cluster=remote).create_hierarchy(
            org=org,
            name=name,
            levels=level,
            private=private
        )
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
