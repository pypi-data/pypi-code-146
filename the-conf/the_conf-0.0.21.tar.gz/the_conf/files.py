import json
import logging
from os.path import abspath, expanduser, splitext

import yaml

from the_conf.utils import Index

logger = logging.getLogger(__name__)


def read(*paths):
    any_found = False
    for path in paths:
        path = abspath(expanduser(path.strip()))
        ext = splitext(path)[1][1:]
        try:
            if ext in {'yml', 'yaml'}:
                with open(path, 'r', encoding='utf8') as fd:
                    yield path, ext, yaml.load(fd.read(),
                                               Loader=yaml.FullLoader)
            elif ext == 'json':
                with open(path, 'r', encoding='utf8') as fd:
                    yield path, ext, json.load(fd)
            else:
                logger.error("File %r ignored: unknown type (%s)", path, ext)
                continue
            any_found = True
        except FileNotFoundError:
            logger.debug('%r not found', path)
        except PermissionError:
            logger.warning('%r: no right to read', path)
    if not any_found:
        logger.warning('no file found among %r', paths)


def extract_value(config, path, full_path=None):
    full_path = full_path or []
    if len(path) == 1 and path[0] in config:
        yield full_path + [path[0]], config[path[0]]
    elif path[0] is Index and isinstance(config, (list, tuple)):
        for index, sub_config in enumerate(config):
            if len(path) == 1:
                yield full_path + [index], sub_config
            else:
                yield from extract_value(config[index], path[1:],
                                         full_path + [index])
    elif path[0] in config:
        yield from extract_value(config[path[0]], path[1:],
                                 full_path + [path[0]])
    else:
        raise ValueError(f"no {path[0]!r} in {config!r}")


def extract_values(paths, config, config_file):
    for path in paths:
        try:
            if Index in path:
                for full_path, sub_value in extract_value(config, path):
                    yield full_path, sub_value
            else:
                for full_path, value in extract_value(config, path):
                    assert full_path == path
                    yield path, value
        except ValueError:
            logger.debug('%s not found in %r', '.'.join(path), config_file)


def write(config, path):
    path = abspath(expanduser(path.strip()))
    ext = splitext(path)[1][1:]
    if ext in {'yml', 'yaml'}:
        with open(path, 'w', encoding='utf8') as fp:
            yaml.dump(config, fp)
    elif ext == 'json':
        with open(path, 'w', encoding='utf8') as fp:
            json.dump(config, fp)
    else:
        raise ValueError("couldn't make out file type, conf file path should "
                         "end with either yml, yaml or json")
