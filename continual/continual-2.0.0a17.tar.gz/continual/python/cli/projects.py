#!/usr/bin/env python3

import typer

from continual.python.cli import utils
from continual.python.sdk.client import Client

from rich.console import Console
from typing import List


app = typer.Typer(help="Manage projects.")


def format_project_data(p, zipped=False):
    create_time = p.create_time.replace(microsecond=0)
    update_time = p.update_time.replace(microsecond=0)
    org = p.organization.split("/")[-1]
    c = Client()
    project_id = p.id
    current_project = c.config.project
    if current_project and current_project == p.name:
        project_id = f"{project_id} (active)"
    data = [
        project_id,
        p.display_name,
        org,
        p.summary.model_count,
        p.summary.model_version_count,
        p.summary.prediction_count,
        create_time,
        # update_time,
    ]
    headers = [
        "ID",
        "Display Name",
        "Organization",
        "Models",
        "Model Versions",
        "Predictions",
        "Created",
        # "Updated",
    ]

    if zipped:
        return tuple(
            [x[0], x[1]] for x in (zip(headers, data))
        )  # for some reason list(zip) causes issues, so ...
    else:
        return (data, headers)


# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        list(n=30, filters=[], style=None)


@app.command("list")
@utils.exit_on_error
def list(
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    filters: List[str] = typer.Option([], "--filter", "-f", help="List of filters."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List projects."""
    c = Client()
    data = []
    headers = []
    filter_snippet = " (n=%s)" % n
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters) + filter_snippet
    for p in c.projects.list(n, filters=filters):
        (p_data, headers) = format_project_data(p)
        data.append(p_data)
    typer.secho("Found %s projects%s:" % (len(data), filter_snippet), fg="blue")
    utils.print_table(data, headers, style=utils.get_style(style))


@app.command("get")
@utils.exit_on_error
def get(
    project_id: str = typer.Argument(..., help="Project ID."),
    json: bool = typer.Option(False, "--json", help="Print full JSON representation."),
):
    """Get project details."""
    project_id = utils.get_project(project_id)  # handle passing in project@env
    c = Client(project=project_id)
    project = c.projects.get(project_id)
    if json:
        console = Console()
        console.print(project.to_dict())
    else:
        data = format_project_data(project, zipped=True)
        typer.secho("\nRetrieving project %s: \n" % (project_id), fg="blue")
        utils.print_info(data)


@app.command("create")
@utils.exit_on_error
def create(
    project: str = typer.Argument(..., help="Name of project."),
    org: str = typer.Option(..., help="Name of organization.", show_default=False),
):
    """Create project."""
    try:
        c = Client(verify=False)
        c.config._raise_exception = True
        c.projects.get(project)
        typer.secho(
            "Project %s already exists. Please try another name.\n" % project, fg="red"
        )
    except:
        try:
            proj = utils.get_or_create_project(project, org)
            typer.secho(
                "Successfully created project %s." % (proj.id),
                fg="green",
            )
        except Exception as e:
            typer.secho(
                "Error creating project %s: %s" % (project, str(e)),
                fg="red",
            )
            raise typer.Exit(code=1)


@app.command("delete")
@utils.exit_on_error
def delete(
    project_id: str = typer.Argument(..., help="Project ID."),
    force: bool = typer.Option(
        False, "--force", help="Force deletion. Skips confirmation."
    ),
):
    """Delete project."""
    project_id = utils.get_project(project_id)
    if not force:
        force = typer.confirm(
            "Are you sure you want to delete the project %s?" % project_id
        )
    if force:
        c = Client(project=project_id)
        project = c.projects.get(project_id)
        project.delete()
        typer.secho("Successfully deleted project %s." % project_id, fg="green")
    else:
        typer.secho("Skipping deletion!")


@app.command("update")
@utils.exit_on_error
def update(
    project_id: str = typer.Argument(..., help="Project ID."),
    new_name: str = typer.Option(None, help="New project name"),
):
    """Update project."""
    project_id = utils.get_project(project_id)
    c = Client(project=project_id)
    project = c.projects.get(project_id)
    if new_name is None:
        new_name = project.display_name
    project.update(display_name=new_name)
    typer.secho("Successfully updated project %s." % project_id, fg="green")
