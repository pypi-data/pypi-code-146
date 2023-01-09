# !/usr/bin/python3
import argparse
from argparse import Namespace
import os
import subprocess
from urllib.parse import urlparse
import sys
from string import Template
import warnings
import tempfile

from . import __version__


def format_str_with_character(s: str):
    max_str_len = 120

    prefix = f'{"+" * 20} {s} '

    suffix_character_len = max_str_len - len(prefix) - 1

    return f'{prefix} {"+" * suffix_character_len}'


def src_dir_path(path):
    if os.path.isdir(path):
        abs_path = os.path.abspath(path)
        files = os.listdir(path)
        if "serving.py" not in files:
            raise argparse.ArgumentTypeError(
                f"serving.py file not found in dir path {abs_path}"
            )

        if "requirements.txt" not in files:
            raise argparse.ArgumentTypeError(
                f"requirements.txt file not found in dir path {abs_path}"
            )

        return abs_path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


dockerfile_string_template = Template(
    """
# 版本跟随 metaai
FROM --platform=linux/amd64 registry.cn-hangzhou.aliyuncs.com/metaai/python-metaai:${metaai_version} as dependencies

ARG PYPI_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
ARG TRUSTED_HOST="pypi.tuna.tsinghua.edu.cn"

WORKDIR /build

COPY ./requirements.txt ./

RUN python3 -m pip config set global.index-url $PYPI_INDEX \
  && python3 -m pip config set global.trusted-host $TRUSTED_HOST \
  && python3 -m pip install --upgrade pip --no-cache-dir \
  && python3 -m pip install -r ./requirements.txt --no-cache-dir \
  && rm /build -rf


FROM dependencies as app

WORKDIR /app

COPY . /app


EXPOSE 8089

CMD ["python3", "serving.py"]
"""
)


def main():
    print(
        format_str_with_character(f"current metaai cli script version is {__version__}")
    )

    dockerfile_string = dockerfile_string_template.safe_substitute(
        {"metaai_version": __version__}
    )

    parser = argparse.ArgumentParser(
        prog="METAAI",
        usage="cli script for metaai",
        description="Provides some command-line functions of the service metaai",
    )

    sub_parser = parser.add_subparsers(
        title="metaai cli subcommands",
    )

    serving_build = sub_parser.add_parser(
        "serving-build",
        help="build serving predict image and batch predict image",
    )

    serving_build.add_argument(
        "-t",
        dest="tag",
        type=str,
        required=True,
        help="build docker image's tag",
    )

    serving_build.add_argument(
        "-s",
        dest="src_path",
        required=True,
        type=src_dir_path,
        help="source code path",
    )

    serving_build.add_argument(
        "--pypi_index",
        dest="pypi_index",
        help="pypi index for pip install，default use 'pypi.tuna.tsinghua.edu.cn' ",
    )

    known_args, _ = parser.parse_known_args()
    if known_args == Namespace():
        parser.parse_args(["--help"])

    # check docker version
    print(format_str_with_character("checking docker version"))

    docker_version = subprocess.Popen(
        "docker version -f {{.Server.Version}}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    min_docker_version_required = (20, 10, 14)

    try:
        local_docker_version = (
            docker_version.stdout.readline().decode("utf-8").splitlines()[0]
        )

        print(
            format_str_with_character(
                f"local current docker server version: {local_docker_version}"
            )
        )

    except Exception as e:
        raise SystemExit(f"parser docker version raise error,msg {e}")
    else:
        local_docker_version = tuple(int(i) for i in local_docker_version.split("."))
        if min_docker_version_required > local_docker_version:
            str_version = ".".join(str(i) for i in min_docker_version_required)
            warnings.warn(f"recommended that docker version be gte {str_version}")

    pypi_index = known_args.pypi_index

    build_args_command = ""
    if pypi_index:
        build_args_command = (
            f"--build-arg PYPI_INDEX={pypi_index} "
            f"--build-arg TRUSTED_HOST={urlparse(pypi_index).netloc}"
        )

    tmp_fp = tempfile.NamedTemporaryFile()
    tmp_fp.write(dockerfile_string.encode())
    tmp_fp.seek(0)

    docker_build_cmd_string = (
        f"docker build -t {known_args.tag} {build_args_command}"
        f"-f {tmp_fp.name} {known_args.src_path}"
    )
    print(docker_build_cmd_string)

    docker_builder = subprocess.Popen(
        docker_build_cmd_string,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    docker_builder.communicate()


if __name__ == "__main__":
    main()
