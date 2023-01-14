import click
import os
from prettytable import PrettyTable
import mmpos.api.rigs as rigs
import mmpos.api.farms as farms
from mmpos.cli.rigs import commands as rigs

@click.group()
def entry_point():
    pass

@click.group()
def farms():
    pass


@click.command()
def get_farms():
    t = PrettyTable()
    data = farms.farms()
    t.field_names = data[0].keys()
    for farm in data:
        t.add_row(farm.values())

    click.echo(t)


@click.command()
@click.argument('farm_id', envvar='MMPOS_FARM_ID', default='first', type=click.STRING)
def get_rigs(farm_id):
    if (farm_id == 'first'):
        farm_id = farms.farms()[0]['id']

    click.echo(rigs.rigs(farm_id))


# @click.command()
# def get_all_rigs():
#     click.echo(rigs.all_rigs())


@click.command()
def gpu_table():
    t = PrettyTable()
    t.field_names = ['rig_name', 'name', 'address', 'gpu_id']

    for rig in rigs.all_rigs():
        for gpu in rig['gpus']:
            t.add_row([rig['name'], gpu['name'], rig['local_addresses']
                       [0], gpu['id']])

    click.echo(t)

@click.command()
def rigs_table():
    t = PrettyTable()
    t.field_names = ['id', 'name', 'address', 'profiles', 'agent_version']

    for rig in rigs.all_rigs():
        profiles = list(
            map(lambda x: x['name'], rig['miner_profiles']))
        t.add_row([rig['id'], rig['name'], rig['local_addresses']
                  [0], profiles, rig['agent_version']])

    click.echo(t)

@click.command()
@click.option('--rig_id', type=click.STRING, required=True, help="The rig name or id, use all to run against all rigs in farm")
@click.option('--farm_id', type=click.STRING, default='first', show_default=True, help="The farm id, defaults to first farm found")
@click.option('--action', required=True,
              type=click.Choice(['disable', 'poweroff', 'reset', 'enable', 'restart', 'reboot'], case_sensitive=False))
def rig_control(action, rig_id, farm_id):
   if (farm_id == 'first'):
     farm_id = farms.default_farm()['id']
   rigs.rig_control(action, rig_id, farm_id, block=lambda name,action: click.echo(f'{name} has been set to {action}'))


    #click.echo(f'{rig_name_list()[rig_id]} has been set to {action}')

entry_point.add_command(rigs_table)
entry_point.add_command(rigs.entry_point, 'rigs')
entry_point.add_command(get_farms)
entry_point.add_command(get_rigs)
entry_point.add_command(gpu_table)
entry_point.add_command(rig_control)

def main():
    if (not os.environ['MMPOS_API_TOKEN']):
        click.echo("You need to set the env variable MMPOS_API_TOKEN")
        exit(1)

    entry_point()

if __name__ == '__main__':
    main()

