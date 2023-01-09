#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""

import click

from energinetml.core.backend import AbstractBackend
from energinetml.core.model import Model
from energinetml.settings import PACKAGE_NAME


def verify_compute_cluster(
    backend: "AbstractBackend",
    model: "Model",
    cluster_name: str,
    modify_vm_size: bool = False,
):
    """Verifies that the compute cluster exists.
    If not, the user is asked to choose another one.

    Args:
        backend (AbstractBackend): The backend to use.
        model (Model): Model which contains information about the compute cluster.
        cluster_name (str): The name of the compute cluster. This could be a new one.
        modify_vm_size (bool, optional): Boolean indicating if this method should
        change the vm_size. Defaults to False.

    Raises:
        click.Abort: If no compute clusters exist.
    """
    workspace = backend.get_workspace(model.project.as_dict())
    existing_clusters = backend.get_compute_clusters(workspace)
    existing_clusters_mapped = {c.name: c for c in existing_clusters}
    existing_cluster_names = [c.name for c in existing_clusters]

    if not existing_clusters:
        click.echo('No compute clusters exists in workspace "%s".' % workspace.name)
        click.echo('Run "%s cluster create" to create a new cluster.' % PACKAGE_NAME)
        raise click.Abort()

    while cluster_name not in existing_cluster_names:
        click.echo(
            (
                f"Could not find compute target '{cluster_name}' in the "
                f"available compute targets: {existing_cluster_names}."
            )
        )

        cluster_name = click.prompt(
            text="Please enter name of a compute cluster to use",
            type=click.Choice(existing_cluster_names),
        )

        click.echo(f"Using cluster '{cluster_name}' from now on.")

    cluster = existing_clusters_mapped[cluster_name]
    model.compute_target = cluster_name

    if modify_vm_size:
        model.vm_size = cluster.vm_size

    model.save()
