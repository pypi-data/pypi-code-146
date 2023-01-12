import click

import sym.flow.cli.helpers.output as cli_output

from ...helpers.debug import do_upload_directory


@click.command(short_help="Share a directory with Sym")
@click.argument("dir", type=click.Path(exists=True, file_okay=False))
def upload_directory(dir: click.Path) -> None:
    """Share the contents of DIR with Sym."""

    cli_output.info("Archiving and uploading...")
    txid = do_upload_directory(str(dir))

    cli_output.success("Your directory was shared with Sym!")
    cli_output.info(f"Transaction ID: {txid}", bold=True)
