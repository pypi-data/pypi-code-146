import rich_click as click
import yaml

from servicefoundry.cli.const import GROUP_CLS

# from servicefoundry.cli.display_util import print_json


@click.group(
    name="deploy",
    cls=GROUP_CLS,
    invoke_without_command=True,
    help="Deploy application",
)
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    default="./servicefoundry.yaml",
    help="path to servicefoundry file",
    show_default=True,
)
@click.option(
    "-w",
    "--workspace-fqn",
    type=click.STRING,
    required=True,
    help="workspace to deploy to",
)
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    show_default=True,
    default=True,
    help="wait and tail the deployment progress",
)
def deploy_v2_command(file: str, workspace_fqn: str, wait: bool):
    from servicefoundry.v2 import Application

    with open(file, "r") as f:
        application_definition = yaml.safe_load(f)

    application = Application.parse_obj(application_definition)
    deployment = application.deploy(workspace_fqn=workspace_fqn, wait=wait)
    # print_json(deployment)
