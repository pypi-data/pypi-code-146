import click
from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgHttpError
from cnvrgv2.utils.validators import validate_user_role


@click.group(name='members')
def members_group():
    pass


@members_group.command()
@click.option('-e', '--email', prompt=messages.MEMBER_ENTER_EMAIL, help=messages.MEMBER_HELP_EMAIL)
@click.option('-r', '--role', prompt=messages.MEMBER_ENTER_ROLE, help=messages.MEMBER_HELP_ROLE)
@prepare_command()
def add(cnvrg, logger, email, role):
    """
    Creates a new memberships
    """

    if not validate_user_role(role):
        logger.log_and_echo(error_messages.MEMBER_NOT_VALID_ROLE.format(role), error=True)

    cnvrg.members.add(email=email, role=role)
    success_message = messages.MEMBER_ADDED_SUCCESS.format(email, role)
    logger.log_and_echo(success_message)


@members_group.command(name='list')
@prepare_command()
def list_command(cnvrg):
    """
    list all members
    """
    members = cnvrg.members.list()
    table = PrettyTable()
    table.field_names = ["Username", "Email", "Role"]
    table.align["Username"] = "l"
    table.align["email"] = "l"
    for member in members:
        table.add_row([member.username, member.email, member.role.capitalize()])
    click.echo(table)


@members_group.command(name='revoke')
@click.option('-e', '--email', prompt=messages.MEMBER_ENTER_EMAIL, help=messages.MEMBER_HELP_EMAIL)
@prepare_command()
def revoke(cnvrg, logger, email):
    """
    removes a memberships
    """
    try:
        cnvrg.members.get(email).revoke()
    except CnvrgHttpError as error:
        logger.log_and_echo(error, error=True)
        return

    success_message = messages.MEMBER_REMOVED_SUCCESS.format(email)
    logger.log_and_echo(success_message)


@members_group.command(name="update")
@click.option('-e', '--email', prompt=messages.MEMBER_ENTER_EMAIL, help=messages.MEMBER_HELP_EMAIL)
@click.option('-r', '--role', prompt=messages.MEMBER_ENTER_ROLE, help=messages.MEMBER_HELP_ROLE)
@prepare_command()
def update(cnvrg, logger, email, role):
    """
    update a membership
    """

    if not validate_user_role(role):
        logger.log_and_echo(error_messages.MEMBER_NOT_VALID_ROLE.format(role), error=True)

    cnvrg.members.get(email=email).update(role=role)
    success_message = messages.MEMBER_UPDATED_SUCCESS.format(email, role)
    logger.log_and_echo(success_message)
