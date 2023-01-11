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

from source.utils.util_methods import get_piped_param
from source.common.commands import org_cluster_options

@click.group()
def access():
    """
    Group for Element Unify Access related commands
    :return: None
    """


@access.command('execute')
@org_cluster_options
@click.option('--output', prompt=False, hide_input=False, default='csv', required=False,
              type=click.Choice(['table', 'csv', 'json']))
@click.argument('query', callback=get_piped_param, required=True)
def execute_query(remote, org, output, query):
    """
    Method to execute a SQL QUERY trhough asset access

    :param remote: CLuster name to be used
    :param org: organization ID where the data set exists
    :param output: return the results in tabulate,csv,json
    :param query: SQL query to be executed
    :return:
    """
    try:
        response = ApiManager(cluster=remote).execute_query(query=query, orgid=org, format=output)

        if output == "table":
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@access.command('databases')
@org_cluster_options
def get_databases(remote, org):
    """
    Method to retrieve the datasets available from and or

    :param remote: Cluster name to be used
    :param org: Organization ID where teh data set exists
    :return:
    """
    try:
        response = ApiManager(cluster=remote).assethub_access_tables(orgid=org)
        response = tabulate_from_json(response)
        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
