"""Helper functions for node based tools"""

import os
import shlex
from pathlib import Path

from pydash import py_

from eze.utils.io.file import parse_json

from eze.utils.cli.run import run_async_cmd, CompletedProcess, has_missing_exe_output
from eze.utils.io.file_scanner import find_files_by_name
from eze.utils.error import EzeExecutableNotFoundError
from typing import Tuple


class Cache:
    """Cache class container"""


__c = Cache()
__c.installed_in_folder = {}

# TODO: handle multiple sdk versions
NPM_DOCKER_IMAGE: str = "node:19.3.0-slim"


def get_npm_projects() -> []:
    """give a list of npm projects"""
    npm_package_jsons = find_files_by_name("^package.json$")
    return npm_package_jsons


def delete_npm_cache() -> None:
    """delete npm caching"""
    __c.installed_in_folder = {}


async def install_npm_in_path(raw_path: Path):
    """Install node dependencies"""
    lookup_key: str = str(raw_path)
    path: Path = Path.joinpath(Path.cwd(), raw_path)
    if not lookup_key in __c.installed_in_folder:
        has_package_json = os.path.isfile(path / "package.json")
        if has_package_json:
            (completed_process, used_docker_npm) = await run_npm_command("npm install", str(path))
    __c.installed_in_folder[lookup_key] = True


async def annotate_transitive_licenses(sbom: dict, project_folder: str, include_dev: True) -> dict:
    """adding annotations to licenses which are not top-level"""
    cmd = "npm list --json" if include_dev else "npm list --json --only=prod"
    (completed_process, used_docker_npm) = await run_npm_command(cmd, project_folder)
    report_text = completed_process.stdout
    parsed_json = parse_json(report_text)
    top_level_packages = py_.get(parsed_json, "dependencies", {})
    for component in py_.get(sbom, "components", []):
        component_name = component["name"]
        is_not_transitive = component_name in top_level_packages
        py_.set(component, "properties.transitive", not is_not_transitive)
    return top_level_packages


async def run_npm_command(npm_command: str, cwd: str) -> Tuple[CompletedProcess, bool]:
    """run npm local command with docker fallback"""
    try:
        completed_process: CompletedProcess = await run_async_cmd(shlex.split(npm_command), True, cwd=cwd)
        output = completed_process.stdout
        if has_missing_exe_output(output):
            raise EzeExecutableNotFoundError("failed local npm try docker")
        return completed_process, False
    except EzeExecutableNotFoundError as error:
        return (
            await run_async_cmd(
                shlex.split(f"docker run --rm -v {cwd}:/src -w /src --rm {NPM_DOCKER_IMAGE} {npm_command}"),
                True,
                cwd=cwd,
            ),
            True,
        )
