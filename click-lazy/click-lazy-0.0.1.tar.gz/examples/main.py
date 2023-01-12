import click

from click_lazy import LazyGroup


@click.group()
def cli():
    pass


@click.command(name='main')
def run_main():
    print('Running command from main.py file')


if __name__ == '__main__':
    cli.add_command(run_main)

    cli.add_command(LazyGroup(name='easy', import_name='group_easy:cli', help='Easy to import set of commands'))
    cli.add_command(LazyGroup(name='heavy', import_name='group_heavy:cli', help='Heavy to import set of commands'))

    cli()
