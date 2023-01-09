import os

import rich_click as click

from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.lib.infra.install_truefoundry import InfraController
from servicefoundry.logger import logger


@click.group(
    name="bootstrap",
    cls=GROUP_CLS,
)
def bootstrap():
    pass


@click.command(
    name="cloud-infra",
    cls=COMMAND_CLS,
    help="Bootstrap Cloud Infrastructure for Truefoundry",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
)
@click.option(
    "--file",
    is_flag=False,
)
def bootstrap_cloud_infra(dry_run: bool, file: str):
    # If file doesn't exist, then print error
    if file and not os.path.exists(file):
        logger.error(
            f"File at path: {file} not found. Please make sure input file exists"
        )
        return
    infra_controller = InfraController(dry_run=dry_run, config_file_path=file)
    infra_controller.create_infra_using_terraform()


@click.command(
    name="kubernetes",
    cls=COMMAND_CLS,
    help="Bootstrap truefoundry platform on an existing Kubernetes cluster",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
)
@click.option(
    "--file",
    is_flag=False,
)
def bootstrap_kubernetes(dry_run: bool, file: str):
    # If file doesn't exist, then print error
    if not file:
        logger.error("Input file needs to be provided")
        return
    if file and not os.path.exists(file):
        logger.error(
            f"File at path: {file} not found. Please make sure input file exists"
        )
        return
    infra_controller = InfraController(dry_run=dry_run, config_file_path=file)
    infra_controller.setup_kubernetes_cluster()
    return


@click.command(
    name="tfy-control-plane",
    cls=COMMAND_CLS,
    help="Bootstrap truefoundry control-plane on a existing kubernetes cluster",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
)
@click.option(
    "--file",
    is_flag=False,
)
def bootstrap_tfy_control_plane(dry_run: bool, file: str):
    # If file doesn't exist, then print error
    if not file:
        logger.error("Input file needs to be provided")
        return
    if file and not os.path.exists(file):
        logger.error(
            f"File at path: {file} not found. Please make sure input file exists"
        )
        return
    infra_controller = InfraController(dry_run=dry_run, config_file_path=file)
    infra_controller.setup_tfy_control_plane()
    return


def get_infra_command():
    bootstrap.add_command(bootstrap_cloud_infra)
    bootstrap.add_command(bootstrap_kubernetes)
    bootstrap.add_command(bootstrap_tfy_control_plane)
    return bootstrap
