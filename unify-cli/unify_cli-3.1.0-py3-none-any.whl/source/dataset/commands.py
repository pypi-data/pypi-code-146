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
def dataset():
    """Group for dataset commands"""


@dataset.command('add')
@org_cluster_options
@click.option('--dtype', prompt="Dataset Type", hide_input=False, default='external', required=False,
              type=click.Choice(['external', 'piconfig']))
@click.option('--name', prompt="Dataset Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def add_dataset(org, remote, dtype, name, content):
    try:
        response = ApiManager(cluster=remote).import_source(content=content, orgid=org, name=name, type=dtype)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@dataset.command('big')
@org_cluster_options
@click.option('--name', prompt="Data set Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--encoding', prompt="File encoding", hide_input=False, default='UTF-8', required=True, type=click.STRING)
@click.option('--chunks', prompt="Chunk size", hide_input=False, default=10000, required=True, type=click.INT)
@click.argument('content', callback=get_piped_param, required=False)
def add_big_dataset(org, remote, name, encoding, chunks, content):
    try:
        response = ApiManager(cluster=remote).import_source(
            content=content,
            orgid=org,
            name=name,
            type="generic",
            chunks=chunks,
            encoding=encoding
        )
        print(response)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@dataset.command('append')
@org_cluster_options
@click.option('--datasetid', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def append_dataset(org, remote, datasetid, content):
    try:
        response = ApiManager(cluster=remote).append_data(content=content, orgid=org, dataset_id=datasetid)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@dataset.command('list')
@org_cluster_options
@click.option('--table', '-t', is_flag=True, help="Print in table")
def list_dataset(org, remote, table):
    try:
        response = ApiManager(cluster=remote).dataset_list(org_id=org)
        if table:
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))

@dataset.command('split')
@org_cluster_options
@click.option('--name', prompt="Data set Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--encoding', prompt="File encoding", hide_input=False, default='UTF-8', required=True, type=click.STRING)
@click.option('--chunks', prompt="Chunk size", hide_input=False, default=10000, required=True, type=click.INT)
@click.argument('content', callback=get_piped_param, required=False)
def split_bid_dataset(org, remote, name, encoding, chunks, content):
    try:
        response = ApiManager(cluster=remote).import_source(
            content=content,
            orgid=org,
            name=name,
            type="split",
            chunks=chunks,
            encoding=encoding
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
