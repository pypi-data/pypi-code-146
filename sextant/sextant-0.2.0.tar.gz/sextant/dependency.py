"""
Simple dependency resolver. It is simplified by the fact our modules have well defined dependencies.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import json
import pathlib
from typing import List, Optional

from sextant import log
from sextant.module import Module, Registry
from sextant.semver import Semver


class DependencyError(Exception):
    """Special exception for dependencies errors."""


class Dependency:
    """Graph edge for the dependency tree"""

    def __init__(self, module: Module, root: Optional["Dependency"]):
        self.root = root
        self.module = module
        self.branches: List["Dependency"] = []

    def is_compatible(self, other: "Dependency") -> bool:
        """Check if two modules are compatible."""
        if self == other:
            return True
        if self.module.namespace != other.module.namespace:
            return True
        if self.module.name != other.module.name:
            return True
        # The modules are different, but they have same module and namespace.
        # This means they're on differing versions. Are those compatible?
        # Modules make the promise of not being incompatible
        # across patch versions.
        # NOTE: given how the Package class works, if this method is called
        # from there, this condition will always be false as the code should
        # always select the same exact patch version.
        if self.module.version.is_compatible(other.module.version):
            return True
        return False

    def __eq__(self, other):
        return self.module == other.module

    def __str__(self) -> str:
        if self.root is None:
            return str(self.module)
        # Here we try to avoid the inception of "required by".
        # TODO: maybe go check the original rootless object and create a chain
        return f"{self.module} (required by {self.root.module})"


class Package:
    """Package dependencies for a helm chart. Holds the whole dependency graph."""

    def __init__(self, registry: Registry, filename: str):
        self.package_modules: List[Dependency] = []
        self.registry = registry
        self.path = pathlib.Path(filename)
        if not self.path.exists():
            raise RuntimeError(f"Dependency file {self.path} does not exist.")
        self.lockfile = self.path.with_suffix(".lock")
        self.modules: List[str] = json.loads(self.path.read_bytes())

    def get(self, force: bool = False) -> List[Module]:
        """Get all the modules from the dependency tree."""
        # First let's check if the lockfile exists
        # and that package.json isn't newer than the lockfile
        if not force and self.lockfile.exists() and self.lockfile.stat().st_mtime >= self.path.stat().st_mtime:
            return self._read_lockfile()
        log.debug("Available modules: %s", self.modules)
        self._fetch_dependencies(*self.modules, root=None)
        log.debug("Computed dependencies: %s", self.package_modules)
        self._check_dependencies()
        self._write_lockfile()
        return [el.module for el in self.package_modules]

    def lock(self, force: bool = False):
        """Just generate the lockfile"""
        if not force and self.lockfile.exists():
            log.info("Lockfile already exists and --force wasn't specified, not overwriting.")
            return
        self._fetch_dependencies(*self.modules, root=None)
        self._check_dependencies()
        self._write_lockfile()

    def update(self, new_module: str) -> bool:
        """Update a dependency to a new version."""
        # Given self.modules is a list, we need to find the index of
        # the entry to overwrite.
        # Positive or zero: index in the modules list
        # -1: not present, to add to the list
        to_overwrite = -1
        try:
            name, ver = new_module.split(":")
            version = Semver(ver)
        except ValueError as exc:
            raise ValueError(f"Module {new_module} is badly formatted.") from exc

        # Cycle through the modules enumerated.
        for idx, mod in enumerate(self.modules):
            my_mod, my_ver = mod.split(":")
            if my_mod != name:
                continue
            if Semver(my_ver) > version:
                continue
            # We're here, we have to update modules.
            to_overwrite = idx
            break

        # If we're updating the package.json file, we want to also unlink the lockfile.
        if to_overwrite >= 0:
            self.modules[to_overwrite] = new_module
            # TODO: move to use missing_ok=True when we drop python 3.7
            if self.lockfile.exists():
                self.lockfile.unlink()
            with self.path.open("w", encoding="utf-8") as fileh:
                json.dump(self.modules, fileh, indent=4)
            log.debug("Updated modules: %s", self.modules)
            return True
        return False

    def _refresh(self):
        """Refresh the modules list"""
        self.modules = json.loads(self.path.read_bytes())

    def _read_lockfile(self) -> List[Module]:
        """Read the contents of the lockfile."""
        try:
            lock = json.loads(self.lockfile.read_bytes())
        except json.decoder.JSONDecodeError as exc:
            raise DependencyError("The lockfile {self.lockfile} contains invalid json data.") from exc
        # If the lockfile is valid, we just need to read the lockfile to load the correct
        # modules.
        out = []
        for mod in lock:
            mods = self.registry.query(**mod)
            if len(mods) != 1:
                raise DependencyError("The lockfile doesn't specify the modules correctly, please regenerate it.")
            out.append(mods[0])
        return out

    def _write_lockfile(self):
        """Write the lockfile."""
        outdata = []
        for dependency in self.package_modules:
            module = dependency.module
            outdata.append(
                {
                    "namespace": module.namespace,
                    "module": module.name,
                    "version": str(module.version),
                }
            )
        log.debug("Writing module dependencies to %s", self.lockfile)
        self.lockfile.write_text(json.dumps(outdata, indent=4), encoding="utf-8")

    def _fetch_dependencies(self, *modules: str, root: Optional[Dependency] = None):
        """Given a list of modules, recursively fetch dependencies from a registry"""
        # Container of the needed modules
        for mod in modules:
            log.debug("Fetching dependency for %s (from %s)", mod, root)
            try:
                base, version = mod.split(":")
                namespace, module = base.split(".")
            except ValueError as exc:
                raise DependencyError(f"dependency '{mod}' is not in the format 'namespace.module:version'") from exc
            # Now we get the highest matching version, then see if it's alread in our package.
            to_add = self.registry.get_newest(namespace=namespace, module=module, version=version)
            if to_add is None:
                msg = f"could not find the module {mod}"
                if root is not None:
                    msg += f" (required by {root.module})"
                raise DependencyError(msg)
            obj = Dependency(to_add, root)
            # We already added this module, so:
            # 1 - do not add it again
            # 2 - go to the next dependency
            # This will work because we consider two dependencies to be
            # equal if their module is equal.
            if obj in self.package_modules:
                continue
            if root is not None:
                root.branches.append(obj)
            self.package_modules.append(obj)
            # Call myself recursively for the dependencies of this module
            # The maximum theoretical recursion depth is the total number of modules we have.
            # when we'll have 1000 modules and this will hit the python recursion limit, we'll rewrite sextant in
            # a language that optimizes tail recursion.
            self._fetch_dependencies(*to_add.dependencies, root=obj)

    def _check_dependencies(self):
        """Check dependencies."""
        # This is a brute-force process.
        # Again, this is ok until we have too many dependencies.
        for i, dep in enumerate(self.package_modules):
            reminder = i + 1
            for other in self.package_modules[reminder:]:
                if not dep.is_compatible(other):
                    raise DependencyError(f"Module {dep} is incompatible with module {other}")
