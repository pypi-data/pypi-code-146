#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""
import click

from energinetml.backend import default_backend as backend
from energinetml.cli.utils import discover_model
from energinetml.cli.utils.verify import verify_compute_cluster
from energinetml.core.model import Model


@click.command()
@discover_model()
@click.option(
    "--cluster-name",
    "cluster_name",
    required=False,
    default=None,
    type=str,
    help="Name of compute cluster, if creating a new cluster",
)
def change(model: Model, cluster_name: str) -> None:
    """Switch to use another (existing) compute cluster."""

    verify_compute_cluster(backend, model, cluster_name, modify_vm_size=True)
