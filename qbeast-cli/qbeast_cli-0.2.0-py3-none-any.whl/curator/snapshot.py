import click
import subprocess
import time

from qbeast.curator.commands import snapshot
from qbeast.curator.utils import is_curator_valid_directory, compress_dir, compile_ingestion_app
from qbeast.curator.api import get_snapshots, post_snapshot, get_snapshot, delete_snapshot
from qbeast.config import *
from tabulate import tabulate

"""Helpers"""
@snapshot.command("select")
@click.option("--snapshot-version", "-s", help="Version of the snapshot to be selected by default")
def select_snapshot(snapshot_version):
    """Selects a snapshot to be used by default"""
    raise NotImplementedError # TODO implement this method



"""Qbeast Curator commands that interact with the API"""


@snapshot.command("list")
@click.option("--project-name", "-p", help="Name of the project")
def list_snapshots(project_name):
    """Lists all the snapshots in the Qbeast Curator"""
    api_response = get_snapshots(project_name)
    if api_response.success:
        table = [[p['projectName'], p['version'], p['created']] for p in api_response.message["items"]]
        print(tabulate(table, headers=["ProjectName", "version", "Created"]))
    else:
        print(api_response.message)


@snapshot.command("create")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--path", default="./", help="Path to the Curator project", show_default=True)
def create_snapshot(project_name, path):
    """Creates a new snapshot in the Qbeast Curator"""
    success, reason = is_curator_valid_directory(path)
    create_dbt_profile()
    if not success:
        print(reason)
        return
    output_name = (f"{project_name}_{time.time()}.tar.gz")

    success, jar_location = compile_ingestion_app(path, "qbeast-ingestion.jar")
    if not success:
        print("Failed building ingestion jar")
        return
    success, file_path = compress_dir(path, output_name, jar_location)
    if not success:
        print("Failed compressing project")
        return

    snapshot_version = subprocess.Popen("git rev-parse HEAD", cwd=path, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip()

    api_response = post_snapshot(project_name, file_path, snapshot_version=snapshot_version)
    if api_response.success:
        print(f"Project {project_name} created!")
        table = [[p['projectName'], p['version'], p['created']] for p in [api_response.message]]
        print(tabulate(table, headers=["Name", "Description", "Created"]))
    else:
        print(api_response.message)


@snapshot.command("info")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def info_snapshot(project_name, snapshot_version):
    """Shows information about a snapshot"""
    api_response = get_snapshot(project_name, snapshot_version)
    if api_response.success:
        table = [[p['projectName'], p['version'], p['created']] for p in [api_response.message]]
        print(tabulate(table, headers=["ProjectName", "version", "Created"]))
    else:
        print(api_response.message)


@snapshot.command("delete")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def do_delete_snapshot(project_name, snapshot_version):
    """Deletes a snapshot"""
    api_response = delete_snapshot(project_name, snapshot_version)
    if api_response.success:
        print(f"Snapshot {snapshot_version} deleted!")
    else:
        print(api_response.message)



@snapshot.command("deployments")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def list_deployments(project_name, snapshot_version):
    """Lists all the deployments of a snapshot"""
    raise NotImplementedError # TODO implement this method