from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from sys import executable
from shutil import rmtree


def get_package_dir() -> Path:
    return Path(__file__).parent


def get_project_dir() -> Path:
    return get_package_dir().parent


def get_requirements_path() -> Path:
    return get_project_dir() / "requirements.txt"


def build_package():
    run([executable, "-m", "build", get_project_dir()], check=True, text=True)


def get_dist_dir() -> Path:
    return get_project_dir() / "dist"


def clean_distributions():
    rmtree(get_dist_dir())


def get_distributions() -> list[Path]:
    dist_dir = get_dist_dir()
    return [dist_dir / dist for dist in dist_dir.iterdir()]


def upload_distributions():
    run(
        [
            executable,
            "-m",
            "twine",
            "upload",
            "--non-interactive",
            *get_distributions(),
        ],
        check=True,
    )


def deploy():
    clean_distributions()
    build_package()
    upload_distributions()


def freeze_requirements():
    requirements = run(
        [executable, "-m", "pip", "freeze", "--all", "--exclude-editable"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    with open(get_requirements_path(), "w") as requirements_file:
        requirements_file.write(requirements)


def main():
    parser = ArgumentParser()
    main_subparsers = parser.add_subparsers(dest="main")

    main_subparsers.add_parser("deploy")
    main_subparsers.add_parser("freeze-requirements")

    args = parser.parse_args()

    function = globals()[args.main.replace("-", "_")]

    function()


if __name__ == "__main__":
    main()
