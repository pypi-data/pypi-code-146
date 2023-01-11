import json
import sys
from typing import List, Optional

import click

from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import HaJobStates
from anyscale.controllers.job_controller import JobController
import anyscale.job
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group("job", help="Interact with production jobs running on Anyscale.")
def job_cli() -> None:
    pass


@job_cli.command(name="submit",)
@click.argument("job-config-file", required=True)
@click.option("--name", "-n", required=False, default=None, help="Name of the job.")
@click.option("--description", required=False, default=None, help="Description of job.")
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log of the created job",
)
@click.option(
    "--wait",
    "-w",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to block this CLI command until the job succeeds (or reaches another terminal state)",
)
@click.argument(
    "entrypoint", required=False, nargs=-1,
)
def submit(
    job_config_file: str,
    entrypoint: List[str],
    name: Optional[str],
    description: Optional[str],
    follow: Optional[bool],
    wait: Optional[bool],
) -> None:
    """ Submit a Production Job

    This function accepts 1 argument, a path to a YAML config file that defines this job.


    To wait for the Job to complete, use the --wait flag as follows.

    $ anyscale job submit job.yaml --wait

    If running from an Anyscale Workspace, this command also support an alternative syntax to specify the entrypoint inline:

    $ anyscale job submit -- python script.py

    The Cluster Environment and Cluster Config are inferred from the Workspace Configuration if running from a workspace.

    """

    job_controller = JobController()
    id = job_controller.submit(  # noqa: A001
        job_config_file,
        name,
        description,
        entrypoint=entrypoint,
        is_entrypoint_cmd="--" in sys.argv,
    )
    if follow:
        job_controller.logs(id, should_follow=follow)
    if wait:
        job_controller.wait(job_id=id)


@job_cli.command(name="list", help="Display information about existing jobs.")
@click.option("--name", "-n", required=False, default=None, help="Filter by job name.")
@click.option(
    "--job-id", "--id", required=False, default=None, help="Filter by job id."
)
@click.option(
    "--project-id", required=False, default=None, help="Filter by project id."
)
@click.option(
    "--include-all-users",
    is_flag=True,
    default=False,
    help="Include jobs not created by current user.",
)
@click.option(
    "--include-archived",
    is_flag=True,
    default=False,
    help=(
        "List archived jobs as well as unarchived jobs."
        "If not provided, defaults to listing only unarchived jobs."
    ),
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
def list(  # noqa: A001
    name: Optional[str],
    job_id: Optional[str],
    project_id: Optional[str],
    include_all_users: bool,
    include_archived: bool,
    max_items: int,
) -> None:
    job_controller = JobController()
    job_controller.list(
        name=name,
        job_id=job_id,
        project_id=project_id,
        include_all_users=include_all_users,
        include_archived=include_archived,
        max_items=max_items,
    )


@job_cli.command(name="archive", help="Archive a job.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def archive(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.archive(job_id=job_id, job_name=name)


@job_cli.command(name="terminate", help="Attempt to terminate a job asynchronously.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def terminate(job_id: Optional[str], name: Optional[str]) -> None:
    job_controller = JobController()
    job_controller.terminate(job_id=job_id, job_name=name)


@job_cli.command(name="logs", help="Print the logs of a job.")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log.",
)
def logs(job_id: Optional[str], name: Optional[str], follow: bool = False,) -> None:
    job_controller = JobController()
    job_controller.logs(
        job_id=job_id, job_name=name, should_follow=follow,
    )


@job_cli.command(name="wait")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--state",
    "-s",
    required=False,
    default=HaJobStates.SUCCESS,
    help="The state to wait for this Job to enter",
)
@click.option(
    "--timeout",
    "-t",
    required=False,
    default=None,
    type=float,
    help="The timeout in seconds after which this command will exit.",
)
def wait(
    job_id: Optional[str],
    name: Optional[str],
    state: str = HaJobStates.SUCCESS,
    timeout=None,
) -> None:
    """Wait for a Job to enter a specific state (default: SUCCESS).

    To specify the Job by name, use the --name flag. To specify the Job by id, use the --job-id flag.

    If the Job reaches the target state, the command will exit successfully.

    If the Job reaches a terminal state other than the target state, the command will exit with an error.

    If the command reaches the timeout, the command will exit with an error.
    """
    state = state.upper()
    job_controller = JobController()
    job_id = job_controller.wait(
        job_id=job_id,
        job_name=name,
        is_service=False,
        target_state=state,
        timeout_secs=timeout,
    )


@job_cli.group("output", help="Interact with Production Job outputs.")
def output_cli() -> None:
    pass


@output_cli.command(name="get")
@click.option("--job-id", "--id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
def get_output(job_id: Optional[str], name: Optional[str]) -> None:
    """Get the output of a Production Job."""
    job_controller = JobController()
    job_controller.retrieve_output(job_name=name, job_id=job_id)


@output_cli.command(name="write")
@click.option(
    "--file",
    "-f",
    required=False,
    type=click.File("rb"),
    help="File to read the output from.",
)
@click.argument(
    "input_str", required=False, type=str,
)
def write_output(file, input_str) -> None:
    """Write the output of a Production Job to Anyscale.

    This command should be called from within a Production Job entrypoint. It will record the JSON output of your Job.
    If you specify neither a file or a string, this command will read from STDIN.

    Examples:

        anyscale job output write -f output.json

        anyscale job output write '{"output": 5}'

        cat output.json | anyscale job output write

    """
    data = None
    if input_str and file:
        raise click.ClickException("Cannot specify both --file and an input string.")
    if input_str is not None:
        data = json.loads(input_str)
    else:
        data = json.load(file or sys.stdin)
    anyscale.job.output(data)
