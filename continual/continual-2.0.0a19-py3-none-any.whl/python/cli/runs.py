import typer

from continual.python.cli import utils
from continual.python.sdk.client import Client

from rich.console import Console

app = typer.Typer(help="Manage runs.")


def format_run_data(r, zipped=False):
    create_time = r.create_time.replace(microsecond=0)
    update_time = r.update_time.replace(microsecond=0)
    last_heartbeat = r.last_heartbeat.replace(microsecond=0)

    if zipped:
        data = [
            r.name,
            r.description,
            r.author,
            create_time,
            update_time,
            last_heartbeat,
            r.state,
            r.error_message,
        ]
        headers = [
            "Name",
            "Description",
            "Author",
            "Created",
            "Updated",
            "Last Heartbeat",
            "State",
            "Error Message",
        ]
        return tuple([x[0], x[1]] for x in (zip(headers, data)))
    else:
        data = [
            r.name,
            r.description,
            r.author,
            create_time,
            update_time,
            last_heartbeat,
            r.state,
            r.error_message,
        ]
        headers = [
            "Name",
            "Description",
            "Author",
            "Created",
            "Updated",
            "Last Heartbeat",
            "State",
            "Error Message",
        ]
        return (data, headers)


# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        list(
            n=30,
            filters=[],
            style=None,
        )


@app.command("list")
@utils.exit_on_error
def list(
    n: int = typer.Option(30, "--num", "-n", help="Number of records to show."),
    style: utils.ContinualStyle = typer.Option(None, help="Color to use for list."),
):
    """List Runs."""
    c = Client()
    data = []
    headers = []
    for r in c.runs.list(n):
        (r_data, headers) = format_run_data(r)
        data.append(r_data)
    typer.secho("Found %s runs:" % (len(data)), fg="blue")
    utils.print_table(data, headers, style=utils.get_style(style))


@app.command("get")
@utils.exit_on_error
def get(
    run: str = typer.Argument(..., help="Run ID."),
    json: bool = typer.Option(False, "--json", help="Show full JSON representation."),
):
    """Get run details."""
    c = Client()
    r = c.runs.get(run)
    if json:
        console = Console()
        console.print(r.to_dict())
    else:
        data = format_run_data(r, zipped=True)
        typer.secho("\nRetrieving Run %s: \n" % (run.split("/")[-1]), fg="blue")
        utils.print_info(data)


@app.command("get-check-summary")
@utils.exit_on_error
def get_check_summary(
    run: str = typer.Argument(..., help="Run ID."),
    # json: bool = typer.Option(False, "--json", help="Show full JSON representation."),
    error_on_fail: bool = typer.Option(
        False, "--error-on-fail", help="Exit with an error if check has failed."
    ),
):
    """Get check summary for run."""
    c = Client()
    r = c.runs.get_check_summary(run)
    console = Console()
    console.print(r.to_dict())

    if error_on_fail and r.state == "FAIL":
        exit(1)
