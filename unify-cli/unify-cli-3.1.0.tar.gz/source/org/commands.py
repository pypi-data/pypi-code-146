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

from unify.properties import Properties
from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json
from source.common.commands import cluster_options
from source.common.commands import org_cluster_options

from source.utils.util_methods import get_piped_param


@click.group()
def org():
    """
    Group for org related commands
    :return: none
    """


@org.command('list')
@click.option('--table', prompt=False, default=True, required=False, type=click.BOOL)
@cluster_options
def org_list(table, remote):
    try:
        response = ApiManager(cluster=remote).orgs.get_org_list()

        if table:
            response = tabulate_from_json(response)

        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@org.command('add')
@click.option('--name', prompt="Org Name", hide_input=False, confirmation_prompt=False, type=click.STRING)
@cluster_options
def org_add(name, remote):
    try:
        response = ApiManager(cluster=remote).orgs.create_organization(org_name=name)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@org.command('delete')
@org_cluster_options
def org_delete(org, remote):
    click.confirm('Do you want to delete org {}? this cant be undone '.format(org), abort=True)
    try:
        response = ApiManager(cluster=remote).orgs.delete_organization(org_id=org)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@org.command('rename')
@click.option('--name', prompt="New name", hide_input=False, confirmation_prompt=False, type=click.STRING)
@org_cluster_options
def org_delete(org, name, remote):
    click.confirm('Do you want to rename org {}?'.format(org), abort=True)
    try:
        response = ApiManager(cluster=remote).orgs.rename_organization(org=org, new_name=name)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))

@org.command('meta')
@click.option('-m', '--metadata', type=click.STRING)
@click.option('--merge/--no-merge', default=True)
@org_cluster_options
def org_update_metadata(org, metadata, merge, remote):
    try:
        response = ApiManager(cluster=remote).orgs.update_org_metadata(org_id=org, metadata=metadata, merge=merge)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))

@org.command('expiry')
@click.option('--days', default=None, hide_input=False, confirmation_prompt=False, type=click.INT)
@org_cluster_options
def org_expire_extend(org, days, remote):
    try:
        response = ApiManager(cluster=remote).orgs.extend_expiration(org_id=org, days=days)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@org.command('sensor')
@org_cluster_options
@click.argument('content', callback=get_piped_param, required=False)
def import_template_config(org, remote, content):
    try:
        response = ApiManager(cluster=remote).orgs.submit_sensor_diagnostics(org_id=org, content=content)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
