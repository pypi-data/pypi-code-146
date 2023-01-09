
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import asyncio
import json
from pathlib import Path
import re
from typing import List
import click
from click import Context
import tinybird.context as context

import humanfriendly
from tinybird.client import DoesNotExistException, JobException, TinyB
from tinybird.config import DEFAULT_API_HOST, FeatureFlags
from tinybird.datafile import folder_push
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, create_tb_client, get_name_tag_version, print_data_table
from tinybird.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def pipe(ctx):
    '''Pipes commands'''


@pipe.command(name="generate", short_help="Generates a pipe file based on a sql query")
@click.argument('name')
@click.argument('query')
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.pass_context
def generate_pipe(ctx, name, query, force):
    pipefile = f"""
NODE endpoint
DESCRIPTION >
    Generated from the command line
SQL >
    {query}

    """
    base = Path('endpoints')
    if not base.exists():
        base = Path()
    f = base / (f"{name}.pipe")
    if not f.exists() or force:
        with open(f'{f}', 'w') as file:
            file.write(pipefile)
        click.echo(FeedbackManager.success_generated_pipe(file=f))
    else:
        click.echo(FeedbackManager.error_exception(error=f'File {f} already exists, use --force to override'))


@pipe.command(name="stats")
@click.argument('pipe', nargs=-1)
@click.pass_context
@coro
async def pipe_stats(ctx, pipe):
    """Print pipe stats"""
    client = ctx.obj['client']
    pipes = await client.pipes()
    pipes_to_get_stats = []
    pipes_ids = {}
    for pipe in pipes:
        name_tag = get_name_tag_version(pipe['name'])
        if name_tag['name'] in pipe['name']:
            pipes_to_get_stats.append(f"'{pipe['id']}'")
            pipes_ids[pipe['id']] = name_tag

    if not pipes_to_get_stats:
        click.echo(FeedbackManager.info_no_pipes_stats())
        return

    sql = f"""
        SELECT
            pipe_id id,
            sumIf(view_count, date > now() - interval 7 day) requests,
            sumIf(view_count, date > now() - interval 14 day and date < now() - interval 7 day) prev_requests,
            sumIf(error_count, date > now() - interval 7 day) errors,
            sumIf(error_count, date > now() - interval 14 day and date < now() - interval 7 day) prev_errors,
            avgMergeIf(avg_duration_state, date > now() - interval 7 day) latency,
            avgMergeIf(avg_duration_state, date > now() - interval 14 day and date < now() - interval 7 day) prev_latency
        FROM tinybird.pipe_stats
        where pipe_id in ({','.join(pipes_to_get_stats)})
        GROUP BY pipe_id
        ORDER BY requests DESC
        FORMAT JSON
    """

    columns = ['prefix', 'version', 'name', 'request count', 'error count', 'avg latency']
    res = await client.query(sql)
    table = []

    if res and 'error' in res:
        click.echo(FeedbackManager.error_exception(error=str(res['error'])))
        return

    if res and 'data' in res:
        for x in res['data']:
            tk = pipes_ids[x['id']]
            table.append((
                tk['tag'] or '',
                tk['version'] if tk['version'] is not None else '',
                tk['name'],
                x['requests'],
                x['errors'],
                x['latency']
            ))

        table.sort(key=lambda x: (x[2], x[1]))
        click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@pipe.command(name="ls")
@click.option('--prefix', default=None, help="Show only resources with this prefix")
@click.option('--match', default=None, help='Retrieve any resourcing matching the pattern. eg --match _test')
@click.option('--format', 'format_', type=click.Choice(['json'], case_sensitive=False), default=None, help="Force a type of the output")
@click.pass_context
@coro
async def pipe_ls(ctx: Context, prefix: str, match: str, format_):
    """List pipes"""

    client: TinyB = ctx.ensure_object(dict)['client']
    pipes = await client.pipes(dependencies=False, node_attrs='name', attrs='name,updated_at')
    pipes = sorted(pipes, key=lambda p: p['updated_at'])

    columns = ['prefix', 'version', 'name', 'published date', 'nodes']
    table_human_readable = []
    table_machine_readable = []
    pattern = re.compile(match) if match else None
    for t in pipes:
        tk = get_name_tag_version(t['name'])
        if (prefix and tk['tag'] != prefix) or (pattern and not pattern.search(tk['name'])):
            continue
        table_human_readable.append((
            tk['tag'] or '',
            tk['version'] if tk['version'] is not None else '',
            tk['name'],
            t['updated_at'][:-7],
            len(t['nodes'])
        ))
        table_machine_readable.append({
            'prefix': tk['tag'] or '',
            'version': tk['version'] if tk['version'] is not None else '',
            'name': tk['name'],
            'published date': t['updated_at'][:-7],
            'nodes': len(t['nodes'])
        })

    if not format_:
        click.echo(FeedbackManager.info_pipes())
        click.echo(humanfriendly.tables.format_smart_table(table_human_readable, column_names=columns))
        click.echo('\n')
    elif format_ == 'json':
        click.echo(json.dumps({'pipes': table_machine_readable}, indent=2))
    else:
        click.echo(FeedbackManager.error_pipe_ls_type)


@pipe.command(name="populate")
@click.argument('pipe_name')
@click.option('--node', type=str, help="Name of the materialized node.")
@click.option('--sql-condition', type=str, default=None, help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.")
@click.option('--truncate', is_flag=True, default=False, help="Truncates the materialized Data Source before populating it.")
@click.option('--unlink-on-populate-error/--preserve-on-populate-error', is_flag=True, default=False, help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View, use --preserve-on-populate-error to keep the Materialized View even when the populate job fails.", hidden=True)
@click.option('--wait', is_flag=True, default=False, help="Waits for populate jobs to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def pipe_populate(ctx, pipe_name, node, sql_condition, truncate, unlink_on_populate_error, wait):
    cl = create_tb_client(ctx)
    response = await cl.populate_node(pipe_name, node, populate_condition=sql_condition, truncate=truncate, unlink_on_populate_error=unlink_on_populate_error)
    if 'job' not in response:
        raise click.ClickException(response)

    job_id = response['job']['id']
    job_url = response['job']['job_url']
    if sql_condition:
        click.echo(FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=sql_condition))
    else:
        click.echo(FeedbackManager.info_populate_job_url(url=job_url))
    if wait:
        with click.progressbar(label="Populating ", length=100, show_eta=False, show_percent=True, fill_char=click.style("█", fg="green")) as progress_bar:
            def progressbar_cb(res):
                if 'progress_percentage' in res:
                    progress_bar.update(int(round(res['progress_percentage'])) - progress_bar.pos)
                elif res['status'] != 'working':
                    progress_bar.update(progress_bar.length)
            try:
                result = await asyncio.wait_for(cl.wait_for_job(job_id, status_callback=progressbar_cb), None)
                if result['status'] != 'done':
                    click.echo(FeedbackManager.error_while_populating(error=result['error']))
                else:
                    progress_bar.update(progress_bar.length)
            except asyncio.TimeoutError:
                await cl.job_cancel(job_id)
                raise click.ClickException(FeedbackManager.error_while_populating(error="Reach timeout, job cancelled"))
            except JobException as e:
                raise click.ClickException(FeedbackManager.error_while_populating(error=str(e)))
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_getting_job_info(error=str(e), url=job_url))


@pipe.command(name="new")
@click.argument('pipe_name')
@click.argument('sql')
@click.pass_context
@coro
async def pipe_create(ctx, pipe_name, sql):
    """Create a new pipe"""
    client = ctx.obj['client']
    host = ctx.obj['config'].get('host', DEFAULT_API_HOST)
    res = await client.pipe_create(pipe_name, sql)
    click.echo(FeedbackManager.success_created_pipe(pipe=pipe_name, node_id=res['nodes'][0]['id'], host=host))


@pipe.command(name="append")
@click.argument('pipe_name_or_uid')
@click.argument('sql')
@click.pass_context
@coro
async def pipe_append_node(ctx, pipe_name_or_uid, sql):
    """Append a node to a pipe"""
    client = ctx.obj['client']
    try:
        res = await client.pipe_append_node(pipe_name_or_uid, sql)
        click.echo(FeedbackManager.success_node_changed(pipe_name_or_uid=pipe_name_or_uid,
                                                        node_name=res['name'],
                                                        node_id=res['id']))
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_uid))


async def common_pipe_publish_node(ctx, pipe_name_or_id, node_uid=None):
    """Change the published node of a pipe"""
    client = ctx.obj['client']
    host = ctx.obj['config'].get('host', DEFAULT_API_HOST)

    try:
        pipe = await client.pipe(pipe_name_or_id)
        if not node_uid:
            node = pipe['nodes'][-1]['name']
            click.echo(FeedbackManager.info_using_node(node=node))
        else:
            node = node_uid

        await client.pipe_set_endpoint(pipe_name_or_id, node)
        click.echo(FeedbackManager.success_node_published(pipe=pipe_name_or_id, host=host))
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))


@pipe.command(name="publish")
@click.argument('pipe_name_or_id')
@click.argument('node_uid', default=None, required=False)
@click.pass_context
@coro
async def pipe_publish_node(ctx, pipe_name_or_id, node_uid=None):
    """Change the published node of a pipe"""
    await common_pipe_publish_node(ctx, pipe_name_or_id, node_uid)


@pipe.command(name="unpublish")
@click.argument('pipe_name_or_id')
@click.argument('node_uid', default=None, required=False)
@click.pass_context
@coro
async def pipe_unpublish_node(ctx, pipe_name_or_id, node_uid=None):
    """Unpublish the endpoint of a pipe"""
    client = ctx.obj['client']
    host = ctx.obj['config'].get('host', DEFAULT_API_HOST)

    try:
        pipe = await client.pipe(pipe_name_or_id)

        if not pipe['endpoint']:
            raise click.ClickException(FeedbackManager.error_remove_no_endpoint())

        if not node_uid:
            node = pipe['endpoint']
            click.echo(FeedbackManager.info_using_node(node=node))
        else:
            node = node_uid

        await client.pipe_remove_endpoint(pipe_name_or_id, node)
        click.echo(FeedbackManager.success_node_unpublished(pipe=pipe_name_or_id, host=host))
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))


@pipe.command(name="set_endpoint")
@click.argument('pipe_name_or_id')
@click.argument('node_uid', default=None, required=False)
@click.pass_context
@coro
async def pipe_published_node(ctx, pipe_name_or_id, node_uid=None):
    """Same as 'publish', change the published node of a pipe"""
    await common_pipe_publish_node(ctx, pipe_name_or_id, node_uid)


@pipe.command(name="rm")
@click.argument('pipe_name_or_id')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def pipe_delete(ctx, pipe_name_or_id, yes):
    """Delete a pipe"""

    client = ctx.obj['client']

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_pipe(pipe=pipe_name_or_id)):
        try:
            await client.pipe_delete(pipe_name_or_id)
        except DoesNotExistException:
            raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name_or_id))

        click.echo(FeedbackManager.success_delete_pipe(pipe=pipe_name_or_id))


@pipe.command(name="token_read")
@click.argument('pipe_name')
@click.pass_context
@coro
async def pipe_token_read(ctx, pipe_name):
    """Retrieve a token to read a pipe"""
    client = ctx.obj['client']

    try:
        await client.pipe_file(pipe_name)
    except DoesNotExistException:
        raise click.ClickException(FeedbackManager.error_pipe_does_not_exist(pipe=pipe_name))

    tokens = await client.tokens()
    token = None

    for t in tokens:
        for scope in t['scopes']:
            if scope['type'] == 'PIPES:READ' and scope['resource'] == pipe_name:
                token = t['token']
    if token:
        click.echo(token)
    else:
        click.echo(FeedbackManager.warning_token_pipe(pipe=pipe_name))


@pipe.command(name="data", context_settings=dict(
    allow_extra_args=True,
    ignore_unknown_options=True,
))
@click.argument('pipe')
@click.option('--query', default=None, help="Run SQL over pipe results")
@click.option('--format', 'format_', type=click.Choice(['json', 'csv'], case_sensitive=False), help="Return format (CSV, JSON)")
@click.pass_context
@coro
async def print_pipe(ctx: Context, pipe: str, query: str, format_: str):
    """Print data returned by a pipe

    Syntax: tb pipe data <pipe_name> --param_name value --param2_name value2 ...
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
    req_format = 'json' if not format_ else format_.lower()
    try:
        res = await client.pipe_data(pipe, format=req_format, sql=query, params=params)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return

    if not format_:
        stats = res['statistics']
        seconds = stats['elapsed']
        rows_read = humanfriendly.format_number(stats['rows_read'])
        bytes_read = humanfriendly.format_size(stats['bytes_read'])

        click.echo(FeedbackManager.success_print_pipe(pipe=pipe))
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))
        print_data_table(res)
        click.echo('\n')
    elif (req_format == 'json'):
        click.echo(json.dumps(res))
    else:
        click.echo(res)


@pipe.command(name="regression-test", short_help="Run regression tests using last requests")
@click.option('--prefix', default='', help="Use prefix for all the resources")
@click.option('--debug', is_flag=True, default=False, help="Prints internal representation, can be combined with any command to get more information.")
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times")
@click.argument('filenames', type=click.Path(exists=True), nargs=-1, default=None)
@click.option('--workspace_map', nargs=2, type=str, multiple=True)
@click.option('--workspace', nargs=2, type=str, multiple=True, help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder")
@click.option('--no-versions', is_flag=True, default=False, help="when set, resource dependency versions are not used, it pushes the dependencies as-is")
@click.option('-l', '--limit', type=click.IntRange(0, 100), default=0, required=False, help="Number of requests to validate")
@click.option('--sample-by-params', type=click.IntRange(1, 100), default=1, required=False, help="When set, we will aggregate the pipe_stats_rt requests by extractURLParameterNames(assumeNotNull(url)) and for each combination we will take a sample of N requests")
@click.option('-m', '--match', multiple=True, required=False, help="Filter the checker requests by specific parameter. You can pass multiple parameters -m foo -m bar")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.option('--validate-processed-bytes', is_flag=True, default=False, help="When set, the checker will validate that the new version doesn't process more than 25% than the current version")
@click.pass_context
@coro
async def regression_test(
        ctx: click.Context,
        prefix: str,
        filenames: Path,
        debug: bool,
        only_response_times: bool,
        workspace_map,
        workspace: str,
        no_versions: bool,
        limit: int,
        sample_by_params: int,
        match: List[str],
        failfast: bool,
        ignore_order: bool,
        validate_processed_bytes: bool):
    """
    Run regression tests on Tinybird
    """

    ignore_sql_errors = FeatureFlags.ignore_sql_errors()

    context.disable_template_security_validation.set(True)
    await folder_push(
        create_tb_client(ctx),
        prefix,
        filenames,
        dry_run=False,
        check=True,
        push_deps=False,
        debug=debug,
        force=False,
        populate=False,
        upload_fixtures=False,
        wait=False,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=False,
        only_response_times=only_response_times,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        no_versions=no_versions,
        timeout=False,
        run_tests=True,
        tests_to_run=limit,
        tests_sample_by_params=sample_by_params,
        tests_filter_by=match,
        tests_failfast=failfast,
        tests_ignore_order=ignore_order,
        tests_validate_processed_bytes=validate_processed_bytes
    )
    return
