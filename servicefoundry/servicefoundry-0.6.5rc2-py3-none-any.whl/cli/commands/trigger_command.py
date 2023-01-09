from typing import Sequence

import rich_click as click

from servicefoundry.cli.console import console
from servicefoundry.cli.const import COMMAND_CLS, GROUP_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.internal import experimental


@click.group(name="trigger", cls=GROUP_CLS)
def trigger_command():
    """
    Trigger a deployed job asynchronously
    """
    pass


@click.command(
    name="job",
    cls=COMMAND_CLS,
    context_settings=dict(ignore_unknown_options=True),
    help="Trigger a Job asynchronously",
)
@click.option(
    "--deployment_fqn",
    type=click.STRING,
    required=True,
    help="FQN of the deployment of the Job. This can be found on the Job details page.",
)
@click.argument("job_command", nargs=-1, type=click.UNPROCESSED)
@handle_exception_wrapper
def trigger_job(deployment_fqn: str, job_command: Sequence[str]):
    response = experimental.trigger_job(
        deployment_fqn=deployment_fqn, command=job_command
    )
    if job_command:
        message = f"Job triggered with command {job_command!r}"
    else:
        message = "Job triggered with pre-configured command"
    console.print(
        f"{message}.\n"
        f"It will be scheduled and visible at {response['previous_runs_url']}"
    )


def get_trigger_command():
    trigger_command.add_command(trigger_job)
    return trigger_command
