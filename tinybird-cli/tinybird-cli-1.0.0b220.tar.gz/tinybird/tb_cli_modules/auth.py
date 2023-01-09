
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
from os import getcwd
from pathlib import Path
from urllib.parse import urlparse
import click
from click import Context

import humanfriendly
from tinybird.client import TinyB
from tinybird.config import DEFAULT_API_HOST, DEFAULT_LOCALHOST, VERSION, FeatureFlags, write_config
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import _compare_hosts, _get_config, authenticate, configure_connector, coro, get_host_from_region, get_regions
from tinybird.feedback_manager import FeedbackManager


@cli.group(invoke_without_command=True)
@click.option('--token', envvar='TB_TOKEN', help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file")
@click.option('--host', envvar='TB_HOST', help="Set custom host if it's different than https://api.tinybird.co. Check https://docs.tinybird.co/cli.html for the available list of regions")
@click.option('--region', envvar='TB_REGION', help="Set region. Run 'tb auth ls' to show available regions")
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Set credentials for one of the supported connectors")
@click.option('-i', '--interactive', is_flag=True, default=False, help="Show available regions and select where to authenticate to")
@click.pass_context
@coro
async def auth(ctx: Context, token: str, host: str, region: str, connector: str, interactive: bool):
    """Configure auth"""
    if connector:
        await configure_connector(connector)
        return

    if host:
        # Let's keep just the basic url
        url_info = urlparse(host)
        host = f"{url_info.scheme}://{url_info.netloc}"

    # only run when doing 'tb auth'
    if not ctx.invoked_subcommand:
        regions = None

        if region:
            regions, host = await get_host_from_region(region, host)

        config = None

        try:
            config = await authenticate(ctx, host=host, token=token, regions=regions, interactive=interactive, try_all_regions=True)
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=str(e)))

        if not config:
            raise click.ClickException(FeedbackManager.error_auth())

    elif ctx.invoked_subcommand == 'ls':
        pass

    else:
        config = None
        try:
            config_file = Path(getcwd()) / ".tinyb"
            with open(config_file) as file:
                config = json.loads(file.read())
            ctx.ensure_object(dict)['client'] = TinyB(config['token'], config.get('host', DEFAULT_API_HOST), version=VERSION)
            ctx.ensure_object(dict)['config'] = config
        except Exception:
            host = ctx.ensure_object(dict)['config'].get('host', DEFAULT_API_HOST)
            token = ctx.ensure_object(dict)['config']['token']

            if not token:
                raise click.ClickException(FeedbackManager.error_notoken())

            config = await _get_config(host, token)
            ctx.ensure_object(dict)['config'] = config

        if not config or not config['token']:
            raise click.ClickException(FeedbackManager.error_wrong_config_file(config_file=config_file))


@auth.command(name="info")
@click.pass_context
@coro
async def auth_info(ctx):
    """Get information about the authentication that is currently being used"""
    config = ctx.obj['config']

    if config and 'id' in config:
        columns = ['user', 'host', 'workspace_name', 'workspace_id']
        table = []
        user_email = config['user_email'] if 'user_email' in config else None

        if user_email:
            table.append([user_email, config['host'], config['name'], config['id']])
        else:
            table.append(['No user', config['host'], config['name'], config['id']])
        click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@auth.command(name="ls")
@click.pass_context
@coro
async def auth_ls(ctx: Context):
    """List available regions to authenticate"""
    config = ctx.ensure_object(dict)['config']

    config_file = Path(getcwd()) / ".tinyb"
    is_localhost = FeatureFlags.is_localhost()
    check_host = config.get('host', DEFAULT_API_HOST)
    check_host = check_host if not is_localhost else DEFAULT_LOCALHOST
    client = TinyB(token='', host=check_host, version=VERSION)

    columns = ['idx', 'region', 'host', 'api', 'current']
    table = []
    click.echo(FeedbackManager.info_available_regions())

    regions = await get_regions(client, config_file)

    if regions:
        for index, region in enumerate(regions):
            table.append([index + 1, region['name'].lower(), region['host'], region['api_host'], _compare_hosts(region, config)])
    else:
        table.append([1, 'default', config['host'], True])

    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@auth.command(name="use")
@click.argument('region_name_or_host_or_id')
@click.pass_context
@coro
async def auth_use(ctx, region_name_or_host_or_id):
    """Switch to a different region.
    You can pass the region name, the region host url, or the region index
    after listing available regions with 'tb auth ls'

    \b
    Example usage:
    \b
    $ tb auth use us-east
    $ tb auth use 1
    $ tb auth use https://ui.us-east.tinybird.co
    """

    config = ctx.obj['config']
    token = None
    host = config.get('host', None)

    regions, host = await get_host_from_region(region_name_or_host_or_id, host)

    if 'tokens' in config and host in config['tokens']:
        token = config['tokens'][host]

    config = await authenticate(ctx, host, token, regions)

    await write_config(config)
    click.echo(FeedbackManager.success_now_using_config(name=config['name'], id=config['id']))
