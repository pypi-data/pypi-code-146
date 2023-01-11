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
from unify.apimanager import ApiManager

from source.utils.util_methods import get_piped_param
from source.common.commands import org_cluster_options


@click.group()
def wf():
    """
    Group for work flow commands
    :return:
    """


@wf.command('export-template')
@org_cluster_options
def export_template(org, remote):
    try:
        response = ApiManager(cluster=remote).templates.download_template_batches(org_id=org)
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-template-config')
@org_cluster_options
@click.argument('content', callback=get_piped_param, required=False)
def import_template_config(org, remote, content):
    try:
        ApiManager(cluster=remote).templates.upload_config_with_content(org_id=org, content=content)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-template-config')
@org_cluster_options
def export_template_config(org, remote):
    try:
        response = ApiManager(cluster=remote).templates.download_all_template_config(org_id=org)
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-template')
@org_cluster_options
@click.argument('content', callback=get_piped_param, required=False)
def import_template(org, remote, content):
    try:
        ApiManager(cluster=remote).templates.upload_string_content_file(org_id=org, content=content)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-pipeline')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--pipeline', prompt="Pipeline id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--skip', multiple=True, required=False, default=[])
def export_pipeline(remote, org, pipeline, skip):
    try:
        response = ApiManager(cluster=remote).create_pipeline_export_data(
            org_id=org,
            pipeline_id=pipeline,
            skip=skip
        )
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-pipeline')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--deduplicate', prompt=False, hide_input=False, default='clone', required=False,
              type=click.Choice(['clone', 'error']))
@click.option('--skip', multiple=True, required=False, default=[])
@click.argument('content', callback=get_piped_param, required=False)
def import_pipeline(remote, org, deduplicate, content, skip):
    try:
        response = ApiManager(cluster=remote).proceses_importing_pipeline_file(
            org_id=org,
            content=content,
            handleduplicates=deduplicate,
            skip=skip
        )

        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--id', multiple=True, required=False, default=[])
def export_dataset(org, remote, id):
    try:
        response = ApiManager(cluster=remote).export_source(
            org_id=org,
            dataset_ids=id
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def import_dataset(org, remote, content):
    try:

        response = ApiManager(cluster=remote).import_sources(
            org_id=org,
            pipeline_id=None,
            content=content,
            update_pipeline=False
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--id', multiple=True, required=False, default=[])
def export_dataset(org, remote, id):
    try:
        response = ApiManager(cluster=remote).export_source(
            org_id=org,
            dataset_ids=id
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def import_dataset(org, remote, content):
    try:

        response = ApiManager(cluster=remote).import_sources(
            org_id=org,
            pipeline_id=None,
            content=content,
            update_pipeline=False
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-function')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--function', prompt="Function id", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--skip', multiple=True, required=False, default=[])
def export_function(remote, org, function, skip):
    try:
        response = ApiManager(cluster=remote).create_pipeline_export_data(
            org_id=org,
            pipeline_id=function,
            skip=skip
        )
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-function')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--deduplicate', prompt=False, hide_input=False, default='clone', required=False,
              type=click.Choice(['clone', 'error']))
@click.option('--skip', multiple=True, required=False, default=[])
@click.argument('content', callback=get_piped_param, required=False)
def import_function(remote, org, deduplicate, content, skip):
    try:
        response = ApiManager(cluster=remote).proceses_importing_pipeline_file(
            org_id=org,
            content=content,
            handleduplicates=deduplicate,
            skip=skip,
            function=True
        )

        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-hierarchy')
@org_cluster_options
@click.option('--hierarchy', prompt=False, hide_input=False, required=True, confirmation_prompt=False,
              type=click.INT)
def export_hierarchy(remote, org, hierarchy):
    try:
        response = ApiManager(cluster=remote).export_hierarchy(org, hierarchy)

        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-hierarchy')
@org_cluster_options
@click.argument('content', callback=get_piped_param, required=False)
def import_hierarchy(remote, org, content):
    try:
        response = ApiManager(cluster=remote).import_hierarchy(org, content)

        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
