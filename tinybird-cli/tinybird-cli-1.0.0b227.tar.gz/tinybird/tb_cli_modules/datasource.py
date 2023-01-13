
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import asyncio
import json
import logging
import re
from typing import Any, Dict, List, Optional

import click
from click import Context
import humanfriendly

from tinybird.client import (
    CanNotBeDeletedException,
    DoesNotExistException,
    TinyB)
from tinybird.connectors import Connector
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import (
    _analyze, _generate_datafile,
    autocomplete_topics, coro,
    get_format_from_filename_or_url,
    get_name_tag_version, load_connector_config,
    push_data, get_config_and_hosts,
    validate_connection_id, validate_datasource_name,
    validate_kafka_auto_offset_reset, validate_kafka_group,
    validate_kafka_topic)


@cli.group()
@click.pass_context
def datasource(ctx):
    '''Data sources commands'''


@datasource.command(name="ls")
@click.option('--prefix', default=None, help="Show only resources with this prefix")
@click.option('--match', default=None, help='Retrieve any resources matching the pattern. eg --match _test')
@click.option('--format', 'format_', type=click.Choice(['json'], case_sensitive=False), default=None, help="Force a type of the output")
@click.pass_context
@coro
async def datasource_ls(ctx: Context, prefix: Optional[str], match: Optional[str], format_: str):
    """List data sources"""
    client: TinyB = ctx.ensure_object(dict)['client']
    ds = await client.datasources()
    columns = ['prefix', 'version', 'shared from', 'name', 'row_count', 'size', 'created at', 'updated at', 'connection']
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None

    for t in ds:
        stats = t.get('stats', None)
        if not stats:
            stats = t.get('statistics', {'bytes': ''})
            if not stats:
                stats = {'bytes': ''}

        tk = get_name_tag_version(t['name'])
        if (prefix and tk['tag'] != prefix) or (pattern and not pattern.search(tk['name'])):
            continue

        if "." in tk['name']:
            shared_from, name = tk['name'].split(".")
        else:
            shared_from, name = '', tk['name']

        table_human_readable.append((
            tk['tag'] or '',
            tk['version'] if tk['version'] is not None else '',
            shared_from,
            name,
            humanfriendly.format_number(stats.get('row_count')) if stats.get('row_count', None) else '-',
            humanfriendly.format_size(int(stats.get('bytes'))) if stats.get('bytes', None) else '-',
            t['created_at'][:-7],
            t['updated_at'][:-7],
            t.get('service', '')
        ))
        table_machine_readable.append({
            'prefix': tk['tag'] or '',
            'version': tk['version'] if tk['version'] is not None else '',
            'shared from': shared_from,
            'name': name,
            'row_count': stats.get('row_count', None) or '-',
            'size': stats.get('bytes', None) or '-',
            'created at': t['created_at'][:-7],
            'updated at': t['updated_at'][:-7],
            'connection': t.get('service', '')
        })

    if not format_:
        click.echo(FeedbackManager.info_datasources())
        click.echo(humanfriendly.tables.format_smart_table(table_human_readable, column_names=columns))
        click.echo('\n')
    elif format_ == 'json':
        click.echo(json.dumps({'datasources': table_machine_readable}, indent=2))
    else:
        click.echo(FeedbackManager.error_datasource_ls_type)


@datasource.command(name="append")
@click.argument('datasource_name')
@click.argument('url', nargs=-1)
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Import from one of the selected connectors", hidden=True)
@click.option('--sql', default=None, help='Query to extract data from one of the SQL connectors', hidden=True)
@click.option('--incremental', default=None, help='It does an incremental append, taking the max value for the date column name provided as a parameter. It only works when the `connector` parameter is passed.', hidden=True)
@click.option('--ignore-empty', help='Wheter or not to ignore empty results from the connector', is_flag=True, default=False, hidden=True)
@click.option('--concurrency', help='How many files to submit concurrently', default=1, hidden=True)
@click.pass_context
@coro
async def datasource_append(ctx, datasource_name, url, connector, sql, incremental, ignore_empty, concurrency):
    """
        Create a data source from a URL, local file or a connector

        - Load from URL `tb datasource append [datasource_name] https://url_to_csv`

        - Load from local file `tb datasource append [datasource_name] /path/to/local/file`

        - Load from connector `tb datasource append [datasource_name] --connector [connector_name] --sql [the_sql_to_extract_from]`
    """

    if not url and not connector:
        click.echo(FeedbackManager.error_missing_url_or_connector(datasource=datasource_name))
        return

    if incremental and not connector:
        click.echo(FeedbackManager.error_incremental_not_supported())
        return

    if incremental:
        date = None
        source_column = incremental.split(':')[0]
        dest_column = incremental.split(':')[-1]
        result = await ctx.obj['client'].query(f'SELECT max({dest_column}) as inc from {datasource_name} FORMAT JSON')
        try:
            date = result['data'][0]['inc']
        except Exception as e:
            raise click.ClickException(f'{str(e)}')
        if date:
            sql = f"{sql} WHERE {source_column} > '{date}'"
    await push_data(ctx, datasource_name, url, connector, sql, mode='append', ignore_empty=ignore_empty, concurrency=concurrency)


@datasource.command(name="replace")
@click.argument('datasource_name')
@click.argument('url', nargs=-1)
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Import from one of the selected connectors", hidden=True)
@click.option('--sql', default=None, help='Query to extract data from one of the SQL connectors', hidden=True)
@click.option('--sql-condition', default=None, help='SQL WHERE condition to replace data', hidden=True)
@click.option('--skip-incompatible-partition-key', is_flag=True, default=False, hidden=True)
@click.option('--ignore-empty', help='Wheter or not to ignore empty results from the connector', is_flag=True, default=False, hidden=True)
@click.pass_context
@coro
async def datasource_replace(ctx, datasource_name, url, connector, sql, sql_condition, skip_incompatible_partition_key, ignore_empty: bool):
    """
        Replaces the data in a data source from a URL, local file or a connector

        - Replace from URL `tb datasource replace [datasource_name] https://url_to_csv --sql-condition "country='ES'"`

        - Replace from local file `tb datasource replace [datasource_name] /path/to/local/file --sql-condition "country='ES'"`

        - Replace from connector `tb datasource replace [datasource_name] --connector [connector_name] --sql [the_sql_to_extract_from] --sql-condition "country='ES'"`
    """
    replace_options = set()
    if skip_incompatible_partition_key:
        replace_options.add("skip_incompatible_partition_key")
    await push_data(ctx, datasource_name, url, connector, sql, mode='replace', sql_condition=sql_condition, replace_options=replace_options, ignore_empty=ignore_empty)


@datasource.command(name='analyze')
@click.argument('url_or_file')
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Use from one of the selected connectors. In this case pass a table name as a parameter instead of a file name or an URL", hidden=True)
@click.pass_context
@coro
async def datasource_analyze(ctx, url_or_file, connector):
    '''Analyze a URL or a file before creating a new data source'''
    client = ctx.obj['client']

    _connector = None
    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.obj:
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.obj[connector]

    def _table(title, columns, data):
        row_format = "{:<25}" * len(columns)
        click.echo(FeedbackManager.info_datasource_title(title=title))
        click.echo(FeedbackManager.info_datasource_row(row=row_format.format(*columns)))
        for t in data:
            click.echo(FeedbackManager.info_datasource_row(row=row_format.format(*[str(element) for element in t])))

    analysis, _ = await _analyze(url_or_file, client, format=get_format_from_filename_or_url(url_or_file), connector=_connector)

    columns = ('name', 'type', 'nullable')
    if 'columns' in analysis['analysis']:
        _table('columns', columns, [(t['name'], t['recommended_type'], 'false' if t['present_pct'] == 1 else 'true') for t in analysis['analysis']['columns']])

    click.echo(FeedbackManager.info_datasource_title(title='SQL Schema'))
    click.echo(analysis['analysis']['schema'])

    values = []

    if 'dialect' in analysis:
        for x in analysis['dialect'].items():
            if x[1] == ' ':
                values.append((x[0], '" "'))
            elif type(x[1]) == str and ('\n' in x[1] or '\r' in x[1]):
                values.append((x[0], x[1].replace('\n', '\\n'). replace('\r', '\\r')))
            else:
                values.append(x)

        _table('dialect', ('name', 'value'), values)


@datasource.command(name="rm")
@click.argument('datasource_name')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def datasource_delete(ctx: Context, datasource_name: str, yes: bool):
    """Delete a data source"""
    client: TinyB = ctx.ensure_object(dict)['client']
    try:
        datasource = await client.get_datasource(datasource_name)
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))
    connector = datasource.get('service', False)

    if connector:
        click.echo(FeedbackManager.warning_datasource_is_connected(datasource=datasource_name, connector=connector))

    try:
        response = await client.datasource_delete(datasource_name, dry_run=True)
        dependencies_information = f'The Data Source is used in => Pipes="{response["dependent_pipes"]}", nodes="{response["dependent_pipes"]}"'
        dependencies_information = dependencies_information if response["dependent_pipes"] else 'The Data Source is not used in any Pipe'
        warning_message = f"\nDo you want to delete {datasource_name}? Once deleted, it can't be recovered."
    except CanNotBeDeletedException as e:
        if 'downstream' not in str(e):
            dependencies_information = str(e)
            warning_message = f"\nDo you want to unlink and delete {datasource_name}? This action can't be undone."
        else:
            raise click.ClickException(FeedbackManager.error_datasource_can_not_be_deleted(datasource=datasource_name, error=e))

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_datasource(warning_message=warning_message, dependencies_information=dependencies_information)):
        try:
            await client.datasource_delete(datasource_name, force=True)
        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except CanNotBeDeletedException as e:
            raise click.ClickException(FeedbackManager.error_datasource_can_not_be_deleted(datasource=datasource_name, error=e))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=e))

        click.echo(FeedbackManager.success_delete_datasource(datasource=datasource_name))


@datasource.command(name="truncate")
@click.argument('datasource_name', required=True)
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--cascade', is_flag=True, default=False, help="Truncate dependent DS attached in cascade to the given DS")
@click.pass_context
@coro
async def datasource_truncate(ctx, datasource_name, yes, cascade):
    """Truncate a data source"""

    client = ctx.obj['client']
    if yes or click.confirm(FeedbackManager.warning_confirm_truncate_datasource(datasource=datasource_name)):
        try:
            await client.datasource_truncate(datasource_name)
        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=e))

        click.echo(FeedbackManager.success_truncate_datasource(datasource=datasource_name))

        if (cascade):
            try:
                ds_cascade_dependencies = await client.datasource_dependencies(no_deps=False, match=None, pipe=None, datasource=datasource_name, check_for_partial_replace=True, recursive=False)
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_exception(error=e))

            cascade_dependent_ds = list(ds_cascade_dependencies.get('dependencies', {}).keys()) + list(ds_cascade_dependencies.get('incompatible_datasources', {}).keys())
            for cascade_ds in cascade_dependent_ds:
                if yes or click.confirm(FeedbackManager.warning_confirm_truncate_datasource(datasource=cascade_ds)):
                    try:
                        await client.datasource_truncate(cascade_ds)
                    except DoesNotExistException:
                        click.echo(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
                    except Exception as e:
                        click.echo(FeedbackManager.error_exception(error=e))
                    click.echo(FeedbackManager.success_truncate_datasource(datasource=cascade_ds))


@datasource.command(name="delete")
@click.argument('datasource_name')
@click.option('--sql-condition', default=None, help='SQL WHERE condition to remove rows', hidden=True, required=True)
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--wait', is_flag=True, default=False, help="Wait for delete job to finish, disabled by default")
@click.pass_context
@coro
async def datasource_delete_rows(ctx, datasource_name, sql_condition, yes, wait):
    """
    Delete rows from a datasource

    - Delete rows with SQL condition: `tb datasource delete [datasource_name] --sql-condition "country='ES'"`

    - Delete rows with SQL condition and wait for the job to finish: `tb datasource delete [datasource_name] --sql-condition "country='ES'" --wait`
    """
    client: TinyB = ctx.ensure_object(dict)['client']
    if yes or click.confirm(FeedbackManager.warning_confirm_delete_rows_datasource(datasource=datasource_name, delete_condition=sql_condition)):
        try:
            res = await client.datasource_delete_rows(datasource_name, sql_condition)
            job_id = res['job_id']
            job_url = res['job_url']
            click.echo(FeedbackManager.info_datasource_delete_rows_job_url(url=job_url))
            if wait:
                progress_symbols = ['-', '\\', '|', '/']
                progress_str = 'Waiting for the job to finish'
                print(f'\n{progress_str}', end="")

                def progress_line(n):
                    print(f'\r{progress_str} {progress_symbols[n % len(progress_symbols)]}', end="")
                i = 0
                while True:
                    try:
                        res = await client._req(f'v0/jobs/{job_id}')
                    except Exception:
                        click.echo(FeedbackManager.error_job_status(url=job_url))
                        break
                    if res['status'] == 'done':
                        print('\n')
                        click.echo(FeedbackManager.success_delete_rows_datasource(datasource=datasource_name, delete_condition=sql_condition))
                        break
                    elif res['status'] == 'error':
                        print('\n')
                        click.echo(FeedbackManager.error_exception(error=res['error']))
                        break
                    await asyncio.sleep(1)
                    i += 1
                    progress_line(i)

        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_exception(error=e))


@datasource.command(name="generate", short_help="Generates a data source file based on a sample CSV, NDJSON or Parquet file from local disk or url")
@click.argument('filenames', nargs=-1, default=None)
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.option('--connector', type=click.Choice(['bigquery', 'snowflake'], case_sensitive=True), help="Use from one of the selected connectors. In this case pass a table name as a parameter instead of a file name", hidden=True)
@click.pass_context
@coro
async def generate_datasource(ctx: Context, connector: str, filenames, force: bool):
    """Generate a data source file based on a sample CSV file from local disk or url"""
    client: TinyB = ctx.ensure_object(dict)['client']

    _connector: Optional[Connector] = None
    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.ensure_object(dict):
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.ensure_object(dict)[connector]

    for filename in filenames:
        await _generate_datafile(filename, client, force=force, format=get_format_from_filename_or_url(filename), connector=_connector)


@datasource.command(name="connect")
@click.argument('connection_id')
@click.argument('datasource_name')
@click.option('--topic', help="Kafka topic", autocompletion=autocomplete_topics)
@click.option('--group', help="Kafka group ID")
@click.option('--auto-offset-reset', default=None, help='Kafka auto.offset.reset config. Valid values are: ["latest", "earliest"]')
@click.pass_context
@coro
# Example usage: tb datasource connect 776824da-ac64-4de4-b8b8-b909f69d5ed5 new_ds --topic a --group b --auto-offset-reset latest
async def datasource_connect(ctx, connection_id, datasource_name, topic, group, auto_offset_reset):
    """Create a new datasource from an existing connection"""
    validate_connection_id(connection_id)
    validate_datasource_name(datasource_name)
    topic and validate_kafka_topic(topic)
    group and validate_kafka_group(group)
    auto_offset_reset and validate_kafka_auto_offset_reset(auto_offset_reset)
    client = ctx.obj['client']
    # TODO check connection id is valid
    if not topic:
        try:
            topics = await client.kafka_list_topics(connection_id)
            click.echo("We've discovered the following topics:")
            for t in topics:
                click.echo(f"    {t}")
        except Exception as e:
            logging.debug(f"Error listing topics: {e}")
        topic = click.prompt("Kafka topic")
        validate_kafka_topic(topic)
    if not group:
        group = click.prompt("Kafka group")
        validate_kafka_group(group)
    if not auto_offset_reset:
        # TODO commits? with preview
        if False:
            auto_offset_reset = "earliest"
            click.echo("Prior commits have been detected on this topic and group ID.")
            click.echo("By continuing we'll read from and commit to this group.")
        else:
            click.echo("Kafka doesn't seem to have prior commits on this topic and group ID")
            click.echo("Setting auto.offset.reset is required. Valid values:")
            click.echo("  latest          Skip earlier messages and ingest only new messages")
            click.echo("  earliest        Start ingestion from the first message")
            auto_offset_reset = click.prompt("Kafka auto.offset.reset config")
            validate_kafka_auto_offset_reset(auto_offset_reset)
        if not click.confirm("Proceed?"):
            return
    resp = await client.datasource_kafka_connect(connection_id, datasource_name, topic, group, auto_offset_reset)
    datasource_id = resp['datasource']['id']
    click.echo(FeedbackManager.success_datasource_kafka_connected(id=datasource_id))


@datasource.command(name="share")
@click.argument('datasource_name')
@click.argument('workspace_name_or_id')
@click.option('--user_token', default=None, help="When passed, we won't prompt asking for it")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def datasource_share(ctx: Context, datasource_name: str, workspace_name_or_id: str, user_token: str, yes: bool):
    """Share a datasource"""

    client: TinyB = ctx.ensure_object(dict)['client']

    config, host, ui_host = await get_config_and_hosts(ctx)

    datasource: Dict[str, Any] = await client.get_datasource(datasource_name)
    workspaces: List[Dict[str, Any]] = (await client.user_workspaces()).get('workspaces', [])
    destination_workspace = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)
    current_workspace = next((workspace for workspace in workspaces if workspace['id'] == config['id']), None)  # type: ignore

    if not destination_workspace:
        click.echo(FeedbackManager.error_workspace(workspace=workspace_name_or_id))
        return

    if not current_workspace:
        click.echo(FeedbackManager.error_not_authenticated())
        return

    if not user_token:
        user_token = click.prompt(
            f"\nIn order to create a new workspace we need your user token. Copy it from {ui_host}/tokens and paste it here",
            hide_input=True)

    client.token = user_token

    if yes or click.confirm(
        FeedbackManager.warning_datasource_share(datasource=datasource_name, source_workspace=current_workspace.get('name'), destination_workspace=destination_workspace['name'])
    ):
        try:
            await client.datasource_share(
                datasource_id=datasource.get('id', ''),
                current_workspace_id=current_workspace.get('id', ''),
                destination_workspace_id=destination_workspace.get('id', ''))
            click.echo(FeedbackManager.success_datasource_shared(datasource=datasource_name, workspace=destination_workspace['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return
