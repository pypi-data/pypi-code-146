import click

from qbeast.curator.commands import run
from tabulate import tabulate
from qbeast.config import *
from qbeast.curator.api import get_runs, post_run, get_run, delete_run, get_run_logs, patch_run

"""Helpers"""
@run.command("select")
@click.option("--run-id", "-r", help="ID of the run to be selected by default")
def select_run(run_id):
    """Selects a run to be used by default"""
    raise NotImplementedError # TODO implement this method



"""Qbeast Curator commands that interact with the API"""


@run.command("list")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def list_runs(project_name, deployment_id, snapshot_version):
    """Lists all the runs in the Qbeast Curator"""
    api_response = get_runs(project_name, snapshot_version, deployment_id)
    if api_response.success:
        table = [[p['projectName'], p['snapshotId'], p['deploymentId'], p['s3_bucket'], p['run_date'], p['gbs_ingested']] for p in api_response.message['items']]
        print(tabulate(table, headers=["DeploymentId", "RunId", "Created", 'Terminated']))
    else:
        print(api_response.message)


@run.command("start")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def start_run(project_name, deployment_id, snapshot_version):
    """Starts a new run in the Qbeast Curator"""
    api_response = post_run(project_name, snapshot_version, deployment_id)
    if api_response.success:
        print(f"Run {api_response.message['id']} created!")
        table = [[p['deploymentId'], p['id'], p['created'], p['terminated'], ] for p in [api_response.message]]
        print(tabulate(table, headers=["DeploymentId", "RunId", "Created", 'Terminated']))
    else:
        print(api_response.message)


@run.command("info")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--run-id", "-r", help="ID of the run")
def info_run(project_name, snapshot_version, deployment_id, run_id):
    """Shows information about a run"""
    api_response = get_run(project_name, snapshot_version, deployment_id, run_id)
    if api_response.success:
        table = [[p['deploymentId'], p['id'], p['created'], p['terminated']] for p in [api_response.message]]
        print(tabulate(table, headers=["DeploymentId", "RunId", "Created", 'Terminated']))
    else:
        print(api_response.message)


@run.command("abort")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--run-id", "-r", help="ID of the run")
def abort_run(project_name, snapshot_version, deployment_id, run_id):
    """Aborts a run"""
    api_response = patch_run(project_name, snapshot_version, deployment_id, run_id)
    if api_response.success:
        print("Run aborted!")
    else:
        print(api_response.message)


@run.command("delete")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--run-id", "-r", help="ID of the run")
def delete_run(project_name, snapshot_version, deployment_id, run_id):
    """Deletes a run"""
    api_response = delete_run(project_name, snapshot_version, deployment_id, run_id)
    if api_response.success:
        print(f"Run {api_response.message['id']} deleted!")
        table = [[p['deploymentId'], p['id'], p['created'], p['terminated']] for p in [api_response.message]]
        print(tabulate(table, headers=["DeploymentId", "RunId", "Created", 'Terminated']))
    else:
        print(api_response.message)


@run.command("logs")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--run-id", "-r", help="ID of the run")
def logs_run(project_name, snapshot_version, deployment_id, run_id):
    """Shows the logs of a run"""
    api_response = get_run_logs(project_name, snapshot_version, deployment_id, run_id)
    if api_response.success:
        print(f"Logs of run {api_response.message['id']}:")
        print(api_response.message['logs'])
    else:
        print(api_response.message)