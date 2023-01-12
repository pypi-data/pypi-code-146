# Build deps.pex, given a project root

import hashlib
import logging
import os
import os.path
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import List, Optional, Tuple

import click
import pkg_resources
from packaging import version

from . import util

STANDARD_PACKAGES = [
    # improves debugging as per https://pex.readthedocs.io/en/latest/recipes.html#long-running-pex-applications-and-daemons
    "setproctitle",
]


@dataclass(frozen=True)
class DepsRequirements:
    requirements_txt: str
    python_version: version.Version
    pex_flags: List[str]

    @property
    def hash(self) -> str:
        # The hash uniquely identifies the list of requirements used to build a deps.pex.
        # This is used as part of the cache key to reuse a cached deps.pex.
        # Note requirements_txt may have floating dependencies, so this is not perfect and may
        # reuse deps.pex even if a new PyPI package is published for a dependency.
        # An easy workaround is to pin the dependency in setup.py.
        normalized_pex_flags = sorted(set(self.pex_flags) - {"--resolve-local-platforms"})
        return hashlib.sha1(
            (
                repr(self.requirements_txt) + str(self.python_version) + repr(normalized_pex_flags)
            ).encode("utf-8")
        ).hexdigest()


@dataclass(frozen=True)
class LocalPackages:
    local_package_paths: List[str]


def local_path_for(line: str, relative_to: str) -> Optional[str]:
    # Return the abspath for a local package, iff this line points to a local package,
    # otherwise return None

    path = None
    # Two kinds of local packages are supported
    # 1. direct references, https://peps.python.org/pep-0440/#direct-references

    match = re.search(r"file://(/\S+)", line)
    if match:
        path = match.group(1)
    # 2. relative or absolute paths, eg "../some/other/dir" or "/abs/dir"
    elif "/" in line:
        path = os.path.abspath(os.path.join(relative_to, line.strip()))

    if path:
        if not os.path.exists(path):
            raise ValueError(
                f"Could not find local directory {path!r} referenced in requirement {line!r}"
            )

        return path

    return None


def get_requirements_lines(local_dir) -> List[str]:
    # Combine dependencies specified in requirements.txt and setup.py
    lines = get_requirements_txt_deps(local_dir)
    lines.extend(get_setup_py_deps(local_dir))
    return lines


def collect_requirements(code_directory) -> Tuple[List[str], List[str]]:
    # traverse all local packages and return the list of local packages and other requirements
    pending = [os.path.abspath(code_directory)]  # local packages to be processed
    seen = set()

    local_package_paths = []
    deps_lines = []

    while pending:
        local_dir = pending.pop()
        if local_dir in seen:
            continue
        seen.add(local_dir)

        lines = get_requirements_lines(local_dir)
        # Separate out the local packages from other requirements
        for line in lines:
            local_package_path = local_path_for(line, relative_to=local_dir)
            if local_package_path:
                if local_package_path not in local_package_paths:
                    local_package_paths.append(local_package_path)
                    pending.append(local_package_path)
            else:
                deps_lines.append(line)

    return local_package_paths, deps_lines


def get_deps_requirements(
    code_directory, python_version: version.Version, build_sdists: bool = True
) -> Tuple[LocalPackages, DepsRequirements]:
    local_package_paths, deps_lines = collect_requirements(code_directory)
    deps_lines.extend(STANDARD_PACKAGES)

    deps_requirements_text = "\n".join(
        sorted(set(deps_lines)) + [""]
    )  # empty string adds trailing newline

    logging.info("List of local packages: %r", local_package_paths)
    logging.info("List of dependencies: %r", deps_requirements_text)

    local_packages = LocalPackages(local_package_paths=local_package_paths)
    deps_requirements = DepsRequirements(
        requirements_txt=deps_requirements_text,
        python_version=python_version,
        pex_flags=util.get_pex_flags(python_version, build_sdists),
    )
    logging.info("deps_requirements_hash: %r", deps_requirements.hash)

    return local_packages, deps_requirements


def build_deps_pex(code_directory, output_directory, python_version) -> Tuple[str, str]:
    _, requirements = get_deps_requirements(code_directory, python_version)
    return build_deps_from_requirements(requirements, output_directory)


# Resolving dependencies can be flaky - depends on the version of pip and the resolver algorithm.
# These flags allow trying multiple ways of building the deps.
# This also allows us to try new flags safely, by having automatic fallback.
TRY_FLAGS = [
    ["--resolver-version=pip-2020-resolver"],  # new resolver as recommended by pex team
    # disabled but left here for easy revert
    # [],  # default set of flags defined in util.py
]


def build_deps_from_requirements(
    requirements: DepsRequirements,
    output_directory: str,
) -> Tuple[str, str]:
    """Builds deps-<HASH>.pex and returns the path to that file and the dagster version."""
    os.makedirs(output_directory, exist_ok=True)
    deps_requirements_path = os.path.join(
        output_directory, f"deps-requirements-{requirements.hash}.txt"
    )
    tmp_pex_path = os.path.join(output_directory, f"deps-from-{requirements.hash}.pex")

    with open(deps_requirements_path, "w", encoding="utf-8") as deps_requirements_file:
        deps_requirements_file.write(requirements.requirements_txt)

    logging.info("Building deps pex for Python version %r", requirements.python_version)

    # We try different sets of build flags and use the first one that works
    try_flags = TRY_FLAGS.copy()
    while try_flags:
        add_on_flags = try_flags.pop(0)
        pex_flags = requirements.pex_flags + add_on_flags
        logging.info("Running pex with %r", " ".join(pex_flags))
        proc = util.build_pex(
            sources_directories=[],
            requirements_filepaths=[deps_requirements_path],
            pex_flags=pex_flags,
            output_pex_path=tmp_pex_path,
            # isolate this pex root from others on same machine. particularly useful in github action
            # environment where pex_root for builder.pex may get shared with this pex_root
            pex_root=os.path.join(output_directory, ".pex"),
        )
        if proc.returncode:
            if try_flags:
                logging.warning(proc.stderr.decode("utf-8"))
                logging.warning("Will retry building deps with a different resolution mechanism")
            else:
                logging.error("Failed to build deps.pex")
                logging.error(proc.stdout.decode("utf-8"))
                logging.error(proc.stderr.decode("utf-8"))
                # exit early for better debugging
                sys.exit(1)
        else:
            break

    pex_info = util.get_pex_info(tmp_pex_path)
    pex_hash = pex_info["pex_hash"]
    final_pex_path = os.path.join(output_directory, f"deps-{pex_hash}.pex")
    os.rename(tmp_pex_path, final_pex_path)
    logging.info("Wrote deps pex: %r", final_pex_path)

    distribution_names = pex_info["distributions"].keys()
    # the distributions are named something like 'dagster-1.0.14-py3-none-any.whl'
    # and 'dagster_cloud-1.1.7-py3-none-any.whl'
    dep_names = ["dagster", "dagster_cloud"]
    dep_versions = {}
    for name in distribution_names:
        for dep_name in dep_names:
            pattern = re.compile(f"{dep_name}-(.+?)-py")
            match = pattern.match(name)
            if match:
                dep_versions[dep_name] = match.group(1)
                break

    for dep_name in dep_names:
        if dep_name not in dep_versions:
            raise ValueError(f"The {dep_name} package dependency was expected but not found.")
        print(f"Found package {dep_name} version {dep_versions[dep_name]}.")

    return final_pex_path, dep_versions["dagster"]


def get_requirements_txt_deps(code_directory: str) -> List[str]:
    requirements_path = os.path.join(code_directory, "requirements.txt")
    if not os.path.exists(requirements_path):
        return []

    # remove current dir from the deps
    return [
        line
        for line in open(requirements_path, encoding="utf-8").read().splitlines()
        if line not in {"", "."}
    ]


def get_setup_py_deps(code_directory: str) -> List[str]:
    setup_py_path = os.path.join(code_directory, "setup.py")
    if not os.path.exists(setup_py_path):
        return []

    lines = []
    # write out egg_info files and load as distribution
    with tempfile.TemporaryDirectory() as temp_dir:
        proc = subprocess.run(
            ["python", setup_py_path, "egg_info", f"--egg-base={temp_dir}"],
            capture_output=True,
            check=False,
        )
        if proc.returncode:
            raise ValueError(
                "Error running setup.py egg_info: "
                + proc.stdout.decode("utf-8")
                + proc.stderr.decode("utf-8")
            )
        # read in requirements using pkg_resources
        dists = list(pkg_resources.find_distributions(temp_dir))
        if len(dists) != 1:
            raise ValueError(f"Could not find distribution for {setup_py_path}")
        dist = dists[0]
        for requirement in dist.requires():
            # the str() for Requirement is correctly formatted requirement
            # https://setuptools.pypa.io/en/latest/pkg_resources.html#requirement-methods-and-attributes
            lines.append(str(requirement))

    return lines


@click.command()
@click.argument("project_dir", type=click.Path(exists=True))
@click.argument("build_output_dir", type=click.Path(exists=False))
@util.python_version_option()
def deps_main(project_dir, build_output_dir, python_version):
    deps_pex_path, dagster_version = build_deps_pex(
        project_dir, build_output_dir, util.parse_python_version(python_version)
    )
    print(f"Wrote: {deps_pex_path} which includes dagster version {dagster_version}")


if __name__ == "__main__":
    deps_main()
