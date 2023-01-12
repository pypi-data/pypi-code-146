import click
from tabulate import tabulate

from qbeast.curator.commands import project
from qbeast.curator.api import get_projects, post_project, get_project, patch_project, delete_project



"""Helpers"""
@project.command("select")
@click.option("--project-name", "-p", help="Name of the project to be selected by default")
def select_project(project_name):
    """Selects a project to be used by default"""
    raise NotImplementedError # TODO implement this method



"""Qbeast Curator commands that interact with the API"""


@project.command("list")
def list_projects():
    """Lists all the projects in the Qbeast Curator"""
    api_response = get_projects()
    if api_response.success:
        table = [[p['name'], p['description'], p['created']] for p in api_response.message['items']]
        print(tabulate(table, headers=["Name", "Description", "Created"]))
    else:
        print(api_response.message)


@project.command("create")
@click.option("--project-name", "-p", help="Name of the new project", required=True)
@click.option("--description", "-D", help="Description of the new project", required=True)
def create_project(project_name, description):
    """Creates a new project in the Qbeast Curator"""
    api_response = post_project(project_name, description)
    if api_response.success:
        print(f"Project {project_name} created!")
        table = [[p['name'], p['description'], p['created']] for p in [api_response.message]]
        print(tabulate(table, headers=["Name", "Description", "Created"]))
    else:
        print(api_response.message)


@project.command("info")
@click.option("--project-name", "-p", help="Name of the project")
def info_project(project_name):
    """Shows information about a project"""
    api_response = get_project(project_name)
    if api_response.success:
        table = [[p['name'], p['description'], p['created']] for p in [api_response.message]]
        print(tabulate(table, headers=["Name", "Description", "Created"]))
    else:
        print(api_response.message)


@project.command("update")
@click.option("--project-name", "-p", help="Name of the project")
@click.option("--description", "-D", help="New description of the project", required=True)
def rename_project(project_name, description):
    """Changes the description of a project"""
    api_response = patch_project(project_name, description)
    if api_response.success:
        print(f"Project {project_name} updated!")
    else:
        print(api_response.message)


@project.command("delete")
@click.option("--project-name", "-p", help="Name of the project")
def do_delete_project(project_name):
    """Deletes a project"""
    api_response = delete_project(project_name)
    if api_response.success:
        print(f"Project {project_name} deleted!")
    else:
        print(api_response.message)