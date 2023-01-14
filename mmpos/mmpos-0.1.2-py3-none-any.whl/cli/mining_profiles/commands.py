import click
from prettytable import PrettyTable
import mmpos.api.profiles as profiles
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
    "--json", "format", default=True, help="Show json output", flag_value="json"
)
@click.option(
    "--all", default=False, help="Show all mining_profiles from all farms", is_flag=True
)
@click.option(
    "--farm_id",
    envvar="MMPOS_FARM_ID",
    default="first",
    type=click.STRING,
    help="The id of the farm",
)
def get(format, all, farm_id):
    output = ""
    if all:
        data = profiles.get_all()
    else:
        if farm_id == "first":
            farm_id = farms.farms()[0]["id"]
        data = profiles.get(farm_id)

    if format == "table":
        output = PrettyTable()
        output.field_names = ["id", "farm_id", "name", "coin", "os"]

        for profile in data:
            output.add_row(
                [
                    profile["id"],
                    profile["farm_id"],
                    profile["name"],
                    profile["coin"],
                    profile["os"],
                ]
            )

    else:
        # json data
        output = json.dumps(data, indent=2)

    click.echo(output)


entry_point.add_command(get, "list")
