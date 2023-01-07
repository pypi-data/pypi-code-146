from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from sys import executable


def get_package_dir() -> Path:
    return Path(__file__).parent


def get_project_dir() -> Path:
    return get_package_dir().parent


def build_package():
    run([executable, "-m", "build", get_project_dir()], check=True, text=True)


def deploy():
    build_package()


def freeze_requirements():
    print("FREEZE")


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
