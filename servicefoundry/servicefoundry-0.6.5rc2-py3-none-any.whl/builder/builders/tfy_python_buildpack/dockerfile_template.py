import json
import os
from typing import List, Optional

from mako.template import Template

from servicefoundry.auto_gen.models import PythonBuild

# Right now `python:${python_version}` will work for sometime.
# later we may need to dynamically select the base image.

DOCKERFILE_TEMPLATE = Template(
    """
FROM python:${python_version}

% if apt_install_command is not None:
RUN ${apt_install_command}
% endif

% if requirements_path is not None:
COPY ${requirements_path} ${requirements_destination_path}
% endif

% if pip_install_command is not None:
RUN ${pip_install_command}
% endif

COPY . /app
WORKDIR /app
ENTRYPOINT ${entrypoint}
"""
)


def resolve_requirements_txt_path(build_configuration: PythonBuild) -> Optional[str]:
    if build_configuration.requirements_path:
        return build_configuration.requirements_path

    # TODO: what if there is a requirements.txt but user does not wants us to use it.
    possible_requirements_txt_path = os.path.join(
        build_configuration.build_context_path, "requirements.txt"
    )

    if os.path.isfile(possible_requirements_txt_path):
        return os.path.relpath(
            possible_requirements_txt_path, start=build_configuration.build_context_path
        )

    return None


def generate_apt_install_command(apt_packages: Optional[List[str]]) -> Optional[str]:
    packages_list = None
    if apt_packages:
        packages_list = " ".join(p.strip() for p in apt_packages if p.strip())
    if not packages_list:
        return None
    apt_update_command = "apt update"
    apt_install_command = f"apt install -y --no-install-recommends {packages_list}"
    clear_apt_lists_command = "rm -rf /var/lib/apt/lists/*"
    return " && ".join(
        [apt_update_command, apt_install_command, clear_apt_lists_command]
    )


def generate_pip_install_command(
    requirements_path: Optional[str], pip_packages: Optional[List[str]]
) -> Optional[str]:
    upgrade_pip_command = "pip install -U pip"
    final_pip_install_command = None
    if requirements_path:
        final_pip_install_command = f"pip install --no-cache-dir -r {requirements_path}"

    if pip_packages:
        final_pip_install_command = (
            final_pip_install_command or "pip install --no-cache-dir"
        )
        final_pip_install_command += " " + " ".join(
            f"'{package}'" for package in pip_packages
        )

    if not final_pip_install_command:
        return None

    return " && ".join([upgrade_pip_command, final_pip_install_command])


def generate_dockerfile_content(
    build_configuration: PythonBuild,
) -> str:
    requirements_path = resolve_requirements_txt_path(build_configuration)
    requirements_destination_path = (
        "/tmp/requirements.txt" if requirements_path else None
    )
    pip_install_command = generate_pip_install_command(
        requirements_path=requirements_destination_path,
        pip_packages=build_configuration.pip_packages,
    )
    apt_install_command = generate_apt_install_command(
        apt_packages=build_configuration.apt_packages
    )
    dockerfile_content = DOCKERFILE_TEMPLATE.render(
        python_version=build_configuration.python_version,
        apt_install_command=apt_install_command,
        requirements_path=requirements_path,
        requirements_destination_path=requirements_destination_path,
        pip_install_command=pip_install_command,
        entrypoint=json.dumps(build_configuration.command)
        if not isinstance(build_configuration.command, str)
        else build_configuration.command,
    )
    return dockerfile_content
