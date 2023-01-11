import inspect
import platform
import site
from enum import Enum
from types import ModuleType
from typing import Any, Callable, Optional, List, Tuple

SITE_PACKAGES_STRING = "site-packages"
SITE_PACKAGES_STRING_LENGTH = 13

# find out where packages can be installed and remove site-packages from the end of this path
PACKAGE_INSTALL_LOCATIONS = site.getsitepackages()
PACKAGE_INSTALL_LOCATIONS.append(site.getusersitepackages())
PACKAGE_INSTALL_LOCATIONS = list(
    map(lambda x: x[:-SITE_PACKAGES_STRING_LENGTH], PACKAGE_INSTALL_LOCATIONS)
)

if platform.system() == "Darwin":
    PACKAGE_INSTALL_LOCATIONS.append("/Library/Frameworks/Python.framework/")
    PACKAGE_INSTALL_LOCATIONS.append("/System/Library/Frameworks/Python.framework/")


class ModuleOrigin(Enum):
    BUILT_IN = "built-in"
    THIRD_PARTY = "third party"
    PYTHON_INTERNAL = "python internal"
    LOCAL = "local"


def get_module_member_modules(module: ModuleType) -> List[Tuple[str, ModuleType]]:
    return get_relevant_module_members(module, predicate=inspect.ismodule)


def get_module_non_module_members(module: ModuleType) -> List[Tuple[str, Any]]:
    def is_not_a_module(obj: Any) -> bool:
        return not inspect.ismodule(obj)

    return get_relevant_module_members(module, predicate=is_not_a_module)


def get_relevant_module_members(
    module: ModuleType, predicate: Optional[Callable[[Any], bool]] = None
) -> List[Tuple[str, Any]]:
    members = []
    for name, value in inspect.getmembers(module, predicate=predicate):
        if not name.startswith("__"):
            members.append((name, value))
    return members


def get_module_origin(module: ModuleType) -> ModuleOrigin:
    try:
        module_source_file = inspect.getsourcefile(module)
        if not module_source_file:
            return ModuleOrigin.BUILT_IN
    except AttributeError:
        return ModuleOrigin.BUILT_IN
    if SITE_PACKAGES_STRING in module_source_file:
        return ModuleOrigin.THIRD_PARTY
    if any(
        pkg_install_path in module_source_file
        for pkg_install_path in PACKAGE_INSTALL_LOCATIONS
    ):
        return ModuleOrigin.PYTHON_INTERNAL
    return ModuleOrigin.LOCAL
