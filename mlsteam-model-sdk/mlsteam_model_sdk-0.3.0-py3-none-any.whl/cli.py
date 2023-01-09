import click

import mlsteam_model_sdk.commands.init
import mlsteam_model_sdk.commands.install_themisdev


@click.group()
def cli():
    pass


cli.add_command(mlsteam_model_sdk.commands.init.cmd, name='init')
cli.add_command(mlsteam_model_sdk.commands.install_themisdev.cmd, name='install-themisdev')


if __name__ == '__main__':
    cli()
