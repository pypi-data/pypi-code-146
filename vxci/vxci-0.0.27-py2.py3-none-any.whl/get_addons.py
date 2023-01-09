#!/usr/bin/env python
"""
Usage: get-addons [-m] path1 [path2 ...]
Given a list  of paths, finds and returns a list of valid addons paths.
With -m flag, will return a list of modules names instead.
"""

from __future__ import print_function
import ast
import os

try:
    from itertools import ifilter, imap
except ImportError:
    ifilter = filter
    imap = map


MANIFEST_FILES = [
    '__manifest__.py',
    '__odoo__.py',
    '__openerp__.py',
    '__terp__.py',
]


def is_module(path):
    """return False if the path doesn't contain an odoo module, and the full
    path to the module manifest otherwise"""

    if not os.path.isdir(path):
        return False
    files = os.listdir(path)
    filtered = [x for x in files if x in (MANIFEST_FILES + ['__init__.py'])]
    if len(filtered) == 2 and '__init__.py' in filtered:
        return os.path.join(
            path, next(x for x in filtered if x != '__init__.py'))
    else:
        return False


def find_module(module, paths):
    '''Find module in paths
    :param module: String with name of module to find in paths.
    :param paths: List of strings with paths to search.
    :return: String with full path of manifest file found'''
    for path in paths:
        module_path = is_module(os.path.join(path, module))
        if module_path:
            return module_path


def is_installable_module(path):
    """return False if the path doesn't contain an installable odoo module,
    and the full path to the module manifest otherwise"""
    manifest_path = is_module(path)
    if manifest_path:
        manifest = ast.literal_eval(open(manifest_path).read())
        if manifest.get('installable', True):
            return manifest_path
    return False


def get_modules(path):

    # Avoid empty basename when path ends with slash
    if not os.path.basename(path):
        path = os.path.dirname(path)

    res = []
    if os.path.isdir(path):
        res = [x for x in os.listdir(path)
               if is_installable_module(os.path.join(path, x))]
    return res


def is_addons(path):
    res = get_modules(path) != []
    return res


def get_addons(path):
    if is_addons(path):
        res = [path]
    else:
        res = [os.path.join(path, x)
               for x in os.listdir(path)
               if is_addons(os.path.join(path, x))]
    return res


def get_depends(addons_path_list, modules_list):
    """Get recursive depends from addons_paths and modules list
    :param modules_list: List of strings with name of modules
    :param addons_path_list: List of strings with path of modules
    :return set: Unsorted set of recursive dependencies of modules
    """
    modules = set(modules_list)
    addons_paths = set(addons_path_list)
    visited = set()
    while modules != visited:
        module = (modules - visited).pop()
        visited.add(module)
        manifest_path = find_module(module, addons_path_list)
        assert manifest_path, "Module not found %s in addons_paths %s" % (
            module, addons_path_list)
        try:
            manifest_filename = next(ifilter(
                os.path.isfile,
                imap(lambda p: os.path.join(p, manifest_path), addons_paths)
            ))
        except StopIteration:
            # For some reason the module wasn't found
            continue
        manifest = eval(open(manifest_filename).read())
        modules.update(manifest.get('depends', []))
    return modules


def get_module_list():
    exclude_modules = [x.strip() for x in os.environ.get('EXCLUDE', '').split(',')]
    lists = get_modules('.')
    if exclude_modules:
        lists = [x for x in lists if x not in exclude_modules]
    return ','.join(lists)


def get_modules2test(folder, include=None, exclude=None):
    if not include:
        # If not 'include' defined means ALL
        modules2test = set(get_modules(folder))
    else:
        # If 'include' defined means only these modules
        modules2test = set(i.strip() for i in include.strip().split(','))
        if 'ALL' in modules2test:
            # 'ALL' = main_repository_all_modules
            # e.g. 'company_country,ALL' means company_country,main_repo_app1,main_repo_app2,...
            modules2test |= set(get_modules(folder))
            modules2test -= {'ALL'}
    if exclude:
        modules2test -= set(i.strip() for i in exclude.strip().split(','))
    return modules2test - {''}


def join_prefix_suffix(items, prefix, suffix=None):
    """Use "str.join" but forcing a prefix even for the first item.

    e.g.
    items = ["module1", "module2", "module3"]
    prefix = "/"
    suffix = ","
    Result = "/module1,/module2,/module3"

    Using the "str.join" method for the same input:
    ',/'.join(items)
    the output is 'module1,/module2,/module3'
    Notice the prefix for first item is missed.
    So, it needs to be inserted (only if the result is not empty).

    items = [""]
    Result: ""

    The default suffix is "," if it is not defined
    """
    if suffix is None:
        suffix = ','
    suffix_prefix = "%s%s" % (suffix, prefix)
    str_join = suffix_prefix.join(items)
    if str_join:
        str_join = "%s%s" % (prefix, str_join)
    return str_join


def get_tags(modules, tags):
    """Transform modules to /tag_module items.

    If the "tags" variable is not defined so all the modules will be the tags.
    modules = ["module1", "module2", "module3"]
    tags = None
    Result: "/module1,/module2,/module3"

    If the "tags" variable has an item with the string "ALL"
    So, the tags related to modules will be appended.
    modules = ["module1", "module2", "module3"]
    tags = "ALL,tag1"
    Result = "/module1,/module2,/module3,tag1"

    Notice the tags do not need extra prefixes but modules.

    if the "tags" variable has an item it will be used without /tag_module items.
    modules = ["module1", "module2", "module3"]
    tags = "-tag1,tag2"
    Result: "-tag1,tag2"

    if the "tags" variable is empty so all the /tag_module will be append.
    """
    if "" in tags:
        tags.remove("")
    if not tags or "ALL" in tags and len(tags) == 1:
        # if "tags" variable is empty or if only have "ALL" value so return /tag_modules
        return join_prefix_suffix(modules, "/")
    if "ALL" in tags:
        # 'ALL' = Insert all modules as tags
        # e.g. modules = 'company_country'
        #      tags = 'ALL,sale'
        # means tags=/company_country,sale
        tags.remove("ALL")
        return "%s,%s" % (join_prefix_suffix(modules, "/"), join_prefix_suffix(tags, ""))
    return "%s" % join_prefix_suffix(tags, "")


if __name__ == "__main__":
    # TODO: Make unittests
    modules = ["module1", "module2"]
    tags = ["tag1"]

    tags_str = get_tags(modules, tags)
    assert tags_str == "tag1"

    tags += ["ALL"]
    tags_str = get_tags(modules, tags)
    assert tags_str == "/module1,/module2,tag1"

    tags = [""]
    tags_str = get_tags(modules, tags)
    assert tags_str == "/module1,/module2"

    tags = []
    tags_str = get_tags(modules, tags)
    assert tags_str == "/module1,/module2"
