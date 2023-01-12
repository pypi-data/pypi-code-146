import click

from qbeast.curator.commands import test


"""Helpers"""
@test.command("select")
@click.option("--test-id", "-t", help="ID of the test to be selected by default")
def select_test(test_id):
    """Selects a test to be used by default"""
    raise NotImplementedError # TODO implement this method


"""Qbeast Curator commands that interact with the API"""


@test.command("list")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def list_tests(project_name, snapshot_version):
    """Lists all the tests in the Qbeast Curator"""
    raise NotImplementedError # TODO implement this method


@test.command("run")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
def run_test(project_name, snapshot_version):
    """Runs a test"""
    raise NotImplementedError # TODO implement this method


@test.command("info")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--test-id", "-t", help="ID of the test")
def info_test(project_name, snapshot_version, test_id):
    """Shows information about a test"""
    raise NotImplementedError # TODO implement this method


@test.command("abort")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--test-id", "-t", help="ID of the test")
def abort_test(project_name, snapshot_version, test_id):
    """Aborts a test"""
    raise NotImplementedError # TODO implement this method


@test.command("delete")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--test-id", "-t", help="ID of the test")
def delete_test(project_name, snapshot_version, test_id):
    """Deletes a test"""
    raise NotImplementedError # TODO implement this method


@test.command("logs")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--snapshot-version", "-s", help="Version of the snapshot")
@click.option("--test-id", "-t", help="ID of the test")
def get_test_logs(project_name, snapshot_version, test_id):
    """Gets the logs of a test"""
    raise NotImplementedError # TODO implement this method