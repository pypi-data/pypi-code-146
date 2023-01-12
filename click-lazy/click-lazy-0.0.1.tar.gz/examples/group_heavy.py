from time import sleep

import click

print('Simulation of havy import. Somthing like tensorflow etc.')
for i in range(3):
    print('Delay {}'.format(i))
    sleep(1)


@click.group()
def cli():
    """Havy script"""


@cli.command(name='heavy_cmd')
def run_heavy_cmd():
    print('Running command from heavy group file')
