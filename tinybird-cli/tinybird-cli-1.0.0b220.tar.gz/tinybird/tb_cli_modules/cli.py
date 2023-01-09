
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import asyncio
import os
from os import environ, getcwd

import json
import logging
import pprint
import re
import shutil
import click
from click import Context

from pathlib import Path
from typing import Any, Optional

import humanfriendly
from toposort import toposort

from tinybird.client import CanNotBeDeletedException, DoesNotExistException, JobException, TinyB
from tinybird.connectors import create_connector

from tinybird.feedback_manager import FeedbackManager
from tinybird.datafile import AlreadyExistsException, ParseException, build_graph, folder_push, format_datasource, format_pipe, get_name_tag_version, get_project_filenames, parse_datasource, parse_pipe
import tinybird.context as context
from tinybird.config import FeatureFlags, get_config, VERSION, CURRENT_VERSION, SUPPORTED_CONNECTORS

from tinybird.tb_cli_modules.common import CatchAuthExceptions, coro, create_tb_client, folder_init, folder_pull, load_connector_config


__old_click_echo = click.echo


@click.group(cls=CatchAuthExceptions, context_settings={"help_option_names": ["-h", "--help"]})  # noqa: C901
@click.option('--debug/--no-debug', default=False, help="Prints internal representation, can be combined with any command to get more information.")
@click.option('--token', envvar='TB_TOKEN', help="Use auth token, defaults to TB_TOKEN envvar, then to the .tinyb file")
@click.option('--host', envvar='TB_HOST', help="Use custom host, defaults to TB_HOST envvar, then to https://api.tinybird.co")
@click.option('--gcp-project-id', help="The Google Cloud project ID", hidden=True)
@click.option('--gcs-bucket', help="The Google Cloud Storage bucket to write temp files when using the connectors", hidden=True)
@click.option('--google-application-credentials', envvar='GOOGLE_APPLICATION_CREDENTIALS', help="Set GOOGLE_APPLICATION_CREDENTIALS", hidden=True)
@click.option('--sf-account', help="The Snowflake Account (e.g. your-domain.west-europe.azure)", hidden=True)
@click.option('--sf-warehouse', help="The Snowflake warehouse name", hidden=True)
@click.option('--sf-database', help="The Snowflake database name", hidden=True)
@click.option('--sf-schema', help="The Snowflake schema name", hidden=True)
@click.option('--sf-role', help="The Snowflake role name", hidden=True)
@click.option('--sf-user', help="The Snowflake user name", hidden=True)
@click.option('--sf-password', help="The Snowflake password", hidden=True)
@click.option('--sf-storage-integration', help="The Snowflake GCS storage integration name (leave empty to auto-generate one)", hidden=True)
@click.option('--sf-stage', help="The Snowflake GCS stage name (leave empty to auto-generate one)", hidden=True)
@click.option('--with-headers', help="Flag to enable connector to export with headers", is_flag=True, default=False, hidden=True)
@click.option('--version-warning/--no-version-warning', envvar='TB_VERSION_WARNING', default=True, help="Don't print version warning message if there's a new available version. You can use TB_VERSION_WARNING envar")
@click.option('--hide-tokens', is_flag=True, default=False, help="Disable the output of tokens")
@click.version_option(version=VERSION)
@click.pass_context
@coro
async def cli(ctx: Context, debug: bool, token: str, host: str, gcp_project_id, gcs_bucket, google_application_credentials, sf_account, sf_warehouse, sf_database, sf_schema, sf_role, sf_user, sf_password, sf_storage_integration, sf_stage, with_headers: bool, version_warning: bool, hide_tokens: bool):  # noqa: C901

    # We need to unpatch for our tests not to break
    if hide_tokens:
        __patch_click_output()
    else:
        __unpatch_click_output()

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called)
    # by means other than the `if` block below
    if not environ.get("PYTEST", None) and version_warning and not token:
        from tinybird.check_pypi import CheckPypi
        latest_version = await CheckPypi().get_latest_version()

        if 'x.y.z' in CURRENT_VERSION:
            click.echo(FeedbackManager.warning_development_cli())

        if 'x.y.z' not in CURRENT_VERSION and latest_version != CURRENT_VERSION:
            click.echo(FeedbackManager.warning_update_version(latest_version=latest_version))
            click.echo(FeedbackManager.warning_current_version(current_version=CURRENT_VERSION))

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    config = await get_config(host, token)
    ctx.ensure_object(dict)['config'] = config

    if ctx.invoked_subcommand == 'auth':
        return

    if gcp_project_id and gcs_bucket and google_application_credentials and not sf_account:
        bq_config = {
            'project_id': gcp_project_id,
            'bucket_name': gcs_bucket,
            'service_account': google_application_credentials,
            'with_headers': with_headers
        }
        ctx.ensure_object(dict)['bigquery'] = create_connector('bigquery', bq_config)
    if sf_account and sf_warehouse and sf_database and sf_schema and sf_role and sf_user and sf_password and gcs_bucket and google_application_credentials and gcp_project_id:
        sf_config = {
            'account': sf_account,
            'warehouse': sf_warehouse,
            'database': sf_database,
            'schema': sf_schema,
            'role': sf_role,
            'user': sf_user,
            'password': sf_password,
            'storage_integration': sf_storage_integration,
            'stage': sf_stage,
            'bucket_name': gcs_bucket,
            'service_account': google_application_credentials,
            'project_id': gcp_project_id,
            'with_headers': with_headers
        }
        ctx.ensure_object(dict)['snowflake'] = create_connector('snowflake', sf_config)

    logging.debug("debug enabled")

    ctx.ensure_object(dict)['client'] = TinyB(config.get('token', None), config['host'], version=VERSION)

    for connector in SUPPORTED_CONNECTORS:
        load_connector_config(ctx, connector, debug, check_uninstalled=True)


@cli.command()
@click.option('--generate-datasources', is_flag=True, default=False, help="Generate datasources based on CSV, NDJSON and Parquet files in this folder")
@click.option('--folder', default=None, type=click.Path(exists=True, file_okay=False), help="Folder where files will be placed")
@click.option('--force', is_flag=True, default=False, help="Overrides existing files")
@click.pass_context
@coro
async def init(ctx, generate_datasources, folder, force):
    """Initialize folder layout"""
    client = ctx.obj['client']
    folder = folder if folder else getcwd()
    await folder_init(client, folder, generate_datasources, force=force)
    return


@cli.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--debug', is_flag=True, default=False, help="Print internal representation")
def check(filename, debug):
    """Check file syntax"""
    click.echo(FeedbackManager.info_processing_file(filename=filename))

    try:
        if '.pipe' in filename:
            doc = parse_pipe(filename)
        else:
            doc = parse_datasource(filename)

        click.echo(FeedbackManager.success_processing_file(filename=filename))

    except ParseException as e:
        raise click.ClickException(FeedbackManager.error_exception(error=e))

    if debug:
        pp = pprint.PrettyPrinter()
        for x in doc.nodes:
            pp.pprint(x)


@cli.command()
@click.option('--prefix', default='', help="Use prefix for all the resources")
@click.option('--dry-run', is_flag=True, default=False, help="Run the command without creating resources on the Tinybird account or any side effect")
@click.option('--check/--no-check', is_flag=True, default=True, help="Enable/Disable output checking, enabled by default")
@click.option('--push-deps', is_flag=True, default=False, help="Push dependencies, disabled by default")
@click.option('--debug', is_flag=True, default=False, help="Prints internal representation, can be combined with any command to get more information.")
@click.option('-f', '--force', is_flag=True, default=False, help="Override pipes when they already exist")
@click.option('--override-datasource', is_flag=True, default=False, help="When pushing a pipe with a Materialized node if the target Data Source exists it will try to override it.")
@click.option('--populate', is_flag=True, default=False, help="Populate materialized nodes when pushing them")
@click.option('--subset', type=float, default=None, help="Populate with a subset percent of the data (limited to a maximum of 2M rows), this is useful to quickly test a materialized node with some data. The subset must be greater than 0 and lower than 0.1. A subset of 0.1 means a 10 percent of the data in the source Data Source will be used to populate the materialized view. Use it together with --populate, it has precedence over --sql-condition")
@click.option('--sql-condition', type=str, default=None, help="Populate with a SQL condition to be applied to the trigger Data Source of the Materialized View. For instance, `--sql-condition='date == toYYYYMM(now())'` it'll populate taking all the rows from the trigger Data Source which `date` is the current month. Use it together with --populate. --sql-condition is not taken into account if the --subset param is present. Including in the ``sql_condition`` any column present in the Data Source ``engine_sorting_key`` will make the populate job process less data.")
@click.option('--unlink-on-populate-error/--preserve-on-populate-error', is_flag=True, default=False, help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View, use --preserve-on-populate-error to keep the Materialized View even when the populate job fails.", hidden=True)
@click.option('--fixtures', is_flag=True, default=False, help="Append fixtures to data sources")
@click.option('--wait', is_flag=True, default=False, help="To be used along with --populate command. Waits for populate jobs to finish, showing a progress bar. Disabled by default.")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--only-response-times', is_flag=True, default=False, help="Checks only response times, when --force push a pipe")
@click.argument('filenames', type=click.Path(exists=True), nargs=-1, default=None)
@click.option('--workspace_map', nargs=2, type=str, multiple=True)
@click.option('--workspace', nargs=2, type=str, multiple=True, help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder")
@click.option('--no-versions', is_flag=True, default=False, help="when set, resource dependency versions are not used, it pushes the dependencies as-is")
@click.option('--timeout', type=float, default=None, help="timeout you want to use for the job populate")
@click.option('-l', '--limit', type=click.IntRange(0, 100), default=0, required=False, help="Number of requests to validate")
@click.option('--sample-by-params', type=click.IntRange(1, 100), default=1, required=False, help="When set, we will aggregate the pipe_stats_rt requests by extractURLParameterNames(assumeNotNull(url)) and for each combination we will take a sample of N requests")
@click.option('-ff', '--failfast', is_flag=True, default=False, help="When set, the checker will exit as soon one test fails")
@click.option('--ignore-order', is_flag=True, default=False, help="When set, the checker will ignore the order of list properties")
@click.option('--validate-processed-bytes', is_flag=True, default=False, help="When set, the checker will validate that the new version doesn't process more than 25% than the current version")
@click.pass_context
@coro
async def push(
    ctx: click.Context,
    prefix: str,
    filenames: Path,
    dry_run: bool,
    check: bool,
    push_deps: bool,
    debug: bool,
    force: bool,
    override_datasource: bool,
    populate: bool,
    subset: Optional[float],
    sql_condition: Optional[str],
    unlink_on_populate_error: bool,
    fixtures: bool,
    wait: bool,
    yes: bool,
    only_response_times: bool,
    workspace_map,
    workspace,
    no_versions: bool,
    timeout: Optional[float],
    limit: int,
    sample_by_params: int,
    failfast: bool,
    ignore_order: bool,
    validate_processed_bytes: bool
):

    """Push files to Tinybird
    """

    ignore_sql_errors = FeatureFlags.ignore_sql_errors()
    context.disable_template_security_validation.set(True)
    await folder_push(
        create_tb_client(ctx),
        prefix,
        filenames,
        dry_run,
        check,
        push_deps,
        debug,
        force,
        override_datasource=override_datasource,
        populate=populate,
        populate_subset=subset,
        populate_condition=sql_condition,
        unlink_on_populate_error=unlink_on_populate_error,
        upload_fixtures=fixtures,
        wait=wait,
        ignore_sql_errors=ignore_sql_errors,
        skip_confirmation=yes,
        only_response_times=only_response_times,
        workspace_map=dict(workspace_map),
        workspace_lib_paths=workspace,
        no_versions=no_versions,
        timeout=timeout,
        run_tests=False,
        tests_to_run=limit,
        tests_sample_by_params=sample_by_params,
        tests_failfast=failfast,
        tests_ignore_order=ignore_order,
        tests_validate_processed_bytes=validate_processed_bytes
    )
    return


@cli.command()  # noqa: C901
@click.option('--folder', default=None, type=click.Path(exists=True, file_okay=False), help="Folder where files will be placed")
@click.option('--auto', is_flag=True, default=False, help="Saves datafiles automatically into their default directories (/datasources or /pipes)")
@click.option('--match', default=None, help='Retrieve any resourcing matching the pattern. eg --match _test')
@click.option('--prefix', default=None, help="Download only resources with this prefix")
@click.option('--force', is_flag=True, default=False, help="Override existing files")
@click.pass_context
@coro
async def pull(ctx, folder, auto, match, prefix, force):
    """Retrieve latest versions for project files from Tinybird"""
    client = ctx.obj['client']
    folder = folder if folder else getcwd()

    return await folder_pull(client, folder, auto, match, prefix, force)


@cli.command()
@click.option('--no-deps', is_flag=True, default=False, help="Print only data sources with no pipes using them")
@click.option('--match', default=None, help='Retrieve any resource matching the pattern')
@click.option('--pipe', default=None, help='Retrieve any resource used by pipe')
@click.option('--datasource', default=None, help='Retrieve resources depending on this Data Source')
@click.option('--check-for-partial-replace', is_flag=True, default=False, help='Retrieve dependant Data Sources that will have their data replaced if a partial replace is executed in the Data Source selected')
@click.option('--recursive', is_flag=True, default=False, help='Calculate recursive dependencies')
@click.pass_context
@coro
async def dependencies(ctx, no_deps, match, pipe, datasource, check_for_partial_replace, recursive):
    """
    Print all data sources dependencies
    """
    client = ctx.obj['client']

    response = await client.datasource_dependencies(no_deps, match, pipe, datasource, check_for_partial_replace, recursive)
    for ds in response['dependencies']:
        click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        for pipe in response['dependencies'][ds]:
            click.echo(FeedbackManager.info_dependency_list_item(dependency=pipe))
    if 'incompatible_datasources' in response and len(response['incompatible_datasources']):
        click.echo(FeedbackManager.info_no_compatible_dependencies_found())
        for ds in response['incompatible_datasources']:
            click.echo(FeedbackManager.info_dependency_list(dependency=ds))
        raise click.ClickException(
            FeedbackManager.error_partial_replace_cant_be_executed(datasource=datasource))


@cli.command()
@click.argument('filenames', type=click.Path(exists=True), nargs=-1, required=True)
@click.option('--line-length', is_flag=False, default=100, help="A number indicating the maximum characters per line in the node SQL, lines will be splitted based on the SQL syntax and the number of characters passed as a parameter")
@click.option('--dry-run', is_flag=True, default=False, help="Don't ask to override the local file")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation to overwrite the local file")
@click.pass_context
@coro
async def fmt(ctx, filenames, line_length: int, dry_run: bool, yes: bool):
    """
    Formats a .datasource, .pipe or .incl file

    This command removes comments starting with # from the file, use DESCRIPTION instead.

    The format command tries to parse the datafile so syntax errors might rise.

    .incl files must contain a NODE definition
    """
    result = ''
    for filename in filenames:
        extension = Path(filename).suffix
        if extension == '.datasource':
            result = format_datasource(filename)
        elif extension in ['.pipe', '.incl']:
            result = format_pipe(filename, line_length)
        else:
            click.echo("Unsupported file type")
            return

        click.echo(result)
        if dry_run:
            return

        if yes or click.confirm(FeedbackManager.prompt_override_local_file(name=filename)):
            with open(f'{filename}', 'w') as file:
                file.write(result)

            click.echo(FeedbackManager.success_generated_local_file(file=filename))

    return result


@cli.command()
@click.argument('query')
@click.option('--rows_limit', default=100, help="Max number of rows retrieved")
@click.option('--format', 'format_', type=click.Choice(['json', 'csv', 'human'], case_sensitive=False), default='human', help="Output format")
@click.option('--stats/--no-stats', default=False, help="Show query stats")
@click.pass_context
@coro
async def sql(ctx, query, rows_limit, format_, stats):
    """Run SQL query over data sources and pipes"""
    client = ctx.obj['client']
    q = query.lower().strip()
    if q.startswith('insert'):
        click.echo(FeedbackManager.error_invalid_query())
        click.echo(FeedbackManager.info_append_data())
        return
    if q.startswith('delete'):
        click.echo(FeedbackManager.error_invalid_query())
        return

    req_format = 'CSVWithNames' if format_ == 'csv' else 'JSON'
    try:
        res = await client.query(f'SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}')
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return
    req_format = 'CSVWithNames' if format_ == 'csv' else 'JSON'
    parsed_query = f'SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT {req_format}'
    res = await client.query(parsed_query)

    if 'error' in res:
        click.echo(FeedbackManager.error_exception(error=res['error']))
        return

    if stats:
        stats_query = f'SELECT * FROM ({query}) LIMIT {rows_limit} FORMAT JSON'
        stats_res = await client.query(stats_query)
        stats = stats_res['statistics']
        seconds = stats['elapsed']
        rows_read = humanfriendly.format_number(stats['rows_read'])
        bytes_read = humanfriendly.format_size(stats['bytes_read'])
        click.echo(FeedbackManager.info_query_stats(seconds=seconds, rows=rows_read, bytes=bytes_read))

    if format_ == 'csv':
        click.echo(res)
    elif 'data' in res and res['data']:
        if format_ == 'json':
            click.echo(json.dumps(res, indent=8))
        else:
            dd = []
            for d in res['data']:
                dd.append(d.values())
            click.echo(humanfriendly.tables.format_smart_table(dd, column_names=res['data'][0].keys()))
    else:
        click.echo(FeedbackManager.info_no_rows())


@cli.command(name="materialize", short_help="Given a local Pipe datafile (.pipe) and a node name it generates the target Data Source and materialized Pipe ready to be pushed and guides you through the process to create the materialized view")
@click.argument('filename', type=click.Path(exists=True))
@click.argument('target_datasource', default=None, required=False)
@click.option('--prefix', default='', help="Use prefix for all the resources")
@click.option('--push-deps', is_flag=True, default=False, help="Push dependencies, disabled by default")
@click.option('--workspace_map', nargs=2, type=str, multiple=True, hidden=True)
@click.option('--workspace', nargs=2, type=str, multiple=True, help="add a workspace path to the list of external workspaces, usage: --workspace name path/to/folder")
@click.option('--no-versions', is_flag=True, default=False, help="when set, resource dependency versions are not used, it pushes the dependencies as-is")
@click.option('--verbose', is_flag=True, default=False, help="Prints more log")
@click.option('--force-populate', default=False, required=False, help="subset or full", hidden=True)
@click.option('--unlink-on-populate-error/--preserve-on-populate-error', is_flag=True, default=False, help="If the populate job fails the Materialized View is unlinked and new data won't be ingested in the Materialized View, use --preserve-on-populate-error to keep the Materialized View even when the populate job fails.", hidden=True)
@click.option('--override-pipe', is_flag=True, default=False, help="Override pipe if exists or prompt", hidden=True)
@click.option('--override-datasource', is_flag=True, default=False, help="Override data source if exists or prompt", hidden=True)
@click.pass_context
@coro
async def materialize(ctx, filename, prefix, push_deps, workspace_map, workspace, no_versions, verbose, force_populate, unlink_on_populate_error, override_pipe, override_datasource, target_datasource=None):
    """[BETA] Given a local Pipe datafile path (FILENAME) and optionally a Materialized View name (TARGET_DATASOURCE), choose one of its nodes to materialize.

    This command guides you to generate the Materialized View with name TARGET_DATASOURCE, the only requirement is having a valid Pipe datafile locally. Use `tb pull` to download resources from your workspace when needed.

    Syntax: tb materialize path/to/pipe.pipe
    """
    cl = create_tb_client(ctx)

    async def _try_push_pipe_to_analyze(pipe_name):
        try:
            to_run = await folder_push(
                cl,
                tag=prefix,
                filenames=[filename],
                dry_run=False,
                check=False,
                push_deps=push_deps,
                debug=False,
                force=False,
                workspace_map=dict(workspace_map),
                workspace_lib_paths=workspace,
                no_versions=no_versions,
                run_tests=False,
                as_standard=True,
                raise_on_exists=True,
                verbose=verbose
            )
        except AlreadyExistsException as e:
            if 'Datasource' in str(e):
                click.echo(str(e))
                return
            if override_pipe or click.confirm(FeedbackManager.info_pipe_exists(name=pipe_name)):
                to_run = await folder_push(
                    cl,
                    tag=prefix,
                    filenames=[filename],
                    dry_run=False,
                    check=False,
                    push_deps=push_deps,
                    debug=False,
                    force=True,
                    workspace_map=dict(workspace_map),
                    workspace_lib_paths=workspace,
                    no_versions=no_versions,
                    run_tests=False,
                    as_standard=True,
                    verbose=verbose
                )
            else:
                return
        except click.ClickException as e:
            click.echo(str(e))

        return to_run

    def _choose_node_name(pipe):
        node = pipe['nodes'][0]
        materialized_nodes = [node for node in pipe['nodes'] if node['type'].lower() == 'materialized']

        if len(materialized_nodes) == 1:
            node = materialized_nodes[0]

        if len(pipe['nodes']) > 1 and len(materialized_nodes) != 1:
            for index, node in enumerate(pipe['nodes'], start=1):
                click.echo(f"  [{index}] Materialize node with name => {node['name']}")
            option = click.prompt(FeedbackManager.prompt_choose_node(), default=len(pipe['nodes']))
            node = pipe['nodes'][option - 1]
        node_name = node['name']
        return node, node_name

    def _choose_target_datasource_name(pipe, node, node_name):
        datasource_name = target_datasource or node.get('datasource', None) or f'mv_{pipe["resource_name"]}_{node_name}'
        if prefix:
            datasource_name = ''.join(datasource_name.split(f'{prefix}__')[1:])
        return datasource_name

    def _save_local_backup_pipe(pipe):
        pipe_bak = f'{filename}_bak'
        shutil.copyfile(filename, pipe_bak)
        pipe_file_name = f"{pipe['resource_name']}.pipe"
        if prefix:
            pipe_file_name = ''.join(pipe_file_name.split(f'{prefix}__')[1:])

        click.echo(FeedbackManager.info_pipe_backup_created(name=pipe_bak))
        return pipe_file_name

    def _save_local_datasource(datasource_name, ds_datafile):
        base = Path('datasources')
        if not base.exists():
            base = Path()
        file_name = f"{datasource_name}.datasource"
        f = base / file_name
        with open(f'{f}', 'w') as file:
            file.write(ds_datafile)

        click.echo(FeedbackManager.success_generated_local_file(file=f))
        return f

    async def _try_push_datasource(datasource_name, f):
        exists = False
        try:
            exists = await cl.get_datasource(datasource_name)
        except Exception:
            pass

        if exists:
            click.echo(FeedbackManager.info_materialize_push_datasource_exists(name=f.name))
            if override_datasource or click.confirm(FeedbackManager.info_materialize_push_datasource_override(name=f)):
                try:
                    await cl.datasource_delete(datasource_name, force=True)
                except DoesNotExistException:
                    pass

        filename = str(f.absolute())
        to_run = await folder_push(
            cl,
            tag=prefix,
            filenames=[filename],
            push_deps=push_deps,
            workspace_map=dict(workspace_map),
            workspace_lib_paths=workspace,
            no_versions=no_versions,
            verbose=verbose
        )
        return to_run

    def _save_local_pipe(pipe_file_name, pipe_datafile, pipe):
        base = Path('pipes')
        if not base.exists():
            base = Path()
        f_pipe = base / pipe_file_name

        with open(f'{f_pipe}', 'w') as file:
            if pipe['version'] is not None and pipe['version'] >= 0:
                pipe_datafile = f"VERSION {pipe['version']} \n {pipe_datafile}"
            prefix_name = ''
            if prefix:
                prefix_name = prefix
            matches = re.findall(rf'(({prefix_name}__)?([^\s\.]*)__v\d+)', pipe_datafile)
            for match in set(matches):
                if match[2] in pipe_datafile:
                    pipe_datafile = pipe_datafile.replace(match[0], match[2])
            file.write(pipe_datafile)

        click.echo(FeedbackManager.success_generated_local_file(file=f_pipe))
        return f_pipe

    async def _try_push_pipe(f_pipe):
        if override_pipe:
            option = 2
        else:
            click.echo(FeedbackManager.info_materialize_push_pipe_skip(name=f_pipe.name))
            click.echo(FeedbackManager.info_materialize_push_pipe_override(name=f_pipe.name))
            option = click.prompt(FeedbackManager.prompt_choose(), default=1)
        force = True
        check = True if option == 1 else False

        filename = str(f_pipe.absolute())
        to_run = await folder_push(
            cl,
            tag=prefix,
            filenames=[filename],
            dry_run=False,
            check=check,
            push_deps=push_deps,
            debug=False,
            force=force,
            unlink_on_populate_error=unlink_on_populate_error,
            workspace_map=dict(workspace_map),
            workspace_lib_paths=workspace,
            no_versions=no_versions,
            run_tests=False,
            verbose=verbose
        )
        return to_run

    async def _populate(pipe, node_name, f_pipe):
        if force_populate or click.confirm(FeedbackManager.prompt_populate(file=f_pipe)):
            if not force_populate:
                click.echo(FeedbackManager.info_materialize_populate_partial())
                click.echo(FeedbackManager.info_materialize_populate_full())
                option = click.prompt(FeedbackManager.prompt_choose(), default=1)
            else:
                option = 1 if force_populate == 'subset' else 2
            populate = False
            populate_subset = False
            if option == 1:
                populate_subset = 0.1
                populate = True
            elif option == 2:
                populate = True

            if populate:
                response = await cl.populate_node(pipe['name'], node_name, populate_subset=populate_subset, unlink_on_populate_error=unlink_on_populate_error)
                if 'job' not in response:
                    raise click.ClickException(response)

                job_url = response.get('job', {}).get('job_url', None)
                job_id = response.get('job', {}).get('job_id', None)
                click.echo(FeedbackManager.info_populate_job_url(url=job_url))
                wait_populate = True
                if wait_populate:
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
                            raise click.ClickException(FeedbackManager.error_getting_populate_info(error=str(e), url=job_url))

    click.echo(FeedbackManager.warning_beta_tester())
    pipe_name = os.path.basename(filename).rsplit('.', 1)[0]
    if prefix:
        pipe_name = f'{prefix}__{pipe_name}'
    click.echo(FeedbackManager.info_before_push_materialize(name=filename))
    try:
        # extracted the materialize logic to local functions so the workflow is more readable
        to_run = await _try_push_pipe_to_analyze(pipe_name)

        if to_run is None:
            return

        pipe = to_run[pipe_name.split('/')[-1]]
        node, node_name = _choose_node_name(pipe)
        datasource_name = _choose_target_datasource_name(pipe, node, node_name)

        click.echo(FeedbackManager.info_before_materialize(name=pipe['name']))
        analysis = await cl.analyze_pipe_node(pipe['name'], node, datasource_name=datasource_name)
        ds_datafile = analysis['analysis']['datasource']['datafile']
        pipe_datafile = analysis['analysis']['pipe']['datafile']

        pipe_file_name = _save_local_backup_pipe(pipe)
        f = _save_local_datasource(datasource_name, ds_datafile)
        await _try_push_datasource(datasource_name, f)

        f_pipe = _save_local_pipe(pipe_file_name, pipe_datafile, pipe)
        await _try_push_pipe(f_pipe)
        await _populate(pipe, node_name, f_pipe)

        prefix_name = f'{prefix}__' if prefix else ''
        click.echo(FeedbackManager.success_created_matview(name=f'{prefix_name}{datasource_name}'))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))


@cli.command(short_help="Drop all the resources inside a project with prefix. This command is dangerous because it removes everything, use with care")  # noqa: C901
@click.argument('prefix')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--dry-run', is_flag=True, default=False, help="Run the command without removing anything")
@click.pass_context
@coro
async def drop_prefix(ctx, prefix, yes, dry_run):  # noqa: C901
    """Drop all the resources inside a project with prefix. This command is dangerous because it removes everything, use with care"""

    if yes or click.confirm(FeedbackManager.warning_confirm_drop_prefix(prefix=prefix)):
        filenames = get_project_filenames(getcwd())
        context.disable_template_security_validation.set(True)
        resources, dep_map = await build_graph(filenames, create_tb_client(ctx), process_dependencies=True)
        names = [r['resource_name'].replace(".", "_") for r in resources.values()]
        res = {}
        client = ctx.obj['client']

        pipes = await client.pipes()
        for pipe in pipes:
            tk = get_name_tag_version(pipe['name'])
            if tk['tag'] == prefix and tk['name'] in names:
                res[tk['name']] = pipe['name']

        for group in reversed(list(toposort(dep_map))):
            for name in group:
                if name in res:
                    if resources[name]['resource'] == 'datasources':
                        if not dry_run:
                            click.echo(FeedbackManager.info_removing_datasource(datasource=res[name]))
                            try:
                                await client.datasource_delete(res[name], force=True)
                            except DoesNotExistException:
                                click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=res[name]))
                            except CanNotBeDeletedException as e:
                                click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=res[name], error=e))
                            except Exception as e:
                                raise click.ClickException(FeedbackManager.error_exception(error=e))
                        else:
                            click.echo(FeedbackManager.info_dry_removing_datasource(datasource=res[name]))
                    else:
                        if not dry_run:
                            click.echo(FeedbackManager.info_removing_pipe(pipe=res[name]))
                            try:
                                await client.pipe_delete(res[name])
                            except DoesNotExistException:
                                click.echo(FeedbackManager.info_removing_pipe_not_found(pipe=res[name]))
                        else:
                            click.echo(FeedbackManager.info_dry_removing_pipe(pipe=res[name]))

        ds = await client.datasources()
        for t in ds:
            tk = get_name_tag_version(t['name'])
            if tk['tag'] == prefix and tk['name'] in names:
                res[tk['name']] = t['name']
                if not dry_run:
                    click.echo(FeedbackManager.info_removing_datasource(datasource=t['name']))
                    try:
                        await client.datasource_delete(t['name'], force=True)
                    except DoesNotExistException:
                        click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=t['name']))
                    except CanNotBeDeletedException as e:
                        click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=t['name'], error=e))
                    except Exception as e:
                        raise click.ClickException(FeedbackManager.error_exception(error=e))
                else:
                    click.echo(FeedbackManager.info_dry_removing_datasource(datasource=t['name']))


def __patch_click_output():
    import re

    __old_click_echo = click.echo

    def obfuscate(msg: Any, *args, **kwargs) -> None:
        msg = re.sub(r'p\.ey[A-Za-z0-9-_\.]+', "p.ey****...****", str(msg))
        __old_click_echo(msg, *args, **kwargs)

    click.echo = obfuscate


def __unpatch_click_output():
    click.echo = __old_click_echo
