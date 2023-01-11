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

@click.group()
def cluster():
    """
    Configuration Setup for Element Unify
    """


@cluster.command('add')
@click.option('--remote', prompt=True, hide_input=False, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--username', prompt=True, hide_input=False, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--password', prompt=True, hide_input=True, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--name', prompt=True, hide_input=False, required=False, default=None, confirmation_prompt=False,
              type=click.STRING)
@click.option('--assetsync', hide_input=False, default=True, type=click.BOOL)
def add_cluster(remote, username, password, name, assetsync):
    """
    Store a new cluster information
    """
    try:

        Properties().store_cluster(
            username=username,
            password=password,
            cluster=remote,
            name=name,
            assetsync=assetsync
        )

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('login')
@cluster_options
def login(remote):

    """
    Creates a auth token to the given cluster
    """

    try:
        auth = ApiManager(cluster=remote).orgs.auth_token()
        Properties().set_auth_token(token=auth, cluster=remote)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('default')
@cluster_options
def set_default(remote):
    """
    Sets the cluster name as default
    """
    try:
        Properties().set_default(name=remote)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('list')
def list_cluster():

    """
    List all the cluster the user has stored on this machine
    """
    try:
        clusters = Properties().get_all_clusters()
        click.echo(click.style(tabulate(tabulate_from_json(clusters), "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('disconnect')
@cluster_options
@click.option('--yes', '-y', is_flag=True,default=False, help="Auto Accept")
def disconnect_cluster(remote,yes):

    """
    Removes the cluster from this machine
    :param remote:
    :return:
    """
    if yes is False:
        click.confirm('Do you want to disconnect from {}?'.format(remote), abort=True)

    try:
        Properties().remove_cluster(name=remote)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
