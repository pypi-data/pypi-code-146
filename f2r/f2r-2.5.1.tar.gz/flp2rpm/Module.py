import os
import logging
import sys

from . import config
from .helpers import runSubprocess


class Module:

    def __init__(self, name):
        self.name = name
        os.environ["MODULEPATH"] = os.path.join(config.ali_prefix, 'sw/MODULES', config.architecture)

    def versions(self, filter = True):
        """ List of available versions of given package """
        avail = runSubprocess(['module', '-t', 'avail', self.name, '--no-pager'], forceTty=True, shell=True)
        if not isinstance(avail, str):
            return []
        versions = []
        for entry in (avail.strip().split()[1:]):
            split = entry.rsplit('/')
            # modules wrongly match prefix, eg. Python matches Python-modules, etc..
            if split[0] != self.name and filter:
                continue
            versions.append(split[1])
        return versions

    def deps(self, version):
        """ List of dependencies and versions according to modulefile  """
        filtered = []
        deps = runSubprocess(['module', 'display', 'BASE/1.0', self.name + '/' + version, '--no-pager'], forceTty=True, shell=True).strip()
        for dep in deps.split('\n'):
            if len(dep) > 1 and dep.split()[0] == 'module':
                filtered += dep.split()[2:]
        return filtered

    def deps_as_dict(self, version):
        """ As above but as dictionary """
        dict = {}
        list = self.deps(version)
        for dep in list:
            temp = dep.split('/')
            dict[temp[0]] = temp[1]
        return dict
