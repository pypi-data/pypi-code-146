
# This is the common file for our CLI. Please keep it clean (as possible)
#
# - Put here any common utility function you consider.
# - If any function is only called within a specific command, consider moving
#   the function to the proper command file.
# - Please, **do not** define commands here.

from copy import deepcopy
import json
from os import environ, getcwd, getenv
from enum import Enum
import sys
from typing import Any, Dict, List, Optional, Tuple
import uuid
import click
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin

from click import Context
import humanfriendly
import humanfriendly.tables
from tinybird.client import TinyB, AuthException, AuthNoTokenException, DoesNotExistException, OperationCanNotBePerformed, ConnectorNothingToLoad
from sys import version_info
from tinybird.connectors import Connector
from tinybird.datafile import get_name_tag_version, wait_job

from tinybird.feedback_manager import FeedbackManager

import asyncio
from functools import wraps

from tinybird.config import DEFAULT_LOCALHOST, get_config, write_config, FeatureFlags, VERSION, SUPPORTED_CONNECTORS, PROJECT_PATHS, DEFAULT_API_HOST, DEFAULT_UI_HOST

import socket
from contextlib import closing

from tinybird.syncasync import async_to_sync

SUPPORTED_FORMATS = ['csv', 'ndjson', 'json', 'parquet']


def create_connector(connector: str, options: Dict[str, Any]):
    # Imported here to improve startup time when the connectors aren't used
    from tinybird.connectors import create_connector as _create_connector, UNINSTALLED_CONNECTORS
    if connector in UNINSTALLED_CONNECTORS:
        raise click.ClickException(FeedbackManager.error_connector_not_installed(connector=connector))
    return _create_connector(connector, options)


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if version_info[1] >= 7:  # FIXME drop python 3.6 support
            return asyncio.run(f(*args, **kwargs))
        else:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(f(*args, **kwargs))
    return wrapper


def print_data_table(res):
    if not res['data']:
        click.echo(FeedbackManager.info_no_rows())
        return

    dd = []
    for d in res['data']:
        dd.append(d.values())
    click.echo(humanfriendly.tables.format_smart_table(dd, column_names=res['data'][0].keys()))


def normalize_datasource_name(s: str) -> str:
    s = re.sub(r'[^0-9a-zA-Z_]', '_', s)
    if s[0] in '0123456789':
        return "c_" + s
    return s


def generate_datafile(datafile: str, filename: str, data: Optional[bytes], force: bool, _format: str = 'csv'):
    p = Path(filename)
    base = Path('datasources')
    if not base.exists():
        base = Path()
    f = base / (normalize_datasource_name(p.stem) + ".datasource")
    if not f.exists() or force:
        with open(f'{f}', 'w') as ds_file:
            ds_file.write(datafile)
        click.echo(FeedbackManager.success_generated_file(file=f, stem=p.stem, filename=filename))

        if data:
            # generate fixture
            if (base / 'fixtures').exists():
                # Generating a fixture for Parquet files is not so trivial, since Parquet format
                # is column-based. We would need to add PyArrow as a dependency (which is huge)
                # just to analyze the whole Parquet file to extract one single row.
                if _format == 'parquet':
                    click.echo(FeedbackManager.warning_parquet_fixtures_not_supported())
                else:
                    f = base / 'fixtures' / (p.stem + f".{_format}")
                    newline = b'\n'  # TODO: guess
                    with open(f, 'wb') as fixture_file:
                        fixture_file.write(data[:data.rfind(newline)])
                    click.echo(FeedbackManager.success_generated_fixture(fixture=f))
    else:
        click.echo(FeedbackManager.error_file_already_exists(file=f))


async def get_config_and_hosts(ctx: Context) -> Tuple[Dict[str, Any], str, str]:
    """Returns (config, host, ui_host)"""

    config = ctx.ensure_object(dict)['config']
    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    host = config['host']
    ui_host = DEFAULT_UI_HOST if host == DEFAULT_API_HOST else host

    return config, host, ui_host


async def get_current_workspace(client, config):
    workspaces: List[Dict[str, Any]] = (await client.user_workspaces()).get('workspaces', [])
    return next((workspace for workspace in workspaces if workspace['id'] == config['id']), None)


class CatchAuthExceptions(click.Group):
    """utility class to get all the auth exceptions"""

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except AuthNoTokenException:
            click.echo(FeedbackManager.error_notoken())
        except AuthException as exc:
            click.echo(FeedbackManager.error_exception(error=exc))


def load_connector_config(ctx: Context, connector_name: str, debug: bool, check_uninstalled: bool = False):
    config_file = Path(getcwd()) / f".tinyb_{connector_name}"
    try:
        if connector_name not in ctx.ensure_object(dict):
            with open(config_file) as file:
                config = json.loads(file.read())
            from tinybird.connectors import UNINSTALLED_CONNECTORS
            if check_uninstalled and connector_name in UNINSTALLED_CONNECTORS:
                click.echo(FeedbackManager.warning_connector_not_installed(connector=connector_name))
                return
            ctx.ensure_object(dict)[connector_name] = create_connector(connector_name, config)
    except IOError:
        if debug:
            click.echo(f"** {connector_name} connector not configured")
        pass


def getenv_bool(key: str, default: bool) -> bool:
    v: Optional[str] = getenv(key)
    if v is None:
        return default
    return v.lower() == 'true' or v == '1'


def _get_tb_client(token: str, host: str) -> TinyB:
    disable_ssl: bool = getenv_bool('TB_DISABLE_SSL_CHECKS', False)
    return TinyB(token, host, version=VERSION, disable_ssl_checks=disable_ssl)


def create_tb_client(ctx: Context) -> TinyB:
    token = ctx.ensure_object(dict)['config'].get('token', '')
    host = ctx.ensure_object(dict)['config'].get('host', DEFAULT_API_HOST)
    return _get_tb_client(token, host)


async def _analyze(filename: str, client: TinyB, format: str, connector: Optional[Connector] = None):
    data: Optional[bytes] = None
    if not connector:
        parsed = urlparse(filename)
        if parsed.scheme in ('http', 'https'):
            meta = await client.datasource_analyze(filename)
        else:
            with open(filename, 'rb') as file:
                # We need to read the whole file in binary for Parquet, while for the
                # others we just read 1KiB
                if format == 'parquet':
                    data = file.read()
                else:
                    data = file.read(1024 * 1024)

            meta = await client.datasource_analyze_file(data)
    else:
        meta = connector.datasource_analyze(filename)
    return meta, data


async def _generate_datafile(filename: str, client: TinyB, force: bool, format: str, connector: Optional[Connector] = None):
    meta, data = await _analyze(filename, client, format, connector=connector)
    schema = meta['analysis']['schema']
    schema = schema.replace(', ', ',\n    ')
    datafile = f"""DESCRIPTION >\n    Generated from {filename}\n\nSCHEMA >\n    {schema}"""
    return generate_datafile(datafile, filename, data, force, _format=format)


async def folder_init(client, folder, generate_datasources=False, force=False):
    for x in PROJECT_PATHS:
        try:
            f = Path(folder) / x
            f.mkdir()
            click.echo(FeedbackManager.info_path_created(path=x))
        except FileExistsError:
            if not force:
                click.echo(FeedbackManager.info_path_already_exists(path=x))
            pass

    if generate_datasources:
        for format in SUPPORTED_FORMATS:
            for path in Path(folder).glob(f'*.{format}'):
                await _generate_datafile(str(path), client, format=format, force=force)


async def folder_pull(client, folder, auto, match, tag, force):  # noqa: C901
    pattern = re.compile(match) if match else None

    def _get_latest_versions(resources, tag):
        versions = {}

        for x in resources:
            t = get_name_tag_version(x)
            t['original_name'] = x
            if t['version'] is None:
                t['version'] = -1
            name = t['name']

            if not tag:
                versions[name] = t
            elif t['tag'] == tag:
                if name in versions:
                    if versions[name]['version'] < t['version']:
                        versions[name] = t
                else:
                    versions[name] = t
        return versions

    def get_file_folder(extension):
        if not auto:
            return None
        if extension == 'datasource':
            return 'datasources'
        if extension == 'pipe':
            return 'pipes'
        return None

    async def write_files(versions, resources, extension, get_resource_function):
        values = versions.values()

        for k in values:
            name = f"{k['name']}.{extension}"

            prefix_info = ''
            prefix_name = ''
            if not tag:
                if k['tag']:
                    prefix_name = f"{k['tag']}"
                    prefix_info = f"({prefix_name})"
            else:
                prefix_name = f"{tag}"
                prefix_info = f"({prefix_name})"

            try:
                if pattern and not pattern.search(name):
                    click.echo(FeedbackManager.info_skipping_resource(resource=name))
                    continue

                resource = await getattr(client, get_resource_function)(k['original_name'])

                dest_folder = folder
                if '.' in k['name']:
                    dest_folder = Path(folder) / 'vendor' / k['name'].split('.', 1)[0]
                    name = f"{k['name'].split('.', 1)[1]}.{extension}"

                file_folder = get_file_folder(extension)
                f = Path(dest_folder) / file_folder if file_folder is not None else Path(dest_folder)

                if not f.exists():
                    f.mkdir(parents=True)

                f = f / name

                click.echo(FeedbackManager.info_writing_resource(resource=f, prefix=prefix_info))
                if not f.exists() or force:
                    with open(f, 'w') as fd:
                        # versions are a client only thing so
                        # datafiles from the server do not contains information about versions
                        if k['version'] >= 0:
                            resource = f"VERSION {k['version']}\n" + resource
                        if resource:
                            matches = re.findall(rf'(({prefix_name}__)?([^\s\.]*)__v\d+)', resource)
                            for match in set(matches):
                                if match[2] in resources:
                                    resource = resource.replace(match[0], match[2])
                            fd.write(resource)
                else:
                    click.echo(FeedbackManager.info_skip_already_exists())
            except Exception as e:
                raise Exception(FeedbackManager.error_exception(error=e))
        return

    try:
        datasources = await client.datasources()
        remote_datasources = sorted([x['name'] for x in datasources])
        datasources_versions = _get_latest_versions(remote_datasources, tag)

        pipes = await client.pipes()
        remote_pipes = sorted([x['name'] for x in pipes])
        pipes_versions = _get_latest_versions(remote_pipes, tag)

        resources = list(datasources_versions.keys()) + list(pipes_versions.keys())

        await write_files(datasources_versions, resources, 'datasource', 'datasource_file')
        await write_files(pipes_versions, resources, 'pipe', 'pipe_file')

        return

    except Exception as e:
        raise click.ClickException(FeedbackManager.error_pull(error=str(e)))


async def configure_connector(connector):
    if connector not in SUPPORTED_CONNECTORS:
        click.echo(FeedbackManager.error_invalid_connector(connectors=', '.join(SUPPORTED_CONNECTORS)))
        return

    file_name = f".tinyb_{connector}"
    config_file = Path(getcwd()) / file_name
    if connector == 'bigquery':
        project = click.prompt("BigQuery project ID")
        service_account = click.prompt("Path to a JSON service account file with permissions to export from BigQuery, write in Storage and sign URLs (leave empty to use GOOGLE_APPLICATION_CREDENTIALS environment variable)", default=environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''))
        bucket_name = click.prompt("Name of a Google Cloud Storage bucket to store temporary exported files")

        try:
            config = {
                'project_id': project,
                'service_account': service_account,
                'bucket_name': bucket_name
            }
            await write_config(config, file_name)
        except Exception:
            raise click.ClickException(FeedbackManager.error_file_config(config_file=config_file))
    elif connector == 'snowflake':
        sf_account = click.prompt("Snowflake Account (e.g. your-domain.west-europe.azure)")
        sf_warehouse = click.prompt("Snowflake warehouse name")
        sf_database = click.prompt("Snowflake database name")
        sf_schema = click.prompt("Snowflake schema name")
        sf_role = click.prompt("Snowflake role name")
        sf_user = click.prompt("Snowflake user name")
        sf_password = click.prompt("Snowflake password")
        sf_storage_integration = click.prompt("Snowflake GCS storage integration name (leave empty to auto-generate one)", default='')
        sf_stage = click.prompt("Snowflake GCS stage name (leave empty to auto-generate one)", default='')
        project = click.prompt("Google Cloud project ID to store temporary files")
        service_account = click.prompt("Path to a JSON service account file with permissions to write in Storagem, sign URLs and IAM (leave empty to use GOOGLE_APPLICATION_CREDENTIALS environment variable)", default=environ.get('GOOGLE_APPLICATION_CREDENTIALS', ''))
        bucket_name = click.prompt("Name of a Google Cloud Storage bucket to store temporary exported files")

        if not service_account:
            service_account = getenv('GOOGLE_APPLICATION_CREDENTIALS')

        try:
            config = {
                'account': sf_account,
                'warehouse': sf_warehouse,
                'database': sf_database,
                'schema': sf_schema,
                'role': sf_role,
                'user': sf_user,
                'password': sf_password,
                'storage_integration': sf_storage_integration,
                'stage': sf_stage,
                'service_account': service_account,
                'bucket_name': bucket_name,
                'project_id': project,
            }
            await write_config(config, file_name)
        except Exception:
            raise click.ClickException(FeedbackManager.error_file_config(config_file=config_file))

        click.echo(FeedbackManager.success_connector_config(connector=connector, file_name=file_name))


async def _get_config(host, token, load_tb_file=True):
    config = {}

    try:
        client = TinyB(token, host, version=VERSION)
        response = await client.workspace_info()
    except Exception:
        raise click.ClickException(FeedbackManager.error_invalid_token_for_host(host=host))

    from_response = load_tb_file

    try:
        config_file = Path(getcwd()) / ".tinyb"
        with open(config_file) as file:
            config = json.loads(file.read())
    except Exception:
        from_response = True

    if not from_response:
        return config

    config.update({
        'host': host,
        'token': token,
        'id': response['id'],
        'name': response['name']
    })

    if 'user_email' in response:
        config['user_email'] = response['user_email']
    if 'user_id' in response:
        config['user_id'] = response['user_id']
    if 'scope' in response:
        config['scope'] = response['scope']
    if 'id' in response:
        config['id'] = response['id']

    tokens = config.get('tokens', {})

    tokens.update({host: token})
    config['tokens'] = tokens
    config['token'] = tokens[host]
    config['host'] = host

    return config


async def get_regions(client: TinyB, config_file: Path) -> List[Dict[str, str]]:
    regions: List[Dict[str, str]] = []
    try:
        response = await client.regions()
        regions = response['regions']
    except Exception:
        pass

    try:
        with open(config_file) as file:
            config = json.loads(file.read())
            if 'tokens' not in config:
                return regions

            for key in config['tokens']:
                region = next((region for region in regions if key == region['api_host'] or key == region['host']), None)
                if region:
                    region['default_password'] = config['tokens'][key]
                else:
                    regions.append({
                        'api_host': format_host(key, subdomain='api'),
                        'host': format_host(key, subdomain='ui'),
                        'name': key,
                        'default_password': config['tokens'][key]
                    })

    except Exception:
        pass

    return regions


def _compare_hosts(region: Dict[str, Any], config: Dict[str, Any]) -> bool:
    return region['host'] == config['host'] or region['api_host'] == config['host']


async def get_host_from_region(region_name_or_host_or_id: str, host: Optional[str] = None):
    is_localhost = FeatureFlags.is_localhost()

    if not host:
        host = DEFAULT_API_HOST if not is_localhost else DEFAULT_LOCALHOST

    client = _get_tb_client(token='', host=host)

    try:
        response = await client.regions()
        regions = response['regions']
    except Exception:
        regions = []

    if not regions:
        click.echo(f"No regions available, using host: {host}")
        return [], host

    try:
        index = int(region_name_or_host_or_id)
        try:
            host = regions[index - 1]['api_host']
        except Exception:
            raise click.ClickException(FeedbackManager.error_getting_region_by_index())
    except Exception:
        region_name_or_host_or_id = region_name_or_host_or_id.lower()
        try:
            region = next((region for region in regions if _compare_region_host(region_name_or_host_or_id, region)), None)
            host = region['api_host'] if region else None
        except Exception:
            raise click.ClickException(FeedbackManager.error_getting_region_by_name_or_url())

    if not host:
        raise click.ClickException(FeedbackManager.error_getting_region_by_name_or_url())

    return regions, host


def _compare_region_host(region_name_or_host: str, region: Dict[str, Any]) -> bool:
    if region['name'].lower() == region_name_or_host:
        return True
    if region['host'] == region_name_or_host:
        return True
    if region['api_host'] == region_name_or_host:
        return True
    return False


def ask_for_region_interactively(regions):
    region_index = -1

    while region_index == -1:
        click.echo(FeedbackManager.info_available_regions())
        for index, region in enumerate(regions):
            click.echo(f"   [{index + 1}] {region['name'].lower()} ({region['host']})")
        click.echo("   [0] Cancel")

        region_index = click.prompt("\nUse region", default=1)

        if region_index == 0:
            click.echo(FeedbackManager.info_auth_cancelled_by_user())
            return None

        try:
            return regions[int(region_index) - 1]
        except Exception:
            available_options = ', '.join(map(str, range(1, len(regions) + 1)))
            click.echo(FeedbackManager.error_region_index(host_index=region_index, available_options=available_options))
            region_index = -1


def get_region_info(ctx, region=None):
    name = region['name'] if region else 'default'
    api_host = format_host(region['api_host'] if region else ctx.obj['config'].get('host', DEFAULT_API_HOST), subdomain='api')
    ui_host = format_host(region['host'] if region else ctx.obj['config'].get('host', DEFAULT_UI_HOST), subdomain='ui')
    return name, api_host, ui_host


def format_host(host: str, subdomain: str = None) -> str:
    """
    >>> format_host('api.tinybird.co')
    'https://api.tinybird.co'
    >>> format_host('https://api.tinybird.co')
    'https://api.tinybird.co'
    >>> format_host('http://localhost:8001')
    'http://localhost:8001'
    >>> format_host('localhost:8001')
    'http://localhost:8001'
    >>> format_host('localhost:8001', subdomain='ui')
    'http://localhost:8001'
    >>> format_host('localhost:8001', subdomain='api')
    'http://localhost:8001'
    >>> format_host('https://api.tinybird.co', subdomain='ui')
    'https://ui.tinybird.co'
    >>> format_host('https://api.us-east.tinybird.co', subdomain='ui')
    'https://ui.us-east.tinybird.co'
    >>> format_host('https://api.us-east.tinybird.co', subdomain='api')
    'https://api.us-east.tinybird.co'
    >>> format_host('https://ui.us-east.tinybird.co', subdomain='api')
    'https://api.us-east.tinybird.co'
    >>> format_host('https://inditex-rt-pro.tinybird.co', subdomain='ui')
    'https://inditex-rt-pro.tinybird.co'
    >>> format_host('https://cluiente-tricky.tinybird.co', subdomain='api')
    'https://cluiente-tricky.tinybird.co'
    """
    is_localhost = FeatureFlags.is_localhost()
    if subdomain and not is_localhost:
        url_info = urlparse(host)
        current_subdomain = url_info.netloc.split('.')[0]
        if current_subdomain == 'api' or current_subdomain == 'ui':
            host = host.replace(current_subdomain, subdomain)
    if 'localhost' in host or is_localhost:
        host = f'http://{host}' if 'http' not in host else host
    elif not host.startswith('http'):
        host = f'https://{host}'
    return host


def region_from_host(region_name_or_host, regions):
    """Returns the region that matches region_name_or_host"""

    return next((r for r in regions if _compare_region_host(region_name_or_host, r)), None)


async def try_get_config(host, token):
    try:
        return await _get_config(host, token)
    except Exception:
        return None


async def authenticate(ctx, host, token=None, regions=None, interactive=False, try_all_regions=False):
    is_localhost = FeatureFlags.is_localhost()
    check_host = DEFAULT_API_HOST if not host and not is_localhost else DEFAULT_LOCALHOST

    client = _get_tb_client(token='', host=check_host)
    config_file = Path(getcwd()) / ".tinyb"
    default_password: Optional[str] = None

    if not regions and interactive:
        regions = await get_regions(client, config_file)

    selected_region = None

    if regions and interactive:
        selected_region = ask_for_region_interactively(regions)
        if selected_region is None:
            return None

        host = selected_region['api_host']
        default_password = selected_region.get('default_password', None)
    elif regions and not interactive:
        selected_region = region_from_host(host, regions)

    if host and not regions and not selected_region:
        name, host, ui_host = (host, format_host(host, subdomain='api'), format_host(host, subdomain='ui'))
    else:
        name, host, ui_host = get_region_info(ctx, selected_region)

    token = token or ctx.ensure_object(dict)['config'].get('token_passed')

    if not token:
        tokens_url = urljoin(ui_host, 'tokens')
        token = click.prompt(
            f"\nCopy the admin token from {tokens_url} and paste it here { f'OR press enter to use the token from .tinyb file' if default_password else ''}",
            hide_input=True,
            show_default=False,
            default=default_password)

    config = await try_get_config(host, token)
    if config is None and not try_all_regions:
        raise click.ClickException(FeedbackManager.error_invalid_token_for_host(host=host))

    # No luck? Let's try auth in all other regions
    if config is None and try_all_regions and not interactive:
        if not regions:
            regions = await get_regions(client, config_file)

        # Check other regions, ignoring the previously tested region
        for region in [r for r in regions if r is not selected_region]:
            name, host, ui_host = get_region_info(ctx, region)
            config = await try_get_config(host, token)
            if config is not None:
                click.echo(FeedbackManager.success_using_host(name=name, host=ui_host))
                break

    if config is None:
        raise click.ClickException(FeedbackManager.error_invalid_token())

    try:
        if 'id' in config:
            await write_config(config)
            ctx.ensure_object(dict)['client'] = _get_tb_client(config['token'], config.get('host', DEFAULT_API_HOST))
            ctx.ensure_object(dict)['config'] = config
        else:
            raise click.ClickException(FeedbackManager.error_not_personal_auth())
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_exception(error=str(e)))

    click.echo(FeedbackManager.success_auth())
    click.echo(FeedbackManager.success_remember_api_host(api_host=host))

    if 'scope' not in config or not config['scope']:
        click.echo(FeedbackManager.warning_token_scope())

    if 'scope' in config and config['scope'] == 'admin':
        click.echo(FeedbackManager.warning_workspaces_admin_token())

    return config


def ask_for_user_token(action: str, ui_host: str) -> str:
    return click.prompt(f"\nIn order to {action} we need your user token. Copy it from {ui_host}/tokens and paste it here",
                        hide_input=True,
                        show_default=False,
                        default=None)


async def get_available_starterkits(ctx: Context) -> List[Dict[str, Any]]:
    ctx_dict = ctx.ensure_object(dict)
    available_starterkits = ctx_dict.get('available_starterkits', None)
    if available_starterkits is not None:
        return available_starterkits

    try:
        client: TinyB = ctx_dict['client']

        available_starterkits = await client.starterkits()
        ctx_dict['available_starterkits'] = available_starterkits
        return available_starterkits
    except Exception as ex:
        click.echo(FeedbackManager.error_exception(error=ex))
        return []


async def get_starterkit(ctx: Context, name: str) -> Optional[Dict[str, Any]]:
    available_starterkits = await get_available_starterkits(ctx)
    if not available_starterkits:
        return None
    return next((sk for sk in available_starterkits if sk.get('friendly_name', None) == name), None)


async def is_valid_starterkit(ctx: Context, name: str) -> bool:
    return await get_starterkit(ctx, name) is not None


async def ask_for_starterkit_interactively(ctx: Context) -> Optional[str]:
    starterkit = [{'friendly_name': 'blank', 'description': 'Empty workspace'}]
    starterkit.extend(await get_available_starterkits(ctx))
    rows = [(index + 1, sk['friendly_name'], sk['description']) for index, sk in enumerate(starterkit)]

    click.echo(humanfriendly.tables.format_smart_table(rows, column_names=['Idx', 'Id', 'Description']))
    click.echo("")
    click.echo("   [0] to cancel")

    sk_index = -1
    while sk_index == -1:
        sk_index = click.prompt("\nUse starter kit", default=1)
        if sk_index < 0 or sk_index > len(starterkit):
            click.echo(FeedbackManager.error_starterkit_index(starterkit_index=sk_index))
            sk_index = -1

    if sk_index == 0:
        click.echo(FeedbackManager.info_cancelled_by_user())
        return None

    return starterkit[sk_index - 1]['friendly_name']


async def fork_workspace(ctx: Context, client: TinyB, user_client: TinyB, created_workspace):
    config, _, _ = await get_config_and_hosts(ctx)

    datasources = await client.datasources()
    for datasource in datasources:
        await user_client.datasource_share(datasource['id'], config['id'], created_workspace['id'])  # type: ignore


async def create_workspace_non_interactive(ctx: Context, workspace_name: str,
                                           starterkit: str, user_token: str,
                                           fork: bool):
    """Creates a workspace using the provided name and starterkit
    """
    client: TinyB = ctx.ensure_object(dict)['client']

    try:
        user_client: TinyB = deepcopy(client)
        user_client.token = user_token

        created_workspace = await user_client.create_workspace(workspace_name, starterkit)
        click.echo(FeedbackManager.success_workspace_created(workspace_name=workspace_name))

        if fork:
            await fork_workspace(ctx, client, user_client, created_workspace)

    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))


async def create_workspace_interactive(ctx: Context, workspace_name: Optional[str],
                                       starterkit: Optional[str], user_token: str,
                                       fork: bool):
    if not starterkit:
        click.echo('\n')
        starterkit = await ask_for_starterkit_interactively(ctx)
        if not starterkit:  # Cancelled by user
            return

        if starterkit == 'blank':  # 'blank' == empty workspace
            starterkit = None

    if not workspace_name:
        """Creates a workspace guiding the user
        """
        click.echo('\n')
        click.echo(FeedbackManager.info_workspace_create_greeting())
        default_name = f'new_workspace_{uuid.uuid4().hex[0:4]}'
        workspace_name = click.prompt("\nWorkspace name", default=default_name, err=True, type=str)  # type: ignore

    await create_workspace_non_interactive(ctx, workspace_name, starterkit,  # type: ignore
                                           user_token, fork)


async def create_workspace_branch(ctx: Context, branch_name: Optional[str], last_partition: Optional[bool], all: Optional[bool], wait: Optional[bool]):
    """
    Creates a workspace branch
    """
    client: TinyB = ctx.ensure_object(dict)['client']

    try:
        config, _, _ = await get_config_and_hosts(ctx)
        workspace = await get_current_workspace(client, config)

        if not branch_name:
            click.echo(FeedbackManager.info_workspace_branch_create_greeting())
            default_name = f"{workspace['name']}_{uuid.uuid4().hex[0:4]}"
            branch_name = click.prompt("\nBranch name", default=default_name, err=True, type=str)  # type: ignore

        response = await client.create_workspace_branch(branch_name, last_partition, all)  # type: ignore
        click.echo(FeedbackManager.success_workspace_branch_created(workspace_name=workspace['name'],
                                                                    branch_name=branch_name))
        await switch_workspace(ctx, branch_name, only_branches=True)
        branch_client: TinyB = ctx.ensure_object(dict)['client']
        if all:
            if 'job' not in response:
                raise click.ClickException(response)
            job_id = response['job']['job_id']
            job_url = response['job']['job_url']
            click.echo(FeedbackManager.info_data_branch_job_url(url=job_url))
            if wait:
                await wait_job(branch_client, job_id, job_url, 'Data branching')
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))


class PlanName(Enum):
    DEV = 'Build'
    PRO = 'Pro'
    ENTERPRISE = 'Enterprise'


def _get_workspace_plan_name(plan):
    if plan == 'dev':
        return PlanName.DEV.value
    if plan == 'pro':
        return PlanName.PRO.value
    if plan == 'enterprise':
        return PlanName.ENTERPRISE.value
    return 'Custom'


def get_format_from_filename_or_url(filename_or_url: str) -> str:
    """
    >>> get_format_from_filename_or_url('wadus_parquet.csv')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_csv.ndjson')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv.json')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet.csv?auth=pepe')
    'csv'
    >>> get_format_from_filename_or_url('wadus_csv.parquet?auth=pepe')
    'parquet'
    >>> get_format_from_filename_or_url('wadus_parquet.ndjson?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus.json?auth=pepe')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_csv_')
    'csv'
    >>> get_format_from_filename_or_url('wadus_json_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_ndjson_')
    'ndjson'
    >>> get_format_from_filename_or_url('wadus_parquet_')
    'parquet'
    >>> get_format_from_filename_or_url('wadus')
    'csv'
    >>> get_format_from_filename_or_url('https://storage.googleapis.com/tinybird-waduscom/stores_stock__v2_1646741850424_final.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=44444444444-compute@developer.gserviceaccount.com/1234/auto/storage/goog4_request&X-Goog-Date=20220308T121750Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=8888888888888888888888888888888888888888888888888888888')
    'csv'
    """
    filename_or_url = filename_or_url.lower()
    if filename_or_url.endswith('json') or filename_or_url.endswith('ndjson'):
        return 'ndjson'
    if filename_or_url.endswith('parquet'):
        return 'parquet'
    if filename_or_url.endswith('csv'):
        return 'csv'
    try:
        parsed = urlparse(filename_or_url)
        if parsed.path.endswith('json') or parsed.path.endswith('ndjson'):
            return 'ndjson'
        if parsed.path.endswith('parquet'):
            return 'parquet'
        if parsed.path.endswith('csv'):
            return 'csv'
    except Exception:
        pass
    if 'csv' in filename_or_url:
        return 'csv'
    if 'json' in filename_or_url:
        return 'ndjson'
    if 'parquet' in filename_or_url:
        return 'parquet'
    return 'csv'


async def push_data(ctx, datasource_name, url, connector, sql, mode='append', sql_condition=None, replace_options=None, ignore_empty=False, concurrency=1):
    if url and type(url) is tuple:
        url = url[0]
    client = ctx.obj['client']

    if connector:
        load_connector_config(ctx, connector, False, check_uninstalled=False)
        if connector not in ctx.obj:
            click.echo(FeedbackManager.error_connector_not_configured(connector=connector))
            return
        else:
            _connector = ctx.obj[connector]
            click.echo(FeedbackManager.info_starting_export_process(connector=connector))
            try:
                url = _connector.export_to_gcs(sql, datasource_name, mode)
            except ConnectorNothingToLoad as e:
                if ignore_empty:
                    click.echo(str(e))
                    return
                else:
                    raise e

    def cb(res):
        if cb.First:
            blocks_to_process = len([x for x in res['block_log'] if x['status'] == 'idle'])
            if blocks_to_process:
                cb.bar = click.progressbar(label=FeedbackManager.info_progress_blocks(), length=blocks_to_process)
                cb.bar.update(0)
                cb.First = False
                cb.blocks_to_process = blocks_to_process
        else:
            done = len([x for x in res['block_log'] if x['status'] == 'done'])
            if done * 2 > cb.blocks_to_process:
                cb.bar.label = FeedbackManager.info_progress_current_blocks()
            cb.bar.update(done - cb.prev_done)
            cb.prev_done = done
    cb.First = True
    cb.prev_done = 0

    click.echo(FeedbackManager.info_starting_import_process())

    if isinstance(url, list):
        urls = url
    else:
        urls = [url]

    async def process_url(datasource_name, url, mode, sql_condition, replace_options):
        parsed = urlparse(url)
        # poor man's format detection
        _format = get_format_from_filename_or_url(url)
        if parsed.scheme in ('http', 'https'):
            res = await client.datasource_create_from_url(datasource_name, url, mode=mode, status_callback=cb, sql_condition=sql_condition, format=_format, replace_options=replace_options)
        else:
            with open(url, mode='rb') as file:
                res = await client.datasource_append_data(datasource_name, file, mode=mode, sql_condition=sql_condition, format=_format, replace_options=replace_options)

        datasource_name = res['datasource']['name']
        try:
            datasource = await client.get_datasource(datasource_name)
        except DoesNotExistException:
            click.echo(FeedbackManager.error_datasource_does_not_exist(datasource=datasource_name))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return

        total_rows = (datasource.get('statistics', {}) or {}).get('row_count', 0)
        appended_rows = 0
        parser = None

        if 'error' in res and res['error']:
            click.echo(FeedbackManager.error_exception(error=res['error']))
        if 'errors' in res and res['errors']:
            click.echo(FeedbackManager.error_exception(error=res['errors']))
        if 'blocks' in res and res['blocks']:
            for block in res['blocks']:
                process_return = block['process_return'][0]
                parser = process_return['parser'] if 'parser' in process_return and process_return['parser'] else parser
                if parser and parser != 'clickhouse':
                    parser = process_return['parser']
                    appended_rows += process_return['lines']

        return parser, total_rows, appended_rows

    async def gather_with_concurrency(n, *tasks):
        semaphore = asyncio.Semaphore(n)

        async def sem_task(task):
            async with semaphore:
                return await task

        return await asyncio.gather(*(sem_task(task) for task in tasks))

    try:
        tasks = [process_url(datasource_name, url, mode, sql_condition, replace_options) for url in urls]
        output = await gather_with_concurrency(concurrency, *tasks)
        parser, total_rows, appended_rows = list(output)[-1]
    except OperationCanNotBePerformed as e:
        click.echo(FeedbackManager.error_operation_can_not_be_performed(error=e))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
        sys.exit(1)
    else:
        click.echo(FeedbackManager.success_progress_blocks())
        if mode == 'append':
            if parser != 'clickhouse':
                click.echo(FeedbackManager.success_appended_rows(appended_rows=appended_rows))

        click.echo(FeedbackManager.success_total_rows(datasource=datasource_name, total_rows=total_rows))

        if mode == 'replace':
            click.echo(FeedbackManager.success_replaced_datasource(datasource=datasource_name))
        else:
            click.echo(FeedbackManager.success_appended_datasource(datasource=datasource_name))
        click.echo(FeedbackManager.info_data_pushed(datasource=datasource_name))
    finally:
        try:
            for url in urls:
                _connector.clean(urlparse(url).path.split('/')[-1])
        except Exception:
            pass


# eval "$(_TB_COMPLETE=source_bash tb)"
def autocomplete_topics(ctx: Context, args, incomplete):
    try:
        config = async_to_sync(get_config)(None, None)
        ctx.ensure_object(dict)['config'] = config
        client = create_tb_client(ctx)
        topics = async_to_sync(client.kafka_list_topics)(args[2])
        return [t for t in topics if incomplete in t]
    except Exception:
        return []


def validate_datasource_name(name):
    if not isinstance(name, str) or str == "":
        raise click.ClickException(FeedbackManager.error_datasource_name())


def validate_connection_id(connection_id):
    if not isinstance(connection_id, str) or str == "":
        raise click.ClickException(FeedbackManager.error_datasource_connection_id())


def validate_kafka_topic(topic):
    if not isinstance(topic, str):
        raise click.ClickException(FeedbackManager.error_kafka_topic())


def validate_kafka_group(group):
    if not isinstance(group, str):
        raise click.ClickException(FeedbackManager.error_kafka_group())


def validate_kafka_auto_offset_reset(auto_offset_reset):
    valid_values = {"latest", "earliest", "none"}
    if not (auto_offset_reset in valid_values):
        raise click.ClickException(FeedbackManager.error_kafka_auto_offset_reset())


def validate_kafka_schema_registry_url(schema_registry_url):
    if not is_url_valid(schema_registry_url):
        raise click.ClickException(FeedbackManager.error_kafka_registry())


def is_url_valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def validate_kafka_bootstrap_servers(host_and_port):
    if not isinstance(host_and_port, str):
        raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server())
    parts = host_and_port.split(":")
    if len(parts) > 2:
        raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server())
    host = parts[0]
    port = parts[1] if len(parts) == 2 else "9092"
    try:
        port = int(port)
    except Exception:
        raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server())
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        try:
            sock.settimeout(3)
            sock.connect((host, port))
        except socket.timeout:
            raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server_conn_timeout())
        except Exception:
            raise click.ClickException(FeedbackManager.error_kafka_bootstrap_server_conn())


def validate_kafka_key(s):
    if not isinstance(s, str):
        raise click.ClickException("Key format is not correct, it should be a string")


def validate_kafka_secret(s):
    if not isinstance(s, str):
        raise click.ClickException("Password format is not correct, it should be a string")


def _get_setting_value(connection, setting, sensitive_settings):
    if setting in sensitive_settings:
        return '*****'
    return connection.get(setting, '')


async def switch_workspace(ctx, workspace_name_or_id, only_branches=False):
    config_file = Path(getcwd()) / ".tinyb"
    config = {}
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    try:
        if 'id' not in config:
            config = await _get_config(config['host'], config['token'], load_tb_file=False)
        else:
            with open(config_file) as file:
                config = json.loads(file.read())

        if only_branches:
            response = await client.user_workspace_branches()
        else:
            response = await client.user_workspaces()

        workspaces = response['workspaces']
        workspace = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)

        if not workspace:
            if only_branches:
                click.echo(FeedbackManager.error_branch(branch=workspace_name_or_id))
            else:
                click.echo(FeedbackManager.error_workspace(workspace=workspace_name_or_id))
            return

        client = _get_tb_client(workspace['token'], config['host'])

        config['id'] = workspace['id']
        config['name'] = workspace['name']
        config['token'] = workspace['token']
        host = config['host']

        tokens = config.get('tokens', {})
        tokens[host] = config['token']

        config['tokens'] = tokens

        ctx.ensure_object(dict)['client'] = client
        ctx.ensure_object(dict)['config'] = config

        await write_config(config)
        click.echo(FeedbackManager.success_now_using_config(name=config['name'], id=config['id']))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


async def print_current_workspace(ctx):
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.user_workspaces_and_branches()

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []

    for workspace in response['workspaces']:
        if config['id'] == workspace['id']:
            if workspace['is_branch']:
                click.echo(FeedbackManager.info_current_branch())
            else:
                click.echo(FeedbackManager.info_current_workspace())
            table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), True])
            break

    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))
