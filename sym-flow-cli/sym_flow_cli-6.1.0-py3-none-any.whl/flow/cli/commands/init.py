import importlib.resources as pkg_resources
import os

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation import (  # import the *package* containing the tf files
    approval,
)
from sym.flow.cli.errors import NonEmptyDirectoryError, NotLoggedInError
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.command(short_help="Generate starter Terraform code")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--workspace-id",
    prompt="Workspace ID",
)
def init(options: GlobalOptions, workspace_id: str) -> None:
    """In an empty directory, generate the Terraform configuration needed to create a Sym approval-only Flow."""

    if not Config.is_logged_in():
        raise NotLoggedInError()

    if os.listdir("."):
        raise NonEmptyDirectoryError()

    # Note: The impl file is stored as a `.txt` resource because PyOxidizer (the tool used to package symflow CLI)
    # Does NOT support reading `.py` files with `importlib.resources`
    # https://github.com/indygreg/PyOxidizer/issues/237
    #
    # However, we don't care about reading the source code, we simply need to pull the text file and write it
    # to the filesystem with a `.py` extension. As a workaround, we have stored `impl.py` as `impl.txt` in the
    # code_generation.approval package so that we can read it with importlib.resources.
    static_files = [("impl.txt", "impl.py"), ("versions.tf", "versions.tf")]

    # These files don't need any values substituted in them.
    for resource_name, output_file in static_files:
        template = pkg_resources.read_text(approval, resource_name)
        with open(output_file, "w") as f:
            f.write(template)

    # Fill in the org slug and workspace ID variables with values
    org = Config.get_org().slug
    main_tf = pkg_resources.read_text(approval, "main.tf")
    with open("main.tf", "w") as f:
        main_tf = main_tf.replace("${var.sym_org_slug}", org)
        main_tf = main_tf.replace("${var.slack_workspace_id}", workspace_id.upper())

        f.write(main_tf)

    cli_output.success(
        "Successfully generated your Sym Terraform configuration! Run the following to apply the Terraform: \n\n terraform init && terraform apply"
    )
