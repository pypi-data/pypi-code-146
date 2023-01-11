import click

import truera.client.cli.cli_logger as cli_logger
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message


@click.group(help="Commands for restoring artifacts in truera")
def restore():
    pass


@restore.command(
    help="Trigger restore from a backup.",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@click.option(
    "--backup_path",
    "--path",
    help="Path to the backup folder, from where to restore.",
    required=True
)
def backup(connection_string, log_level, backup_path):
    UncaughtExceptionHandler.wrap(
        _restore_backup, connection_string, log_level, backup_path
    )


def _restore_backup(connection_string, log_level, backup_path):
    logger = cli_logger.create_cli_logger(log_level)
    backup_client = cli_utils.get_backup_client(connection_string, logger)
    backup_client.trigger_restore(backup_path=backup_path)
    click.echo("Successfully restored.")


if __name__ == '__main__':
    restore()
