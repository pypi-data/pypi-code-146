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
def template():
    """Group for template commands"""
    pass


@template.command('show')
@org_cluster_options
def show_templates(remote, org):
    try:
        response = ApiManager(cluster=remote).templates.list_asset_templates(org_id=org)
        click.echo(click.style(tabulate(tabulate_from_json(response), "keys"), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
