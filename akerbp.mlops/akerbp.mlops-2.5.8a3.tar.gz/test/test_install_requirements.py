import os
import subprocess
from pathlib import Path
from akerbp.mlops.core import config
from akerbp.mlops.core.exceptions import VirtualEnvironmentError
from akerbp.mlops.deployment.helpers import (
    create_venv,
    install_requirements,
    delete_venv,
    set_up_requirements,
)

test_venv = "test-venv"
requirements_file = "test/test_requirements.txt"


def test_create_venv_creates_venv_no_exception_raised(venv_name=test_venv):
    try:
        create_venv(venv_name=venv_name)
    except VirtualEnvironmentError as exc:
        raise AssertionError(f"Virtual environment not created ({exc})") from None


def test_install_requirements_install_single_test_requirement_in_venv_with_no_deps(
    req_file=requirements_file, venv_name=test_venv
):
    venv_dir = os.path.join(os.getcwd(), venv_name)
    install_requirements(
        req_file=req_file, venv_dir=venv_dir, with_deps=False, setup_venv=True
    )
    cmd = ["bin/pip", "list"]
    output = subprocess.Popen(
        cmd, cwd=venv_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, _ = output.communicate()
    package, version = stdout.decode().split("\n")[2:-1][0].split()
    expected = {
        "package": "minimal",
        "version": "0.1.0",
    }

    assert package == expected["package"] and version == expected["version"]


def test_delete_venv_deletes_venv_no_exception_raised(venv_name=test_venv):
    try:
        delete_venv(venv_name=venv_name)
    except VirtualEnvironmentError as exc:
        raise AssertionError(f"Virtual environment not deleted ({exc})") from None


def test_set_up_requirements_from_settings_install_deps_in_venv():
    project_settings = config.read_project_settings(
        yaml_file=Path("test/test_settings/installing_reqs_in_venv.yaml")
    )
    deps_installed_in_venv = []
    expected = {
        "package": "minimal",
        "version": "0.1.0",
    }
    for setting in project_settings:
        venv_dir = set_up_requirements(
            c=setting,
            venv_name=test_venv,
            with_deps=False,
            unit_testing=True,
            setup_venv=True,
        )
        cmd = ["bin/pip", "list"]
        output = subprocess.Popen(
            cmd, cwd=venv_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        stdout, _ = output.communicate()
        package, version = stdout.decode().split("\n")[2:-1][0].split()

        if package == expected["package"] and version == expected["version"]:
            deps_installed_in_venv.append(True)
        else:
            deps_installed_in_venv.append(False)
    delete_venv(venv_name=test_venv)
    assert sum(deps_installed_in_venv) == len(deps_installed_in_venv)
