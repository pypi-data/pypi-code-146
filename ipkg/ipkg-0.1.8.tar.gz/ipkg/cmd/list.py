import importlib.util
import pkgutil
from importlib.machinery import ModuleSpec

import click
from rich import print
from rich.columns import Columns
from rich.tree import Tree

from ..utils.name import package_name


def get_list(spec: ModuleSpec) -> list[str]:
    names: set[str] = set()
    for module in pkgutil.iter_modules(path=spec.submodule_search_locations):
        names.add(package_name(mod_name=module.name))
    return list(names)


def get_tree(spec: ModuleSpec) -> Tree:
    tree: Tree = Tree(package_name(spec.name.split(sep=".")[-1]))
    names: set[str] = set()
    for module in pkgutil.iter_modules(path=spec.submodule_search_locations):
        if module.name in names:
            continue
        names.add(module.name)
        if module.ispkg:
            sub_spec = importlib.util.find_spec(name=f"{spec.name}.{module.name}")
            assert sub_spec
            tree.add(get_tree(spec=sub_spec))
        else:
            tree.add(package_name(mod_name=module.name))
    return tree


@click.command(name="list")
@click.option("--tree", is_flag=True)
@click.argument("pkg", required=False, default="")
def cmd_list(tree: bool, pkg: str):
    if pkg:
        spec = importlib.util.find_spec(name=f"ipkg.pkg.{pkg}")
        if not spec:
            raise LookupError(f'Package "{pkg}" Not Found!')
    else:
        spec = importlib.util.find_spec(name="ipkg.pkg")
    assert spec
    if tree:
        names = get_tree(spec=spec)
        print(names)
    else:
        names = get_list(spec=spec)
        print(Columns(names, expand=False, equal=True))
