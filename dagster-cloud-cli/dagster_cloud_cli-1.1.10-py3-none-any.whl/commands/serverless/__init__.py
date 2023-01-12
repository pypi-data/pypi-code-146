import base64
import os
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional

import pkg_resources
import typer
from typer import Argument, Option, Typer

from dagster_cloud_cli import gql, pex_utils, ui, version
from dagster_cloud_cli.commands.workspace import wait_for_load
from dagster_cloud_cli.config_utils import (
    DEPLOYMENT_CLI_OPTIONS,
    dagster_cloud_options,
    get_location_document,
)
from dagster_cloud_cli.core import pex_builder
from dagster_cloud_cli.utils import add_options

app = Typer(help="Build and deploy your code to Dagster Cloud.")

_BUILD_OPTIONS = {
    "source_directory": (
        Path,
        Option(
            None,
            "--source-directory",
            "-d",
            exists=False,
            help="Source directory to build for the image.",
        ),
    ),
    "base_image": (
        str,
        Option(None, "--base-image", exists=False),
    ),
    "env": (
        List[str],
        Option(
            [],
            "--env",
            exists=False,
            help="Environment variable to be defined in image, in the form of `MY_ENV_VAR=hello`",
        ),
    ),
}

DEPLOY_DOCKER_OPTIONS = {
    "image": (
        str,
        Option(
            None,
            "--image",
            exists=False,
            help="Override built Docker image tag. Should not be needed outside of debugging.",
            hidden=True,
        ),
    ),
    "base_image": (
        str,
        Option(None, "--base-image", exists=False, help="Custom base image"),
    ),
    "env": (
        List[str],
        Option(
            [],
            "--env",
            exists=False,
            help="Environment variable to be defined in image, in the form of `MY_ENV_VAR=hello`",
        ),
    ),
}


@contextmanager
def _template_dockerfile(env_vars, custom_base_image=None):
    DOCKERFILE_TEMPLATE = pkg_resources.resource_filename(
        "dagster_cloud_cli", "commands/serverless/Dockerfile"
    )
    base_image_command = (
        f"FROM {custom_base_image}" if custom_base_image else "FROM python:3.8-slim"
    )
    with open(DOCKERFILE_TEMPLATE, "r", encoding="utf-8") as template:
        dockerfile_content = "\n".join(
            [base_image_command, template.read(), *[f"ENV {env_var}" for env_var in env_vars]]
        )

        yield bytes(dockerfile_content, "utf-8")


def _build_image(source_directory, image, registry_info, env_vars, base_image):
    registry = registry_info["registry_url"]
    with _template_dockerfile(env_vars, base_image) as dockerfile_content:
        cmd = [
            "docker",
            "build",
            source_directory,
            "-t",
            f"{registry}:{image}",
            "-f",
            "-",
            "--platform",
            "linux/amd64",
        ]
        return subprocess.run(cmd, input=dockerfile_content, check=True).returncode


@app.command(name="build", short_help="Build image for Dagster Cloud code location.", hidden=True)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(_BUILD_OPTIONS)
def build_command(
    api_token: str,
    url: str,
    location_load_timeout: int,  # pylint: disable=unused-argument
    agent_heartbeat_timeout: int,  # pylint: disable=unused-argument
    image: str = Argument(None, help="Image name."),
    **kwargs,
):
    """Add or update the image for a code location in the workspace."""
    source_directory = str(kwargs.get("source_directory"))
    base_image = kwargs.get("base_image")
    env_vars = kwargs.get("env", [])
    _verify_docker()

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]

        if base_image and not ecr_info.get("allow_custom_base"):
            ui.warn("Custom base images are not enabled for this organization.")
            base_image = None

        retval = _build_image(source_directory, image, ecr_info, env_vars, base_image)
        if retval == 0:
            ui.print(f"Built image {registry}:{image}")


def _upload_image(image, registry_info):
    registry = registry_info["registry_url"]
    aws_token = registry_info["aws_auth_token"]
    if not registry or not aws_token:
        raise ui.error(
            "No registry found. You may need to wait for your Dagster serverless deployment to"
            " activate."
        )

    username, password = base64.b64decode(aws_token).decode("utf-8").split(":")
    subprocess.check_output(
        (
            f"echo {str(password)} | docker login --username {str(username)} --password-stdin"
            f" {registry}"
        ),
        shell=True,
    )
    return subprocess.call(
        ["docker", "push", f"{registry}:{image}"], stderr=sys.stderr, stdout=sys.stdout
    )


@app.command(
    name="upload",
    short_help="Upload the built code location image to Dagster Cloud's image repository.",
    hidden=True,
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def upload_command(
    api_token: str,
    url: str,
    location_load_timeout: int,  # pylint: disable=unused-argument
    agent_heartbeat_timeout: int,  # pylint: disable=unused-argument
    image: str = Argument(None, help="Image name."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a code location in the workspace."""

    _verify_docker()

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]
        retval = _upload_image(image, ecr_info)
        if retval == 0:
            ui.print(f"Pushed image {image} to {registry}")


@app.command(
    name="registry-info",
    short_help="Get registry information and temporary creds for an image repository",
    hidden=True,
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def registry_info_command(
    api_token: str,
    url: str,
    location_load_timeout: int,  # pylint: disable=unused-argument
    agent_heartbeat_timeout: int,  # pylint: disable=unused-argument
    **kwargs,  # pylint: disable=unused-argument
):
    """Add or update the image for a code location in the workspace. Used by GH action to
    authenticate to the image registry"""

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry_url = ecr_info["registry_url"]
        aws_region = ecr_info.get("aws_region", "us-west-2")
        aws_token = ecr_info["aws_auth_token"]
        custom_base_image_allowed = ecr_info["allow_custom_base"]

        if not aws_token or not registry_url:
            return

        username, password = base64.b64decode(aws_token).decode("utf-8").split(":")

        values = [
            f"REGISTRY_URL={registry_url}",
            f"AWS_DEFAULT_REGION={aws_region}",
            f"AWS_ECR_USERNAME={username}",
            f"AWS_ECR_PASSWORD={password}",
        ]
        if custom_base_image_allowed:
            values.append("CUSTOM_BASE_IMAGE_ALLOWED=1")
        ui.print("\n".join(values) + "\n")


@app.command(name="deploy", short_help="Alias for 'deploy-docker'.", hidden=True)
@app.command(
    name="deploy-docker",
    short_help=(
        "Add a code location from a local directory, deployed as a Docker image. "
        "Also see 'deploy-python-executable' as an alternative deployment method."
    ),
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(DEPLOY_DOCKER_OPTIONS)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def deploy_command(
    api_token: str,
    url: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    deployment: str,
    source_directory: Path = Argument(".", help="Source directory."),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add a code location from a local directory, deployed as a Docker image."""

    location_name = kwargs.get("location_name")
    if not location_name:
        raise ui.error(
            "No location name provided. You must specify the location name as an argument."
        )

    if not source_directory:
        raise ui.error("No source directory provided.")

    _check_source_directory(source_directory)
    _verify_docker()

    env_vars = kwargs.get("env", [])
    base_image = kwargs.get("base_image")

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]

        commit_hash = kwargs.get("commit_hash") or str(uuid.uuid4().hex)
        default_image_tag = f"{deployment}-{location_name}-{commit_hash}"
        image_tag = kwargs.get("image") or default_image_tag

        retval = _build_image(source_directory, image_tag, ecr_info, env_vars, base_image)
        if retval != 0:
            return

        retval = _upload_image(image_tag, ecr_info)
        if retval != 0:
            return

        location_args = {**kwargs, "image": f"{registry}:{image_tag}"}
        location_document = get_location_document(location_name, location_args)
        gql.add_or_update_code_location(client, location_document)

        wait_for_load(
            client,
            [location_name],
            location_load_timeout=location_load_timeout,
            agent_heartbeat_timeout=agent_heartbeat_timeout,
            url=url,
        )

        workspace_url = f"{url}/workspace"
        ui.print(
            f"Added or updated location {location_name}. "
            f"View the status of your workspace at {workspace_url}."
        )


@app.command(
    name="upload-base-image",
    short_help=(
        "Upload a local Docker image to Dagster cloud, to use as a custom base image for"
        " deploy-python-executable."
    ),
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
def upload_base_image_command(
    api_token: str,
    url: str,
    local_image: str = Argument(..., help="Pre-built local image, eg. 'local-image:local-tag'"),
    published_tag: str = Option(
        None,
        help=(
            "Published tag used to identify this image in Dagster Cloud. "
            "A tag is auto-generated if not provided."
        ),
    ),
):
    if not published_tag:
        published_tag = _generate_published_tag_for_image(local_image)

    with gql.graphql_client_from_url(url, api_token) as client:
        ecr_info = gql.get_ecr_info(client)
        registry = ecr_info["registry_url"]
        published_image = f"{registry}:{published_tag}"

        # tag local image with new tag
        cmd = [
            "docker",
            "tag",
            local_image,
            published_image,
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as err:
            raise ui.error(
                f"Error tagging local image {local_image}: " + err.stderr.decode("utf-8")
            )

        # upload tagged image
        retval = _upload_image(image=published_tag, registry_info=ecr_info)
        if retval == 0:
            ui.print(f"Pushed image {published_tag} to {registry}.")
            ui.print(
                "To use the uploaded image run: "
                f"dagster-cloud deploy-python-executable --base-image-tag={published_tag} [ARGS]"
            )


def _generate_published_tag_for_image(image: str):
    image_id = subprocess.check_output(["docker", "inspect", image, "--format={{.Id}}"])
    #  The id is something like 'sha256:518ad2f92b078c63c60e89f0310f13f19d3a1c7ea9e1976d67d59fcb7040d0d6'
    return image_id.decode("utf-8").replace(":", "_").strip()


@app.command(name="build-python-executable", short_help="Build a Python Executable", hidden=True)
def build_python_executable_command(
    code_directory: str,
    output_directory: str,
    python_version: str = typer.Option("3.8", help="Target Python version as 'major.minor'"),
):
    parsed_python_version = pex_builder.util.parse_python_version(python_version)
    code_directory = os.path.abspath(code_directory)
    output_directory = os.path.abspath(output_directory)

    local_packages, requirements = pex_builder.deps.get_deps_requirements(
        code_directory=code_directory, python_version=parsed_python_version
    )

    ui.print("Building source...")
    source_path = pex_builder.source.build_source_pex(
        code_directory,
        local_package_paths=local_packages.local_package_paths,
        output_directory=output_directory,
        python_version=parsed_python_version,
    )
    ui.print(f"Built {source_path}")
    ui.print(f" - {code_directory}")
    for local_path in local_packages.local_package_paths:
        ui.print(f" - {local_path}")

    ui.print("Building dependencies...")
    deps_path, dagster_version = pex_builder.deps.build_deps_from_requirements(
        requirements,
        output_directory=output_directory,
    )
    ui.print(f"Built {deps_path} with Dagster {dagster_version}")
    for line in sorted(requirements.requirements_txt.splitlines(keepends=False)):
        print(f" - {line}")


@app.command(
    name="deploy-python-executable",
    short_help=(
        "[Fast Deploys] Add a code location from a local directory, deployed as a Python"
        " executable. Also see 'deploy-docker' as an alternative deployment method."
    ),
)
@dagster_cloud_options(allow_empty=True, requires_url=True)
@add_options(pex_utils.DEPLOY_PEX_OPTIONS)
@add_options(DEPLOYMENT_CLI_OPTIONS)
def deploy_python_executable_command(
    api_token: str,
    url: str,
    location_load_timeout: int,
    agent_heartbeat_timeout: int,
    source_directory: Path = Argument(".", help="Source directory."),
    build_in_linux_docker: bool = Option(
        False,
        help=(
            "Build the Python executable within a Linux Docker environment. This is useful if some"
            " of the dependencies require a Linux build environment and you are running on"
            " another OS."
        ),
    ),
    **kwargs,  # pylint: disable=unused-argument
):
    """Add a code location from a local directory, deployed as a Python executable."""

    location_name = kwargs.get("location_name")
    if not location_name:
        raise ui.error(
            "No location name provided. You must specify the location name as an argument."
        )

    if not source_directory:
        raise ui.error("No source directory provided.")

    _check_source_directory(source_directory)

    # If requested, forward this command to run in a Linux docker
    if build_in_linux_docker and not os.getenv("DAGSTER_CLOUD_CLI_IN_DOCKER"):
        if sys.platform == "linux":
            ui.warn("Running in Linux but '--build-in-linux-docker' still requested.")

        ui.print("Preparing to run deploy-python-executable within a Linux docker environment.")
        _verify_docker()

        # sanity check the args
        if sys.argv[1:3] != ["serverless", "deploy-python-executable"]:
            found_cmd = " ".join(sys.argv[1:3])
            raise ui.error(
                "Cannot forward command, expected 'serverless deploy-python-executable', "
                f"found {found_cmd!r}"
            )
        forward_args = sys.argv[4:]  # everything after 'deploy-python-executable'
        if "--build-in-linux-docker" in forward_args:
            forward_args.remove("--build-in-linux-docker")

        # DAGSTER_CLOUD_CLI_DOCKER_VERSION is useful in any dev environment
        dagster_cloud_cli_version = os.getenv(
            "DAGSTER_CLOUD_CLI_DOCKER_VERSION", version.__version__
        )
        linux_docker_image = _get_linux_docker_image_for_build(
            dagster_cloud_cli_version, kwargs["python_version"]
        )
        _run_command_in_docker(
            linux_docker_image,
            map_folders={"/source_dir": os.path.abspath(source_directory)},
            run_args=["serverless", "deploy-python-executable", "/source_dir", *forward_args],
        )
    else:
        kwargs = pex_utils.build_upload_pex(
            url=url,
            api_token=api_token,
            location=location_name,
            python_source_dir=source_directory,
            kwargs=kwargs,
        )
        with gql.graphql_client_from_url(url, api_token) as client:
            location_document = get_location_document(location_name, kwargs)
            gql.add_or_update_code_location(client, location_document)

            wait_for_load(
                client,
                [location_name],
                location_load_timeout=location_load_timeout,
                agent_heartbeat_timeout=agent_heartbeat_timeout,
                url=url,
            )

            workspace_url = f"{url}/workspace"
            ui.print(
                f"Added or updated location {location_name}. "
                f"View the status of your workspace at {workspace_url}."
            )


def _get_linux_docker_image_for_build(
    dagster_cloud_cli_version: str, python_version: str = "3.8"
) -> str:
    # Builds a `dagster-cloud-cli:<version>` image if not present.
    dockerfile_path = pkg_resources.resource_filename(
        "dagster_cloud_cli", "commands/serverless/Dockerfile.dagster-cloud-cli"
    )
    base_image = f"FROM python:{python_version}-slim\n"
    dockerfile_content = base_image + open(dockerfile_path, "r", encoding="utf-8").read()

    if dagster_cloud_cli_version == "1!0+dev":
        # use the local dev version of dagster cloud
        dockerfile_dir = str(Path(__file__).parents[4])
        dockerfile_content = dockerfile_content.replace("# dev: ", "")
        dagster_cloud_dependency = "dagster-cloud-cli @ file:///dagster-cloud-cli"
        dagster_cloud_cli_image = f"dagster-cloud-cli-py{python_version}:dev"
    else:
        dockerfile_dir, _ = os.path.split(dockerfile_path)
        dagster_cloud_dependency = f"dagster_cloud=={dagster_cloud_cli_version}"
        dagster_cloud_cli_image = (
            f"dagster-cloud-cli-py{python_version}:{dagster_cloud_cli_version}"
        )

    if not _image_exists(dagster_cloud_cli_image):
        ui.print(f"Building Docker image: {dagster_cloud_cli_image}")

        proc = _build_local_image(
            dagster_cloud_cli_image,
            dockerfile_dir,
            dockerfile_content.encode("utf-8"),
            {"DAGSTER_CLOUD_DEPENDENCY": dagster_cloud_dependency},
        )
        if proc.returncode:
            raise ui.error(f"Could not build Docker image: {dagster_cloud_cli_image}")
    else:
        ui.print(f"Found existing Docker image: {dagster_cloud_cli_image}")

    return dagster_cloud_cli_image


def _run_command_in_docker(
    dagster_cloud_cli_image, map_folders: Dict[str, str], run_args: List[str]
):
    # Runs a dagster-cloud cli command in a Docker container using the same version and args
    # as the current dagster-cloud.
    # Useful when a Linux environment is needed for a command.
    ui.print(f"Running image {dagster_cloud_cli_image} with {' '.join(run_args)!r}")

    map_folders = map_folders.copy()
    dot_dagster_cloud_cli_path = os.path.expanduser("~/.dagster_cloud_cli")
    if os.path.exists(dot_dagster_cloud_cli_path):
        map_folders["/dot_dagster_cloud_cli"] = dot_dagster_cloud_cli_path

    ui.print("Mapped folders:")
    for target_dir, source_dir in map_folders.items():
        ui.print(f" - {source_dir} -> {target_dir}")

    proc = _run_docker_image(
        dagster_cloud_cli_image,
        map_folders,
        env={"DAGSTER_CLOUD_URL": None, "DAGSTER_CLOUD_API_TOKEN": None},
        run_args=run_args,
    )
    return proc


def _run_docker_image(
    image_name, map_folders: Dict[str, str], env: Dict[str, Optional[str]], run_args: List[str]
):
    mount_args = []
    for target_folder, source_folder in map_folders.items():
        mount_args.extend(["--mount", f"type=bind,source={source_folder},target={target_folder}"])

    env_args = []
    for env_name, env_value in env.items():
        if env_value is None:
            # specifying just the name copies the env from the calling environment
            env_args.extend(["--env", env_name])
        else:
            env_args.extend(["--env", f"{env_name}={env_value}"])

    cmd = ["docker", "run", "--platform=linux/amd64", *env_args, *mount_args, image_name, *run_args]
    return subprocess.run(cmd, check=False)


def _image_exists(image_name):
    try:
        subprocess.check_output(["docker", "inspect", image_name], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def _build_local_image(image_name, dockerfile_dir, dockerfile_content, build_args: Dict[str, str]):
    # build a docker image with dagster-cloud
    docker_build_args = []
    for build_arg_name, build_arg_value in build_args.items():
        docker_build_args.append(f"--build-arg={build_arg_name}={build_arg_value}")

    cmd = [
        "docker",
        "build",
        dockerfile_dir,
        "-f",
        "-",
        "-t",
        image_name,
        "--platform",
        "linux/amd64",
        *docker_build_args,
    ]
    return subprocess.run(cmd, input=dockerfile_content, check=False)


def _verify_docker():
    if subprocess.call("docker -v", shell=True) != 0:
        raise ui.error("Docker must be installed locally to deploy to Dagster Cloud Serverless")


SOURCE_INSTRUCTIONS = (
    "You can specify the directory you want to deploy by using the `--source-directory` argument "
    "(defaults to current directory)."
)


def _check_source_directory(source_directory):
    contents = os.listdir(source_directory)

    if "setup.py" not in contents and "requirements.txt" not in contents:
        message = (
            "Could not find a `setup.py` or `requirements.txt` in the target directory. You must "
            "specify your required Python dependencies (including the `dagster-cloud` package) "
            "along with your source files to deploy to Dagster Cloud."
        )
        if source_directory == ".":
            message = f"{message} {SOURCE_INSTRUCTIONS}"
        raise ui.error(message)
