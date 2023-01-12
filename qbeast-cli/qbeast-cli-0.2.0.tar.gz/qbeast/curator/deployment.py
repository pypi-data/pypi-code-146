import click

from qbeast.curator.commands import deployment
from qbeast.config import *
from qbeast.curator.api import get_deployments, post_deployment, get_deployment, delete_deployment
from qbeast.config import *
from tabulate import tabulate

"""Helpers"""
@deployment.command("select")
@click.option("--deployment-id", "-d", help="ID of the deployment to be selected by default")
def select_deployment(deployment_id):
    """Selects a deployment to be used by default"""
    



"""Qbeast Curator commands that interact with the API"""


@deployment.command("list")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--status", help="Status of the deployment")
def list_deployments(project_name, status):
    """Lists all the deployments in the Qbeast Curator"""
    api_response = get_deployments(project_name) # TODO call the API filtering by status
    if api_response.success:
        table = [[p['projectName'], p['id'], p['snapshotVersion'], p['created']] for p in api_response.message['items']]
        print(tabulate(table, headers=["ProjectName", "DeploymentId", 'SnapshotVersion' "Created"]))
    else:
        print(api_response.message)


@deployment.command("create")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def create_deployment(project_name, snapshot_version):
    """Creates a new deployment in the Qbeast Curator"""
    api_response = post_deployment(project_name, snapshot_version)
    if api_response.success:
        print(f"Deployment created!")
    else:
        print(api_response.message)


@deployment.command("info")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
def info_deployment(project_name, snapshot_version, deployment_id):
    """Shows information about a deployment"""
    api_response = get_deployment(project_name, snapshot_version, deployment_id)
    if api_response.success:
        table = [[p['projectName'], p['id'], p['snapshotVersion'], p['created']] for p in [api_response.message]]
        print(tabulate(table, headers=["ProjectName", "DeploymentId", 'SnapshotVersion' "Created"]))
    else:
        print(api_response.message)


@deployment.command("update")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
@click.option("--action", help="Action to be performed", required=True)
def update_deployment(project_name, snapshot_version, deployment_id, action):
    """Updates a deployment"""
    raise NotImplementedError # TODO implement this method


@deployment.command("delete")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--deployment-id", "-d", help="ID of the deployment")
def do_delete_deployment(project_name, snapshot_version, deployment_id):
    """Deletes a deployment"""
    api_response = delete_deployment(project_name, snapshot_version, deployment_id)
    if api_response.success:
        print(f"Deployment {deployment_id} deleted!")
    else:
        print(api_response.message)