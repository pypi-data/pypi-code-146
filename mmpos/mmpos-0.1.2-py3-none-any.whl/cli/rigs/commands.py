import click
from prettytable import PrettyTable
import mmpos.api.rigs as rigs
import mmpos.api.farms as farms
import json


@click.group()
def entry_point():
    pass


@click.command()
@click.option(
    "--farm_id",
    envvar="MMPOS_FARM_ID",
    default="first",
    type=click.STRING,
    required=True,
    help="The id of the farm",
)
@click.option(
    "--rig_id",
    type=click.STRING,
    required=True,
    help="The rig id, not required when using --all or --everywhere flags",
)
@click.option(
    "--mining_profiles_ids",
    type=click.STRING,
    required=True,
    help="The mining profile ids",
)
@click.option(
    "--simulate", is_flag=True, default=False, help="Simulate the action only"
)
@click.option(
    "--table", "format", default=True, help="Show table output", flag_value="table"
)
@click.option(
    "--json", "format", default=True, help="Show json output", flag_value="json"
)
def set_mining_profiles(farm_id, rig_id, mining_profiles_ids, format, simulate):
    rig = rigs.set_mining_profiles(farm_id, rig_id, mining_profiles_ids, simulate,)


    print_rigs([rig], format)


def print_rigs(rigs, format):
    if format == "table":
        output = PrettyTable()
        output.field_names = ["id", "rig_name", "address", "profiles", "agent_version"]

        for rig in rigs:
            profiles = list(map(lambda x: x["name"], rig["miner_profiles"]))
            output.add_row(
                [
                    rig["id"],
                    rig["name"],
                    rig["local_addresses"][0],
                    profiles,
                    rig["agent_version"],
                ]
            )

    else:
        # json data
        output = json.dumps(rigs, indent=2)

    click.echo(output)


@click.command()
@click.option(
    "--table", "format", default=True, help="Show table output", flag_value="table"
)
@click.option(
    "--json", "format", default=True, help="Show json output", flag_value="json"
)
@click.option("--all", default=False, help="Show all rigs from all farms", is_flag=True)
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
        data = rigs.all_rigs()
    else:
        if farm_id == "first":
            farm_id = farms.farms()[0]["id"]
        data = rigs.rigs(farm_id)

    print_rigs(data, format)


@click.command()
def show():
    pass


@click.command()
@click.option(
    "--table", "format", default=True, help="Show table output", flag_value="table"
)
@click.option(
    "--json", "format", default=True, help="Show json output", flag_value="json"
)
def gpu_table(format):
    if format == "table":
        output = PrettyTable()
        output.field_names = ["rig_name", "name", "address", "gpu_id", "pci_id"]

        for rig in rigs.all_rigs():
            for gpu in rig["gpus"]:
                output.add_row(
                    [
                        rig["name"],
                        gpu["name"],
                        rig["local_addresses"][0],
                        gpu["id"],
                        gpu["pci_id"],
                    ]
                )
        click.echo(output)

    else:
        output = []
        for rig in rigs.all_rigs():
            for gpu in rig["gpus"]:
                output.append(
                    {
                        "rig_name": rig["name"],
                        "name": gpu["name"],
                        "address": rig["local_addresses"][0],
                        "gpu_id": gpu["id"],
                        "pci_id": gpu["pci_id"],
                    }
                )

        click.echo(json.dumps(output, indent=2))


@click.command()
@click.option(
    "--rig_id",
    type=click.STRING,
    help="The rig id, not required when using --all or --everywhere flags",
)
@click.option(
    "--farm_id",
    type=click.STRING,
    default="first",
    show_default=True,
    help="The farm id, defaults to first farm found, use '--all' flag for all farms",
)
@click.option(
    "--all",
    default=False,
    help="Run action on all rigs across the entire farm",
    is_flag=True,
)
@click.option(
    "--everywhere",
    default=False,
    help="Danger: Run action on all rigs across all farms",
    is_flag=True,
)
@click.option(
    "--action",
    required=True,
    type=click.Choice(
        ["disable", "poweroff", "reset", "enable", "restart", "reboot"],
        case_sensitive=False,
    ),
)
@click.option(
    "--simulate", is_flag=True, default=False, help="Simulate the action only"
)
@click.option(
    "--table", "format", default=True, help="Show table output", flag_value="table"
)
@click.option(
    "--json", "format", default=True, help="Show json output", flag_value="json"
)
@click.option(
    "--plain", "format", default=True, help="Show plain output", flag_value="plain"
)
def rig_control(action, rig_id, farm_id, all, everywhere, simulate, format):
    farm_ids = []
    if farm_id == "first":
        farm_ids = [farms.default_farm()["id"]]
    elif farm_id:
        farm_ids = [farm_id]
    elif everywhere:
        farm_ids = farms.farm_ids()
    else:
        farm_ids = []

    output = []
    if format == "table":
        output = PrettyTable()
        output.field_names = ["rig_name", "action"]
        format_block = lambda name, action: output.add_row([name, action])
    elif format == "json":
        output = []
        format_block = lambda name, action: output.append(
            {"rig_name": name, "action": action}
        )
    else:
        format_block = lambda name, action: output.append(
            f"{name} has been set to {action}"
        )

    if not rig_id and (all or everywhere):
        for farm_id in farm_ids:
            rigs.rig_control(
                action, "all", farm_id, simulate=simulate, block=format_block
            )
    else:
        rigs.rig_control(action, rig_id, farm_id, simulate=simulate, block=format_block)

    if format == "table":
        click.echo(output)
    elif format == "json":
        click.echo(json.dumps(output, indent=2))
    else:
        click.echo("\n".join(output))


entry_point.add_command(gpu_table, "gpus")
entry_point.add_command(rig_control, "control")
entry_point.add_command(get, "list")
entry_point.add_command(set_mining_profiles, "set-profiles")
