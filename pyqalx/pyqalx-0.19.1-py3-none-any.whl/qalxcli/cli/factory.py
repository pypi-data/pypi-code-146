import logging

import click

from pyqalx import QalxSession
from pyqalx.core.errors import (
    QalxFactoryValidationError,
    QalxFactoryPackError,
    QalxFactoryBuildError,
    QalxFactoryDemolishError,
)
from pyqalx.factories.factory import Factory
from pyqalx.factories.sectors.providers import AWSProvider

from .. import cli_types
from ..cli.qalx import qalx
from ..utils import DemolishFactoryTabulation, FactoryTabulation


@qalx.command("factory-validate")
@click.option(
    "--plan",
    type=click.Path(exists=True),
    help="The path to the file that contains the factory plan definition",
    required=True,
)
@click.option(
    "-aws",
    "--aws-profile",
    help="The AWS profile name to use for remote stacks",
    default=AWSProvider.default_profile_name(),
)
@click.pass_context
def validate(ctx, plan, aws_profile):
    """
    Validate a factory
    """
    session = QalxSession(profile_name=ctx.obj["USER_PROFILE"])
    factory = Factory(
        session,
        user_profile=ctx.obj["USER_PROFILE"],
        bot_profile=ctx.obj["BOT_PROFILE"],
        aws_profile=aws_profile,
    )

    try:
        factory.validate(plan=plan)
    except QalxFactoryValidationError as exc:
        # QalxFactoryValidationError: An error occurred while validating
        factory._msg_user(title="validation", msg=str(exc), level=logging.ERROR)
        factory._msg_user(msg="Factory Validation Failed")


@qalx.command("factory-pack")
@click.option(
    "--stage", type=cli_types.QALX_FACTORY_STAGE, help="The stage to pack"
)
@click.option(
    "--plan",
    type=click.Path(exists=True),
    help="The path to the file that contains the factory plan definition",
    required=True,
    is_eager=True,
)
@click.option(
    "--no-delete",
    is_flag=True,
    help="If provided will *not* delete the packed bots when this command"
    " completes. By default, the packed bots will be deleted.",
)
@click.option(
    "-aws",
    "--aws-profile",
    help="The AWS profile name to use for remote stacks",
    default=AWSProvider.default_profile_name(),
)
@click.pass_context
def pack(ctx, plan, stage, aws_profile, no_delete):
    """
    Pack a factory
    """
    session = QalxSession(profile_name=ctx.obj["USER_PROFILE"])
    factory = Factory(
        session,
        user_profile=ctx.obj["USER_PROFILE"],
        bot_profile=ctx.obj["BOT_PROFILE"],
        aws_profile=aws_profile,
    )
    try:
        factory.pack(plan=plan, stage=stage, delete=not no_delete)
    except (QalxFactoryValidationError, QalxFactoryPackError) as exc:
        # QalxFactoryValidationError: An error occurred while validating
        # QalxFactoryPackError: An error occurred while packing
        factory._msg_user(title="pack", msg=str(exc), level=logging.ERROR)
        factory._msg_user(msg="Factory Pack Failed")


@qalx.command("factory-build")
@click.option(
    "--stage",
    type=cli_types.QALX_FACTORY_STAGE,
    help="The stage to build",
    required=True,
)
@click.option(
    "--plan",
    type=click.Path(exists=True),
    help="The path to the file that contains the factory plan definition",
    required=True,
    is_eager=True,
)
@click.option(
    "-aws",
    "--aws-profile",
    help="The AWS profile name to use for remote stacks",
    default=AWSProvider.default_profile_name(),
)
@click.pass_context
def build(ctx, plan, stage, aws_profile):
    """
    Build a factory
    """
    session = QalxSession(profile_name=ctx.obj["USER_PROFILE"])
    factory = Factory(
        session,
        user_profile=ctx.obj["USER_PROFILE"],
        bot_profile=ctx.obj["BOT_PROFILE"],
        aws_profile=aws_profile,
    )
    try:
        factory.build(plan=plan, stage=stage)
    except (
        QalxFactoryValidationError,
        QalxFactoryPackError,
        QalxFactoryBuildError,
    ) as exc:
        # QalxFactoryValidationError: An error occurred while validating
        # QalxFactoryPackError: An error occurred while packing
        # QalxFactoryBuildError: There was an error with building. Most of
        #                        these are handled internally by build as
        #                        resources need to be tidied up
        factory._msg_user(title="build", msg=str(exc), level=logging.ERROR)
        factory._msg_user(msg="Factory Build Failed")


@qalx.command("factory-demolish")
@click.option(
    "--name", type=click.STRING, help="The name of the factory", required=True
)
@click.pass_context
def demolish(ctx, name):
    """
    Demolish a factory. If a factory to demolish is identified, the user is
    asked for confirmation before the demolish method is called
    """
    session = QalxSession(profile_name=ctx.obj["USER_PROFILE"])
    factory = Factory(session)
    factory_tabulation = DemolishFactoryTabulation(session, name)
    factory_to_demolish = factory_tabulation.get_entity_or_display()

    if factory_to_demolish:
        if click.confirm(f"Are you sure you want to demolish factory: {name}?"):
            try:
                factory.demolish(factory_to_demolish.guid)
            except QalxFactoryDemolishError as exc:
                # QalxFactoryDemolishError: There was an error with demolishing
                factory._msg_user(
                    title="demolish", msg=str(exc), level=logging.ERROR
                )
                factory._msg_user(msg="Factory Demolish Failed")


@qalx.command("factory-info")
@click.option(
    "--name", type=click.STRING, help="The name of the factory", required=True
)
@click.pass_context
def info(ctx, name):
    """
    Get info about a factory
    """
    session = QalxSession(profile_name=ctx.obj["USER_PROFILE"])
    factory_tabulation = FactoryTabulation(session, name, tabulate_single=True)
    factory_tabulation.get_entity_or_display()
