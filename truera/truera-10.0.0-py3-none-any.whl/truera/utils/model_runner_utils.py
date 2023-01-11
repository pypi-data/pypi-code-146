import os
from typing import Mapping, Optional, Sequence

from packaging.requirements import Requirement
import yaml

from truera.utils.package_requirement_utils import PythonPackageRequirement

DEFAULT_MR_PIP_VERSION = "22.1.2"


class CondaYamlParser:

    def __init__(self, conda_env_path: str):
        if not os.path.exists(conda_env_path):
            raise ValueError(
                f"Provided path to conda env does not exist: {conda_env_path}"
            )
        with open(conda_env_path, "r") as h:
            self.conda_yaml = yaml.safe_load(h)
        self.initial_pip_modifications = False

    def get_yaml(self) -> Mapping:
        return self.conda_yaml

    def save_conda_yaml(self, filepath: str):
        new_contents = yaml.dump(self.conda_yaml)
        if os.path.exists(filepath):
            with open(filepath, "r") as h:
                old_contents = h.read()
            if new_contents == old_contents:
                return
        with open(filepath, "w") as h:
            yaml.dump(self.conda_yaml, h)

    def _parse_conda_dep(self, conda_dep: str) -> Optional[Requirement]:
        try:
            if "<=" not in conda_dep and ">=" not in conda_dep and conda_dep.count(
                "="
            ) == 1:
                # pip requirements are of the form x==y rather than x=y and we are using a pip parser.
                conda_dep = conda_dep.replace("=", "==")
            return Requirement(conda_dep)
        except:
            return None

    def _get_conda_dependencies(self) -> Sequence[Optional[Requirement]]:
        if "dependencies" not in self.conda_yaml:
            return []
        return [
            self._parse_conda_dep(dep)
            for dep in self.conda_yaml["dependencies"]
            if isinstance(dep, str)
        ]

    def _initialize_pip_modifications(self):
        # if no dependencies declared, add pip and return
        if "dependencies" not in self.conda_yaml:
            self.conda_yaml["dependencies"] = [
                f"pip={DEFAULT_MR_PIP_VERSION}", {
                    "pip": []
                }
            ]

        # determine whether "pip" is a declared dependency and if so, what version
        contains_pip_dep = False
        needs_resolution_flag = False  # pip<20.3 uses an old dependency resolver that misses dependency chains.
        for dep in self.conda_yaml["dependencies"]:
            if not isinstance(dep, str):
                continue
            parsed_conda_dep = self._parse_conda_dep(dep)
            if parsed_conda_dep and parsed_conda_dep.name == "pip":
                contains_pip_dep = True
                if not parsed_conda_dep.specifier.contains("20.3") and any(
                    parsed_conda_dep.specifier.filter(
                        ['20.2', '20.2.1', '20.2.2', '20.2.3', '20.2.4']
                    )
                ):
                    # we are using pip 20.2.x and thus can default to the new resolver with a flag
                    needs_resolution_flag = True
                break

        # if pip-specific deps are already specified, add resolver + specify version
        for i, dep in enumerate(self.conda_yaml["dependencies"]):
            if isinstance(dep, dict) and "pip" in dep:
                if not contains_pip_dep:
                    self.conda_yaml["dependencies"].insert(
                        i, f"pip={DEFAULT_MR_PIP_VERSION}"
                    )
                    contains_pip_dep = True
                if needs_resolution_flag:
                    dep["pip"].append("--use-feature=2020-resolver")
                    needs_resolution_flag = False

        if not contains_pip_dep:
            self.conda_yaml["dependencies"].append(
                f"pip={DEFAULT_MR_PIP_VERSION}"
            )

        if needs_resolution_flag:
            self.conda_yaml["dependencies"].append(
                {"pip": ["--use-feature=2020-resolver"]}
            )

        self.initial_pip_modifications = True

    def _get_pip_dependencies(self):
        if not self.initial_pip_modifications:
            self._initialize_pip_modifications()

        for dep in self.conda_yaml["dependencies"]:
            if isinstance(dep, dict) and "pip" in dep:
                return dep["pip"]

        pip_deps = []
        self.conda_yaml["dependencies"].append({"pip": pip_deps})
        return pip_deps

    def add_truera_qii_pip_requirement(self, path_to_truera_qii: str):
        current_pip_deps = self._get_pip_dependencies()
        current_pip_deps.append(
            f"--find-links file://{os.path.abspath(path_to_truera_qii)}"
        )
        current_pip_deps.append("truera_qii")

    def add_pip_requirement(self, requirement: PythonPackageRequirement):
        safe_to_add = True
        pip_deps = self._get_pip_dependencies()
        conda_deps = self._get_conda_dependencies()

        for pip_dep in pip_deps:
            try:
                dep_name = Requirement(pip_dep).name
                if dep_name == requirement.package_name:
                    safe_to_add = False
            except:
                # in case we can't parse a particular line of the dependency yaml, suppress errors
                pass

        for conda_dep in conda_deps:
            if conda_dep and conda_dep.name == requirement.package_name:
                safe_to_add = False
                break

        if safe_to_add:
            pip_deps.append(f"{requirement.get_requirement_string()}")
