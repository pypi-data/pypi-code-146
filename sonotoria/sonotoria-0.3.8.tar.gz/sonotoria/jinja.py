# -*- coding: utf-8 -*-
import os
import shutil
import logging
from typing import Any, Dict, Callable

import jinja2
from benedict import benedict

from .template_config import load_env, unified_loop_config, unified_rename_config, WrongConfigException

logger = logging.getLogger(__name__)

def template_string(
    str_: str,
    context: Dict[str, Any]                   = None,
    filters: Dict[str, Callable[[Any], Any]]  = None,
    tests:   Dict[str, Callable[[Any], bool]] = None
) -> str:
    """This function templates a given string using jinja2 engine.

    Args:
        str_: The string to template.
        context: A dict with the context of the template.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.

    Returns:
        The templated string

    Examples:
       >>> from sonotoria import jinja
       >>> jinja.template_string('my {{ name }} is rich', context={'name': 'tailor'})
       my tailor is rich
    """
    context = context or {}

    # Somehow trailing line feed are removed by jinja2 readding them
    add_trail = '\n' if str_.endswith('\n') else ''

    env = jinja2.Environment()
    for name, filter_ in (filters or {}).items():
        env.filters[name] = filter_
    for name, test in (tests or {}).items():
        env.tests[name] = test
    try:
        return env.from_string(str_).render(**context) + add_trail
    except TypeError: # Yaml Objects
        return env.from_string(str_).render(**context.__dict__) + add_trail

def template_file(
    src: str,
    dest: str,
    context: Dict[str, Any]                   = None,
    filters: Dict[str, Callable[[Any], Any]]  = None,
    tests:   Dict[str, Callable[[Any], bool]] = None
) -> str:
    """This function templates a given file using jinja2 engine.

    Args:
        src: The path to the file to template.
        dest: The path where to create the resulting templated file.
        context: A dict with the context of the template.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.

    Returns:
        Nothing

    Examples:
       >>> from sonotoria import jinja
       >>> jinja.template_file('mytemplate', 'templated', context={'name': 'tailor'})
    """
    with open(src, 'r', encoding='utf-8') as src_f:
        content = template_string(src_f.read(), context, filters, tests)

    if '/' in dest:
        os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(dest, 'w', encoding='utf-8') as dest_f:
        dest_f.write(content)

def template_folder(
    src: str,
    dest: str,
    context: Dict[str, Any]                   = None,
    filters: Dict[str, Callable[[Any], Any]]  = None,
    tests:   Dict[str, Callable[[Any], bool]] = None
) -> str:
    """This function templates a given folder using jinja2 engine and configuration provided in this folder. Examples found in README.

    Args:
        src: The path to the folder to template.
        dest: The path where to create the resulting templated folder.
        context: A dict with the context of the template.
        filters: A dict with filters to add to the template engine. Names as keys, functions as values.
        tests: A dict of tests to add to the template engine. Names as keys, functions as values.

    Returns:
        Nothing

    Examples:
       >>> from sonotoria import jinja
       >>> jinja.template_folder('mytemplate', 'templated', context={'name': 'tailor'})
    """
    env = load_env(src, context, filters, tests)

    if 'template' not in env['config']:
        logger.warning('No template config found.')
        handle_folder(src, dest, env)
    else:
        handle_node(env['config']['template'], src, dest, env)

def without_excluded(env):
    return {
        'context': env['context'],
        'filters': env['filters'],
        'tests': env['tests']
    }

def handle_node(node_config, src, dest, env):
    handled_paths = []
    for loop in node_config.get('loop', []):
        handled_paths += handle_loop(loop, src, dest, env)
    for rename in node_config.get('rename', []):
        handled_paths += handle_rename(rename, src, dest, env)

    handled_paths += handle_folder(src, dest, env, handled_paths)
    return handled_paths

def handle_folder(src, dest, env, handled_paths=None):
    newly_handled_path = []
    paths_to_handle = unhandled_paths(src, handled_paths or [], env.get('excluded_paths', []))
    for path in paths_to_handle:
        path_dest = path.replace(src, dest)
        if os.path.isdir(path):
            os.mkdir(path_dest)
        if os.path.isfile(path):
            try:
                template_file(path, path_dest, **without_excluded(env))
            except UnicodeDecodeError as err:
                print(f'Could not template {path} -> {path_dest} due to non unicode encoding.')
                print(err)
                print('File will be copied as is.')
                os.makedirs(os.path.dirname(path_dest), exist_ok=True)
                shutil.copy(path, path_dest)
        newly_handled_path.append(path)
    return newly_handled_path

def unhandled_paths(root, handled_paths, excluded_paths):
    paths = []
    for rootdir, dirs, files in os.walk(root):
        for file_ in files:
            paths.append(os.path.join(rootdir, file_))
        for subdir in dirs:
            paths.append(os.path.join(rootdir, subdir))

    return [path for path in paths if is_unhandled(path, handled_paths, excluded_paths)]

def is_unhandled(path, handled_paths, excluded_paths):
    return not any(path.startswith(excluded_path+'/') or path == excluded_path for excluded_path in excluded_paths) and path not in handled_paths

def handle_rename(rename, src, dest, env):
    config = unified_rename_config(rename)
    handled_paths = [config['path']]

    folder_path = '/'.join(config['path'].split('/')[:-1])

    src_path = f'{src}/{config["path"]}'
    dest_path = '/'.join((dest, folder_path, template_string(config['transform'], **without_excluded(env))))

    if src_path not in env['excluded']:

        if config['type'] == 'file':
            template_file(src_path, dest_path, **without_excluded(env))
            handled_paths.append(src_path)
        if config['type'] == 'folder':
            os.mkdir(dest_path)
            handled_paths.append(src_path)
            handled_paths += handle_node(config, src_path, dest_path, env)

    return handled_paths

def handle_loop(loop, src, dest, env):
    config = unified_loop_config(loop)
    handled_paths = [config['path']]

    context = benedict(env['context'])

    if config['var'] not in context:
        raise WrongConfigException(f'The variable {config["var"]} does not exist in the context.')

    src_path = f'{src}/{config["path"]}'
    local_env = lambda item: {
        'context': {config['item']: item, **env['context']},
        'filters': env['filters'],
        'tests': env['tests']
    }
    dest_path = lambda item: '/'.join((
        dest,
        '/'.join(config['path'].split('/')[:-1]),
        template_string(config['transform'], **local_env(item))
    ))

    if src_path not in env['excluded']:

        items = context[config['var']]
        for test in config['tests']:
            items = [item for item in items if env['tests'][test](item)]
        items = [item for item in items if item not in config['excluded_values']]
        for filter_ in config['filters']:
            items = env['filters'][filter_](items)

        if config['type'] == 'file':
            for item in items:
                template_file(src_path, dest_path(item), **local_env(item))
                handled_paths.append(src_path)
        if config['type'] == 'folder':
            for item in items:
                local_dest = dest_path(item)
                os.mkdir(local_dest)
                handled_paths.append(src_path)
                handled_paths += handle_node(config, src_path, local_dest, {**env, **local_env(item)})

    return handled_paths
