import click
import requests
import validators

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.config import Config, store_login_config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.jwt import JWT
from sym.flow.cli.helpers.login.login_flow import BrowserRedirectFlow


def validate_email(ctx, param, value):
    """Returns value if the email address is valid, raises otherwise."""
    if value and not validators.email(value):
        raise click.BadParameter("must enter a valid email address")
    return value


@click.command(short_help="Log in to your Sym account")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--port",
    default=11001,
    help="Port to use for the local webserver.",
    show_default=True,
)
@click.option(
    "--org-id",
    prompt="Org ID",
    default=lambda: Config.instance().get("org"),
    help="The ID of the Organization you want to log in to.",
)
def login(options: GlobalOptions, port: int, org_id: str) -> None:
    """Log in to your Sym account to authenticate with the Sym API. This is required to enable privileged actions
    within your Organization such as authoring Sym Flows or installing the Slack App.

    \b
    Example:
        `symflow login --org-id S-0FNWNPZVI4`
    """
    if options.access_token:
        cli_output.fail("SYM_JWT is set, unset SYM_JWT to log in as a regular user")

    org = options.sym_api.get_organization_from_slug(org_id)

    # Save the organization to config so it will be autopopulated the next time `symflow login` is called.
    Config.set_org(org)

    flow = BrowserRedirectFlow(port)

    url, *_ = flow.gen_browser_login_params(options, org)
    styled_url = click.style(requests.utils.requote_uri(url), bold=True)  # type: ignore
    cli_output.info(
        f"Opening the login page in your browser. If this doesn't work, please visit the following URL:"
        + "\n"
        + styled_url
        + "\n"
    )

    # It's possible to not get an auth_token AND not have raised an exception before getting here
    # if the user has just signed up.
    if auth_token := flow.login(options, org):
        options.set_access_token(auth_token["access_token"])
        options.dprint(auth_token=auth_token)
        cli_output.success("Login succeeded")

        jwt = JWT.from_access_token(auth_token["access_token"], auth_url=options.auth_url)
        store_login_config(jwt.email, org, auth_token)


@click.command(short_help="Log out of your Sym account")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def logout(options: GlobalOptions) -> None:
    if not Config.is_logged_in() and not options.access_token:
        cli_output.fail("✖ You are already logged out!")

    if options.access_token:
        cli_output.fail("✖ You are logged in via SYM_JWT, you must unset SYM_JWT manually")

    if Config.is_logged_in():
        Config.logout()
        cli_output.success("✔️  You successfully logged out!")
