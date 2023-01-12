""" Command Line Utilities for Sermos Deployments
"""
import logging
import click
from sermos.deploy import SermosDeploy

logger = logging.getLogger(__name__)


@click.group()
def deployment():
    """ Deployment command group.
    """


@deployment.command()
@click.option('--sermos-yaml', required=False, default=None)
@click.option('--output-file', required=False, default=None)
@click.option('--output-format', required=False, default='yaml')
@click.option("--print-output", is_flag=True, show_default=True, default=False)
def validate(sermos_yaml: str = None,
             output_file: str = None,
             output_format: str = 'yaml',
             print_output: bool = False):
    """ Validate a compiled Sermos yaml is ready for deployment.

        Arguments::

            sermos-yaml (optional): Path to find your `sermos.yaml`
                configuration file. Defaults to `sermos.yaml`
    """
    # Instantiate SermosDeploy
    sd = SermosDeploy(access_key='fake', sermos_yaml_filename=sermos_yaml)

    # Validate deployment
    sd.validate_deployment(output_file=output_file,
                           output_format=output_format,
                           print_output=print_output)
    click.echo("Configuration is Valid and ready to Deploy.")


@deployment.command()
@click.option('--deployment-id', required=False, default=None)
@click.option('--access-key', required=False, default=None)
@click.option('--sermos-yaml', required=False, default=None)
@click.option('--base-url', required=False, default=None)
@click.option('--deploy-branch', required=False, default='main')
def deploy(deployment_id: str = None,
           access_key: str = None,
           sermos_yaml: str = None,
           base_url: str = None):
    """ Invoke a Sermos build for your application.

        Arguments:

            deployment-id (optional): UUID for Deployment. Find in your Sermos
                Cloud Console. Will look under `SERMOS_DEPLOYMENT_ID` in
                environment if not provided.

            access-key (optional): Defaults to checking the environment for
                `SERMOS_ACCESS_KEY`. If not found, will exit.

            sermos-yaml (optional): Path to find your `sermos.yaml`
                configuration file. Defaults to `sermos.yaml`

            base-url (optional): Defaults to primary Sermos Cloud base URL.
                    Only modify this if there is a specific, known reason to do so.
                    Can also set through environment `SERMOS_BASE_URL`.
    """
    # Instantiate SermosDeploy
    sd = SermosDeploy(deployment_id=deployment_id,
                      access_key=access_key,
                      sermos_yaml_filename=sermos_yaml,
                      base_url=base_url)

    # Validate deployment
    sd.validate_deployment()

    # Invoke deployment
    result = sd.invoke_deployment()
    content = result.json()
    if result.status_code < 300:
        click.echo(content['data']['status'])
    else:
        logger.error(f"{content}")


@deployment.command()
@click.option('--deployment-id', required=False, default=None)
@click.option('--access-key', required=False, default=None)
@click.option('--base-url', required=False, default=None)
def status(deployment_id: str = None,
           access_key: str = None,
           base_url: str = None):
    """ Check on the status of a Sermos build.

        Arguments:
            deployment-id (optional): UUID for Deployment. Find in your Sermos
                Cloud Console. If not provided, looks in environment under
                `SERMOS_DEPLOYMENT_ID`
            access-key (optional): Defaults to checking the environment for
                `SERMOS_ACCESS_KEY`. If not found, will exit.
            base-url (optional): Defaults to primary Sermos Cloud base URL.
                    Only modify this if there is a specific, known reason to do so.
                    Can also set through environment `SERMOS_BASE_URL`.
    """
    # Instantiate SermosDeploy
    sd = SermosDeploy(deployment_id=deployment_id,
                      access_key=access_key,
                      base_url=base_url)

    # Check deployment status
    result = sd.get_deployment_status()
    try:
        click.echo(result['data']['results'])
    except Exception as e:
        logger.error(f"{result} / {e}")
