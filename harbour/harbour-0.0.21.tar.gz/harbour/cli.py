import click

from harbour.client import Client
from harbour.client.artifact import Artifact

@click.group()
def cli():
    pass

@cli.command()
def configure():
    """Configures the credentials file"""

    client = Client()

    domain = click.prompt('Habour domain', type=str)
    key = click.prompt('Habour key', type=str)

    client.configure(domain, key)

@cli.command()
@click.option('--path', required=True, help='Root directory of the project')
@click.option('--name', required=True, help='Image name:tag. If tag is ommited, latest is considered.')
def register(**kwargs):
    """Uploads a code to the repository"""

    client = Client()

    result = client.register(**kwargs)


if __name__ == '__main__':
    cli()


@cli.command()
@click.option('--cpu', required=False, help='Execution CPU override')
@click.option('--memory', required=False, help='Execution memory override')
@click.option('--role', required=False, help='Execution role override')
@click.option('--environment', '-e', multiple=True, help='Overrides the environment variable. Format: NAME=value')
@click.argument('image')
def execute(*args, **kwargs):
    """Executes a image"""

    client = Client()

    # Parses the environment variables
    environment = {}

    for env in kwargs.get('environment', []):

        key, value = env.split('=')

        environment[key] = value

    kwargs['environment'] = environment

    result = client.execute(**kwargs)


@cli.command()
@click.argument('path')
def package(path):
    """Packages a distribution"""

    artifact = Artifact()

    filepath = artifact.package(path)

    click.echo(filepath)
