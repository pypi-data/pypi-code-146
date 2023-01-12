"""
Datafile is like a Dockerfile but to describe ETL processes
"""
import logging
import asyncio
import textwrap
import json
from operator import itemgetter
import shlex
import sys
import re
from typing import Any, Dict, Iterable, List, Optional
import difflib
import click
import glob
import pprint
import requests
import unittest
from string import Template
from toposort import toposort
from pathlib import Path
import urllib.parse
from urllib.parse import urlencode, urlparse, parse_qs
from collections import namedtuple
from io import StringIO
import os.path
from copy import deepcopy
import traceback

from .sql import parse_table_structure, schema_to_sql_columns
from .client import JobException, TinyB, DoesNotExistException
from .sql_template import render_sql_template, get_used_tables_in_template
from tinybird.sql_template_fmt import format_sql_template
from .feedback_manager import FeedbackManager
from .ch_utils.engine import ENABLED_ENGINES
from tinybird.syncasync import sync_to_async
from statistics import mean, median
import math
from humanfriendly.tables import format_pretty_table
from humanfriendly import format_size

INTERNAL_TABLES = ('datasources_ops_log', 'snapshot_views', 'pipe_stats', 'pipe_stats_rt', 'block_log',
                   'data_connectors_log', 'kafka_ops_log', 'datasources_storage')

requests_get = sync_to_async(requests.get, thread_sensitive=False)
requests_delete = sync_to_async(requests.delete, thread_sensitive=False)

pp = pprint.PrettyPrinter()


class AlreadyExistsException(click.ClickException):
    pass


class ParseException(Exception):
    def __init__(self, err, lineno=-1):
        self.lineno = lineno
        super().__init__(err)


class ValidationException(Exception):
    def __init__(self, err, lineno=-1):
        self.lineno = lineno
        super().__init__(err)


def sizeof_fmt(num, suffix='b'):
    """Readable file size
    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def is_shared_datasource(ds_name):
    """just looking for a dot in the name is fine, dot are not allowed in regular datasources"""
    return '.' in ds_name


class Datafile:

    def __init__(self):
        self.maintainer = None
        self.sources = []
        self.nodes = []
        self.tokens = []
        self.keys = []
        self.version = None
        self.description = None
        self.raw = None
        self.includes = {}

    def validate(self):
        for x in self.nodes:
            if not x['name'].strip():
                raise ValidationException("invalid node name, can't be empty")
            if 'sql' not in x:
                raise ValidationException(
                    "node %s must have a SQL query" % x['name'])
        if self.version is not None and (not isinstance(self.version, int) or self.version < 0):
            raise ValidationException("version must be a positive integer")

    def is_equal(self, other):
        if len(self.nodes) != len(other.nodes):
            return False

        for i, _ in enumerate(self.nodes):
            if self.nodes[i] != other.nodes[i]:
                return False

        return True


def parse_datasource(filename):
    with open(filename) as file:
        s = file.read()
    basepath = os.path.dirname(filename)

    try:
        doc = parse(s, 'default', basepath)
    except ParseException as e:
        raise click.ClickException(FeedbackManager.error_parsing_file(filename=filename, lineno=e.lineno, error=e)) from None

    if len(doc.nodes) > 1:
        raise ValueError(f"{filename}: datasources can't have more than one node")

    return doc


def parse_pipe(filename):
    with open(filename) as file:
        s = file.read()
    basepath = os.path.dirname(filename)

    try:
        doc = parse(s, basepath=basepath)
        for node in doc.nodes:
            sql = node.get('sql', '')
            if sql.strip()[0] == '%':
                sql, _ = render_sql_template(sql[1:], test_mode=True)
            # it'll fail with a ModuleNotFoundError when the toolset is not available but it returns the parsed doc
            from tinybird.sql_toolset import format_sql
            format_sql(sql)
    except ParseException as e:
        raise click.ClickException(FeedbackManager.error_parsing_file(filename=filename, lineno=e.lineno, error=e))
    except ValueError as e:
        raise click.ClickException(FeedbackManager.error_parsing_file(filename=filename, lineno='', error=e))
    except ModuleNotFoundError:
        pass

    return doc


def parse(s, default_node=None, basepath='.'):  # noqa: C901
    """
    Parses `s` string into a document
    >>> d = parse("FROM SCRATCH\\nSOURCE 'https://example.com'\\n#this is a comment\\nMAINTAINER 'rambo' #this is me\\nNODE \\"test_01\\"\\n    DESCRIPTION this is a node that does whatever\\nSQL >\\n\\n        SELECT * from test_00\\n\\n\\nNODE \\"test_02\\"\\n    DESCRIPTION this is a node that does whatever\\nSQL >\\n\\n    SELECT * from test_01\\n    WHERE a > 1\\n    GROUP by a\\n")
    >>> d.maintainer
    'rambo'
    >>> d.sources
    ['https://example.com']
    >>> len(d.nodes)
    2
    >>> d.nodes[0]
    {'name': 'test_01', 'description': 'this is a node that does whatever', 'sql': 'SELECT * from test_00'}
    >>> d.nodes[1]
    {'name': 'test_02', 'description': 'this is a node that does whatever', 'sql': 'SELECT * from test_01\\nWHERE a > 1\\nGROUP by a'}
    """
    lines = list(StringIO(s, newline=None))

    doc = Datafile()
    doc.raw = list(StringIO(s, newline=None))

    parser_state = namedtuple(
        'ParserState',
        ['multiline', 'current_node', 'command', 'multiline_string', 'is_sql'])

    parser_state.multiline = False
    parser_state.current_node = False

    def _unquote(x):
        QUOTES = ('"', "'")
        if x[0] in QUOTES and x[-1] in QUOTES:
            x = x[1:-1]
        return x

    def assign(attr):
        def _fn(x, **kwargs):
            setattr(doc, attr, _unquote(x))
        return _fn

    def schema(*args, **kwargs):
        s = _unquote(''.join(args))
        try:
            sh = parse_table_structure(s)
        except Exception as e:
            raise ParseException(FeedbackManager.error_parsing_schema(line=kwargs['lineno'], error=e))
        parser_state.current_node['schema'] = ','.join(
            schema_to_sql_columns(sh))
        parser_state.current_node['columns'] = sh

    def eval_var(s):
        # replace ENV variables
        # it's probably a bad idea to allow to get any env var
        return Template(s).safe_substitute(os.environ)

    def assign_var(v):
        def _f(*args, **kwargs):
            s = _unquote((' '.join(args)).strip())
            parser_state.current_node[v.lower()] = eval_var(s)
        return _f

    def sources(x, **kwargs):
        doc.sources.append(_unquote(x))

    def node(*args, **kwargs):
        node = {
            'name': eval_var(_unquote(args[0]))
        }
        doc.nodes.append(node)
        parser_state.current_node = node

    def description(*args, **kwargs):
        description = (' '.join(args)).strip()

        if parser_state.current_node:
            parser_state.current_node['description'] = description
        else:
            doc.description = description

    def sql(sql, **kwargs):
        if not parser_state.current_node:
            raise ParseException("SQL must be called after a NODE command")
        parser_state.current_node['sql'] = textwrap.dedent(sql).rstrip() if '%' not in sql.strip()[0] else sql.strip()

    def assign_node_var(v):
        def _f(*args, **kwargs):
            if not parser_state.current_node:
                raise ParseException("%s must be called after a NODE command" % v)
            return assign_var(v)(*args, **kwargs)
        return _f

    def add_token(*args, **kwargs):  # token_name, permissions):
        if len(args) < 2:
            raise ParseException('TOKEN gets two params, token name and permissions e.g TOKEN "read api token" READ')
        doc.tokens.append({
            'token_name': _unquote(args[0]),
            'permissions': args[1]
        })

    def add_key(*args, **kwargs):  # token_name, permissions):
        if len(args) < 1:
            raise ParseException('KEY gets one params')
        doc.keys.append({
            'column': _unquote(args[0])
        })

    def test(*args, **kwargs):
        print("test", args, kwargs)

    def include(*args, **kwargs):
        f = _unquote(args[0])
        f = eval_var(f)
        attrs = dict(_unquote(x).split('=', 1) for x in args[1:])
        nonlocal lines
        lineno = kwargs['lineno']
        n = lineno
        try:
            while True:
                n += 1
                if len(lines) <= n:
                    break
                if 'NODE' in lines[n]:
                    doc.includes[args[0]] = lines[n]
                    break
            if args[0] not in doc.includes:
                doc.includes[args[0]] = ''
        except Exception:
            pass
        # be sure to replace the include line
        p = Path(basepath)
        with open(p / f) as file:
            try:
                ll = list(StringIO(file.read(), newline=None))
                node_line = [line for line in ll if 'NODE' in line]
                if node_line and doc.includes[args[0]]:
                    doc.includes[node_line[0].split('NODE')[-1].split('\n')[0].strip()] = ''
            except Exception:
                pass
            finally:
                file.seek(0)
            lines[lineno:lineno + 1] = [''] + list(StringIO(Template(file.read()).safe_substitute(attrs), newline=None))

    def version(*args, **kwargs):
        if len(args) < 1:
            raise ParseException('VERSION gets one positive integer param')
        try:
            version = int(args[0])
            if version < 0:
                raise ValidationException('version must be a positive integer e.g VERSION 2')
            doc.version = version
        except ValueError:
            raise ValidationException('version must be a positive integer e.g VERSION 2')

    def __init_engine(v):
        if not parser_state.current_node:
            raise Exception(f"{v} must be called after a NODE command")
        if 'engine' not in parser_state.current_node:
            parser_state.current_node['engine'] = {'type': None, 'args': []}

    def set_engine(*args, **kwargs):
        __init_engine('ENGINE')
        engine_type = _unquote((' '.join(args)).strip())
        parser_state.current_node['engine']['type'] = engine_type

    def add_engine_var(v):
        def _f(*args, **kwargs):
            __init_engine(f"ENGINE_{v}".upper())
            engine_arg = _unquote((' '.join(args)).strip())
            parser_state.current_node['engine']['args'].append((v, engine_arg))
        return _f

    cmds = {
        'from': assign('from'),
        'source': sources,
        'maintainer': assign('maintainer'),
        'schema': schema,
        'engine': set_engine,
        'partition_key': assign_var('partition_key'),
        'sorting_key': assign_var('sorting_key'),
        'primary_key': assign_var('primary_key'),
        'sampling_key': assign_var('sampling_key'),
        'ttl': assign_var('ttl'),
        'settings': assign_var('settings'),
        'node': node,
        'description': description,
        'type': assign_node_var('type'),
        'datasource': assign_node_var('datasource'),
        'tags': assign_node_var('tags'),
        'token': add_token,
        'key': add_key,
        'test': test,
        'include': include,
        'sql': sql,
        'version': version,
        'kafka_connection_name': assign_var('kafka_connection_name'),
        'kafka_topic': assign_var('kafka_topic'),
        'kafka_group_id': assign_var('kafka_group_id'),
        'kafka_bootstrap_servers': assign_var('kafka_bootstrap_servers'),
        'kafka_key': assign_var('kafka_key'),
        'kafka_secret': assign_var('kafka_secret'),
        'kafka_schema_registry_url': assign_var('kafka_schema_registry_url'),
        'kafka_target_partitions': assign_var('kafka_target_partitions'),
        'kafka_auto_offset_reset': assign_var('kafka_auto_offset_reset'),
        'kafka_store_raw_value': assign_var('kafka_store_raw_value'),
        'kafka_key_avro_deserialization': assign_var('kafka_key_avro_deserialization'),
    }

    engine_vars = set()

    for _engine, (params, options) in ENABLED_ENGINES:
        for p in params:
            engine_vars.add(p.name)
        for o in options:
            engine_vars.add(o.name)
    for v in engine_vars:
        cmds[f"engine_{v}"] = add_engine_var(v)

    if default_node:
        node(default_node)

    lineno = 0
    try:
        while lineno < len(lines):
            line = lines[lineno]
            try:
                sa = shlex.shlex(line)
                sa.whitespace_split = True
                lexer = list(sa)
            except ValueError:
                sa = shlex.shlex(shlex.quote(line))
                sa.whitespace_split = True
                lexer = list(sa)
            if lexer:
                cmd, args = lexer[0], lexer[1:]

                if parser_state.multiline and cmd.lower() in cmds and not (line.startswith(' ') or line.startswith('\t') or line.lower().startswith('from')):
                    parser_state.multiline = False
                    cmds[parser_state.command](parser_state.multiline_string, lineno=lineno)

                if not parser_state.multiline:
                    if len(args) >= 1 and args[0] == ">":
                        parser_state.multiline = True
                        parser_state.command = cmd.lower()
                        parser_state.multiline_string = ''
                    else:
                        if cmd.lower() in cmds:
                            cmds[cmd.lower()](*args, lineno=lineno)
                        else:
                            raise click.ClickException(FeedbackManager.error_option(option=cmd.upper()))
                else:
                    parser_state.multiline_string += line
            lineno += 1
        # close final state
        if parser_state.multiline:
            cmds[parser_state.command](parser_state.multiline_string, lineno=lineno)
    except ParseException as e:
        raise ParseException(str(e), lineno=lineno)
    except ValidationException as e:
        raise ValidationException(str(e), lineno=lineno)
    except IndexError as e:
        raise ValidationException(f'Validation error, found {line} in line {str(lineno)}: {str(e)}', lineno=lineno)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise ParseException(f"Unexpected error: {e}", lineno=lineno)

    return doc


def generate_resource_for_key(key, name, schema, version, res_name):
    resources = []
    # datasource
    ds_name = f"{name}_join_by_{key}{version}"
    params = {
        "name": ds_name,
        "schema": schema,
        'engine': 'Join',
        'engine_join_strictness': 'ANY',
        'engine_join_type': 'LEFT',
        'engine_key_columns': key,
    }
    resources.append({
        'resource_name': f'{name}_join_by_{key}',
        'resource': 'datasources',
        'params': params,
        'filename': f"{params['name']}.datasource"
    })
    resources.append({
        'resource_name': f'{name}_join_by_{key}_pipe',
        'resource': 'pipes',
        'filename': f"{params['name']}.pipe",
        "name": f"{name}_join_by_{key}_pipe{version}",
        "schema": schema,
        'nodes': [{
            'sql': f"select * from {name}{version}",
            'params': {
                "name": f"{name}_join_by_{key}_view",
                'type': 'materialized',
                'datasource': ds_name
            }
        }],
        'deps': [res_name],  # [ds_name],
        'tokens': []
    })
    return resources


async def process_file(filename, tb_client, dir_path, tag='', resource_versions=None, verbose=False, skip_connectors=False, workspace_map={}, workspace_lib_paths=None):  # noqa: C901 B006

    if resource_versions is None:
        resource_versions = {}
    resource_versions_string = {k: f'__v{v}' for k, v in resource_versions.items() if v >= 0}

    def get_engine_params(node):
        params = {}

        if 'engine' in node:
            engine = node['engine']['type']
            params['engine'] = engine
            args = node['engine']['args']
            for (k, v) in args:
                params[f'engine_{k}'] = v
        return params

    async def get_kafka_params(node):
        params = {
            key: value
            for key, value in node.items() if key.startswith('kafka')
        }

        if not skip_connectors:
            try:
                connector_params = {
                    'kafka_bootstrap_servers': params.get('kafka_bootstrap_servers', None),
                    'kafka_key': params.get('kafka_key', None),
                    'kafka_secret': params.get('kafka_secret', None),
                    'kafka_connection_name': params.get('kafka_connection_name', None),
                    'kafka_auto_offset_reset': params.get('kafka_auto_offset_reset', None),
                    'kafka_schema_registry_url': params.get('kafka_schema_registry_url', None)
                }
                connector = await tb_client.get_connection(**connector_params)

                if not connector:
                    click.echo(FeedbackManager.success_connection_creating(connection_name=params['kafka_connection_name']))
                    connector = await tb_client.connection_create_kafka(**connector_params)
            except Exception as e:
                raise click.ClickException(
                    FeedbackManager.error_connection_create(connection_name=params['kafka_connection_name'], error=str(e)))

            click.echo(FeedbackManager.success_connection_using(connection_name=connector['name']))

            params.update({
                'connector': connector['id'],
                'service': 'kafka',
            })

        return params

    if '.datasource' in filename:
        doc = parse_datasource(filename)
        node = doc.nodes[0]
        deps = []
        # reemplace tables on materialized columns
        columns = parse_table_structure(node['schema'])

        _format = 'csv'
        for x in columns:
            if x['default_value'] and x['default_value'].lower().startswith('materialized'):
                # turn expression to a select query to sql_get_used_tables can get the used tables
                q = 'select ' + x['default_value'][len('materialized'):]
                tables = await tb_client.sql_get_used_tables(q)
                # materialized columns expressions could have joins so we need to add them as a dep
                deps += tables
                # generate replacements and replace the query
                replacements = {t: t + resource_versions_string.get(t, '') for t in tables}

                replaced_results = await tb_client.replace_tables(q, replacements)
                x['default_value'] = replaced_results.replace('SELECT', 'materialized', 1)
            if x.get('jsonpath', None):
                _format = 'ndjson'

        schema = ','.join(schema_to_sql_columns(columns))

        name = os.path.basename(filename).rsplit('.', 1)[0]

        if workspace_lib_paths:
            for wk_name, wk_path in workspace_lib_paths:
                try:
                    Path(filename).relative_to(wk_path)
                    name = f'{workspace_map.get(wk_name, wk_name)}.{name}'
                except ValueError:
                    # the path was not relative, not inside workspace
                    pass
        #
        res_name = name
        if tag and not is_shared_datasource(name):
            name = f'{tag}__{name}'

        version = (f'__v{doc.version}' if doc.version is not None else '')

        def append_version_to_name(name, version):
            if version != '':
                name = name.replace(".", "_")
                return name + version
            return name

        description = node.get('description', '')
        params = {
            "name": append_version_to_name(name, version),
            "description": description,
            "schema": schema,
            "format": _format
        }

        params.update(get_engine_params(node))

        if 'kafka_connection_name' in node:
            kafka_params = await get_kafka_params(node)
            params.update(kafka_params)
            del params["engine"]
            del params["format"]

        if 'tags' in node:
            tags = {k: v[0]
                    for k, v in urllib.parse.parse_qs(node['tags']).items()}
            params.update(tags)

        resources = []

        resources.append({
            'resource': 'datasources',
            'resource_name': name,
            "version": doc.version,
            'params': params,
            'filename': filename,
            'keys': doc.keys,
            'deps': deps,
            'tokens': doc.tokens
        })

        # generate extra resources in case of the key
        if doc.keys:
            for k in doc.keys:
                resources += generate_resource_for_key(
                    k['column'],
                    name,
                    params['schema'],
                    version,
                    res_name
                )
                # set derived resources version the same the parent
                for x in resources:
                    x['version'] = doc.version

        return resources

    elif '.pipe' in filename:
        doc = parse_pipe(filename)
        version = (f'__v{doc.version}' if doc.version is not None else '')
        name = os.path.basename(filename).split('.')[0]
        description = doc.description if doc.description is not None else ''

        if tag and not is_shared_datasource(name):
            name = f'{tag}__{name}'

        deps = []
        nodes = []

        for node in doc.nodes:
            sql = node['sql']
            params = {
                'name': node['name'],
                'type': node.get('type', 'standard'),
                'description': node.get('description', ''),
            }
            if node.get('type', '').lower() == 'materialized':
                params.update({
                    'type': 'materialized',
                })

            sql = sql.strip()
            is_template = False
            if sql[0] == '%':
                try:
                    sql_rendered, _ = render_sql_template(sql[1:], test_mode=True)
                except Exception as e:
                    raise click.ClickException(FeedbackManager.error_parsing_node(
                        node=node['name'], pipe=name, error=str(e)))
                is_template = True
            else:
                sql_rendered = sql

            try:
                dependencies = await tb_client.sql_get_used_tables(sql_rendered, raising=True)
                deps += [t for t in dependencies if t not in [n['name'] for n in doc.nodes]]

            except Exception as e:
                raise click.ClickException(FeedbackManager.error_parsing_node(
                    node=node['name'], pipe=name, error=str(e)))

            if is_template:
                deps += get_used_tables_in_template(sql[1:])

            tag_ = ''
            if tag:
                tag_ = f'{tag}__'

            if ('engine' in node) and 'datasource' not in node:
                raise ValueError('Defining ENGINE options in a node requires a DATASOURCE')

            if 'datasource' in node:
                params['datasource'] = tag_ + node['datasource'] + \
                    resource_versions_string.get(tag_ + node['datasource'], '')
                deps += [node['datasource']]

            params.update(get_engine_params(node))

            def create_replacement_for_resource(tag, name):
                for old_ws, new_ws in workspace_map.items():
                    name = name.replace(f'{old_ws}.', f'{new_ws}.')
                if tag != '' and not is_shared_datasource(name):
                    name = tag + name
                return name + resource_versions_string.get(name, '')

            replacements = {x: create_replacement_for_resource(tag_, x) for x in deps if x not in [
                n['name'] for n in doc.nodes]}

            # FIXME: Ideally we should use await tb_client.replace_tables(sql, replacements)
            for old, new in replacements.items():
                sql = re.sub('([\t \\n\']+|^)' + old + '([\t \\n\'\\)]+|$)', "\\1" + new + "\\2", sql)

            if 'tags' in node:
                tags = {k: v[0]
                        for k, v in urllib.parse.parse_qs(node['tags']).items()}
                params.update(tags)

            nodes.append({
                'sql': sql,
                'params': params
            })

        return [{
            'resource': 'pipes',
            'resource_name': name,
            "version": doc.version,
            'filename': filename,
            'name': name + version,
            'nodes': nodes,
            'deps': [x for x in set(deps)],
            'tokens': doc.tokens,
            'description': description
        }]
    else:
        raise Exception(FeedbackManager.error_file_extension(filename=filename))


def full_path_by_name(folder, name, workspace_lib_paths=None):
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return f / ds
    if os.path.isfile(f / 'datasources' / ds):
        return f / 'datasources' / ds

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return f / pipe

    if os.path.isfile(f / 'endpoints' / pipe):
        return f / 'endpoints' / pipe

    if os.path.isfile(f / 'pipes' / pipe):
        return f / 'pipes' / pipe

    if workspace_lib_paths:
        for wk_name, wk_path in workspace_lib_paths:
            if name.startswith(f'{wk_name}.'):
                r = full_path_by_name(wk_path, name.replace(f'{wk_name}.', ''))
                if r:
                    return r


def find_file_by_name(folder, name, verbose=False, is_raw=False, workspace_lib_paths=None, resource=None, deps_tag=''):
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return ds, None
    if os.path.isfile(f / 'datasources' / ds):
        return ds, None

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return pipe, None

    if os.path.isfile(f / 'endpoints' / pipe):
        return pipe, None

    if os.path.isfile(f / 'pipes' / pipe):
        return pipe, None

    # look for the file in subdirectories if it's not found in datasources folder
    if workspace_lib_paths:
        _resource = None
        for wk_name, wk_path in workspace_lib_paths:
            file = None
            if name.startswith(f'{wk_name}.'):
                file, _resource = find_file_by_name(wk_path, name.replace(f'{wk_name}.', ''), verbose, is_raw, resource=resource, deps_tag=deps_tag)
            if file:
                return file, _resource

    if not is_raw:
        f, raw = find_file_by_name(folder, get_dep_from_raw_tables(name), verbose=verbose, is_raw=True, workspace_lib_paths=workspace_lib_paths, resource=resource, deps_tag=deps_tag)
        return f, raw

    # materialized node with DATASOURCE definition
    if resource and 'nodes' in resource:
        for node in resource['nodes']:
            params = node.get('params', {})
            if params.get('type', None) == 'materialized' and params.get('engine', None) and params.get('datasource', None):
                pipe = resource['resource_name'].replace(deps_tag, '') + '.pipe'
                pipe_file_exists = (os.path.isfile(os.path.join(folder, pipe)) or os.path.isfile(f / 'endpoints' / pipe) or os.path.isfile(f / 'pipes' / pipe))
                is_target_datasource = (params['datasource'] == name)
                if pipe_file_exists and is_target_datasource:
                    return pipe, {'resource_name': params.get('datasource')}

    if verbose:
        click.echo(FeedbackManager.warning_file_not_found_inside(name=name, folder=folder))

    return None, None


def drop_token(url: str) -> str:
    """
    drops token param from the url query string
    >>> drop_token('https://api.tinybird.co/v0/pipes/aaa.json?token=abcd&a=1')
    'https://api.tinybird.co/v0/pipes/aaa.json?a=1'
    >>> drop_token('https://api.tinybird.co/v0/pipes/aaa.json?a=1')
    'https://api.tinybird.co/v0/pipes/aaa.json?a=1'
    """
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs_simplify = {k: v[0] for k, v in qs.items()}  # change several arguments to single one
    if 'token' in qs_simplify:
        del qs_simplify['token']
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(qs_simplify)}"


class PipeChecker(unittest.TestCase):

    current_response_time: float = 0
    checker_response_time: float = 0

    current_read_bytes: int = 0
    checker_read_bytes: int = 0

    def __init__(
        self,
        current_pipe_url: str,
        pipe_name: str,
        checker_pipe_name: str,
        token: str,
        only_response_times: bool,
        ignore_order: bool,
        validate_processed_bytes: bool,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.current_pipe_url = current_pipe_url.replace('.ndjson', '.json').replace('.csv', '.json').replace('.parquet', '.json')
        self.current_pipe_url = drop_token(self.current_pipe_url)
        self.current_pipe_url += ('&' if '?' in self.current_pipe_url else '?') + "pipe_checker=true"
        self.checker_pipe_name = checker_pipe_name
        self.pipe_name = pipe_name
        self.token = token
        self.only_response_times = only_response_times
        self.ignore_order = ignore_order
        self.validate_processed_bytes = validate_processed_bytes
        parsed = urlparse(self.current_pipe_url)
        self.qs = parse_qs(parsed.query)
        self.checker_pipe_url = f"{parsed.scheme}://{parsed.netloc}/v0/pipes/{self.checker_pipe_name}.json?{parsed.query}"

    def __str__(self):
        return f"current {self.current_pipe_url}\n    new {self.checker_pipe_url}"

    def diff(self, a: Dict[str, Any], b: Dict[str, Any]) -> str:
        a_properties = list(map(lambda x: f"{x}:{a[x]}\n", a.keys()))
        b_properties = list(map(lambda x: f"{x}:{b[x]}\n", b.keys()))

        return ''.join(difflib.context_diff(a_properties, b_properties, self.pipe_name, self.checker_pipe_name))

    def runTest(self):
        if 'debug' in self.qs or ('from' in self.qs and self.qs['from'] == 'ui'):
            self.skipTest('found debug param')
        headers = {'Authorization': f'Bearer {self.token}'}

        current_r = requests.get(self.current_pipe_url, headers=headers)
        checker_r = requests.get(self.checker_pipe_url, headers=headers)
        try:
            self.current_response_time = current_r.elapsed.total_seconds()
            self.checker_response_time = checker_r.elapsed.total_seconds()
        except Exception:
            pass

        current_response: Dict[str, Any] = current_r.json()
        checker_response: Dict[str, Any] = checker_r.json()

        current_data: List[Dict[str, Any]] = current_response.get('data', [])
        checker_data: List[Dict[str, Any]] = checker_response.get('data', [])

        self.current_read_bytes = current_response.get('statistics', {}).get('bytes_read', 0)
        self.checker_read_bytes = checker_response.get('statistics', {}).get('bytes_read', 0)

        error_check_fixtures_data: Optional[str] = checker_response.get('error', None)
        self.assertIsNone(error_check_fixtures_data, 'You are trying to push a pipe with errors, please check the output or run with --no-check')

        increase_response_time = (checker_r.elapsed.total_seconds() - current_r.elapsed.total_seconds()) / current_r.elapsed.total_seconds()
        if self.only_response_times:
            self.assertLess(
                increase_response_time,
                0.25,
                msg=f"response time has increased {round(increase_response_time * 100)}%"
            )
            return

        self.assertEqual(len(current_data), len(checker_data), "Number of elements does not match")

        if self.validate_processed_bytes:
            increase_read_bytes = (self.checker_read_bytes - self.current_read_bytes) / self.current_read_bytes
            self.assertLess(
                round(increase_read_bytes, 2),
                0.25,
                msg=f"The number of processed bytes has increased {round(increase_read_bytes * 100)}%"
            )

        if self.ignore_order:
            current_data = sorted(
                current_data,
                key=itemgetter(*[k for k in current_data[0].keys()])
            ) if len(current_data) > 0 else current_data
            checker_data = sorted(
                checker_data,
                key=itemgetter(*[k for k in checker_data[0].keys()])
            ) if len(checker_data) > 0 else checker_data

        for _, (current_data_e, check_fixtures_data_e) in enumerate(zip(current_data, checker_data)):
            self.assertEqual(list(current_data_e.keys()),
                             list(check_fixtures_data_e.keys()))
            for x in current_data_e.keys():
                if type(current_data_e[x]) == float:
                    d = abs(current_data_e[x] - check_fixtures_data_e[x])
                    self.assertLessEqual(
                        d / current_data_e[x],
                        0.01,
                        f"key {x}. old value: {current_data_e[x]}, new value {check_fixtures_data_e[x]}\n{self.diff(current_data_e, check_fixtures_data_e)}")
                elif not isinstance(current_data_e[x], (str, bytes)) and isinstance(current_data_e[x], Iterable) and self.ignore_order:
                    def flatten(items):
                        """Yield items from any nested iterable; see Reference."""
                        output = []
                        for x in items:
                            if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
                                output.extend(flatten(x))
                            else:
                                output.append(x)
                        return output

                    self.assertEqual(
                        flatten(current_data_e[x]).sort(),
                        flatten(check_fixtures_data_e[x]).sort(),
                        '\n' + self.diff(current_data_e, check_fixtures_data_e))
                else:
                    self.assertEqual(
                        current_data_e[x],
                        check_fixtures_data_e[x],
                        '\n' + self.diff(current_data_e, check_fixtures_data_e))


async def check_pipe(
    pipe,
    host: str,
    token: str,
    populate: bool,
    cl: TinyB,
    limit: int = 0,
    sample_by_params: int = 0,
    only_response_times=False,
    matches: Optional[List[str]] = None,
    failfast: bool = False,
    validate_processed_bytes: bool = False,
    ignore_order: bool = False
):
    checker_pipe = deepcopy(pipe)
    checker_pipe['name'] = f"{checker_pipe['name']}__checker"

    # In case of doing --force for a materialized view, checker is being created as standard pipe
    for node in checker_pipe['nodes']:
        node['params']['type'] = 'standard'

    if populate:
        raise Exception(FeedbackManager.error_check_pipes_populate())

    headers = {'Authorization': f'Bearer {token}'}
    sql_for_coverage = f"""
                SELECT extractURLParameterNames(assumeNotNull(url)) as params, groupArraySample({sample_by_params if sample_by_params > 0 else 1})(url) as endpoint_url
                FROM tinybird.pipe_stats_rt
                WHERE
                    url like '%/{pipe['name']}.%'
                    AND url IS NOT NULL
                    AND extractURLParameter(assumeNotNull(url), 'from') <> 'ui'
                    AND extractURLParameter(assumeNotNull(url), 'pipe_checker') <> 'true'
                    AND extractURLParameter(assumeNotNull(url), 'debug') <> 'query'
                    { " AND " + " AND ".join([f"has(params, '{match}')" for match in matches])  if matches and len(matches) > 0 else ''}
                GROUP BY params
                FORMAT JSON
            """
    sql_latest_requests = f"""
                SELECT groupArray(*) as endpoint_url
                FROM (
                    WITH extractURLParameterNames(assumeNotNull(url)) as params
                    SELECT distinct(url)
                    FROM tinybird.pipe_stats_rt
                    WHERE
                        url like '%/{pipe['name']}.%'
                        AND url is not null
                        AND extractURLParameter(assumeNotNull(url), 'from') <> 'ui'
                        AND extractURLParameter(assumeNotNull(url), 'pipe_checker') <> 'true'
                        AND extractURLParameter(assumeNotNull(url), 'debug') <> 'query'
                        { " AND " + " AND ".join([f"has(params, '{match}')" for match in matches])  if matches and len(matches) > 0 else ''}
                    LIMIT {limit}
                )
                FORMAT JSON
            """
    params = {'q': sql_for_coverage if limit == 0 and sample_by_params > 0 else sql_latest_requests}
    r: requests.Response = await requests_get(f"{host}/v0/sql?{urlencode(params)}", headers=headers)

    # If we get a timeout, fallback to just the last requests
    if not r or r.status_code == 408:
        params = {'q': sql_latest_requests}
        r = await requests_get(f"{host}/v0/sql?{urlencode(params)}", headers=headers)

    if not r or r.status_code != 200:
        raise Exception(FeedbackManager.error_check_pipes_api(pipe=pipe['name']))

    pipe_top_requests: List[Dict[str, str]] = []
    for x in r.json().get('data', []):
        pipe_top_requests += [{'endpoint_url': f"{host}{request}"} for request in x['endpoint_url']]

    # Let's query if there are no results from tinybird.pipe_stats_rt
    if not pipe_top_requests:
        r = await requests_get(f"{host}/v0/pipes/{pipe['name']}/requests", headers=headers)
        if r.status_code != 200:
            raise Exception(FeedbackManager.error_check_pipes_api(pipe=pipe['name']))
        pipe_top_requests = r.json().get('requests', {}).get('top', [])
        if matches:
            requests_filter = []
            for request in pipe_top_requests:
                if all([request['endpoint_url'].find(match) != -1 for match in matches]):
                    requests_filter.append(request)
            pipe_top_requests = requests_filter

        pipe_top_requests = pipe_top_requests[:limit]

    if not pipe_top_requests:
        return

    suite = unittest.TestSuite()
    await new_pipe(checker_pipe, cl, force=True, check=False, populate=populate)

    class PipeCheckerTextTestResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super(PipeCheckerTextTestResult, self).__init__(*args, **kwargs)
            self.success: List[PipeChecker] = []

        def addSuccess(self, test: PipeChecker):  # type: ignore
            super(PipeCheckerTextTestResult, self).addSuccess(test)
            self.success.append(test)

    for _, request in enumerate(pipe_top_requests):
        suite.addTest(PipeChecker(request['endpoint_url'], pipe['name'], checker_pipe['name'], token, only_response_times, ignore_order, validate_processed_bytes))
    result = PipeCheckerTextTestResult(unittest.runner._WritelnDecorator(sys.stdout), descriptions=True, verbosity=2)  # type: ignore
    result.failfast = failfast
    suite.run(result)
    try:
        current_response_times: List[float] = []
        checker_response_times: List[float] = []

        current_read_bytes: List[int] = []
        checker_read_bytes: List[int] = []

        if result.success:
            for test in result.success:
                current_response_times.append(test.current_response_time)
                checker_response_times.append(test.checker_response_time)

                current_read_bytes.append(test.current_read_bytes)
                checker_read_bytes.append(test.checker_read_bytes)

            for test, _ in result.failures:  # type: ignore
                current_response_times.append(test.current_response_time)
                checker_response_times.append(test.checker_response_time)

                current_read_bytes.append(test.current_read_bytes)
                checker_read_bytes.append(test.checker_read_bytes)

        metrics = []
        metrics.append(['min response time', min(current_response_times), min(checker_response_times)])
        metrics.append(['max response time', max(current_response_times), max(checker_response_times)])
        metrics.append(['mean response time', format(mean(current_response_times), '.6f'), format(mean(checker_response_times), '.6f')])
        metrics.append(['median response time', median(current_response_times), median(checker_response_times)])
        metrics.append(['p90 response time', sorted(current_response_times)[math.ceil(len(current_response_times) * .9) - 1], sorted(checker_response_times)[math.ceil(len(checker_response_times) * .9) - 1]])

        metrics.append(['min read bytes', format_size(min(current_read_bytes)), format_size(min(checker_read_bytes))])
        metrics.append(['max read bytes', format_size(max(current_read_bytes)), format_size(max(checker_read_bytes))])
        metrics.append(['mean read bytes', format_size(mean(current_read_bytes)), format_size(mean(checker_read_bytes))])
        metrics.append(['median read bytes', format_size(median(current_read_bytes)), format_size(median(checker_read_bytes))])
        metrics.append(['p90 read bytes', format_size(sorted(current_read_bytes)[math.ceil(len(current_read_bytes) * .9) - 1]), format_size(sorted(checker_read_bytes)[math.ceil(len(checker_read_bytes) * .9) - 1])])
        column_names = ['Timing Metric (s)', 'Current', 'New']

        click.echo('\n==== Test Metrics ====\n')
        click.echo(format_pretty_table([[result.testsRun, len(result.success), len(result.failures), len(result.success) * 100 / result.testsRun, len(result.failures) * 100 / result.testsRun]], column_names=['Test Run', 'Test Passed', 'Test Failed', '% Test Passed', '% Test Failed']))

        click.echo('\n==== Response Time Metrics ====\n')
        click.echo(format_pretty_table(metrics, column_names=column_names))
    except Exception:
        pass

    if not result.wasSuccessful():
        for _test, err in result.failures:
            try:
                i = err.index('AssertionError') + len('AssertionError :')
                click.echo('==== Test FAILED ====\n')
                click.echo(_test)
                click.echo(FeedbackManager.error_check_pipe(error=err[i:]))
                click.echo('=====================\n\n\n')
            except Exception:
                pass
        raise RuntimeError('Invalid results, you can bypass checks by running push with the --no-check flag')

    # Only delete if no errors, so we can check results after failure
    r = await requests_delete(f"{host}/v0/pipes/{checker_pipe['name']}", headers=headers)
    if r.status_code != 204:
        click.echo(FeedbackManager.warning_check_pipe(content=r.content))


async def check_materialized(pipe, host, token, cl, override_datasource=False):
    checker_pipe = deepcopy(pipe)
    checker_pipe['name'] = f"{checker_pipe['name']}__checker"
    headers = {'Authorization': f'Bearer {token}'}

    materialized_node = None
    for node in checker_pipe['nodes']:
        if node['params']['type'] == 'materialized':
            materialized_node = deepcopy(node)
            materialized_node['params']['override_datasource'] = 'true' if override_datasource else 'false'
        node['params']['type'] = 'standard'

    try:
        pipe_created = False
        await new_pipe(checker_pipe, cl, force=True, check=False, populate=False, skip_tokens=True, ignore_sql_errors=False)
        pipe_created = True
        response = await cl.analyze_pipe_node(checker_pipe['name'], materialized_node, dry_run='true')
        if response.get('warnings'):
            show_materialized_view_warnings(response['warnings'])

    except Exception as e:
        raise click.ClickException(FeedbackManager.error_while_check_materialized(error=str(e)))
    finally:
        if pipe_created:
            r = await requests_delete(f"{host}/v0/pipes/{checker_pipe['name']}", headers=headers)
            if r.status_code != 204:
                click.echo(FeedbackManager.warning_check_pipe(content=r.content))


def show_materialized_view_warnings(warnings):
    """
    >>> show_materialized_view_warnings([{'code': 'SIM', 'weight': 1}])

    >>> show_materialized_view_warnings([{'code': 'SIM', 'weight': 1}, {'code': 'HUGE_JOIN', 'weight': 2}, {'text': "Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query.", 'code': 'GROUP_BY', 'weight': 100, 'documentation': 'https://docs.tinybird.co/tips/materialized-view-tips.html'}])
    ⚠️  Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query. For more information read https://docs.tinybird.co/tips/materialized-view-tips.html or contact us at support@tinybird.co
    >>> show_materialized_view_warnings([{'code': 'SINGLE_JOIN', 'weight': 300}, {'text': "Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query.", 'code': 'GROUP_BY', 'weight': 100, 'documentation': 'https://docs.tinybird.co/tips/materialized-view-tips.html'}])
    ⚠️  Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query. For more information read https://docs.tinybird.co/tips/materialized-view-tips.html or contact us at support@tinybird.co
    """
    excluded_warnings = ['SIM', 'SIM_UNKNOWN', 'HUGE_JOIN']
    sorted_warnings = sorted(warnings, key=lambda warning: warning['weight'])
    most_important_warning = {}
    for warning in sorted_warnings:
        if warning.get('code') and warning['code'] not in excluded_warnings:
            most_important_warning = warning
            break
    if most_important_warning:
        click.echo(FeedbackManager.single_warning_materialized_pipe(content=most_important_warning['text'], docs_url=most_important_warning['documentation']))


async def new_pipe(
        p,
        tb_client: TinyB,
        force: bool = False,
        check: bool = True,
        populate: bool = False,
        populate_subset=None,
        populate_condition=None,
        unlink_on_populate_error: bool = False,
        wait_populate: bool = False,
        skip_tokens: bool = False,
        tag: str = '',
        ignore_sql_errors: bool = False,
        only_response_times: bool = False,
        timeout=None,
        run_tests: bool = False,
        as_standard: bool = False,
        tests_to_run: int = 0,
        tests_to_sample_by_params: int = 0,
        tests_filter_by: Optional[List[str]] = None,
        tests_failfast: bool = False,
        tests_ignore_order: bool = False,
        tests_validate_processed_bytes: bool = False,
        override_datasource: bool = False
):  # noqa: C901
    # TODO use tb_client instead of calling the urls directly.
    host = tb_client.host
    token = tb_client.token

    headers = {'Authorization': f'Bearer {token}'}

    if tag:
        tag = tag + "__"

    cli_params = {}
    cli_params['cli_version'] = tb_client.version
    cli_params['description'] = p.get('description', '')
    cli_params['ignore_sql_errors'] = 'true' if ignore_sql_errors else 'false'

    r: requests.Response = await requests_get(f"{host}/v0/pipes/{p['name']}?{urlencode(cli_params)}", headers=headers)

    is_materialized = any([node.get('params', {}).get('type', None) == 'materialized' for node in p['nodes']])

    if r.status_code == 200:
        if force or run_tests:
            # TODO: this should create a different node and rename it to the final one on success
            if check and not populate:
                if not is_materialized:
                    await check_pipe(
                        p,
                        host,
                        token,
                        populate,
                        tb_client,
                        only_response_times=only_response_times,
                        limit=tests_to_run,
                        sample_by_params=tests_to_sample_by_params,
                        matches=tests_filter_by,
                        failfast=tests_failfast,
                        validate_processed_bytes=tests_validate_processed_bytes,
                        ignore_order=tests_ignore_order)
                else:
                    await check_materialized(p, host, token, tb_client, override_datasource=override_datasource)

            if run_tests:
                logging.info(f"skipping force override of {p['name']}")
                return
        else:
            raise click.ClickException(FeedbackManager.error_pipe_already_exists(pipe=p['name']))
    elif r.status_code == 404 and is_materialized and check:
        await check_materialized(p, host, token, tb_client, override_datasource=override_datasource)

    params = {}
    params.update(cli_params)

    if force:
        params['force'] = 'true'
    if populate:
        params['populate'] = 'true'
    if populate_condition:
        params['populate_condition'] = populate_condition
    if populate_subset:
        params['populate_subset'] = populate_subset
    params['unlink_on_populate_error'] = 'true' if unlink_on_populate_error else 'false'

    body = {
        'name': p['name'],
        'description': p.get('description', '')
    }

    def parse_node(node):
        if 'params' in node:
            node.update(node['params'])
            if node.get('type', '') == 'materialized' and override_datasource:
                node['override_datasource'] = 'true'
            del node['params']
        return node

    if p['nodes']:
        body['nodes'] = [parse_node(n) for n in p['nodes']]

    post_headers = {
        'Content-Type': 'application/json'
    }

    post_headers.update(headers)

    try:
        data = await tb_client._req(f"/v0/pipes?{urlencode(params)}", method='POST', headers=post_headers, data=json.dumps(body))
    except Exception as e:
        raise Exception(FeedbackManager.error_pushing_pipe(pipe=p['name'], error=str(e)))

    datasource = data.get('datasource', None)
    created_datasource = data.get('created_datasource', None)

    if datasource and created_datasource:
        click.echo(FeedbackManager.info_materialized_datasource_created(pipe=p['name'], datasource=datasource['name']))
    elif datasource and not created_datasource:
        click.echo(FeedbackManager.info_materialized_datasource_used(pipe=p['name'], datasource=datasource['name']))

    if datasource and populate:
        job_url = data.get('job', {}).get('job_url', None)
        job_id = data.get('job', {}).get('job_id', None)
        if populate_subset:
            click.echo(FeedbackManager.info_populate_subset_job_url(url=job_url, subset=populate_subset))
        elif populate_condition:
            click.echo(FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=populate_condition))
        else:
            click.echo(FeedbackManager.info_populate_job_url(url=job_url))

        if wait_populate:
            await wait_job(tb_client, job_id, job_url, 'Populating', timeout)
    else:
        if not is_materialized and not skip_tokens and not as_standard and not data.get('endpoint'):
            # FIXME: set option to add last node as endpoint in the API
            endpoint_node = next((node for node in data.get('nodes', []) if node.get('type') == 'endpoint'), data.get('nodes', [])[-1])
            try:
                r = await tb_client._req(f"/v0/pipes/{p['name']}/nodes/{endpoint_node.get('id')}/endpoint?{urlencode(cli_params)}", method='POST', headers=headers)
            except Exception as e:
                raise Exception(FeedbackManager.error_creating_endpoint(node=endpoint_node.get('name'), pipe=p['name'], error=str(e)))

            click.echo(FeedbackManager.success_test_endpoint_no_token(host=host, pipe=p['name']))

    if p['tokens'] and not skip_tokens and not as_standard:
        # search for token with specified name and adds it if not found or adds permissions to it
        t = None
        for tk in p['tokens']:
            token_name = tag + tk['token_name']
            t = await tb_client.get_token_by_name(token_name)
            if t:
                break
        if not t:
            token_name = tag + tk['token_name']
            click.echo(FeedbackManager.info_create_not_found_token(token=token_name))
            try:
                r = await tb_client.create_token(token_name, f"PIPES:{tk['permissions']}:{p['name']}", "P", p['name'])
                token = r['token']  # type: ignore
            except Exception as e:
                raise Exception(FeedbackManager.error_creating_pipe(error=e))
        else:
            click.echo(FeedbackManager.info_create_found_token(token=token_name))
            scopes = [f"PIPES:{tk['permissions']}:{p['name']}"]
            for x in t['scopes']:
                sc = x['type'] if 'resource' not in x else f"{x['type']}:{x['resource']}"
                scopes.append(sc)
            try:
                r = await tb_client.alter_tokens(token_name, scopes)
                token = r['token']  # type: ignore
            except Exception as e:
                raise Exception(FeedbackManager.error_creating_pipe(error=e))
        click.echo(FeedbackManager.success_test_endpoint(host=host, pipe=p['name'], token=token))


async def new_ds(ds, client: TinyB, force=False, skip_confirmation=False):
    ds_name = ds['params']['name']

    async def manage_tokens():
        # search for token with specified name and adds it if not found or adds permissions to it
        t = None
        for tk in ds['tokens']:
            token_name = tk['token_name']
            t = await client.get_token_by_name(token_name)
            if t:
                break
        if not t:
            token_name = tk['token_name']
            click.echo(FeedbackManager.info_create_not_found_token(token=token_name))
            # DS == token_origin.Origins.DATASOURCE
            await client.create_token(token_name, f"DATASOURCES:{tk['permissions']}:{ds_name}", "DS", ds_name)
        else:
            click.echo(FeedbackManager.info_create_found_token(token=token_name))
            scopes = [f"DATASOURCES:{tk['permissions']}:{ds_name}"]
            for x in t['scopes']:
                sc = x['type'] if 'resource' not in x else f"{x['type']}:{x['resource']}"
                scopes.append(sc)
            await client.alter_tokens(token_name, scopes)

    try:
        existing_ds = await client.get_datasource(ds_name)
        datasource_exists = True
    except DoesNotExistException:
        datasource_exists = False

    if not datasource_exists:
        params = ds['params']

        try:
            await client.datasource_create_from_definition(params)
            if 'tokens' in ds and ds['tokens']:
                await manage_tokens()
        except Exception as e:
            raise Exception(FeedbackManager.error_creating_datasource(error=str(e)))
        return

    if not force:
        raise click.ClickException(FeedbackManager.error_datasource_already_exists(datasource=ds_name))

    alter_response = None
    alter_error_message = None
    new_description = None
    new_schema = None
    new_ttl = None

    try:
        if datasource_exists and ds['params']['description'] != existing_ds['description']:
            new_description = ds['params']['description']

        if datasource_exists and ds['params'].get('engine_ttl') != existing_ds['engine'].get('ttl'):
            new_ttl = ds['params'].get('engine_ttl', 'false')

        # Schema fixed by the kafka connector
        if ('kafka_connection_name' not in ds['params']) and datasource_exists and \
           (ds['params']['schema'].replace(' ', '') != existing_ds['schema']['sql_schema'].replace(' ', '')):
            new_schema = ds['params']['schema']

        if new_description or new_schema or new_ttl:
            alter_response = await client.alter_datasource(ds_name, new_schema=new_schema, description=new_description, ttl=new_ttl, dry_run=True)
    except Exception as e:
        if "There were no operations to perform" in str(e):
            pass
        else:
            alter_error_message = str(e)

    if alter_response:
        click.echo(FeedbackManager.info_datasource_doesnt_match(datasource=ds_name))
        for operation in alter_response["operations"]:
            click.echo(f"**   -  {operation}")

        if skip_confirmation:
            make_changes = True
        else:
            make_changes = click.prompt(FeedbackManager.info_ask_for_alter_confirmation()).lower() == "y"

        if make_changes:
            await client.alter_datasource(ds_name, new_schema=new_schema, description=new_description, ttl=new_ttl, dry_run=False)
            click.echo(FeedbackManager.success_datasource_alter())
            return
        else:
            alter_error_message = "Alter datasource cancelled"

    # removed replacing by default. When a datasource is removed data is
    # removed and all the references needs to be updated
    if os.getenv('TB_I_KNOW_WHAT_I_AM_DOING') and click.prompt(FeedbackManager.info_ask_for_datasource_confirmation()) == ds_name:  # TODO move to CLI
        try:
            await client.datasource_delete(ds_name)
            click.echo(FeedbackManager.success_delete_datasource(datasource=ds_name))
        except Exception:
            raise Exception(FeedbackManager.error_removing_datasource(datasource=ds_name))
        return
    else:
        if alter_error_message:
            raise click.ClickException(FeedbackManager.error_datasource_already_exists_and_alter_failed(
                datasource=ds_name, alter_error_message=alter_error_message))
        else:
            click.echo(FeedbackManager.warning_datasource_already_exists(datasource=ds_name))


async def exec_file(
        r,
        tb_client: TinyB,
        force: bool,
        check: bool,
        debug: bool,
        populate: bool,
        populate_subset,
        populate_condition,
        unlink_on_populate_error,
        wait_populate,
        tag,
        override_datasource: bool = False,
        ignore_sql_errors: bool = False,
        skip_confirmation: bool = False,
        only_response_times: bool = False,
        timeout=None,
        run_tests=False,
        as_standard=False,
        tests_to_run: int = 0,
        tests_to_sample_by_params: int = 0,
        tests_filter_by: Optional[List[str]] = None,
        tests_failfast: bool = False,
        tests_ignore_order: bool = False,
        tests_validate_processed_bytes: bool = False
):
    if debug:
        click.echo(FeedbackManager.debug_running_file(file=pp.pformat(r)))
    if r['resource'] == 'pipes':
        await new_pipe(
            r,
            tb_client,
            force,
            check,
            populate,
            populate_subset,
            populate_condition,
            unlink_on_populate_error,
            wait_populate,
            tag=tag,
            ignore_sql_errors=ignore_sql_errors,
            only_response_times=only_response_times,
            timeout=timeout,
            run_tests=run_tests,
            as_standard=as_standard,
            tests_to_run=tests_to_run,
            tests_to_sample_by_params=tests_to_sample_by_params,
            tests_filter_by=tests_filter_by,
            tests_failfast=tests_failfast,
            tests_ignore_order=tests_ignore_order,
            tests_validate_processed_bytes=tests_validate_processed_bytes,
            override_datasource=override_datasource)

    elif r['resource'] == 'datasources':
        await new_ds(
            r,
            tb_client,
            force,
            skip_confirmation=skip_confirmation
        )
    else:
        raise Exception(FeedbackManager.error_unknown_resource(resource=r['resource']))


def get_name_tag_version(ds: str):
    """
    Given a name like "name__dev__v0" returns ['name', 'dev', 'v0']
    >>> get_name_tag_version('dev__name__v0')
    {'name': 'name', 'tag': 'dev', 'version': 0}
    >>> get_name_tag_version('name__v0')
    {'name': 'name', 'tag': None, 'version': 0}
    >>> get_name_tag_version('dev__name')
    {'name': 'name', 'tag': 'dev', 'version': None}
    >>> get_name_tag_version('name')
    {'name': 'name', 'tag': None, 'version': None}
    >>> get_name_tag_version('horario__3__pipe')
    {'name': '3__pipe', 'tag': 'horario', 'version': None}
    >>> get_name_tag_version('horario__checker')
    {'name': 'horario__checker', 'tag': None, 'version': None}
    >>> get_name_tag_version('dev__horario__checker')
    {'name': 'horario__checker', 'tag': 'dev', 'version': None}
    >>> get_name_tag_version('tg__dActividades__v0_pipe_3907')
    {'name': 'dActividades', 'tag': 'tg', 'version': 0}
    >>> get_name_tag_version('tg__dActividades__va_pipe_3907')
    {'name': 'dActividades__va_pipe_3907', 'tag': 'tg', 'version': None}
    >>> get_name_tag_version('tg__origin_workspace.shared_ds__v3907')
    {'name': 'origin_workspace.shared_ds', 'tag': 'tg', 'version': 3907}
    >>> get_name_tag_version('tmph8egtl__')
    {'name': 'tmph8egtl__', 'tag': None, 'version': None}
    >>> get_name_tag_version('tmph8egtl__123__')
    {'name': 'tmph8egtl__123__', 'tag': None, 'version': None}
    """
    tk = ds.rsplit('__', 2)
    if len(tk) == 1:
        return {'name': tk[0], 'tag': None, 'version': None}
    elif len(tk) == 2:
        if len(tk[1]):
            if tk[1][0] == 'v' and re.match('[0-9]+$', tk[1][1:]):
                return {'name': tk[0], 'tag': None, 'version': int(tk[1][1:])}
            else:
                if tk[1] == 'checker':
                    return {'name': tk[0] + "__" + tk[1], 'tag': None, 'version': None}
                return {'name': tk[1], 'tag': tk[0], 'version': None}
    elif len(tk) == 3:
        if len(tk[2]):
            if tk[2] == 'checker':
                return {'name': tk[1] + "__" + tk[2], 'tag': tk[0], 'version': None}
            if tk[2][0] == 'v':
                parts = tk[2].split('_')
                try:
                    return {'name': tk[1], 'tag': tk[0], 'version': int(parts[0][1:])}
                except ValueError:
                    return {'name': f'{tk[1]}__{tk[2]}', 'tag': tk[0], 'version': None}
            else:
                return {'name': '__'.join(tk[1:]), 'tag': tk[0], 'version': None}

    return {'name': ds, 'tag': None, 'version': None}


def get_resource_versions(datasources: List[str]):
    """
    return the latest version for all the datasources
    """
    versions = {}
    for x in datasources:
        t = get_name_tag_version(x)
        name = t['name']
        if t['tag']:
            name = f"{t['tag']}__{name}"
        if t.get('version', None) is not None:
            versions[name] = t['version']
    return versions


def get_remote_resource_name_without_version(remote_resource_name: str) -> str:
    """
    >>> get_remote_resource_name_without_version("r__datasource")
    'r__datasource'
    >>> get_remote_resource_name_without_version("r__datasource__v0")
    'r__datasource'
    >>> get_remote_resource_name_without_version("datasource")
    'datasource'
    """
    parts = get_name_tag_version(remote_resource_name)
    if parts['tag']:
        return parts['tag'] + '__' + parts['name']
    else:
        return parts['name']


def get_dep_from_raw_tables(x):
    """
    datasources KEY command generates tables, this transform the used table with the source file
    >>> get_dep_from_raw_tables('test')
    'test'
    >>> get_dep_from_raw_tables('test_join_by_column')
    'test'
    """

    try:
        return x[:x.index('_join_by_')]
    except ValueError:
        return x


async def build_graph(filenames, tb_client, dir_path=None, tag='', resource_versions=None, workspace_map=None, process_dependencies=False, verbose=False, skip_connectors=False, workspace_lib_paths=None):  # noqa: C901 B006
    """process files"""
    to_run = {}
    deps = []
    dep_map = {}
    embedded_datasources = {}
    if not workspace_map:
        workspace_map = {}

    deps_tag = ''
    if tag:
        deps_tag = f'{tag}__'

    if dir_path is None:
        dir_path = os.getcwd()

    async def process(filename, deps, dep_map, to_run, workspace_lib_paths, deps_tag):
        name, kind = filename.rsplit('.', 1)

        try:
            res = await process_file(
                filename,
                tb_client,
                dir_path,
                tag,
                resource_versions=resource_versions,
                verbose=verbose,
                skip_connectors=skip_connectors,
                workspace_map=workspace_map,
                workspace_lib_paths=workspace_lib_paths
            )
        except click.ClickException as e:
            raise e
        except Exception as e:
            raise click.ClickException(str(e))

        for r in res:
            fn = r['resource_name']
            to_run[fn] = r
            file_deps = r.get('deps', [])
            deps += file_deps
            # calculate and look for deps
            dep_list = []
            for x in file_deps:
                if x not in INTERNAL_TABLES:
                    f, ds = find_file_by_name(dir_path, x, verbose, workspace_lib_paths=workspace_lib_paths, resource=r, deps_tag=deps_tag)
                    if f:
                        dep_list.append(deps_tag + f.rsplit('.', 1)[0])
                    if ds:
                        ds_fn = ds['resource_name']
                        prev = to_run.get(ds_fn, {})
                        to_run[ds_fn] = deepcopy(r)
                        try:
                            to_run[ds_fn]['deps'] = list(set(to_run[ds_fn].get('deps', []) + prev.get('deps', []) + [fn.replace(deps_tag, '')]))
                        except ValueError:
                            pass
                        embedded_datasources[x] = to_run[ds_fn]
                    else:
                        e_ds = embedded_datasources.get(x, None)
                        if e_ds:
                            dep_list.append(e_ds['resource_name'])
            dep_map[fn] = set(dep_list)
        return os.path.basename(name)

    processed = set()

    async def get_processed(filenames):
        for filename in filenames:
            if os.path.isdir(filename):
                await get_processed(filenames=get_project_filenames(filename))
            else:
                if verbose:
                    click.echo(FeedbackManager.info_processing_file(filename=filename))

                if '.incl' in filename:
                    click.echo(FeedbackManager.warning_skipping_include_file(file=filename))

                name = await process(filename, deps, dep_map, to_run, workspace_lib_paths, deps_tag)
                processed.add(name)

    await get_processed(filenames=filenames)

    if process_dependencies:
        while len(deps) > 0:
            dep = deps.pop()
            if dep not in processed:
                processed.add(dep)
                f = full_path_by_name(dir_path, dep, workspace_lib_paths)
                if f:
                    if verbose:
                        try:
                            processed_filename = f.relative_to(os.getcwd())
                        except ValueError:
                            processed_filename = f
                        click.echo(FeedbackManager.info_processing_file(filename=processed_filename))
                    await process(str(f), deps, dep_map, to_run, workspace_lib_paths, deps_tag)

    return to_run, dep_map


def get_project_filenames(folder):
    folders = [
        f'{folder}/*.datasource',
        f'{folder}/datasources/*.datasource',
        f'{folder}/*.pipe',
        f'{folder}/pipes/*.pipe',
        f'{folder}/endpoints/*.pipe',
    ]
    filenames = []
    for x in folders:
        filenames += glob.glob(x)
    return filenames


async def folder_push(
    tb_client: TinyB,
    tag: str = '',
    filenames=None,
    dry_run=False,
    check=False,
    push_deps: bool = False,
    debug: bool = False,
    force: bool = False,
    override_datasource: bool = False,
    folder: str = '.',
    populate: bool = False,
    populate_subset=None,
    populate_condition: Optional[str] = None,
    unlink_on_populate_error: bool = False,
    upload_fixtures: bool = False,
    wait: bool = False,
    ignore_sql_errors: bool = False,
    skip_confirmation: bool = False,
    only_response_times: bool = False,
    workspace_map=None,
    workspace_lib_paths=None,
    no_versions: bool = False,
    timeout=None,
    run_tests: bool = False,
    as_standard: bool = False,
    raise_on_exists: bool = False,
    verbose: bool = True,
    tests_to_run: int = 0,
    tests_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False
):  # noqa: C901

    if not workspace_map:
        workspace_map = {}
    if not workspace_lib_paths:
        workspace_lib_paths = []

    workspace_lib_paths = list(workspace_lib_paths)
    # include vendor libs without overriding user ones without overriding user ones
    existing_workspaces = set(x[1] for x in workspace_lib_paths)
    vendor_path = Path('vendor')
    if vendor_path.exists():
        for x in vendor_path.iterdir():
            if x.is_dir() and x.name not in existing_workspaces:
                workspace_lib_paths.append((x.name, x))

    datasources: List[Dict[str, Any]] = await tb_client.datasources()  # type: ignore
    pipes: List[Dict[str, Any]] = await tb_client.pipes()  # type: ignore

    existing_resources: List[str] = [x['name'] for x in datasources] + [x['name'] for x in pipes]
    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        existing_resources = [re.sub(f'^{old_ws}\.', f'{new_ws}.', x) for x in existing_resources]

    if not no_versions:
        resource_versions = get_resource_versions(existing_resources)
    else:
        resource_versions = {}

    remote_resource_names = [get_remote_resource_name_without_version(x) for x in existing_resources]

    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        remote_resource_names = [re.sub(f'^{old_ws}\.', f'{new_ws}.', x) for x in remote_resource_names]

    if not filenames:
        filenames = get_project_filenames(folder)

    # build graph to get new versions for all the files involved in the query
    # dependencies need to be processed always to get the versions
    resources, dep_map = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        tag=tag,
        process_dependencies=True,
        workspace_map=workspace_map,
        skip_connectors=True,
        workspace_lib_paths=workspace_lib_paths
    )

    # update existing versions
    if not no_versions:
        latest_datasource_versions = resource_versions.copy()

        for dep in resources.values():
            ds = dep['resource_name']
            if dep['version'] is not None:
                latest_datasource_versions[ds] = dep['version']
    else:
        latest_datasource_versions = {}

    # build the graph again with the rigth version
    to_run, dep_map = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        tag=tag,
        resource_versions=latest_datasource_versions,
        workspace_map=workspace_map,
        process_dependencies=push_deps,
        verbose=verbose,
        workspace_lib_paths=workspace_lib_paths
    )

    if debug:
        pp.pprint(to_run)

    if verbose:
        click.echo(FeedbackManager.info_building_dependencies())

    def should_push_file():
        """
            Function to know if we need to run a file or not
        """
        if name not in remote_resource_names:
            return True
        # When we need to try to push a file when it doesn't exist and the version is different that the existing one
        resource_full_name = f"{name}__v{latest_datasource_versions.get(name)}" if name in latest_datasource_versions else name
        if resource_full_name not in existing_resources:
            return True
        if force or run_tests:
            return True
        return False

    for group in toposort(dep_map):
        for name in group:
            if name in to_run:
                if not dry_run:
                    if should_push_file():
                        if name not in resource_versions:
                            version = ''
                            if name in latest_datasource_versions:
                                version = f'(v{latest_datasource_versions[name]})'
                            click.echo(FeedbackManager.info_processing_new_resource(name=name, version=version))
                        else:
                            click.echo(FeedbackManager.info_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name)
                            ))
                        try:
                            await exec_file(
                                to_run[name],
                                tb_client,
                                force,
                                check,
                                debug and verbose,
                                populate,
                                populate_subset,
                                populate_condition,
                                unlink_on_populate_error,
                                wait,
                                tag,
                                override_datasource,
                                ignore_sql_errors,
                                skip_confirmation,
                                only_response_times,
                                timeout,
                                run_tests,
                                as_standard,
                                tests_to_run,
                                tests_sample_by_params,
                                tests_filter_by,
                                tests_failfast,
                                tests_ignore_order,
                                tests_validate_processed_bytes)
                            if not run_tests:
                                click.echo(FeedbackManager.success_create(
                                    name=name if to_run[name]['version'] is None else f'{name}__v{to_run[name]["version"]}'))
                        except Exception as e:
                            exception = FeedbackManager.error_push_file_exception(filename=to_run[name]['filename'], error=e)
                            raise click.ClickException(exception)
                    else:
                        if raise_on_exists:
                            raise AlreadyExistsException(FeedbackManager.warning_name_already_exists(
                                name=name if to_run[name]['version'] is None else f'{name}__v{to_run[name]["version"]}'))
                        else:
                            click.echo(FeedbackManager.warning_name_already_exists(
                                name=name if to_run[name]['version'] is None else f'{name}__v{to_run[name]["version"]}'))
                else:
                    if name not in remote_resource_names or resource_versions.get(name.replace(".", "_"), '') != latest_datasource_versions.get(name, '') or force:
                        if name not in resource_versions:
                            version = ''
                            if name in latest_datasource_versions:
                                version = f'(v{latest_datasource_versions[name]})'
                            click.echo(FeedbackManager.info_dry_processing_new_resource(name=name, version=version))
                        else:
                            click.echo(FeedbackManager.info_dry_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name)
                            ))
                    else:
                        click.echo(FeedbackManager.warning_dry_name_already_exists(name=name))

    if not dry_run and not run_tests:
        if upload_fixtures:
            click.echo(FeedbackManager.info_pushing_fixtures())
            processed = set()
            for group in toposort(dep_map):
                for f in group:
                    name = os.path.basename(f)
                    if name not in processed:
                        if name in to_run:
                            await check_fixtures_data(tb_client, to_run[name], debug, folder, force)
                            processed.add(name)
            for f in to_run:
                if f not in processed:
                    await check_fixtures_data(tb_client, to_run[f], debug, folder, force)
        else:
            if verbose:
                click.echo(FeedbackManager.info_not_pushing_fixtures())

    return to_run


async def check_fixtures_data(cl, r, debug, folder='', force=False):
    if debug:
        click.echo(FeedbackManager.info_checking_file(file=pp.pformat(r)))
    if r['resource'] == 'pipes':
        pass
    elif r['resource'] == 'datasources':
        datasource_name = r['params']['name']
        result = await cl.query(sql=f'SELECT count() as c FROM {datasource_name} FORMAT JSON')
        count = result['data'][0]['c']

        if count > 0 and not force:
            raise click.ClickException(
                FeedbackManager.error_push_fixture_will_replace_data(datasource=datasource_name))

        name = os.path.basename(r['filename']).rsplit('.', 1)[0]
        csv_test_file = Path(folder) / 'fixtures' / f'{name}.csv'
        if not csv_test_file.exists():
            csv_test_file = Path(folder) / 'datasources' / 'fixtures' / f'{name}.csv'
        if not csv_test_file.exists():
            csv_test_file = Path(folder) / 'datasources' / 'fixtures' / f'{name}.ndjson'
        if csv_test_file.exists():
            click.echo(FeedbackManager.info_checking_file_size(filename=r['filename'], size=sizeof_fmt(os.stat(csv_test_file).st_size)))
            sys.stdout.flush()
            try:
                with open(csv_test_file, 'rb') as file:
                    await cl.datasource_append_data(
                        datasource_name=r['params']['name'],
                        f=file,
                        mode='replace',
                        sql_condition='1=1',
                        format=csv_test_file.suffix[1:]
                    )
                click.echo(FeedbackManager.success_processing_data())
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_processing_blocks(error=e))

        else:
            click.echo(FeedbackManager.warning_file_not_found(name=csv_test_file))

    else:
        raise Exception(FeedbackManager.error_unknown_resource(resource=r['resource']))


DATAFILE_NEW_LINE = '\n'
DATAFILE_INDENT = ' ' * 4


def format_schema(file_parts, node):
    file_parts.append('SCHEMA >')
    file_parts.append(DATAFILE_NEW_LINE)
    columns = schema_to_sql_columns(node['columns'])
    file_parts.append(f',{DATAFILE_NEW_LINE}'.join(map(lambda x: f'    {x}', columns)))
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_data_connector(file_parts, node):
    ll = len(file_parts)
    [file_parts.append(f'{k.upper()} {v}{DATAFILE_NEW_LINE}') for k, v in node.items() if 'kafka' in k]
    if ll < len(file_parts):
        file_parts.append(DATAFILE_NEW_LINE)


def format_include(file_parts, doc):
    include = [line for line in doc.raw if 'INCLUDE' in line and '.incl' in line]
    if len(include):
        file_parts.append(include[0])
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_datasource(filename):
    doc = parse_datasource(filename)
    file_parts = []

    format_sources(file_parts, doc)
    format_maintainer(file_parts, doc)
    format_version(file_parts, doc)
    format_description(file_parts, doc)
    format_tokens(file_parts, doc)
    format_schema(file_parts, doc.nodes[0])
    format_engine(file_parts, doc.nodes[0])
    format_include(file_parts, doc)
    format_data_connector(file_parts, doc.nodes[0])
    return ''.join(file_parts)


def format_version(file_parts, doc):
    version = doc.version if doc.version is not None else ''
    if version != '':
        file_parts.append(f'VERSION {version}')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_maintainer(file_parts, doc):
    maintainer = doc.maintainer if doc.maintainer is not None else ''
    if maintainer:
        file_parts.append(f'MAINTAINER {maintainer}')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_sources(file_parts, doc):
    for source in doc.sources:
        file_parts.append(f'SOURCE {source}')
        file_parts.append(DATAFILE_NEW_LINE)
    if len(doc.tokens):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_description(file_parts, doc):
    description = doc.description if doc.description is not None else ''
    if description:
        file_parts.append('DESCRIPTION >')
        file_parts.append(DATAFILE_NEW_LINE)
        [file_parts.append(f'{DATAFILE_INDENT}{d.strip()}\n') for d in description.split(DATAFILE_NEW_LINE) if d.strip()]
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_tokens(file_parts, doc):
    for token in doc.tokens:
        file_parts.append(f'TOKEN "{token["token_name"]}" {token["permissions"]}')
        file_parts.append(DATAFILE_NEW_LINE)
    if len(doc.tokens):
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_node_sql(file_parts, node, line_length=None):
    file_parts.append('SQL >')
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(format_sql(node["sql"], DATAFILE_INDENT, line_length=line_length))
    file_parts.append(DATAFILE_NEW_LINE)
    file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_engine(file_parts, node):
    if node.get('engine', None):
        file_parts.append(f'ENGINE {node["engine"]["type"]}' if node.get('engine', {}).get('type') else '')
        file_parts.append(DATAFILE_NEW_LINE)
        for arg in node['engine'].get('args', []):
            file_parts.append(f'ENGINE_{arg[0].upper()} {arg[1]}')
            file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_node_type(file_parts, node):
    if node.get('type', '').lower() == 'materialized':
        file_parts.append(f'TYPE {node["type"]}')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(f'DATASOURCE {node["datasource"]}')
        file_parts.append(DATAFILE_NEW_LINE)
        format_engine(file_parts, node)
    return file_parts


def format_pipe_include(file_parts, node, includes):
    if includes:
        for k, v in includes.copy().items():
            if node['name'] in v:
                file_parts.append(f'INCLUDE {k}')
                file_parts.append(DATAFILE_NEW_LINE)
                file_parts.append(DATAFILE_NEW_LINE)
                file_parts.append(DATAFILE_NEW_LINE)
                del includes[k]
    return file_parts


def format_node(file_parts, node, includes, line_length=None):
    format_pipe_include(file_parts, node, includes)
    item = [k for k, _ in includes.items() if node['name'].strip() in k]
    if item:
        return

    file_parts.append(f'NODE {node["name"].strip()}')
    file_parts.append(DATAFILE_NEW_LINE)

    from collections import namedtuple
    Doc = namedtuple('doc', ['description'])
    format_description(file_parts, Doc(node.get('description', '')))
    format_node_sql(file_parts, node, line_length=line_length)
    format_node_type(file_parts, node)


def format_pipe(filename, line_length):
    doc = parse_pipe(filename)

    file_parts = []
    format_sources(file_parts, doc)
    format_maintainer(file_parts, doc)
    format_version(file_parts, doc)
    format_description(file_parts, doc)
    format_tokens(file_parts, doc)
    if doc.includes:
        for node in doc.nodes.copy():
            item = [k for k, _ in doc.includes.items() if node['name'].strip() in k]
            if item:
                doc.nodes.remove(node)
    for node in doc.nodes:
        format_node(file_parts, node, doc.includes, line_length=line_length)

    for k, _ in doc.includes.items():
        if '.incl' not in k:
            continue
        file_parts.append(f'INCLUDE {k}')
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)
        file_parts.append(DATAFILE_NEW_LINE)

    return ''.join(file_parts)


def format_sql(sql, DATAFILE_INDENT, line_length=None):
    sql = format_sql_template(sql.strip(), line_length=line_length)
    return '\n'.join([f'{DATAFILE_INDENT}{part}' for part in sql.split('\n') if len(part.strip())])


async def wait_job(tb_client, job_id, job_url, label, timeout=None):
    with click.progressbar(label=f"{label} ", length=100, show_eta=False, show_percent=True, fill_char=click.style("█", fg="green")) as progress_bar:
        def progressbar_cb(res):
            if 'progress_percentage' in res:
                progress_bar.update(int(round(res['progress_percentage'])) - progress_bar.pos)
            elif res['status'] != 'working':
                progress_bar.update(progress_bar.length)
        try:
            result = await asyncio.wait_for(tb_client.wait_for_job(job_id, status_callback=progressbar_cb), timeout)
            if result['status'] != 'done':
                click.echo(FeedbackManager.error_while_running_job(error=result['error']))
        except asyncio.TimeoutError:
            await tb_client.job_cancel(job_id)
            raise click.ClickException(FeedbackManager.error_while_running_job(error="Reach timeout, job cancelled"))
        except JobException as e:
            raise click.ClickException(FeedbackManager.error_while_running_job(error=str(e)))
        except Exception as e:
            raise click.ClickException(FeedbackManager.error_getting_job_info(error=str(e), url=job_url))
