from dataclasses import dataclass
import os
import re
import sys
from typing import Optional, Sequence

try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version
except:
    # this provides a backport of importlib.metadata for Python versions < 3.10
    # we cannot expect clients (e.g. Python SDK) to be on 3.10+ so we
    # install the backport by default in the SDK.
    from importlib_metadata import PackageNotFoundError
    from importlib_metadata import version


def get_python_version_str() -> str:
    version = sys.version_info
    return f"{version.major}.{version.minor}.{version.micro}"


def get_module_version(module_name: str) -> Optional[str]:
    # devnote: using importlib_metadata over __version__ which does not work for some libs
    try:
        return version(module_name)
    except PackageNotFoundError:
        return None


@dataclass(frozen=True)
class PythonPackageRequirement:
    # min and max versions are inclusive.
    package_name: str
    min_version: Optional[str] = None
    max_version: Optional[str] = None

    def get_requirement_string(self) -> str:
        req_string = self.package_name
        version_strings = []
        if self.min_version:
            version_strings.append(f">={self.min_version}")
        if self.max_version:
            version_strings.append(f"<={self.max_version}")
        return req_string + ",".join(version_strings)


def _construct_requirement(req_string: str) -> PythonPackageRequirement:
    split = re.split("(>=|<=|==|<|>)", req_string)
    package_name = split[0]
    min_version = None
    max_version = None
    for i in range(1, len(split), 2):
        version = split[i + 1]
        version = version.strip(",")
        version = version.strip()
        if split[i] == ">=":
            min_version = version
        elif split[i] == "<=":
            max_version = version
        elif split[i] == "==":
            min_version = version
            max_version = version
        else:
            raise ValueError("Only '<=', '>=', '==' operations are supported!")
    return PythonPackageRequirement(package_name, min_version, max_version)


def _requirements_from_file(file: str) -> Sequence[PythonPackageRequirement]:
    with open(
        os.path.join(os.path.dirname(__file__), "env_requirements", file)
    ) as f:
        lines = f.read().splitlines()
        return [_construct_requirement(line) for line in lines]


def model_runner_ml_requirements() -> Sequence[PythonPackageRequirement]:
    return _requirements_from_file("model_runner_ml_requirements.txt")


def model_runner_sys_requirements() -> Sequence[PythonPackageRequirement]:
    return _requirements_from_file("model_runner_sys_requirements.txt")


def sdk_packaging_requirements() -> Sequence[PythonPackageRequirement]:
    return _requirements_from_file("sdk_packaging_requirements.txt")
