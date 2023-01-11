import importlib
import os
import pkgutil
import sys
from functools import reduce, wraps
from typing import Any, List

from click import Command, Parameter

from sym.shared.cli.helpers.updater import SymUpdater


def is_prod_mode():
    return not SymUpdater().is_local() and not _sym_api_url_is_local()


def _sym_api_url_is_local():
    if sym_api_url := os.getenv("SYM_API_URL"):
        # Local if SYM_API_URL is set and does not point to staging or production.
        return (
            sym_api_url != "https://api.staging.symops.com/api/v1"
            and sym_api_url != "https://api.symops.com/api/v1"
        )

    return False


def import_all(name):
    for _, module_name, _ in pkgutil.walk_packages(sys.modules[name].__path__):
        importlib.import_module(f"{name}.{module_name}")


def requires_all_imports(import_all):
    def wrapper(fn):
        all_imported = False

        @wraps(fn)
        def wrapped(*args, **kwargs):
            nonlocal all_imported

            if not all_imported:
                import_all()
                all_imported = True

            return fn(*args, **kwargs)

        return wrapped

    return wrapper


def wrap(val):
    if isinstance(val, (list, tuple)):
        return val
    else:
        return (val,)


def flow(fns: List, val: Any):
    return reduce(lambda f, x: x(f), fns, val)


def get_param(command: Command, name: str) -> Parameter:
    return next(p for p in command.params if p.name == name)
