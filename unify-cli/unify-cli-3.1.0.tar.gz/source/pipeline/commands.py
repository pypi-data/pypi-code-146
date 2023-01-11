import json

import click

from tabulate import tabulate

from unify.properties import Properties
from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json

from source.common.commands import org_cluster_options


@click.group()
def pipeline():
    """Group for pipeline commands"""
    pass


@pipeline.command('list')
@org_cluster_options
@click.option('--table', '-t', is_flag=True, help="Print in table")
def list_pipeline(org, remote, table):
    try:
        response = ApiManager(cluster=remote).pipeline_list(org_id=org)
        if table:
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))

@pipeline.command('duplicate')
@org_cluster_options
@click.option('--pipeline_id', prompt=False, hide_input=False, required=False, confirmation_prompt=False,type=click.STRING)
@click.option('--new_name', prompt=False, hide_input=False, required=False, confirmation_prompt=False,type=click.STRING)
def duplicate_pipeline(org, remote, pipeline_id,new_name):
    try:
        response = ApiManager(cluster=remote).regular_pipeline_duplicate(
            org_id=org,
            pipeline_id=pipeline_id,
            new_name=new_name
        )
        click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))
