from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import yaml

DEFAULT_PIP_VERSION = "22.1.2"

if TYPE_CHECKING:
    from truera.client.model_preprocessing import PipDependencyParser


def convert_string_to_dep_list(str):
    out = []
    for dep in str.split(","):
        if dep == '':
            continue
        if dep:
            out.append(dep.strip())

    return out


class CondaTemplate(yaml.YAMLObject):

    def noop(self, *args, **kw):
        pass

    yaml.emitter.Emitter.process_tag = noop

    def __init__(
        self,
        in_dependencies: str,
        in_pip_dependencies: PipDependencyParser,
        *,
        python_version: Optional[str] = None,
        pip_version: Optional[str] = None
    ):
        if python_version:
            if not python_version.startswith("python="):
                python_version = "python=" + python_version

        default_python_version = "python=3.7.3"
        python_version = python_version or default_python_version
        pip_version = f"pip={pip_version or DEFAULT_PIP_VERSION}"

        self.name = "truera-env"

        in_dependencies = in_dependencies or ""

        self.dependencies = convert_string_to_dep_list(in_dependencies)

        if len(
            [
                dep for dep in self.dependencies
                if isinstance(dep, str) and dep.split('=')[0] == "python"
            ]
        ) == 0:
            self.dependencies.append(python_version)

        if len(
            [
                dep for dep in self.dependencies
                if isinstance(dep, str) and dep.split('=')[0] == "pip"
            ]
        ) == 0:
            self.dependencies.append(pip_version)

        # re-append pip dependencies
        self.dependencies.append(
            {"pip": in_pip_dependencies.get_dependencies()}
        )
