
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import click
from click import Context


from tinybird.client import TinyB
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, get_config_and_hosts, \
    create_workspace_branch, switch_workspace, print_current_workspace, _get_config
from tinybird.feedback_manager import FeedbackManager
import humanfriendly


@cli.group(hidden=True)
@click.pass_context
def branch(ctx):
    '''Branch commands'''


@branch.command(name="ls", hidden=True)
@click.pass_context
@coro
async def branch_ls(ctx):
    """List all the branches from the workspace token
    """
    client = ctx.obj['client']
    config = ctx.obj['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.branches()

    columns = ['name', 'id']
    table = []

    for branch in response['branches']:
        table.append([branch['name'], branch['id']])

    await print_current_workspace(ctx)

    click.echo(FeedbackManager.info_branches())
    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@branch.command(name='use', hidden=True)
@click.argument('branch_name_or_id')
@click.pass_context
@coro
async def branch_use(ctx: Context, branch_name_or_id: str):
    """Switch to another branch. Use 'tb branch ls' to list the branches you have access to.
    """
    await switch_workspace(ctx, branch_name_or_id, only_branches=True)


@branch.command(name='current', hidden=True)
@click.pass_context
@coro
async def branch_current(ctx: Context):
    """Show the branch you're currently authenticated to
    """
    await print_current_workspace(ctx)


@branch.command(name='create', short_help="Create a new Branch from the Workspace you are authenticated", hidden=True)
@click.argument('branch_name', required=False)
@click.option('--last-partition', is_flag=True, default=False, help="When enabled, last modified partition is attached from the origin Workspace to the Branch")
@click.pass_context
@coro
async def create_branch(ctx: Context, branch_name: str, last_partition: bool):
    await create_workspace_branch(ctx, branch_name, last_partition)


@branch.command(name='rm', short_help="Removes a Branch for your Tinybird user and it can't be recovered.", hidden=True)
@click.argument('branch_name_or_id')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def delete_branch(ctx: Context, branch_name_or_id: str, yes: bool):
    """Remove a branch where you are admin"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_branch()):
        workspaces = (await client.user_workspace_branches()).get('workspaces', [])
        workspace_to_delete = next((workspace for workspace in workspaces if workspace['name'] == branch_name_or_id or workspace['id'] == branch_name_or_id), None)

        if not workspace_to_delete:
            raise click.ClickException(FeedbackManager.error_branch(branch=branch_name_or_id))

        try:
            await client.delete_branch(workspace_to_delete['id'])
            click.echo(FeedbackManager.success_branch_deleted(branch_name=workspace_to_delete['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return


@branch.command(name='data', short_help="Perform a data branch operation, see flags for details", hidden=True)
@click.argument('origin_workspace_id', required=False)
@click.option('--last-partition', is_flag=True, default=True, help="When enabled, last modified partition is attached from the origin Workspace to the Branch")
@click.pass_context
@coro
async def data_branch(ctx, origin_workspace_id, last_partition):
    client = ctx.obj['client']
    config = ctx.ensure_object(dict)['config']

    try:
        await client.branch_workspace_data(config['id'], origin_workspace_id, last_partition)
        click.echo(FeedbackManager.success_workspace_data_branch())
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return
