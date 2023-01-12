import os as _os
import subprocess as _subprocess

try:
    import emzed  # noqa F401
except Exception:
    pass

_os.environ["QT_API"] = "pyqt5"


def _inspect(*what, **kw):
    from emzed.gui import inspect

    try:
        inspect(*what, **kw)
    except Exception:
        import traceback

        emzed.gui.show_warning(traceback.format_exc())


def _import_from_spyder(module_name):
    """import helper for loacl imports from emzed_spyder within jupyter terminal.
    (the kernel is not aware of emzed_spyder and e.g. 'import folders' would
    not work)."""

    import importlib
    import sys

    here = _os.path.dirname(_os.path.abspath(__file__))
    sys.path.insert(0, here)
    try:
        return importlib.import_module(module_name)
    except Exception:
        import traceback
        from datetime import datetime

        path = _os.path.expanduser("~/_spyder_bootstrap_traceback.log")
        with open(path, "a") as fh:
            print(datetime.now(), file=fh)
            print(file=fh)
            traceback.print_exc(file=fh)
            print(file=fh)

    finally:
        sys.path.pop(0)


_utils = _import_from_spyder("utils")


def emzed_help():
    """shows this help"""
    print()
    for name, function in globals().items():
        if name.startswith("emzed_"):
            print("{:34s}: {}".format(name, (function.__doc__ or "").split("\n")[0]))
    print()
    print("you can also run e.g. help(emzed_project_new) for more detailed help.")
    print()


def emzed_download_examples():
    """downloads some emzed example scripts"""

    import re
    import traceback

    import requests

    URL = "http://emzed.ethz.ch/downloads/example_scripts/"
    print()

    try:
        folder_listing_html = requests.get(URL).text

        links = re.findall(r'href="([^"]+)"', folder_listing_html)

        if "/downloads/" not in links:
            with open("error.txt", "w") as fh:
                print("invalid response from", URL, file=fh)
                print(file=fh)
                print(folder_listing_html, file=fh)
                print(file=fh)
            return

        # file names start after '/downloads'
        for file_name in links[links.index("/downloads/") + 1 :]:
            print("download", file_name)
            with open(file_name, "w") as fh:
                fh.write(requests.get(URL + file_name).text)
        print()
        print("done")
        print()

    except Exception:
        with open("error.txt", "w") as fh:
            traceback.print_exc(file=fh)


def emzed_update():
    """updates emzed3 and emzed3_gui (in active project)"""
    import sys

    _utils.setup_venv(sys.executable.replace("pythonw.exe", "python.exe"))
    print()
    print("please close this terminal and start a new one to load all updates")
    print()


def emzed_install_ext(name):
    """install emzed extension, e.g. emzed_install_ext("mzmine")"""
    full_name = f"emzed_ext_{name}"

    import importlib
    import sys

    _execute(f"{sys.executable} -m pip install --upgrade" f" {full_name}")

    try:
        sys.modules[f"emzed.ext.{name}"] = importlib.import_module(full_name)
        importlib.import_module(f"emzed.ext.{name}")
    except ImportError:
        print()
        print(f"installation failed, can not import {full_name}")
    else:
        # update repl completion:
        import emzed.ext

        emzed.ext._ext_names[:] = emzed.ext._find_extensions()

        print()
        print(
            f"installation succeeded. please create a new session to use"
            f" emzed.ext.{name}"
        )


def _check_name(name):
    from string import ascii_lowercase, digits

    if not name:
        return "name is empty"

    if name[0] not in ascii_lowercase:
        return "first character must be lower case letter"

    valid_charachters = ascii_lowercase + digits + "_"
    invalid_characters_in_name = set(name) - set(valid_charachters)

    if not invalid_characters_in_name:
        return None

    return "invalid name. following letter(s) are not allowed: {}".format(
        ", ".join(map(repr, sorted(invalid_characters_in_name)))
    )


def emzed_project_new(name=None):
    """creates new project"""
    import glob

    from cookiecutter.main import cookiecutter

    if name is None:
        name = _ask_nonempty("project name? ")
        if name is None:
            return

    message = _check_name(name)
    if message is not None:
        print()
        print(message)
        return

    project_folder = _utils.get_project_folder(name)
    if project_folder.exists():
        print(f"project with name {name} already exists.")
        return

    here = _os.path.dirname(_os.path.abspath(__file__))

    cookiecutter(
        _os.path.join(here, "emzed_package_template"),
        extra_context=dict(pkg_name=name, directory_name=str(project_folder)),
        no_input=True,
    )
    for p in glob.glob(
        _os.path.join(project_folder, "**", "*.pytemplate"), recursive=True
    ):
        _os.rename(p, p[: -len("template")])

    venv_folder = project_folder / ".venv"

    # might be out of date after update:
    if not _utils.is_valid_venv(_utils.remote_venv_folder):
        _utils.create_fresh_venv(_utils.remote_venv_folder)

    remote_venv_site_packages = _utils.find_site_packages(_utils.remote_venv_folder)

    _utils.create_fresh_venv(venv_folder, inherit_from=remote_venv_site_packages)

    _utils.set_next_active_project(name)

    get_ipython().find_magic("edit")(f"{project_folder}/setup.py")  # noqa: F821

    print()
    print()
    print(
        f"1. please start a fresh ipython console to use the activated project {name}"
    )
    print(f"2. edit {project_folder}/setup.py")
    print("3. run 'emzed_project_update()'")
    print()


def emzed_project_activate(name=None):
    """activate (another) project"""

    name = _choose_name(name)
    if name is None:
        return
    if _utils.is_valid_project(name):
        _utils.set_next_active_project(name)
        print(
            f"please start a fresh ipython console to use the activated project {name}"
        )
        print()
    else:
        print("this project either does not exist or is corrupted")
        print()


def emzed_project_deactivate():
    """deactivate current project"""
    _utils.set_next_active_project("")
    print("please start a fresh ipython console.")
    print()


def _list_projects():
    project_names = [
        p.name
        for p in _utils.emzed_projects.iterdir()
        if _utils.is_valid_project(p.name)
    ]
    return project_names


def emzed_project_list():
    """lists emzed3 projects"""
    print()
    print("valid emzed projects:")
    for name in _list_projects():
        print(f"  - {name}")


def _resolve_name(name):
    if name is None:
        name = _utils.get_active_project()
        if name is None:
            print("you have to activate a project first of specify a name")
            print()
            return None

    if not _utils.is_valid_project(name):
        print(f"project {name} either does not exist or is corrupted")
        print()
        return None

    folder = _utils.get_project_folder(name)
    if _utils.is_valid_project(folder):
        return folder

    print(f"project folder {folder} is invalid / corrupted")
    print()
    return None


def _choose_name(name):
    if name is None:
        names = _list_projects()
        print()
        print("choose a project:")
        for i, name in enumerate(names, 1):
            print(f"  {i}: {name}")
        while True:
            try:
                index = input("(x=abort) ? ")
            except KeyboardInterrupt:
                return None
            if index == "x":
                return None
            try:
                index = int(index)
                if 1 <= index <= len(names):
                    return names[index - 1]
            except ValueError:
                pass
    return name


def _execute(cmd):
    p = _subprocess.Popen(
        cmd, shell=True, stderr=_subprocess.STDOUT, stdout=_subprocess.PIPE
    )
    for line in iter(p.stdout.readline, b""):
        print(str(line, "utf-8").rstrip())
    p.wait()  # wait until process finishes, also sets returncode
    return p.returncode


def emzed_project_update(name=None):
    """updates local project after changes of setup.py and requirements_dev.txt"""

    project_folder = _resolve_name(name)
    if project_folder is None:
        return

    python_exe = _utils.python_executable_in(project_folder / ".venv")
    _execute(f'"{python_exe}" -u -m pip install -U pip setuptools')

    pip_path = _utils.pip_in(project_folder)
    if pip_path is None:
        print(f".venv in {name} has no pip command installed")
        print("(did you run 'emzed_project_update()'?")
        print()
        return

    _execute(f'"{pip_path}" install -e "{project_folder}"')

    requirements_file = project_folder / "requirements_dev.txt"
    if requirements_file.exists():
        _execute(f'"{pip_path}" install -r "{requirements_file}"')


def emzed_project_test(name=None, *, opts="--color=yes -v"):
    """runs test suite"""

    result = _check_tests(name)
    if result is None:
        return

    pytest_path, project_folder, tests_folder = result
    _execute(f'"{pytest_path}" {opts} "{tests_folder}"')


def _check_tests(name):

    project_folder = _resolve_name(name)
    if project_folder is None:
        return

    pytest_path = _utils.pytest_in(project_folder)
    if pytest_path is None:
        print(f".venv in {project_folder} has no pytest command installed")
        print("(did you run 'emzed_project_update()'?")
        print()
        return

    tests_folder = project_folder / "tests"
    if not tests_folder.exists():
        print(f"{tests_folder} does not exist")
        print()
        return

    return pytest_path, project_folder, tests_folder


def emzed_project_test_coverage(name=None, *, opts="--color=yes -v"):
    """runs test suite and computes test coverage"""

    result = _check_tests(name)
    if result is None:
        return

    pytest_path, project_folder, tests_folder = result

    src_folder = project_folder / "src"
    html_cov_folder = project_folder / "coverage_report"

    exit_code = _execute(
        f'"{pytest_path}" {opts}'
        f' --cov="{src_folder}" --cov-report=html:"{html_cov_folder}" --cov-report=term'
        f' "{tests_folder}"'
    )

    if exit_code == 0:
        import webbrowser

        webbrowser.open(f"file://{html_cov_folder}/index.html")


def emzed_project_test_installability(name=None):
    """checks if project can be installed"""
    _emzed_project_test_installability(name)


def _emzed_project_test_installability(name):
    project_folder = _resolve_name(name)
    if project_folder is None:
        return

    pytest_path = _utils.pytest_in(project_folder)
    if pytest_path is None:
        print(f".venv in {project_folder} has no pytest command installed")
        print("(did you run 'emzed_project_update()'?")
        print()
        return

    tox_path = _utils.tox_in(project_folder)
    if tox_path is None:
        print(f".venv in {project_folder} has no tox command installed")
        print("(did you run 'emzed_project_update()'?")
        print()
        return

    return _execute(f'"{tox_path}" -v -r "{project_folder}"')


def emzed_project_install_local(name=None):
    """installs other local emzed3 project into currently active project.

    The installation is in "edit mode" such that changes in the remote project
    are directly visible in the active project
    """

    name = _choose_name(name)
    if name is None:
        return
    if not _utils.is_valid_project(name):
        print()
        print(f"project {name} is not valid")
        return

    project_folder = _utils.get_project_folder(name)

    python_exe = _utils.active_python_exe()
    _execute(f'"{python_exe}" -u -m pip install {project_folder}')


def emzed_project_build_wheel(name=None):
    """creates a wheel file which can be shipped and installed on other
    computers without the need to upload package to pypi"""

    project_folder = _resolve_name(name)
    if project_folder is None:
        return

    result = _emzed_project_test_installability(name)
    if result is None:
        return

    if _build_wheel(project_folder):
        print()
        print("something went wrong")
        return

    print()
    print(f"check {project_folder}/dist")
    print()


def _build_wheel(project_folder):
    import shutil

    python_exe = _utils.python_executable_in(project_folder / ".venv")
    shutil.rmtree(f"{project_folder}/dist", ignore_errors=True)
    return _execute(
        f'"{python_exe}" -u "{project_folder}/setup.py" bdist_wheel'
        f' -d "{project_folder}/dist"'
    )


def emzed_project_upload_test(name=None):
    """uploads package to test-pypi.org server"""

    result = _emzed_project_test_installability(name)
    if result is None:
        return

    if result != 0:
        print()
        print("your package appears to be broken.")
        return

    project_folder = _resolve_name(name)
    if _build_wheel(project_folder):
        print()
        print("something went wrong")
        return

    _run_twine(project_folder, "https://test.pypi.org/legacy/")


def emzed_project_upload(name=None):
    """uploads package to pypi.org server"""

    import re

    import requests

    result = _emzed_project_test_installability(name)
    if result is None:
        return

    if result != 0:
        print()
        print("your package appears to be broken.")
        return

    project_folder = _resolve_name(name)
    if _build_wheel(project_folder):
        print()
        print("something went wrong")
        return

    wheel_path = next((project_folder / "dist").iterdir())
    version_tag = re.findall(r"\d+\.\d+\.\d+", str(wheel_path))

    if not version_tag or len(version_tag) > 1:
        print()
        print(f"can not parse version tag of {wheel_path}")
        return

    pypi_test_url = (
        "https://test.pypi.org/project/"
        f"emzed_ext_{project_folder.name}/{version_tag[0]}"
    )
    response = requests.get(pypi_test_url)

    if response.status_code != 200:
        print()
        print("did you upload to pypi test server using project_upload_test() already?")
        print(f"... access to {pypi_test_url} failed")
        return

    _run_twine(project_folder)


def _run_twine(project_folder, url=None):

    if url is not None:
        repository = f"--repository-url {url}"
    else:
        repository = ""

    twine_exe = _utils.twine_in(project_folder)

    while True:

        answer = _ask_user_and_password()
        if answer is None:
            return

        user, password = answer

        result = _execute(
            f"{twine_exe} upload -u {user} -p {password} {repository}"
            f' "{project_folder}/dist/*"'
        )

        if result == 0:
            print()
            print("done.")
            return

        print()
        print("twine upload failed. possible causes: ")
        print("   1. your username / password did not match")
        print(
            "   2. the package with the same version number was already uploaded before"
        )
        print("read the error messages above to understand your issue better.")
        print()

        while True:
            again = _ask_nonempty("do you want to try again (y/n)? ")
            if again[0] in "nN":
                return
            if again[0] in "yY":
                break


def _ask_user_and_password():
    import getpass

    print()
    print("you need and user accout and pypi.org to upload a package.")

    user = _ask_nonempty("pypi user (x=abort)? ")
    if user == "x":
        return

    password = _ask_nonempty("pypi password (x=abort)? ", getpass.getpass)
    if password == "x":
        return

    return user, password


def _ask_nonempty(message, _input=None):
    while True:

        if _input is None:
            answer = input(message).strip()
        else:
            answer = _input(prompt=message).strip()

        if answer:
            return answer
