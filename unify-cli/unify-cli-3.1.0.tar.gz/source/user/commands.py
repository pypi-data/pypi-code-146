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
import json

import click
from tabulate import tabulate

from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json
from source.common.commands import org_cluster_options, cluster_option


@click.group()
def user():
    """Group for the user related commands"""
    pass


@user.command('list')
@cluster_option
def user_list(remote):
    try:
        response = ApiManager(cluster=remote).orgs.retrieve_all_users()
        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('org-list')
@org_cluster_options
def org_user_list(org, remote):
    try:
        response = ApiManager(cluster=remote).orgs.retrieve_all_users_form_org(org)
        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('move')
@cluster_option
@click.option('--user', prompt="User Id", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--group', prompt="Group Id", hide_input=False, default=None, required=True, type=click.STRING)
def org_user_list(remote, user, group):
    try:
        response = ApiManager(cluster=remote).orgs.move_user_to_group(user_id=user, group_id=group)
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('group-list')
@cluster_option
@click.option('--table', '-t', is_flag=True, help="Print in table")
def group_list(remote, table):
    try:
        response = ApiManager(cluster=remote).orgs.get_all_groups()
        if table:
            response = tabulate_from_json(response["allGroups"])
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('add')
@org_cluster_options
@click.option('--email', prompt="User Email", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--name', prompt="Person Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False,
              type=click.Choice(['Admin', 'Contributor']))
def user_add(org, remote, email, name, role):
    try:
        response = ApiManager(cluster=remote).orgs.invite_user(
            org_id=org,
            email=email,
            name=name,
            role=role
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('addserviceaccount')
@org_cluster_options
@click.option('--service_account_name', prompt="Service Account Name", hide_input=False, default=None, required=True,
              type=click.STRING)
@click.option('--service_account_id', prompt="Service Account ID (UUID format)", hide_input=False, default=None,
              required=True, type=click.STRING)
@click.option('--service_account_password', prompt="Service Account Password (UUIC format)", hide_input=True,
              default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False,
              type=click.Choice(['Admin', 'Contributor']))
def service_account_add(org, remote, service_account_name, service_account_id, service_account_password, role):
    try:
        response = ApiManager(cluster=remote).orgs.invite_machine_user(
            org_id=org,
            fullname=service_account_name,
            id=service_account_id,
            password=service_account_password,
            role=role
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
