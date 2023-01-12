import click

cmd_called = False


@click.group()
def cli():
    """This script"""


@cli.command(name='thecmd')
def run_thecmd():
    global cmd_called
    cmd_called = True

    run_thecmd._called = True
