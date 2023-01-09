import click

import sym.flow.cli.helpers.output as cli_output

from ...helpers.debug import do_upload_file


@click.command(short_help="Share a file with Sym")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
def upload_file(file: click.Path) -> None:
    """Share the contents of FILE with Sym."""

    cli_output.info("Uploading...")
    txid = do_upload_file(str(file))
    cli_output.success("Your file was shared with Sym!")
    cli_output.info(f"Transaction ID: {txid}", bold=True)
