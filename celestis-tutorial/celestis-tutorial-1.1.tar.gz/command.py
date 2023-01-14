import click
from create_files import create_app

@click.command()
@click.argument("subcommand", required=True)
def celestis(subcommand):
    if subcommand == "start-project":
        project_name = str(input("What is your project name?"))
        create_app(project_name)
        click.echo("Cool! Your files have been created!")