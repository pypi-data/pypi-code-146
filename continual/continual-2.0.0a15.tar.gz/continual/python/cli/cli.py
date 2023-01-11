import typer
import os
import click
import urllib.parse

import socket
import threading
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from continual.python.sdk.client import Client, __version__

from pathlib import Path


from continual.python.cli import (
    models,
    model_versions,
    experiments,
    projects,
    environments,
    organizations,
    users,
    batch_predictions,
    promotions,
    utils,
    events,
    reports,
    config,
    runs,
)
from typing import Optional
from continual.python.cli.utils import exit_with_error


def version_callback(value: bool):
    if value:
        try:
            c = Client()
            client_version, server_version, upgrade_required = c.version()
            typer.echo(f"Continual SDK Version: {client_version}")
            typer.echo(f"Continual Server Version: {server_version}")
            if upgrade_required:
                typer.secho(
                    f"Upgrade is required",
                    fg="red",
                )
        except Exception as e:
            typer.echo(f"Continual SDK Version: {__version__}")
            typer.secho(
                f"Unable to retrieve Continual Server Version",
                fg="red",
            )
            exit_with_error(e)
        raise typer.Exit()


# ************************#
# Define Typer Structure #
# ************************#


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()


app_helptext = "Continual - Operational AI. Simplified."

cli = typer.Typer(cls=NaturalOrderGroup, help=app_helptext, no_args_is_help=True)

cli.add_typer(models.app, name="models")
cli.add_typer(model_versions.app, name="model-versions")
cli.add_typer(experiments.app, name="experiments")
cli.add_typer(promotions.app, name="promotions")
cli.add_typer(batch_predictions.app, name="batch-predictions")
cli.add_typer(projects.app, name="projects")
cli.add_typer(environments.app, name="environments")
cli.add_typer(organizations.app, name="organizations")
cli.add_typer(users.app, name="users")
cli.add_typer(events.app, name="events")
cli.add_typer(runs.app, name="runs")
cli.add_typer(reports.app, name="report", hidden=True)
cli.add_typer(config.app, name="config")


@cli.callback(context_settings=dict(help_option_names=["-h", "--help"]))
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print Continual CLI version",
    ),
):
    return


@cli.command("help", add_help_option=False, options_metavar="")
def help(ctx: typer.Context):
    """Show CLI usage help."""
    ctx.info_name = None
    typer.echo(ctx.parent.command.get_help(ctx))


def get_verification_token_oob(params: dict) -> str:
    endpoint = utils.get_app_url()
    sso_link = "{}/s/sso/auth?mode=cli-oob".format(endpoint)
    for k, v in params.items():
        sso_link += f"&{k}={urllib.parse.quote_plus(v)}"

    typer.secho("\nVisit the following link to log in:")
    typer.secho(f"\n\t{sso_link}", fg="blue")

    typer.echo("")

    verification_code = ""
    try:
        verification_code = typer.prompt("Verification code", hide_input=True)
    except typer.Abort:
        typer.secho("Aborted!")
        exit(1)

    if not verification_code:
        typer.secho("Invalid verification token.", fg="red")
        exit(1)

    return verification_code


def find_open_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def is_ssh(echo: bool = False) -> bool:
    val = os.getenv("SSH_CLIENT") is not None or os.getenv("SSH_TTY") is not None
    if echo:
        typer.secho(f"is SSH?: {val}")
    return val


def is_docker(echo: bool = False) -> bool:
    cgroup = Path("/proc/self/cgroup")
    val = (
        Path("/.dockerenv").is_file()
        or cgroup.is_file()
        and cgroup.read_text().find("docker") > -1
    )
    if echo:
        typer.secho(f"is Docker?: {val}")
    return val


def get_verification_token_inband(params: dict) -> str:
    open_port = find_open_port()

    endpoint = utils.get_app_url()
    sso_link = "{}/s/sso/auth?mode=cli&next={}".format(
        endpoint,
        urllib.parse.quote_plus(f"http://localhost:{open_port}/continual-auth"),
    )
    for k, v in params.items():
        sso_link += f"&{k}={urllib.parse.quote_plus(v)}"

    verification_token = ""

    class AuthHandler(SimpleHTTPRequestHandler):

        verification_token = ""

        def log_message(self, format, *args):
            pass

        def do_GET(self):
            if self.path.startswith("/continual-auth"):
                if self.path.split("?")[-1]:
                    query = urllib.parse.parse_qs(self.path.split("?")[-1])
                    if "token" in query:
                        AuthHandler.verification_token = query["token"][0]
                        self.send_response(301)
                        self.send_header(
                            "Location", f"{endpoint}/notifications/cli-login-success"
                        )
                        self.end_headers()

                self.send_response(301)
                self.send_header(
                    "Location", f"{endpoint}/notifications/cli-login-failure"
                )
                self.end_headers()
            else:
                super().do_GET()
            self.server.shutdown()

    class AuthServer(threading.Thread):
        def run(self):
            self.server = ThreadingHTTPServer(("localhost", open_port), AuthHandler)
            self.server.serve_forever()

        def stop(self):
            self.server.shutdown()

    server = AuthServer()
    server.setDaemon(True)
    server.start()

    typer.secho("\nVisit the following link to log in:")
    typer.secho(f"\n\t{sso_link}", fg="blue")

    try:
        typer.secho("\nWaiting for response...")
        while server.is_alive():
            time.sleep(1)
    except typer.Abort:
        typer.echo("Aborted!")
        exit(1)

    verification_token = AuthHandler.verification_token or verification_token
    if not verification_token:
        typer.secho("Invalid verification token.", fg="red")
        exit(1)

    return verification_token


def verify_token(client: Client, token: str) -> str:
    from continual.rpc.management.v1 import management_pb2

    old_api_key = client.config._api_key
    client.config._api_key = ""
    req = management_pb2.ExchangeTokenRequest(token=token)
    res = client._management.ExchangeToken(req)
    if res.token:
        client.config._api_key = old_api_key
        return res.token
    client.config._api_key = old_api_key
    return ""


def sso_login(client: Client, org: str = "", oob: bool = None):
    if oob is None:
        oob = is_ssh() or is_docker()
    try:
        org = typer.prompt("Organization name (organizations/abc)")
    except typer.Abort:
        typer.secho("Aborted!")
        exit(1)

    verification_code = ""
    if oob:
        verification_code = get_verification_token_oob(dict(org=org))
    else:
        verification_code = get_verification_token_inband(dict(org=org))

    api_key = verify_token(client, verification_code)

    old_api_key = client.config._api_key
    client.set_config_api_key(api_key, save=False)

    organization = None

    try:
        user = client.viewer()
        organization = client.organizations.get(org.split("/")[-1])
        typer.secho(
            f"\n🚀 Hey {user.first_name}! We've successfully logged you in to {organization.display_name} (id: {organization.id}) via SAML SSO.\n",
            fg="blue",
        )
        client.config.save()
    except Exception:
        typer.secho("Failed to authenticate user.", fg="red")
        client.config.set_api_key(old_api_key)
        exit(1)

    if organization:
        client.config._project = None
        projects = organization.projects.list_all()
        i = 1
        proj_list = []
        if len(list(projects)) > 0:
            for project in projects:
                if i == 1:
                    typer.echo("Select default project:")
                project_id = project.name.split("/")[-1]
                proj_list.append(project.name)
                typer.echo(f" [{i}]: {project.display_name} ({project_id})")
                i += 1
            key = typer.prompt("Choice")
            client.config._project = proj_list[int(key) - 1]
            client.config._environment = "production"
            client.config.save()
        else:
            typer.secho(
                "This organization has no associated projects. You should create a project in the Continual Web UI and then use `continual config set-project <project>` to use the CLI."
            )
        exit(0)
    else:
        typer.secho("Could not find current organization.", fg="red")
        exit(1)


def oauth_login(
    client: Client, oob: bool = None, google: bool = False, microsoft: bool = False
):
    if oob is None:
        oob = is_ssh() or is_docker()

    provider = ""
    if google:
        provider = "GoogleOAuth"
    elif microsoft:
        provider = "MicrosoftOAuth"
    else:
        typer.secho("An OAuth provider was not specified.", fg="red")

    verification_code = ""
    if oob:
        verification_code = get_verification_token_oob(dict(provider=provider))
    else:
        verification_code = get_verification_token_inband(dict(provider=provider))

    api_key = verify_token(client, verification_code)

    old_api_key = client.config.api_key
    client.set_config_api_key(api_key, save=False)

    try:
        user = client.viewer()
        typer.secho(
            f"\n🚀 Hey {user.first_name}! We've successfully logged you in to Continual via {'Google' if google else 'Microsoft'} OAuth.\n",
            fg="blue",
        )
        client.config.save()
    except Exception:
        typer.secho("Failed to authenticate user.", fg="red")
        client.config.set_api_key(old_api_key)
        exit(1)


@cli.command("login")
@utils.exit_on_error
def login(
    email: str = typer.Option(default="", help="Email address."),
    password: str = typer.Option(default="", help="Password."),
    project: str = typer.Option(None, help="Default project."),
    sso: bool = typer.Option(False, "--sso", help="Log in with SAML SSO."),
    oauth: bool = typer.Option(
        False, "--oauth", help="Log in with a supported OAuth provider."
    ),
    google: bool = typer.Option(False, "--google", help="Log in with Google OAuth."),
    microsoft: bool = typer.Option(
        False, "--microsoft", help="Log in with Microsoft OAuth."
    ),
    endpoint: str = typer.Option(
        None,
        envvar="CONTINUAL_ENDPOINT",
        help="Optional endpoint for private cloud installations.",
    ),
):
    """Log in to Continual.

    Logs in to Continual and saves the session information to
    ~/.continual/continual.yaml which is used by the SDK/CLI. All
    future commands will use the session information to authenticate
    and use the default project if not explicitly passed.
    """
    client = Client(endpoint=endpoint, verify=False)
    if sso:
        return sso_login(client)
    elif google or microsoft or oauth:
        if oauth and not (google or microsoft):
            typer.secho("Pick an OAuth provider to log in with:\n")
            choices = ["Google OAuth", "Microsoft OAuth"]
            for idx, choice in enumerate(choices):
                typer.echo(f" [{idx + 1}]: {choice}")
            typer.echo("")
            try:
                key = typer.prompt("Choice")
                oauth_choice = choices[int(key) - 1]
                if oauth_choice == "Google OAuth":
                    google = True
                elif oauth_choice == "Microsoft OAuth":
                    microsoft = True
            except typer.Abort:
                typer.secho("Aborted!")
                exit(1)
        return oauth_login(client, google=google, microsoft=microsoft)
    else:
        if not email:
            try:
                email = typer.prompt("Email")
            except typer.Abort:
                typer.secho("Aborted!")
                exit(1)

        if not password:
            try:
                password = typer.prompt("Password", hide_input=True)
            except typer.Abort:
                typer.secho("Aborted!")
                exit(1)

    user = client.login(email=email, password=password)
    if project is None:
        client.config._project = None
        projects = client.projects.list_all()
        i = 1
        proj_list = []
        if len(list(projects)) > 0:
            for project in projects:
                if i == 1:
                    typer.echo("Select default project:")
                project_id = project.name.split("/")[-1]
                proj_list.append(project.name)
                typer.echo(f" [{i}]: {project.display_name} ({project_id})")
                i += 1
            key = typer.prompt("Choice")
            client.config._project = proj_list[int(key) - 1]
            client.config._environment = "production"
        else:
            typer.secho(
                "You have no projects created in Continual. You should create a project in the Continual Web UI and then use `continual config set-project <project>` to use the CLI."
            )
    else:
        client.config._project = project
        client.config._environment = "production"
    client.config.save()
    typer.echo(
        f"🚀 Login successful.  Welcome to Continual, {user.first_name} {user.last_name}."
    )


@cli.command("logout")
@utils.exit_on_error
def logout():
    """Log out of Continual.

    Logs out of the current session.
    """
    c = Client(verify=False)
    c.logout()
    typer.echo("👋 See you later, come back soon!")


if __name__ == "__main__":
    cli()
