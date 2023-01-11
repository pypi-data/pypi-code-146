from contextlib import contextmanager
from copy import deepcopy
import datetime
import ipaddress
import logging
import os
import random
import string
import sys
import time
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    Generator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)
from urllib.parse import quote as quote_sanitize, urlencode, urljoin
import webbrowser

import boto3
from boto3.resources.base import ServiceResource as Boto3Resource
from botocore.config import Config
from botocore.exceptions import ClientError, NoRegionError
import click
from packaging import version
import requests
from requests import Response
import yaml

from anyscale.authenticate import get_auth_api_client
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.api.default_api import DefaultApi as ProductApi
from anyscale.client.openapi_client.models.decorated_compute_template import (
    DecoratedComputeTemplate,
)
from anyscale.client.openapi_client.models.user_info import UserInfo
from anyscale.cluster_compute import get_cluster_compute_from_name
import anyscale.conf
from anyscale.conf import MINIMUM_RAY_VERSION
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi as BaseApi
from anyscale.sdk.anyscale_client.models.compute_template import ComputeTemplate
import anyscale.shared_anyscale_utils.conf as shared_anyscale_conf
from anyscale.shared_anyscale_utils.util import get_container_name


logger = logging.getLogger(__file__)

BOTO_MAX_RETRIES = 5
PROJECT_NAME_ENV_VAR = "ANYSCALE_PROJECT_NAME"

VALID_BYOD_PYTHON_VERSIONS = ["py36", "py37", "py38", "py39"]

log = BlockLogger()  # Anyscale CLI Logger

VPC_CIDR_RANGE = "10.0.0.0/16"

DEFAULT_RAY_VERSION = "1.7.0"


def confirm(msg: str, yes: bool) -> Optional[bool]:
    return None if yes else click.confirm(msg, abort=True)


class AnyscaleEndpointFormatter:
    def __init__(self, host: Optional[str] = None):
        self.host = host or shared_anyscale_conf.ANYSCALE_HOST

    def get_endpoint(self, endpoint: str) -> str:
        return str(urljoin(self.host, endpoint))

    def get_job_endpoint(self, job_id: str) -> str:
        return self.get_endpoint(f"/jobs/{job_id}")

    def get_schedule_endpoint(self, schedule_id: str) -> str:
        return self.get_endpoint(f"/scheduled-jobs/{schedule_id}")


def get_endpoint(endpoint: str, host: Optional[str] = None) -> str:
    return str(urljoin(host or shared_anyscale_conf.ANYSCALE_HOST, endpoint))


def send_json_request_raw(
    endpoint: str,
    json_args: Dict[str, Any],
    method: str = "GET",
    cli_token: Optional[str] = None,
    host: Optional[str] = None,
) -> Response:
    get_auth_api_client(cli_token=cli_token, host=host)

    url = get_endpoint(endpoint, host=host)
    cookies = {"cli_token": cli_token or anyscale.conf.CLI_TOKEN or ""}
    try:
        if method == "GET":
            resp = requests.get(url, params=json_args, cookies=cookies)
        elif method == "POST":
            resp = requests.post(url, json=json_args, cookies=cookies)
        elif method == "DELETE":
            resp = requests.delete(url, json=json_args, cookies=cookies)
        elif method == "PATCH":
            resp = requests.patch(url, data=json_args, cookies=cookies)
        elif method == "PUT":
            resp = requests.put(url, json=json_args, cookies=cookies)
        else:
            raise AssertionError("unknown method {}".format(method))
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Failed to connect to anyscale server at {}".format(url)
        )

    return resp


def send_json_request(
    endpoint: str,
    json_args: Dict[str, Any],
    method: str = "GET",
    cli_token: Optional[str] = None,
    host: Optional[str] = None,
) -> Dict[str, Any]:
    resp = send_json_request_raw(
        endpoint, json_args, method=method, cli_token=cli_token, host=host,
    )

    if not resp.ok:
        if resp.status_code == 500:
            raise click.ClickException(
                "There was an internal error in this command. "
                "Please report this to the Anyscale team at support@anyscale.zendesk.com "
                "with the token '{}'.".format(resp.headers["x-trace-id"])
            )

        raise click.ClickException("{}: {}.".format(resp.status_code, resp.text))

    if resp.status_code == 204:
        return {}

    json_resp: Dict[str, Any] = resp.json()
    if "error" in json_resp:
        raise click.ClickException("{}".format(json_resp["error"]))

    return json_resp


def deserialize_datetime(s: str) -> datetime.datetime:
    if sys.version_info < (3, 7) and s[-3:-2] == ":":
        s = s[:-3] + s[-2:]

    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")


def humanize_timestamp(timestamp: datetime.datetime) -> str:
    delta = datetime.datetime.now(datetime.timezone.utc) - timestamp
    offset = float(delta.seconds + (delta.days * 60 * 60 * 24))
    delta_s = int(offset % 60)
    offset /= 60
    delta_m = int(offset % 60)
    offset /= 60
    delta_h = int(offset % 24)
    offset /= 24
    delta_d = int(offset)

    if delta_d >= 1:
        return "{} day{} ago".format(delta_d, "s" if delta_d > 1 else "")
    if delta_h > 0:
        return "{} hour{} ago".format(delta_h, "s" if delta_h > 1 else "")
    if delta_m > 0:
        return "{} minute{} ago".format(delta_m, "s" if delta_m > 1 else "")
    else:
        return "{} second{} ago".format(delta_s, "s" if delta_s > 1 else "")


def get_cluster_config(config_path: str) -> Dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_requirements(requirements_path: str) -> str:
    with open(requirements_path) as f:
        return f.read()


def _resource(name: str, region: str) -> Boto3Resource:
    boto_config = Config(retries={"max_attempts": BOTO_MAX_RETRIES})
    return boto3.resource(name, region, config=boto_config)  # type: ignore


def _client(name: str, region: str) -> Any:
    return _resource(name, region).meta.client


def _get_role(role_name: str, region: str) -> Optional[Boto3Resource]:
    iam = _resource("iam", region)
    role = iam.Role(role_name)  # type: ignore
    try:
        role.load()
        return role  # type: ignore
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def _get_subnet(subnet_arn: str, region: str) -> Optional[Boto3Resource]:
    ec2 = _resource("ec2", region)  # TODO: take a resource as an argument
    subnet = ec2.Subnet(subnet_arn)  # type: ignore
    try:
        subnet.load()
        return subnet  # type: ignore
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidSubnetID.NotFound":
            return None
        raise e


def get_available_regions() -> List[str]:
    try:
        client = boto3.client("ec2")
    except NoRegionError:
        # If there is no region, default to `us-west-2`
        client = boto3.client("ec2", region_name="us-west-2")
    return [region["RegionName"] for region in client.describe_regions()["Regions"]]


def get_availability_zones(region: str) -> List[str]:
    client = boto3.client("ec2", region_name=region)
    return [
        region["ZoneName"]
        for region in client.describe_availability_zones()["AvailabilityZones"]
    ]


def launch_gcp_cloud_setup(
    name: str,
    region: str,
    is_k8s: Optional[bool],
    folder_id: Optional[int],
    vpc_peering_ip_range: Optional[str],
    vpc_peering_target_project_id: Optional[str],
    vpc_peering_target_vpc_id: Optional[str],
) -> None:
    # TODO: enforce uniqueness for user's clouds
    quote_safe_name = quote_sanitize(name, safe="")
    query_params: Dict[str, Any] = {
        "region": region,
    }
    if is_k8s is not None:
        query_params["is_k8s"] = is_k8s
    if folder_id:
        query_params["folder_id"] = str(folder_id)
    if (
        vpc_peering_ip_range
        and vpc_peering_target_project_id
        and vpc_peering_target_vpc_id
    ):
        query_params.update(
            {
                "vpc_peering_ip_range": vpc_peering_ip_range,
                "vpc_peering_target_project_id": vpc_peering_target_project_id,
                "vpc_peering_target_vpc_id": vpc_peering_target_vpc_id,
            }
        )
    # TODO: Replace this with a proper endpoint
    endpoint = f"/api/v2/clouds/gcp/create/{quote_safe_name}?{urlencode(query_params)}"
    full_url = get_endpoint(endpoint)
    print(
        f"Launching GCP Oauth Flow:\n{full_url}\n(If this window does not auto-launch, use the link above)"
    )
    webbrowser.open(full_url)


def get_project_directory_name(project_id: str, api_client: ProductApi = None) -> str:
    if api_client is None:
        api_client = get_auth_api_client().api_client

    # TODO (yiran): return error early if project doesn't exist.
    resp = api_client.get_project_api_v2_projects_project_id_get(project_id)
    directory_name = resp.result.directory_name
    assert len(directory_name) > 0, "Empty directory name found."
    return cast(str, directory_name)


def get_working_dir(
    cluster_config: Dict[str, Any], project_id: str, api_client: ProductApi = None
) -> str:
    working_dir: Optional[str] = (
        cluster_config.get("metadata", {}).get("anyscale", {}).get("working_dir")
    )
    if working_dir:
        return working_dir
    else:
        return f"/home/ray/{get_project_directory_name(project_id, api_client)}"


def get_wheel_url(
    ray_commit: str,
    ray_version: str,
    py_version: Optional[str] = None,
    sys_platform: Optional[str] = None,
) -> str:
    """Return S3 URL for the given release spec or 'latest'."""
    if py_version is None:
        py_version = "".join(str(x) for x in sys.version_info[0:2])
    if sys_platform is None:
        sys_platform = sys.platform

    if sys_platform == "darwin":
        if py_version == "38":
            platform = "macosx_10_15_x86_64"
        else:
            platform = "macosx_10_15_intel"
    elif sys_platform == "win32":
        platform = "win_amd64"
    else:
        platform = "manylinux2014_x86_64"

    if py_version == "38":
        py_version_malloc = py_version
    else:
        py_version_malloc = f"{py_version}m"

    if "dev" in ray_version:
        ray_release = f"master/{ray_commit}"
    else:
        ray_release = f"releases/{ray_version}/{ray_commit}"
    return (
        "https://s3-us-west-2.amazonaws.com/ray-wheels/"
        "{}/ray-{}-cp{}-cp{}-{}.whl".format(
            ray_release, ray_version, py_version, py_version_malloc, platform
        )
    )


@contextmanager
def updating_printer() -> Generator[Callable[[str], None], None, None]:
    import shutil

    cols, _ = shutil.get_terminal_size()

    def print_status(status: str) -> None:
        lines = status.splitlines()
        first_line = lines[0]
        truncated_first_line = (
            first_line[0:cols]
            if len(first_line) <= cols and len(lines) == 1
            else (first_line[0 : cols - 3] + "...")
        )
        # Clear the line first
        print("\r" + " " * cols, end="\r")
        print(truncated_first_line, end="", flush=True)

    try:
        yield print_status
    finally:
        # Clear out the status and return to the beginning to reprint
        print("\r" + " " * cols, end="\r", flush=True)


def wait_for_session_start(
    project_id: str,
    session_name: str,
    api_client: Optional[ProductApi] = None,
    log: BlockLogger = log,
    block_label: Optional[str] = None,
) -> str:
    if block_label:
        log.info(
            f"Waiting for cluster {BlockLogger.highlight(session_name)} to start. This may take a few minutes",
            block_label=block_label,
        )
    else:
        log.info(
            f"Waiting for cluster {session_name} to start. This may take a few minutes"
        )

    if api_client is None:
        api_client = get_auth_api_client().api_client

    with updating_printer() as print_status:
        while True:
            sessions = api_client.list_sessions_api_v2_sessions_get(
                project_id=project_id, name=session_name, active_only=False
            ).results

            if len(sessions) > 0:
                session = sessions[0]

                # TODO: Remove "session.host_name" check once https://github.com/anyscale/product/issues/15502 is fixed
                # A cluster may have "running" state while its dns is not set up yet. When DNS is not ready,
                # many cluster operations, like ray job submission will fail. So we wait until DNS info
                # is ready.
                if (
                    session.state == "Running"
                    and session.pending_state is None
                    and session.host_name
                ):
                    return cast(str, session.id)

                # Check for start up errors
                if (
                    session.state_data
                    and session.state_data.startup
                    and session.state_data.startup.startup_error
                ):
                    raise click.ClickException(
                        f"Error while starting cluster {session_name}: {session.state_data.startup.startup_error}"
                    )
                elif (
                    session.state
                    and "Errored" in session.state
                    and session.pending_state is None
                ):
                    raise click.ClickException(
                        f"Error while starting cluster {session_name}: Cluster startup failed due to an error ({session.state})."
                    )
                elif (
                    session.state
                    and session.state in {"Terminated", "Stopped"}
                    and session.pending_state is None
                ):
                    # Cluster is created in Terminated state; Check pending state to see if it is pending transition.
                    raise click.ClickException(
                        f"Error while starting cluster {session_name}: Cluster is still in stopped/terminated state."
                    )
                elif (
                    session.state_data
                    and session.state_data.startup
                    and session.state_data.startup.startup_progress
                ):
                    # Print the latest status
                    print_status(
                        "Starting up " + session.state_data.startup.startup_progress
                    )
                elif (
                    session.state != "StartingUp"
                    and session.pending_state == "StartingUp"
                ):
                    print_status("Waiting for start up...")
            else:
                raise click.ClickException(
                    f"Error while starting cluster {session_name}: Cluster doesn't exist."
                )

            time.sleep(2)


def _get_rsync_args(rsync_exclude: List[str], rsync_filter: List[str]) -> List[str]:
    rsync_exclude_args = [["--exclude", exclude] for exclude in rsync_exclude]
    rsync_filter_args = [["--filter", f"dir-merge,- {f}"] for f in rsync_filter]

    # Combine and flatten the two lists
    return [
        arg for sublist in rsync_exclude_args + rsync_filter_args for arg in sublist
    ]


def get_rsync_command(
    ssh_command: List[str],
    source: str,
    ssh_user: str,
    head_ip: str,
    target: str,
    delete: bool,
    rsync_exclude: Optional[List[str]] = None,
    rsync_filter: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Tuple[List[str], Optional[Dict[str, Any]]]:
    rsync_executable = "rsync"
    env = None
    if rsync_exclude is None:
        rsync_exclude = []
    if rsync_filter is None:
        rsync_filter = []

    command_list = [
        rsync_executable,
        "--rsh",
        " ".join(ssh_command),
        "-avz",
    ]
    command_list += _get_rsync_args(rsync_exclude, rsync_filter)

    if delete:
        # Deletes files in target that doesn't exist in source
        command_list.append("--delete")

    if dry_run:
        command_list += [
            "--dry-run",
            "--itemize-changes",
            "--out-format",
            "%o %f",
        ]

    command_list += [
        source,
        "{}@{}:{}".format(ssh_user, head_ip, target),
    ]
    return command_list, env


def populate_session_args(cluster_config_str: str, config_file_name: str) -> str:
    import jinja2

    env = jinja2.Environment()
    t = env.parse(cluster_config_str)
    for elem in t.body[0].nodes:  # type: ignore

        if isinstance(elem, jinja2.nodes.Getattr):  # type: ignore
            if elem.attr not in os.environ:
                prefixed_command = " ".join(
                    [f"{elem.attr}=<value>", "anyscale"] + sys.argv[1:]
                )
                raise click.ClickException(
                    f"\tThe environment variable {elem.attr} was not set, yet it is required "
                    f"for configuration file {config_file_name}.\n\tPlease specify {elem.attr} "
                    f"by prefixing the command.\n\t\t{prefixed_command}"
                )

    template = jinja2.Template(cluster_config_str)
    cluster_config_filled = template.render(env=os.environ)
    return cluster_config_filled


def canonicalize_remote_location(
    cluster_config: Dict[str, Any], remote_location: Optional[str], project_id: str
) -> Optional[str]:
    """Returns remote_location, but changes it from being based
    in "~/", "/root/" or "/ray" to match working_dir
    """
    # Include the /root path to ensure that absolute paths also work
    # This is because of an implementation detail in OSS Ray's rsync
    if bool(get_container_name(cluster_config)) and bool(remote_location):
        remote_location = str(remote_location)
        working_dir = get_working_dir(cluster_config, project_id)
        for possible_name in ["root", "ray"]:
            full_name = f"/{possible_name}/"
            # TODO(ilr) upstream this to OSS Ray
            if working_dir.startswith("~/") and remote_location.startswith(full_name):
                return remote_location.replace(full_name, "~/", 1)

            if working_dir.startswith(full_name) and remote_location.startswith("~/"):
                return remote_location.replace("~/", full_name, 1)

    return remote_location


def get_user_info() -> Optional[UserInfo]:
    try:
        api_client = get_auth_api_client().api_client
    except click.exceptions.ClickException:
        return None
    return api_client.get_user_info_api_v2_userinfo_get().result


def generate_slug(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def validate_non_negative_arg(ctx, param, value):  # noqa: ARG001
    """
    Checks that an integer option to click command is non-negative.
    """
    if value < 0:
        raise click.ClickException(
            f"Please specify a non-negative value for {param.opts[0]}"
        )
    return value


def _update_external_ids_for_policy(
    original_policy: Dict[str, Any], new_external_id: str
):
    """Gets All External IDs From policy Dict."""
    policy = deepcopy(original_policy)
    external_ids = [
        statement.setdefault("Condition", {})
        .setdefault("StringEquals", {})
        .setdefault("sts:ExternalId", [])
        for statement in policy.get("Statement", [])
    ]

    external_ids = [
        [i, new_external_id] if isinstance(i, str) else i + [new_external_id]
        for i in external_ids
    ]

    _ = [
        policy["Statement"][i]["Condition"]["StringEquals"].update(
            {"sts:ExternalId": external_ids[i]}
        )
        for i in range(len(policy.get("Statement", [])))
    ]
    return policy


def extract_versions_from_image_name(image_name: str) -> Tuple[str, str]:
    """Returns the python version and ray extracted from an image tag.
    This should be used when creating BYOD images.

    Args:
        image_name: e.g. anyscale/ray-ml:1.11.1-py38-gpu

    Returns:
        The (python version, ray version), e.g. ("py38", "1.11.1")
    """
    # e.g. 1.11.1-py32-gpu
    image_version = image_name.split(":")[-1]
    parts = image_version.split("-")
    # e.g. 1.11.1

    if len(parts) < 2:
        raise ValueError(
            f"Expected the docker image name have an image version tag (something like ray-ml:1.11.1-py38-gpu), got {image_version}."
        )

    ray_version = parts[0]
    # Verify ray_version is valid.
    _ray_version_major_minor(ray_version)

    python_version = parts[1]
    _check_python_version(python_version)
    return (python_version, ray_version)


def _ray_version_major_minor(ray_version: str) -> Tuple[int, int]:
    """Takes in a Ray version such as "1.9.0rc1", "1.10.2", "2.0.0dev0".

    Returns the major minor pair e.g. (1,9) (1,10) (2,0).

    To avoid introducing undesirable dependencies, partly duplicates logic from the Anyscale
    backend.
    """
    invalid_ray_version_msg = (
        f"The Ray version `{ray_version}` has an unexpected format."
    )
    version_components = ray_version.split(".")
    assert len(version_components) >= 2, invalid_ray_version_msg
    major_str, minor_str = version_components[:2]
    assert major_str.isnumeric() and minor_str.isnumeric(), invalid_ray_version_msg
    major_int, minor_int = int(major_str), int(minor_str)
    return (major_int, minor_int)


def _check_python_version(python_version: str) -> None:
    assert (
        python_version in VALID_BYOD_PYTHON_VERSIONS
    ), f"Expected python_version to be one of {VALID_BYOD_PYTHON_VERSIONS}, got {python_version}."


def sleep_till(wake_time: float) -> None:
    """Sleep till the designated time"""
    time.sleep(max(0, wake_time - time.time()))


def poll(
    interval_secs: float = 1,
    timeout_secs: Optional[float] = None,
    max_iter: Optional[int] = None,
) -> Generator[int, None, None]:
    """Poll every interval_secs, until timeout_secs, or max iterations has been reached.
    Yield the iteration number, starting at 1.
    """
    last_poll_time = time.time()
    end_time = time.time() + timeout_secs if timeout_secs else None
    count = 0
    should_continue_iter = max_iter is None or count < max_iter
    should_continue_time = end_time is None or time.time() < end_time
    while should_continue_iter and should_continue_time:
        count += 1
        last_poll_time = time.time()
        yield count
        sleep_till(last_poll_time + interval_secs)
        should_continue_iter = max_iter is None or count < max_iter
        should_continue_time = end_time is None or time.time() < end_time


def is_anyscale_workspace() -> bool:
    return "ANYSCALE_EXPERIMENTAL_WORKSPACE_ID" in os.environ


def credentials_check_sanity(credentials_str: str) -> bool:
    """
    The main goal of this function is to perform a minimal sanity check
    to make sure that the CLI token string (entered by user or read from file)
    is not totally broken.
    refer to https://www.notion.so/anyscale-hq/Authentication-Infrastructure
    """
    # Old token style
    if credentials_str.startswith("sss_"):
        return True
    # Future token style
    if credentials_str.startswith("a") and credentials_str.count("_") > 0:
        return True
    return False


def get_current_cluster_id() -> Optional[str]:
    """If we are running on an Anyscale Cluster, return the id from the environment."""
    return os.getenv("ANYSCALE_SESSION_ID")


def str_data_size(s: str) -> int:
    """Returns the size of the string when encoded to raw bytes."""
    return len(s.encode("utf-8"))


def get_user_env_aws_account(region: str) -> str:
    """Get the AWS account used in the user environment"""
    return boto3.client("sts", region_name=region).get_caller_identity()["Account"]


def prepare_cloudformation_template(
    region: str, cfn_stack_name: str, cloud_id: str
) -> str:
    with open(f"{anyscale.conf.ROOT_DIR_PATH}/anyscale-cloud-setup.yaml") as f:
        body = f.read()

    azs = get_availability_zones(region)
    subnet_templates: List[str] = []
    subnets_route_table_association: List[str] = []
    subnets_with_availability_zones: List[str] = []

    vpc_cidr = ipaddress.ip_network(VPC_CIDR_RANGE)
    if len(azs) > 4:
        subnet_cidrs = list(vpc_cidr.subnets(prefixlen_diff=3))
    else:
        subnet_cidrs = list(vpc_cidr.subnets(prefixlen_diff=2))

    for i, az in enumerate(azs):
        subnet_templates.append(
            f"""
  Subnet{i}:
    Type: AWS::EC2::Subnet
    Properties:
        VpcId: !Ref VPC
        AvailabilityZone: {az}
        CidrBlock: {subnet_cidrs[i]}
        MapPublicIpOnLaunch: true
        Tags:
        - Key: Name
          Value: {cfn_stack_name}-subnet-{az}
        - Key: anyscale-cloud-id
          Value: {cloud_id}"""
        )

        subnets_route_table_association.append(
            f"""
  Subnet{i}RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
        RouteTableId: !Ref PublicRouteTable
        SubnetId: !Ref Subnet{i}"""
        )

        subnets_with_availability_zones.append(
            f'{{"subnet_id": !Ref Subnet{i}, "availability_zone": !GetAtt Subnet{i}.AvailabilityZone}}'
        )

    body = body.replace("$SUBNETS_TEMPLATES", "\n".join(subnet_templates))
    body = body.replace(
        "$SUBNETS_ROUTE_TABLE_ASSOCIATION", "\n".join(subnets_route_table_association),
    )
    body = body.replace(
        "$SUBNETS_WITH_AVAILABILITY_ZONES",
        f'[{",".join(subnets_with_availability_zones)}]',
    )
    body = body.replace("$ALLOWED_ORIGIN", shared_anyscale_conf.ANYSCALE_HOST)

    return body


def get_latest_ray_version():
    """
    Gets latest Ray version from PYPI. This method should not
    assume Ray is already installed.
    """
    try:
        response = requests.get("https://pypi.org/pypi/ray/json")
        latest_version = response.json()["info"]["version"]
    except Exception as e:
        log.debug(
            f"Unable to get latest Ray version from https://pypi.org/pypi/ray/json {str(e)}"
        )
        latest_version = DEFAULT_RAY_VERSION
    return latest_version


def get_ray_and_py_version_for_default_cluster_env() -> Tuple[str, str]:
    py_version = "".join(str(x) for x in sys.version_info[0:2])
    try:
        import ray

        ray_version = ray.__version__
        if version.parse(ray_version) < version.parse(MINIMUM_RAY_VERSION):
            raise ValueError(
                f"No default cluster env for Ray version {ray_version}. Please upgrade "
                f'to a version >= {MINIMUM_RAY_VERSION} with `pip install "ray>={MINIMUM_RAY_VERSION}"`.'
            )
        if "dev0" in ray_version:
            raise ValueError(
                f"Your locally installed Ray version is {ray_version}. "
                "There is no default cluster environments for nightly versions of Ray."
            )
    except ImportError:
        # Use latest Ray version if Ray not locally installed, because Anyscale cluster envs for
        # new Ray versions are available before the open source package is released on PYPI.
        ray_version = get_latest_ray_version()
        log.debug(
            f"Ray is not installed locally. Using latest Ray version {ray_version} for "
            "the cluster env."
        )

    return ray_version, py_version


def validate_job_config_dict(
    config_dict: Dict[str, Any], api_client: ProductApi
) -> None:
    """
    Throws an exception if there are invalid values in the config dict.
    """
    compute_config: Optional[Union[ComputeTemplate, DecoratedComputeTemplate]] = None
    if "compute_config" in config_dict and isinstance(
        config_dict["compute_config"], str
    ):
        compute_config = get_cluster_compute_from_name(
            config_dict["compute_config"], api_client
        )
    elif "compute_config_id" in config_dict:
        cluster_compute_id = config_dict["compute_config_id"]
        compute_config = api_client.get_compute_template_api_v2_compute_templates_template_id_get(
            cluster_compute_id
        ).result

    if compute_config and compute_config.archived_at:
        raise click.ClickException(
            "This job is using an archived compute config. To submit this job, specify a new compute config."
        )


def populate_dict_with_workspace_config_if_exists(
    config_dict: Dict[str, Any], anyscale_api_client: BaseApi
) -> Dict[str, Any]:
    """
    If the job is submitted from the workspace, we populate values from the workspace
    if the config doesn't specify them, such as cluster env and compute config.
    """
    if "ANYSCALE_EXPERIMENTAL_WORKSPACE_ID" in os.environ:
        if "ANYSCALE_SESSION_ID" in os.environ:
            cluster = anyscale_api_client.get_cluster(
                os.environ["ANYSCALE_SESSION_ID"]
            ).result
            # If the job configs are not specified, infer them from the workspace:
            if "build_id" not in config_dict and "cluster_env" not in config_dict:
                config_dict["build_id"] = cluster.cluster_environment_build_id
            if "project_id" not in config_dict:
                config_dict["project_id"] = cluster.project_id
            if (
                "compute_config" not in config_dict
                and "compute_config_id" not in config_dict
            ):
                config_dict["compute_config_id"] = cluster.cluster_compute_id
    return config_dict


def filter_actions_from_policy_document(
    policy_document: Dict[Any, Any], filter: Callable[[Dict], bool] = None
) -> set:
    if filter is None:
        filter = lambda statement: statement["Effect"] == "Allow"  # noqa: E731
    return {
        action
        for statement in _coerce_to_list(policy_document["Statement"])
        for action in _coerce_to_list(statement["Action"])
        if filter(statement)
    }


def filter_actions_associated_with_role(
    boto3_session: boto3.Session,
    role: Boto3Resource,
    filter: Callable[[Dict], bool] = None,
) -> Set[str]:
    iam = boto3_session.resource("iam")
    attached_policy_documents = [
        iam.PolicyVersion(policy.arn, policy.default_version_id).document
        for policy in role.attached_policies.all()  # type: ignore
    ]

    role_policy_documents = [policy.policy_document for policy in role.policies.all()]  # type: ignore

    list_of_allow_actions_sets = [
        filter_actions_from_policy_document(policy_document, filter)
        for policy_document in role_policy_documents + attached_policy_documents
    ]
    return (
        set.union(*list_of_allow_actions_sets) if list_of_allow_actions_sets else set()
    )


def contains_control_plane_role(
    assume_role_policy_document: Dict[str, Any], anyscale_aws_account: str
) -> bool:
    def filter(statement: dict):
        # Ensure it is `Allow` & `sts:AssumeRole`
        if (
            statement["Effect"] != "Allow"
            or statement.get("Action") != "sts:AssumeRole"
        ):
            return False

        expected_accounts = {
            f"arn:aws:iam::{anyscale_aws_account}:root",
            anyscale_aws_account,
        }
        return any(
            aws_principal in expected_accounts
            for aws_principal in _coerce_to_list(statement["Principal"].get("AWS"))
        )

    return (
        len(filter_actions_from_policy_document(assume_role_policy_document, filter))
        > 0
    )


T = TypeVar("T")


def _coerce_to_list(maybe_list: Union[T, List[T]]) -> List[T]:
    return maybe_list if isinstance(maybe_list, list) else [maybe_list]
