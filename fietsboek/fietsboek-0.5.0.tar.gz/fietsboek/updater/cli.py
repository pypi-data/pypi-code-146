"""Updater for Fietsboek.

While this script does not download and install the latest Fietsboek version
itself (as this step depends on where you got Fietsboek from), it takes care of
managing migrations between Fietsboek versions. In particular, the updater
takes care of running the database migrations, migrating the data directory and
migrating the configuration.
"""
import logging.config

import click

from . import Updater

# We keep this as a separate option that is added to each subcommand as Click
# (unlike argparse) cannot handle "--help" without the required arguments of
# the parent (so "fietsupdate update --help" would error out)
# See also
# https://github.com/pallets/click/issues/295
# https://github.com/pallets/click/issues/814
config_option = click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to the Fietsboek configuration file",
)


def user_confirm(verb):
    """Ask the user for confirmation before proceeding.

    Aborts the program if no confirmation is given.

    :param verb: The verb to use in the text.
    :type verb: str
    """
    click.secho("Warning:", fg="yellow")
    click.echo(
        f"{verb} *may* cause data loss. Make sure to have a backup of the "
        "database and the data directory!"
    )
    click.echo("For more information, please consult the documentation.")
    click.confirm("Proceed?", abort=True)


@click.group(
    help=__doc__,
    context_settings={"help_option_names": ["-h", "--help"]},
)
def cli():
    """CLI main entry point."""


@cli.command("update")
@config_option
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Skip the safety question and just run the update",
)
@click.argument("version", required=False)
@click.pass_context
def update(ctx, config, version, force):
    """Run the update process.

    Make sure to consult the documentation and ensure that you have a backup
    before starting the update, to prevent any data loss!

    VERSION specifies the version you want to update to. Leave empty to choose
    the latest version.
    """
    logging.config.fileConfig(config)
    updater = Updater(config)
    updater.load()
    if version and not updater.exists(version):
        ctx.fail(f"Version {version!r} not found")

    version_str = ", ".join(updater.current_versions())
    click.echo(f"Current version: {version_str}")
    if not version:
        heads = updater.heads()
        if len(heads) != 1:
            ctx.fail("Ambiguous heads, please specify the version to update to")

        version = heads[0]

    click.echo(f"Selected version: {version}")
    if updater.has_applied(version):
        click.secho("Nothing to do", fg="green")
        ctx.exit()

    if not force:
        user_confirm("Updating")
    updater.upgrade(version)
    version_str = ", ".join(updater.current_versions())
    click.secho(f"Update succeeded, version: {version_str}", fg="green")


@cli.command("downgrade")
@config_option
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Skip the safety question and just run the downgrade",
)
@click.argument("version")
@click.pass_context
def downgrade(ctx, config, version, force):
    """Run the downgrade process.

    Make sure to consult the documentation and ensure that you have a backup
    before starting the downgrade, to prevent any data loss!

    VERSION specifies the version you want to downgrade to.
    """
    logging.config.fileConfig(config)
    updater = Updater(config)
    updater.load()
    if version and not updater.exists(version):
        ctx.fail(f"Version {version!r} not found")

    version_str = ", ".join(updater.current_versions())
    click.echo(f"Current version: {version_str}")
    click.echo(f"Downgrade to version {version}")
    if updater.has_applied(version, backward=True):
        click.secho("Nothing to do", fg="green")
        ctx.exit()
    if not force:
        user_confirm("Downgrading")
    updater.downgrade(version)
    version_str = ", ".join(updater.current_versions())
    click.secho(f"Downgrade succeeded, version: {version_str}", fg="green")


@cli.command("revision", hidden=True)
@config_option
@click.argument("revision_id", required=False)
def revision(config, revision_id):
    """Create a new revision.

    This automatically populates the revision dependencies and alembic
    versions, based on the current state.

    This command is useful for developers who work on Fietsboek.
    """
    logging.config.fileConfig(config)
    updater = Updater(config)
    updater.load()
    current = updater.current_versions()
    heads = updater.heads()
    if not any(version in heads for version in current):
        click.secho("Warning:", fg="yellow")
        click.echo("Your current revision is not a head. This will create a branch!")
        click.echo(
            "If this is not what you intended, make sure to update to the latest "
            "version first before creating a new revision."
        )
        click.confirm("Proceed?", abort=True)
    filename = updater.new_revision(revision_id)
    click.echo(f"Revision saved to {filename}")


@cli.command("status")
@config_option
def status(config):
    """Display information about the current version and available updates."""
    logging.config.fileConfig(config)
    updater = Updater(config)
    updater.load()
    current = updater.current_versions()
    heads = updater.heads()
    click.secho("Current versions:", fg="yellow")
    if current:
        has_unknown = False
        for i in current:
            if updater.exists(i):
                click.echo(i)
            else:
                click.echo(f"{i} [unknown]")
                has_unknown = True
        if has_unknown:
            click.echo("[*] Your version contains revisions that are unknown to me")
            click.echo("[*] This can happen if you apply an update and then downgrade the code")
            click.echo("[*] Make sure to keep your code and data in sync!")
    else:
        click.secho("No current version", fg="red")
    click.secho("Available updates:", fg="yellow")
    updates = set(heads) - set(current)
    if updates:
        for i in updates:
            click.echo(i)
    else:
        click.secho("All updates applied!", fg="green")


@cli.command("help", hidden=True)
@click.pass_context
@click.argument("subcommand", required=False)
def help_(ctx, subcommand):
    """Shows the help for a given subcommand.

    This is equivalent to using the --help option.
    """
    if not subcommand:
        click.echo(cli.get_help(ctx.parent))
        return
    cmd = cli.get_command(ctx, subcommand)
    if cmd is None:
        click.echo(f"Error: Command {subcommand} not found")
    else:
        # Create a new context so that the usage shows "fietsboek subcommand"
        # instead of "fietsboek help"
        with click.Context(cmd, ctx.parent, subcommand) as subcontext:
            click.echo(cmd.get_help(subcontext))


if __name__ == "__main__":
    cli()
