import typer

from continual.python.cli import utils
from continual.python.sdk.client import Client

from rich.console import Console
from typing import List

app = typer.Typer(help="Manage models.")


def get_linked_entities(columns):
    entities = {}
    for c in columns:
        entity = c.entity
        if entity is not None and len(entity) > 0:
            entities[c.name] = entity
    return "\n".join(["%s : %s" % (k, v) for k, v in entities.items()])


def format_model_data(m, zipped=False, all_projects=False):
    create_time = m.create_time.replace(microsecond=0)
    update_time = m.update_time.replace(microsecond=0)
    num_bpj = len(m.batch_predictions.list(1000))
    num_d = len(m.promotions.list(1000))
    num_mv = len(m.model_versions.list(1000))
    latest_version = m.latest_model_version.split("/")[-1]
    if latest_version:
        mv_state = m.model_versions.get(latest_version).state.value
    else:
        mv_state = "N/A"
    current_version = m.current_version.split("/")[-1]
    mv_type = "N/A"
    mv_perf_metric = "N/A"
    mv_perf_metric_val = "N/A"
    if current_version:
        mv = m.model_versions.get(current_version)
        try:
            mv_type = mv.experiment.type.split("/")[1]
        except:
            mv_type = "N/A"
        mv_perf_metric = mv.performance_metric
        mv_perf_metric_val = round(mv.performance_metric_val, 4)
    linked_entities = get_linked_entities(m.schema.columns)
    project = m.parent.split("/")[-1]
    if zipped:
        data = [
            m.id,
            m.name,
            m.state,
            project,
            latest_version,
            mv_state,
            current_version,
            mv_type,
            mv_perf_metric,
            mv_perf_metric_val,
            m.latest_batch_prediction,
            linked_entities,
            num_mv,
            num_d,
            num_bpj,
            create_time,
            update_time,
        ]
        headers = [
            "ID",
            "Name",
            "State",
            "Project",
            "Latest Model Version",
            "Latest Version State",
            "Current Version",
            "Current Version Type",
            "Current Version Performance Metric",
            "Current Version Performance Metric Value",
            "Latest Batch Prediction",
            "Linked Entities",
            "Model Versions",
            "Promotions",
            "Batch Predictions",
            "Created",
            "Updated",
        ]
        return tuple(
            [x[0], x[1]] for x in (zip(headers, data))
        )  # for some reason list(zip) causes issues, so ...
    else:
        data = [
            m.id,
            m.state,
            latest_version,
            mv_state,
            current_version,
            mv_type,
            mv_perf_metric,
            mv_perf_metric_val,
            linked_entities,
            num_mv,
            num_d,
            num_bpj,
            create_time,
            # update_time,
        ]
        headers = [
            "ID",
            "State",
            "Latest Version",
            "Latest Version State",
            "Current Version",
            "Current Version Type",
            "Current Version Perf Metric",
            "Current Version Perf Metric Val",
            "Linked Entities",
            "Model Versions",
            "Promotions",
            "Batch Predictions",
            "Created",
            # "Updated",
        ]
        if all_projects:
            data.insert(0, m.parent.split("/")[1])
            headers.insert(0, "Project")
        return (data, headers)


# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        model_list(
            project=None,
            environment=None,
            n=30,
            filters=[],
            all_projects=False,
            style=None,
        )


@app.command("list")
@utils.exit_on_error
def model_list(
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    filters: List[str] = typer.Option([], "--filter", "-f", help="List of filters."),
    all_projects: bool = typer.Option(False, "--all", "-a", help="Show all projects."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List models.

    Filter can include:
        - state  (i.e. state:HEALTHY)
        - latest_mv_state (i.e. latest_mv_state:SUCCEEDED)
    """
    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    filter_snippet = " (n=%s)" % n
    project_snippet = "project %s, environment %s" % (project, environment)
    if all_projects:
        project_snippet = "all accessible projects"
    if len(filters) > 0:
        filter_snippet = " with filter %s" % str(filters) + filter_snippet
    data = []
    headers = []
    for m in c.models.list(n, filters=filters, all_projects=all_projects):
        (m_data, headers) = format_model_data(m, all_projects=all_projects)
        data.append(m_data)
    typer.secho(
        "\nFound %s models in %s%s:" % (len(data), project_snippet, filter_snippet),
        fg="blue",
    )
    utils.print_table(data, headers, style=utils.get_style(style))


@app.command("get")
@utils.exit_on_error
def get(
    model: str = typer.Argument(..., help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    to_json: bool = typer.Option(
        False, "--json", help="Show full JSON representation."
    ),
):
    """Get model details."""
    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    m = c.models.get(model)
    console = Console()
    if to_json:
        console.print(m.to_dict())
    else:
        data = format_model_data(m, zipped=True)
        typer.secho("\nRetrieving model %s: \n" % (model), fg="blue")
        utils.print_info(data)
        typer.secho("\nModel schema:\n", fg="blue")
        console.print(m.schema.to_dict())


@app.command("create-local-dev-batch-prediction")
@utils.exit_on_error
def create_local_dev(
    model: str = typer.Argument(..., help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    to_json: bool = typer.Option(
        False, "--json", help="Show full JSON representation."
    ),
):
    """Create model version for local development."""
    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    mv = c.models.create_local_dev_model_version(model)
    console = Console()
    if to_json:
        console.print(mv.to_dict())
    else:
        typer.secho("Created model version %s \n" % (mv.name), fg="blue")


@app.command("delete")
@utils.exit_on_error
def delete(
    model: str = typer.Argument(..., help="Model ID."),
    project: str = typer.Option(None, help="Project ID."),
    environment: str = typer.Option(None, "--env", help="Environment ID."),
    force: bool = typer.Option(
        False, "--force", help="Force deletion. Skips confirmation."
    ),
):
    """Delete model."""
    project, environment = utils.get_project_and_environment(project, environment)
    c = Client(project=utils.get_environment_name(project, environment))

    if not force:
        force = typer.confirm(
            "Are you sure you want to delete model %s in project %s, environment %s?"
            % (model, project, environment)
        )
    if force:
        m = c.models.get(model)
        m.delete()
        typer.secho("Successfully deleted model %s." % m.id, fg="green")
    else:
        typer.secho("Cancelled model deletion!", fg="blue")
