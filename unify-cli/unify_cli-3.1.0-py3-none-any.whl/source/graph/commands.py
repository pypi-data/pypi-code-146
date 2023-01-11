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

from source.utils.util_methods import get_piped_param
from source.common.commands import org_cluster_options


@click.group()
def graph():
    """
    Graphs v2 command line group
    """
    pass


@graph.command('list')
@org_cluster_options
@click.option('--table', '-t', is_flag=True, help="Print in table")
def list_graphs(org, remote, table):
    try:
        response = ApiManager(cluster=remote).graphs_list(org_id=org)
        if table:
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@graph.command('query')
@org_cluster_options
@click.option('--graph', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--format', '-j', is_flag=True, help="Json format")
@click.argument('query', callback=get_piped_param, required=True)
def query_graphs(org, remote, graph, query, format):
    try:
        response = ApiManager(cluster=remote).query_graph(
            org=org,
            graph=graph,
            query=query,
            json_format=format
        )
        if format:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(response, blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
