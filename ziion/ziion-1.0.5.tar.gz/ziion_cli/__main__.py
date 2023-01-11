import click
import sys
from ziion_cli.dispatcher import *
from ziion_cli.__version__ import __version__
import platform
from ziion_cli.constants import (
    METAPACKAGES,
)

@click.group()
@click.version_option(version=__version__) 
def commands():
    pass

def solc() -> None:
    solc_imp()
    

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    commands()
    
@click.command()
def list_metapackages():
    for key in METAPACKAGES.keys() :
        click.echo(key)

@click.command()
def self_update():
    update_cli()
    

@click.command()
@click.argument("metapackage", type=click.Choice(METAPACKAGES.keys()), nargs=-1)
@click.option("--dryrun",is_flag=True, help="Flag to preview the packages to be updated.")
def update(metapackage, dryrun):
    if metapackage == ():
        click.echo("Error, at least on package from list_metapackages must be specified!")
        exit
    for package in metapackage:
        update_packages(METAPACKAGES.get(package), dryrun)

@click.command()
@click.argument("version", required=False)
@click.option("--install",is_flag=True, help="Flag to install the artifact if not installed yet.")
@click.option("--versions",is_flag=True, help="Flag to preview the installed solc versions.")
def solc_select(version, install, versions):
    if versions:
        solc_select_get_versions()
        pass
    elif version == None:
        click.echo("Missing version to be selected.")
    else:
        solc_select_imp(version, install)

commands.add_command(list_metapackages)
commands.add_command(self_update)
commands.add_command(update)
if platform.machine() == 'aarch64':
    commands.add_command(solc_select)

if __name__ == "__main__":
    main()