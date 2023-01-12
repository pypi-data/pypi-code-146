import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.global_options import GlobalOptions

from ...helpers.debug import do_upload_terraform_output


@click.command(short_help="Share Terraform output with Sym")
@click.argument("tf_dir", type=click.Path(exists=True, file_okay=False), default=".")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def upload_terraform_output(options: GlobalOptions, tf_dir: click.Path) -> None:
    """Share the output from Terraform in TF_DIR with Sym."""

    cli_output.info("Running `terraform output` and uploading...")
    txid = do_upload_terraform_output(str(tf_dir), options)
    cli_output.success("Your Terraform output was shared with Sym!")
    cli_output.info(f"Transaction ID: {txid}", bold=True)
