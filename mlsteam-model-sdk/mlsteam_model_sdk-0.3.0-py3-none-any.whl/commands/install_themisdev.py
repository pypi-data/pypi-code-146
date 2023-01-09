import os.path
import subprocess

import click


PlatformChoice = click.Choice(['debian', 'ubuntu'], case_sensitive=False)


@click.command(help='install Themis encryption development package')
@click.option('-p', '--platform', type=PlatformChoice, prompt=True, help='installation platform')
def cmd(platform):
    script_dir = os.path.join(
        os.path.realpath(os.path.dirname(__file__)),
        'utils')
    if platform in ['debian', 'ubuntu']:
        subprocess.run(
            [os.path.join(script_dir, 'install_themisdev_ubuntu.sh')],
            shell=True)
