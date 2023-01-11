import typer

from continual.python.cli import utils
from continual.python.sdk.client import Client


app = typer.Typer(help="Manage CLI configuration.")

# use callback to run list command if nothing is passed in
@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is not None:
        return
    else:
        show()


@app.command("clear-all")
@utils.exit_on_error
def continual_clear_all(
    print: bool = typer.Option(True, help="Print config after modification."),
):
    """Clear all configuration options.

    Clear all configurations and save the new configuration.
    """

    try:
        continual_clear(
            project=True,
            environment=True,
            style=True,
            endpoint=True,
            api_key=True,
            print=print,
        )
    except:
        typer.secho(
            "Error clearing all of the config",
            fg="red",
        )


@app.command("clear")
@utils.exit_on_error
def continual_clear(
    project: bool = typer.Option(False, "--project", help="Project ID."),
    environment: bool = typer.Option(False, "--environment", help="Environment Id"),
    style: bool = typer.Option(False, "--style", help="Display style."),
    endpoint: bool = typer.Option(
        False, "--endpoint", help="Optional endpoint for private cloud installations."
    ),
    api_key: bool = typer.Option(False, "--api-key", help="Api Key."),
    print: bool = typer.Option(True, help="Print config after modification."),
):
    """Clear configurations.

    Clear specific configurations and save the new configuration.
    """

    try:
        client = Client(verify=False)
        if project:
            client.config._project = ""
        if environment:
            client.config._environment = ""
        if style:
            client.config._style = "GREEN"
        if endpoint:
            client.config._endpoint = ""
        if api_key:
            client.config._api_key = ""

        client.config.save()

        if print:
            client.config.show()
    except:
        typer.secho(
            "Error clearing config",
            fg="red",
        )


@app.command("init")
@utils.exit_on_error
def continual_init(
    project: str = typer.Option(..., help="Project ID."),
    environment: str = typer.Option(None, help="Environment Id"),
    style: utils.ContinualStyle = typer.Option(None, help="Display style."),
):
    """Initialize configuration.

    Sets the default project, environment, and style for the SDK and CLI.  All future commands
    will use the default project if no project is explicitly passed. You may
    set the project and environment at the same time via project@environment.
    """
    try:
        c = Client(verify=False)
        set_project(project=project, print=False)
        if environment:
            set_environment(environment=environment, print=False)
        if style:
            set_style(style=style, print=False)
        c.config.show()
    except Exception as e:
        typer.secho(
            "Configuration initialization failed: %s" % e,
            fg="red",
        )


@app.command("set-project")
@utils.exit_on_error
def set_project(
    project: str = typer.Argument(..., help="Project ID."),
    print: bool = typer.Option(True, help="Print config after modification."),
):
    """Set default project.

    Sets the default project for the SDK and CLI.  All future commands
    will use the default project if no project is explicitly passed. You may
    set the project and environment at the same time via project@environment.
    """
    try:
        client = Client(verify=False)
        client.set_config_project(project, save=True)
        if print:
            client.config.show()
    except:
        typer.secho(
            "Project %s does not exist. Please create the project first!" % project,
            fg="red",
        )


@app.command("set-endpoint")
@utils.exit_on_error
def set_endpoint(
    endpoint: str = typer.Argument(..., help="Continual environment endpoint"),
    print: bool = typer.Option(True, help="Print config after modification."),
):
    """Set default endpoint"""
    c = Client(verify=False)
    old_endpoint = c.config.endpoint
    c.config._endpoint = endpoint
    c.config.save()

    # Reload client to check endpoint validity
    try:
        c = Client(verify=False)
        typer.secho(f"Sucessfully set endpoint to {endpoint}", fg="green")
        if print:
            c.config.show()
    except ValueError as e:
        c.config._endpoint = old_endpoint
        c.config.save()
        typer.secho("Endpoint %s is not valid : %s" % (endpoint, e), fg="red")


@app.command("set-environment")
@utils.exit_on_error
def set_environment(
    environment: str = typer.Argument(..., help="Environment ID."),
    print: bool = typer.Option(True, help="Print config after modification."),
):
    """Set default environment.

    Sets the default environment for the SDK and CLI.  All future commands
    will use the default environment if no environment is explicitly passed.
    """
    try:
        client = Client(verify=False)
        client.set_config_environment(environment=environment, save=True)
        if print:
            client.config.show()
    except:
        typer.secho(
            "Environment %s does not exist. Please create the environment first!"
            % environment,
            fg="red",
        )


@app.command("set-style")
@utils.exit_on_error
def set_style(
    style: utils.ContinualStyle = typer.Argument(..., help="Display style."),
    print: bool = typer.Option(True, help="Print config after modification."),
):
    """Set default CLI display style."""
    c = Client(verify=False)
    c.config._style = style.value
    c.config.save()
    if print:
        c.config.show()


@app.command("show")
@utils.exit_on_error
def show():
    """Show current config.

    Shows the current session configuration
    """
    c = Client(verify=False)
    c.config.show()
