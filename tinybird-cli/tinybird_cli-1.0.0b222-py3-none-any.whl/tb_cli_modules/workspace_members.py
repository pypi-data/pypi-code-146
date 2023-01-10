
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Tuple
import click
from click import Context

import humanfriendly
from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.common import ask_for_user_token, coro, get_config_and_hosts, get_current_workspace
from tinybird.tb_cli_modules.workspace import workspace


@dataclass
class WorkspaceMemberCommandContext:
    client: TinyB
    config: Dict[str, Any]
    host: str
    ui_host: str
    workspace: Dict[str, Any]


async def get_command_context(ctx: click.Context) -> WorkspaceMemberCommandContext:
    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    workspace = await get_current_workspace(client, config)
    if not workspace:
        raise click.ClickException(FeedbackManager.error_unknown_resource(resource=config['d']))  # type: ignore

    return WorkspaceMemberCommandContext(client, config, host, ui_host, workspace)


def get_workspace_users(cmd_ctx: WorkspaceMemberCommandContext) -> Tuple[Any, ...]:
    return tuple(u['email'] for u in cmd_ctx.workspace['members'])


@workspace.group()
@click.pass_context
def members(ctx):
    '''Workspace members management commands'''


@members.command(name='add', short_help="Adds members to the current Workspace")
@click.argument('members_emails')
@click.option('--user_token', is_flag=False, default=None, help="When passed, we won't prompt asking for it")
@click.pass_context
@coro
async def add_members_to_workspace(ctx: Context, members_emails: str, user_token: str):
    """Adds members to the current Workspace"""

    cmd_ctx = await get_command_context(ctx)

    requested_users = members_emails.split(',')
    users_to_add = [u for u in requested_users if u not in get_workspace_users(cmd_ctx)]

    if len(users_to_add) == 0:
        msg = FeedbackManager.info_user_already_exists(user=requested_users[0], workspace_name=cmd_ctx.workspace['name']) if len(requested_users) == 1 else FeedbackManager.info_users_already_exists(workspace_name=cmd_ctx.workspace['name'])
        click.echo(msg)
    else:
        if not user_token:
            user_token = ask_for_user_token(f"add users to {cmd_ctx.workspace['name']}", cmd_ctx.ui_host)

        user_client: TinyB = deepcopy(cmd_ctx.client)
        user_client.token = user_token
        await user_client.add_users_to_workspace(cmd_ctx.workspace, users_to_add)
        msg = FeedbackManager.success_workspace_user_added(user=users_to_add[0], workspace_name=cmd_ctx.workspace['name']) if len(users_to_add) == 1 else FeedbackManager.success_workspace_users_added(workspace_name=cmd_ctx.workspace['name'])
        click.echo(msg)


@members.command(name='ls', short_help="List members in the current Workspace")
@click.pass_context
@coro
async def list_members_in_workspace(ctx: Context):
    """List members in the current Workspace"""

    cmd_ctx = await get_command_context(ctx)
    users = tuple([u] for u in get_workspace_users(cmd_ctx))

    print(humanfriendly.tables.format_smart_table(users, column_names=['email']))


@members.command(name='rm', short_help="Removes members from the current Workspace")
@click.argument('members_emails')
@click.option('--user_token', is_flag=False, default=None, help="When passed, we won't prompt asking for it")
@click.pass_context
@coro
async def remove_members_from_workspace(ctx: Context, members_emails: str, user_token: str):
    """Removes members from the current Workspace"""

    cmd_ctx = await get_command_context(ctx)

    requested_users = members_emails.split(',')
    workspace_users = get_workspace_users(cmd_ctx)
    users_to_remove = [u for u in requested_users if u in workspace_users]
    non_valid_users = [u for u in requested_users if u not in workspace_users]

    if len(users_to_remove) == 0:
        msg = FeedbackManager.info_user_not_exists(user=requested_users[0], workspace_name=cmd_ctx.workspace['name']) if len(requested_users) == 1 else FeedbackManager.info_users_not_exists(workspace_name=cmd_ctx.workspace['name'])
        click.echo(msg)
    else:
        if not user_token:
            user_token = ask_for_user_token(f"remove users from {cmd_ctx.workspace['name']}", cmd_ctx.ui_host)

        if len(non_valid_users) > 0:
            click.echo(FeedbackManager.warning_user_doesnt_exist(user=non_valid_users[0], workspace=cmd_ctx.workspace['name']) if len(non_valid_users) == 1 else FeedbackManager.warning_users_dont_exist(users=', '.join(non_valid_users), workspace=cmd_ctx.workspace['name']))

        user_client: TinyB = deepcopy(cmd_ctx.client)
        user_client.token = user_token
        await user_client.remove_users_from_workspace(cmd_ctx.workspace, users_to_remove)
        msg = FeedbackManager.success_workspace_user_removed(user=users_to_remove[0], workspace_name=cmd_ctx.workspace['name']) if len(users_to_remove) == 1 else FeedbackManager.success_workspace_users_removed(workspace_name=cmd_ctx.workspace['name'])
        click.echo(msg)


@members.command(name='set-role', short_help="Sets the role for existing workspace members")
@click.argument('role', required=True, type=click.Choice(['guest', 'admin']))
@click.argument('members_emails', required=True, type=str)
@click.option('--user_token', is_flag=False, default=None, help="When passed, we won't prompt asking for it")
@click.pass_context
@coro
async def set_workspace_member_role(ctx: Context, role: str, members_emails: str, user_token: str):
    """Sets the role for existing workspace members"""

    cmd_ctx = await get_command_context(ctx)

    requested_users = members_emails.split(',')
    workspace_users = get_workspace_users(cmd_ctx)
    users_to_change = [u for u in requested_users if u in workspace_users]
    non_valid_users = [u for u in requested_users if u not in workspace_users]

    if len(users_to_change) == 0:
        msg = FeedbackManager.info_user_not_exists(user=requested_users[0], workspace_name=cmd_ctx.workspace['name']) if len(requested_users) == 1 else FeedbackManager.info_users_not_exists(workspace_name=cmd_ctx.workspace['name'])
        click.echo(msg)
    else:
        if not user_token:
            user_token = ask_for_user_token(f"change user roles in {cmd_ctx.workspace['name']}", cmd_ctx.ui_host)

        if len(non_valid_users) > 0:
            click.echo(FeedbackManager.warning_user_doesnt_exist(user=non_valid_users[0], workspace=cmd_ctx.workspace['name']) if len(non_valid_users) == 1 else FeedbackManager.warning_users_dont_exist(users=', '.join(non_valid_users), workspace=cmd_ctx.workspace['name']))

        user_client: TinyB = deepcopy(cmd_ctx.client)
        user_client.token = user_token
        await user_client.set_role_for_users_in_workspace(cmd_ctx.workspace, users_to_change, role=role)
        msg = FeedbackManager.success_workspace_user_changed_role(user=users_to_change[0], role=role, workspace_name=cmd_ctx.workspace['name']) if len(users_to_change) == 1 else FeedbackManager.success_workspace_users_changed_role(role=role, workspace_name=cmd_ctx.workspace['name'])
        click.echo(msg)
