# Copyright 2022 The Pigweed Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Check Python package install_requires are covered."""

import argparse
from pathlib import Path
import sys
import re
from typing import List
import importlib.metadata

try:
    from pw_build.python_package import load_packages, PythonPackage
except ImportError:
    # Load from python_package from this directory if pw_build is not available.
    from python_package import load_packages, PythonPackage  # type: ignore


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--setup-dir',
        type=Path,
        required=True,
        help=
        'Path to a text file containing the list of Python package metadata.')
    parser.add_argument(
        '--python-dep-list-files',
        type=Path,
        required=True,
        help=
        'Path to a text file containing the list of Python package metadata '
        'json files.',
    )
    parser.add_argument(
        '--constraint',
        nargs='+',
        type=Path,
        help='constraint files to check',
    )
    parser.add_argument(
        '--requirement',
        nargs='+',
        type=Path,
        help='requirement files to check',
    )
    return parser.parse_args()


_PYPI_NAME_REGEX = re.compile(r'^([A-Z0-9][A-Z0-9._-]*[A-Z0-9]).*$',
                              re.IGNORECASE)


def _normalize_pip_dep(name: str) -> str:
    return name.lower().replace('_', '-')


def _extract_package_name(line: str) -> str:
    dep_name = ''
    match = _PYPI_NAME_REGEX.match(line)
    if match:
        dep_name = _normalize_pip_dep(match.group(1))
    return dep_name


class MissingPipDependency(Exception):
    """An error occurred while processing a Python dependency."""


def check_install_requires(
    setup_cfg: Path,
    pkg: PythonPackage,
    constraint: List[Path],  # pylint: disable=unused-argument
    requirement: List[Path],
) -> bool:
    """Perform checks on a Python package's install_requires entries.

    This function raises errors if the give PythonPackage's install_requires
    entries are not covered by the given requirements.txt files.
    """

    # Don't perform any checks if this Python package has no install_requires.
    if not pkg.config:
        return True
    if not pkg.config.has_option('options', 'install_requires'):
        return True

    # Don't perform any checks if no requirements.txt files were provided.
    if not requirement:
        return True

    install_requires = pkg.install_requires_entries()
    missing_deps = {}

    # WIP: Should we check constraints here?
    # constraints = []
    # for constraint_file in constraint:
    #     for line in constraint_file.read_text().splitlines():
    #         dep = _extract_package_name(line)
    #         if not dep:
    #             continue
    #         constraints.append(dep)
    # unique_constraints = set(constraints)

    requirements = []
    for requirement_file in requirement:
        for line in requirement_file.read_text().splitlines():
            dep = _extract_package_name(line)
            if not dep:
                continue
            requirements.append(dep)

    unique_requirements = set(requirements)

    for dep in install_requires:
        sanitized_dep = _extract_package_name(dep)
        if not sanitized_dep:
            continue
        if sanitized_dep not in unique_requirements:
            dist = None
            try:
                dist = importlib.metadata.distribution(sanitized_dep)
            except importlib.metadata.PackageNotFoundError:
                pass
            found_version = dist.version if dist else None
            missing_deps[sanitized_dep] = found_version

    if missing_deps:
        raise MissingPipDependency(
            f'\n\nERROR: {setup_cfg.resolve()} defines the following pip '
            'dependencies:\n\n' +
            '\n'.join(name for name, version in missing_deps.items()) + '\n\n'
            'Which are missing from the project requirements.txt files:\n\n' +
            '\n'.join(
                str((Path.cwd() / req_file).resolve())
                for req_file in requirement) + '\n')

    return True


class MissingSetupCfgFile(Exception):
    """An error occurred while processing a Python dependency."""


class NoMatchingPythonPackage(Exception):
    """An error occurred while processing a Python dependency."""


def main(
    setup_dir: Path,
    python_dep_list_files: Path,
    constraint: List[Path],
    requirement: List[Path],
) -> int:
    """Check Python package setup.cfg correctness."""

    setup_cfg = setup_dir / 'setup.cfg'
    if not setup_cfg.is_file():
        raise MissingSetupCfgFile(
            f'\n\nERROR: "{setup_cfg}" file could not be found.\n\n')

    py_packages = load_packages([python_dep_list_files], ignore_missing=False)

    package_to_check = None
    for pkg in py_packages:
        if pkg.setup_cfg == setup_cfg:
            package_to_check = pkg

    if not package_to_check:
        raise MissingSetupCfgFile(
            f'\n\nERROR: "{setup_cfg}" is not found in any of the following'
            'Python packages:\n' + '\n'.join(
                str((Path.cwd() / pkg.package_dir).resolve())
                for pkg in py_packages) + '\n')

    if not check_install_requires(setup_cfg, package_to_check, constraint,
                                  requirement):
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main(**vars(_parse_args())))
