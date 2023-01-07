#! /usr/bin/env python
#
# Copyright (c) 2022 Alberto Mardegan <mardy@users.sourceforge.net>
#
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.

from .generator import Generator


def all_generators():
    import importlib
    import inspect
    import os.path
    import pkgutil
    pkg_dir = os.path.dirname(__file__)
    generators = []
    for (module_loader, name, ispkg) in pkgutil.iter_modules([pkg_dir]):
        module = importlib.import_module('.' + name, __package__)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and \
                    issubclass(obj, Generator) and \
                    hasattr(obj, 'name'):
                generators.append(obj)
    return generators


def get_by_name(name, config):
    for gen in all_generators():
        if gen.name == name:
            return gen(config)
    return None
