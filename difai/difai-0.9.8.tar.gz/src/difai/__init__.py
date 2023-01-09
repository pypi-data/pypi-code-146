from __future__ import annotations

import ast
import logging
import subprocess
from pathlib import Path

import nbformat
import nbconvert
import pkg_resources
import re


logger = logging.getLogger(__name__)

# This is probably too crude
VERSION_RE = re.compile(r"([\w-]+)([<>^=]{1,2})([\w\d\.]+)")


def _walk_tree_and_update_imports(tree: ast.Module, imports: set[str]) -> None:
    for i in ast.walk(tree):
        if isinstance(i, ast.Import):
            for name in i.names:
                imports.add(name.name.split(".")[0])
        elif isinstance(i, ast.ImportFrom):
            module = i.module
            # None happens e.g. for "from . import"
            if module is not None:
                imports.add(module.split(".")[0])
        # what about dynamically loaded modules, e.g. importlib?


def collect_imports(in_path: Path) -> set[str]:
    logger.info("Collecting imports")
    imports: set[str] = set()
    for filename in in_path.glob("**/*.py"):
        with open(filename, "r") as f:
            file = f.read()
        _walk_tree_and_update_imports(ast.parse(file), imports)

    for filename in in_path.glob("**/*.ipynb"):
        with open(filename, "r") as f:
            notebook = nbformat.read(f, as_version=4)
        if notebook["metadata"]["kernelspec"]["language"] != "python":
            continue
        code, _ = nbconvert.PythonExporter().from_notebook_node(notebook)
        _walk_tree_and_update_imports(ast.parse(code), imports)

    logger.info(f">>> {imports}")
    return imports


def collect_installed_packages() -> dict[str, str]:
    env = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    # Remove backports
    env.pop("dataclasses", None)
    return env


def get_package_versions(
    imports: set[str], env: dict[str, str]
) -> dict[str, str]:
    # filter out standard library
    installed_packages = [i for i in sorted(imports) if i in env]
    return {k: env[k] for k in installed_packages}


def load_previous_infile(
    out_path: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    previous_imports: dict[str, str] = {}
    qualifiers: dict[str, str] = {}
    file = out_path / "requirements.in"
    if not file.exists():
        return previous_imports, qualifiers

    with open(file, "r") as f:
        for line in f:
            match = VERSION_RE.match(line)
            if match is None:
                continue
            name, qualifier, version = match.groups()
            previous_imports[name] = version
            qualifiers[name] = qualifier
    return previous_imports, qualifiers


def update_pkg_versions_with_previous(
    pkg_versions: dict[str, str], previous_imports: dict[str, str]
) -> None:
    for name, version in previous_imports.items():
        if name in pkg_versions:
            # Don't overwrite new versions
            continue
        pkg_versions[name] = version
    return None


def write_requirements_in(
    out_path: Path, pkg_versions: dict[str, str], qualifiers: dict[str, str]
) -> None:
    logger.info("Generating requirements.in file")
    with open(out_path / "requirements.in", "w") as f:
        for pkg, version in pkg_versions.items():
            qualifier = qualifiers.get(pkg, ">=")
            f.write(f"{pkg}{qualifier}{version}\n")


def write_requirements_txt(out_path: Path) -> None:
    logger.info("Generating requirements.txt file")
    subprocess.check_output(
        ["pip-compile", "--generate-hashes", "requirements.in"],
        cwd=out_path,
    )
