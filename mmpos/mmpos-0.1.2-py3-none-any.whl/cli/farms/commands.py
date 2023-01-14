import click

from prettytable import PrettyTable
import mmpos.api.farms as farms
import json


@click.group()
def entry_point():
    pass


@click.command()
@click.option(
    "--table", "format", default=True, help="Show table output", flag_value="table"
)
@click.option(
    "--json", "format", default=False, help="Show output as json", flag_value="json"
)
def get(format):
    data = farms.farms()
    if format == "table":
        t = PrettyTable()
        t.field_names = data[0].keys()
        for farm in data:
            t.add_row(farm.values())
        click.echo(t)
    else:
        click.echo(json.dumps(data, indent=2))


@click.command()
def show():
    pass


entry_point.add_command(get, "list")
