import sys
import logging
import click
import platform
from apigtool.utility import work_on_apigs
from apigtool.utility import list_apigs
from apigtool.auth_state import set_iam_auth

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S'
)

valid_systems = [
    'linux',
    'darwin'
]


@click.group()
@click.version_option(version='0.3.0')
def cli():
    pass


@cli.command()
@click.option('--apig', '-a', help='APIG of interest', required=True)
@click.option('--stage', '-s', help='APIG stage of interest', required=True)
@click.option('--profile', '-p', help='credential profile')
@click.option('--region', '-r', help='AWS region')
@click.option('--on', '-o', help='on: true | false')
def log(apig, stage, profile, region, on):
    '''
    Work on logging for an APIG
    '''
    work_on_apigs(
        apig=apig,
        stage=stage,
        profile=profile,
        region=region,
        on=on
    )


@cli.command()
@click.option('--profile', '-p', help='credential profile')
@click.option('--region', '-r', help='AWS region')
def list(profile, region):
    '''
    Work on listing the API's
    '''
    list_apigs(
        profile=profile,
        region=region
    )


@cli.command()
@click.option('--profile', help='credential profile')
@click.option('--region', help='AWS region')
@click.option('--api-name', '-a', help='name of the API of interest', required=True)
@click.option('--stage', '-s', help='deployment stage', required=True)
@click.option('--path', '-p', help='deployment stage', required=True)
@click.option('--on', '-o', help='on: true | false', required=True)
@click.option('--method', '-m', help='HTTP method on the resource')
def authiam(**kwargs):
    '''
    Turn on IAM authorization
    '''
    set_iam_auth(**kwargs)

def verify_real_system():
    try:
        current_system = platform.system().lower()
        return current_system in valid_systems
    except:
        return False

if not verify_real_system():
    print('error: unsupported system')
    sys.exit(1)
