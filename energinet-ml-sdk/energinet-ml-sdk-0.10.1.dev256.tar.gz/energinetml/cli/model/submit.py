#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""
from typing import Tuple, Union

import click

from energinetml.backend import default_backend as backend
from energinetml.cli.utils import discover_model
from energinetml.cli.utils.verify import verify_compute_cluster
from energinetml.core.backend import AbstractBackend
from energinetml.core.model import Model
from energinetml.settings import PACKAGE_NAME, PACKAGE_REQUIREMENT, PACKAGE_VERSION


@click.command()
@discover_model()
@click.argument("parameters", nargs=-1)
@click.option(
    "--wait/--nowait",
    default=True,
    help="Wait for experiment to complete before exiting (default: yes)",
)
@click.option(
    "--download", "-d", is_flag=True, help="Download output files after Run completed"
)
@click.option("--seed", "-s", required=False, default=None, type=str, help="Seed value")
def submit(
    parameters: Tuple[str, ...],
    wait: bool,
    download: bool,
    seed: Union[int, str],
    model: Model,
) -> None:
    """Submit a model to be trained in the cloud."""
    if download and not wait:
        click.echo("Can not use -d/--download together with --nowait")
        raise click.Abort()

    # -- Verify SDK requirement ----------------------------------------------

    # Verify requirements.txt contains energinet-ml-sdk
    if PACKAGE_NAME not in model.requirements:
        click.echo(
            (
                f"Could not find '{PACKAGE_NAME}' in the project's "
                f"requirements.txt file: {model.project.requirements_file_path}"
            )
        )
        click.echo("I suggest you add the following line:")
        click.echo("")
        click.echo(f"    {PACKAGE_REQUIREMENT}")
        click.echo("")
        raise click.Abort()

    required_sdk_version = model.requirements.get_version(PACKAGE_NAME)

    if required_sdk_version is None:
        click.echo(
            f"Using latest version of {PACKAGE_NAME} when training in the cloud."
        )
    else:
        if required_sdk_version < PACKAGE_VERSION:
            click.echo("=" * 79)
            click.echo(
                (
                    "WARNING: Your requirements.txt file contains a version of "
                    "%s (%s) which is older than your current installation (%s). "
                    "I suggest you update your requirements.txt to match "
                    "your current installation. "
                )
                % (PACKAGE_NAME, required_sdk_version, PACKAGE_VERSION)
            )
            click.echo("=" * 79)
        elif required_sdk_version > PACKAGE_VERSION:
            click.echo("=" * 79)
            click.echo(
                (
                    "WARNING: Your requirements.txt file contains a version of "
                    "%s (%s) which is newer than your current installation (%s). "
                    "I suggest you upgrade your installation using "
                    '"pip install --upgrade %s ...". '
                )
                % (PACKAGE_NAME, required_sdk_version, PACKAGE_VERSION, PACKAGE_NAME)
            )
            click.echo("=" * 79)

        click.echo(
            "Using {} version {} when training in the cloud.".format(
                PACKAGE_NAME, required_sdk_version
            )
        )

    # -- Verify computer cluster ---------------------------------------------
    verify_compute_cluster(backend, model, model.compute_target)
    verify_vm_size(backend, model)

    # -- Train Parameters ----------------------------------------------------

    if seed:
        parameters = list(parameters)
        parameters.extend(("--seed", seed))

    # -- Submit --------------------------------------------------------------

    context = backend.submit_model(model=model, params=parameters)

    # Stream output to console?
    if wait:
        click.echo("-" * 79)
        click.echo("Streaming Run log...")
        click.echo("-" * 79)

        try:
            context.wait_for_completion()
        except context.FailedToWait as e:
            click.echo("-" * 79)
            click.echo(str(e))
            click.echo("")
            raise click.Abort()

    # -- Post-Run ------------------------------------------------------------

    # Download output files?
    if download:
        click.echo("-" * 79)
        click.echo("Downloading files...")
        context.download_files()


def verify_vm_size(backend: AbstractBackend, model: Model):
    """Verifies that the VM size of the compute cluster matches
    the model's requirements.

    Args:
        backend (AbstractBackend): The backend to use.
        model (Model): The model that specifies the vm size

    Raises:
        click.Abort: If the compute cluster VM size does not match the
            model's requirements.
    """

    workspace = backend.get_workspace(model.project.as_dict())
    existing_clusters = backend.get_compute_clusters(workspace)
    existing_cluster_names = [c.name for c in existing_clusters]

    cluster_name = model.compute_target
    cluster = existing_clusters[existing_cluster_names.index(cluster_name)]

    if cluster.vm_size.casefold() != model.vm_size.casefold():
        click.echo(
            (
                f"WARNING: The VM size ({model.vm_size.casefold()}) "
                f"specified in {model._CONFIG_FILE_NAME}"
                " does not match the actual VM size of the "
                f"compute cluster ({cluster.vm_size.casefold()})."
            ),
            err=True,
        )
        raise click.Abort()
