from __future__ import annotations

import logging
import os
from pathlib import Path

import typer

from . import (
    collect_imports,
    collect_installed_packages,
    get_package_versions,
    load_previous_infile,
    write_requirements_in,
    write_requirements_txt,
    update_pkg_versions_with_previous,
)

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def main(
    exclude: list[str] = typer.Option(list),
    in_path: Path = typer.Option(Path(".")),
    out_path: Path = typer.Option(Path(os.getcwd())),
    verbose: bool = typer.Option(False),
) -> None:
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    logger.info(f"Using {in_path} to search for project files")
    logger.info(f"Using {out_path} as target folder for requirement files")

    previous_imports, qualifiers = load_previous_infile(out_path)

    imports = collect_imports(in_path)
    imports = imports.difference(exclude)
    env = collect_installed_packages()
    pkg_versions = get_package_versions(imports, env)
    update_pkg_versions_with_previous(pkg_versions, previous_imports)

    write_requirements_in(out_path, pkg_versions, qualifiers)
    write_requirements_txt(out_path)


if __name__ == "__main__":
    app()
