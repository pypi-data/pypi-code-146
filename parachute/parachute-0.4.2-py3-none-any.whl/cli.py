#!/usr/bin/env python3
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TextIO
from typing import Union

import click
import json5

from . import utils
from .craft_communication import CraftCommunication
from .data_types import Backup
from .data_types import Parameter
from .utils import bitmask_int_to_str
from .utils import debug
from .utils import get_craft_name
from .utils import RegexType
from .utils import set_bit
from .utils import TablePrinter


DEFAULT_SOCKET = "auto"
PARAM_REGEX = re.compile(
    r"^(?P<name>[A-Za-z0-9_]+)(?:(?:\:(?P<bit_index>\d+)|)=(?P<value>-?[\d\.]+)|)$"
)


class ParamType(click.ParamType):
    """The AP parameter type, for Click completion."""

    def shell_complete(self, ctx, param, incomplete):
        from .constants import AP_PARAMS

        return [click.shell_completion.CompletionItem(name) for name in AP_PARAMS]


def load_backup_from_file(backup_file: TextIO) -> Backup:
    """Load a list of parameters from a file."""
    data = json5.load(backup_file)
    return Backup.from_dict(data)


def option_decorator(fn: Callable) -> Callable:
    """Gather multiple reused options into one neat decorator."""
    fn = click.option(
        "-s",
        "--socket",
        default=DEFAULT_SOCKET,
        show_default=True,
        help="Path to the USB socket.",
    )(fn)
    fn = click.option(
        "-d",
        "--baud-rate",
        default=115200,
        show_default=True,
        help="The baud rate to use with the socket.",
    )(fn)
    return fn


def save_backup_to_file(backup: Backup, outfile: TextIO) -> None:
    """Save a list of parameters to a file."""
    # Brace yourselves, we're going to perform some horrible hacks to
    # format the file for readability.

    # Write the status comment.
    outfile.write(backup.status_str)

    backup_dict = backup.as_dict()

    # Pop the parameters from the backup dict so we can write them later.
    parameters = backup_dict.pop("parameters")
    backup_dict["parameters"] = {}

    # Write the top-level backup.
    backup_str = json5.dumps(backup_dict, indent=2)

    param_str = "".join(
        (
            "    " + json5.dumps({name: data})[1:-1] + ",\n"
            for name, data in parameters.items()
        )
    )

    # Insert the param_str into the rest of the file and write it.
    outfile.write(backup_str[:-4] + "\n" + param_str + "  " + backup_str[-4:])


def read_backup_from_craft(socket: str, baud_rate: int) -> Backup:
    """Read all the parameters from a craft."""
    # From https://www.ardusub.com/developers/pymavlink.html.
    craft = CraftCommunication(socket, baud_rate)
    backup = Backup()
    param_generator = craft.list_params()
    backup.status = next(param_generator)  # type: ignore
    debug(backup.status)
    count = next(param_generator)
    for parameter in param_generator:
        debug(parameter)
        click.echo(f"- {str(parameter.index).rjust(4)} / {count}  \r", nl=False, err=True)  # type: ignore
        backup.parameters[parameter.name] = parameter  # type: ignore
    return backup


@click.group()
@click.option("--debug", is_flag=True, help="Print debug information.")
@click.version_option()
def cli(debug: bool):
    utils.DEBUG = debug


@cli.command(help="Compare a previous backup to the parameters on a craft.")
@click.argument("backup_file", type=click.File("r"))
@click.argument("backup_file2", type=click.File("r"), required=False)
@option_decorator
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.option(
    "-b", "--only-backup", is_flag=True, help="Only show values in the backup file."
)
@click.option("-c", "--only-craft", is_flag=True, help="Only show values in the craft.")
def compare(
    backup_file: TextIO,
    baud_rate: int,
    socket: str,
    filter: Optional[re.Pattern],
    backup_file2: Optional[TextIO] = None,
    only_backup: bool = False,
    only_craft: bool = False,
):
    backup_name = get_craft_name(backup_file.name, "Backup")
    if backup_file2:
        click.echo("Comparing parameters between two backups...", err=True)
        backup2 = load_backup_from_file(backup_file2)
        count = len(backup2.parameters)
        param_generator: Iterable[Parameter] = backup2.parameters.values()

        backup2_name = get_craft_name(backup_file2.name, "Backup 2")
    else:
        click.echo("Comparing parameters between a backup and a craft...", err=True)

        craft = CraftCommunication(socket, baud_rate)

        param_generator = craft.list_params()  # type: ignore
        next(param_generator)  # type: ignore
        count = next(param_generator)  # type: ignore
        backup2_name = "Craft"

    with TablePrinter("Parameter name", backup_name, backup2_name) as p:
        backup = load_backup_from_file(backup_file)
        backup.filter(filter)

        all_parameters = set(backup.parameters.keys())
        seen_parameters = set()

        # Print parameters on the craft.
        for parameter in param_generator:
            click.echo(
                f"- {str(parameter.index).rjust(4)} / {count}  \r", nl=False, err=True
            )
            # Ignore filtered parameters.
            if filter and not filter.search(parameter.name):
                continue

            if parameter.name in seen_parameters:
                # We've already seen this one.
                continue
            else:
                seen_parameters.add(parameter.name)

            if parameter.name in all_parameters:
                backup_value = backup.parameters[parameter.name].value
            else:
                if only_backup:
                    # We only want to see parameters that exist in the file,
                    # so skip this line.
                    continue
                backup_value = "-"

            if parameter.value != backup_value:
                p(parameter.name, backup_value, parameter.value)

        if not only_craft:
            # Print parameters that were in the backup file but not the craft.
            for pname in sorted(all_parameters - seen_parameters):
                p(pname, backup.parameters[pname].value, "-")


@cli.command(help="Reset the craft parameters to their default values.")
@option_decorator
def reset_to_defaults(socket: str, baud_rate: int):
    click.echo("Resetting all parameters to their default values...")
    craft = CraftCommunication(socket, baud_rate)
    craft.reset_to_default()
    click.echo("Rebooting...")
    craft.reboot()
    click.echo("Done.")


@cli.command(
    help="Force the FC to accept the current accel/compass calibration (make"
    " sure to have the values already loaded)."
)
@option_decorator
def force_accept_calibration(socket: str, baud_rate: int):
    click.echo("Accepting calibration...")
    craft = CraftCommunication(socket, baud_rate)
    craft.force_accept_calibration(component="both")
    click.echo("Rebooting...")
    craft.reboot()
    click.echo("Done.")


@cli.command(help="Reboot the controller.")
@option_decorator
def reboot(socket: str, baud_rate: int):
    click.echo("Rebooting...")
    craft = CraftCommunication(socket, baud_rate)
    craft.reboot()
    click.echo("Done.")


@cli.command(help="Restore a previous backup to a craft.")
@click.argument("backup_file", type=click.File("r"))
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.option(
    "-c",
    "--compare",
    is_flag=True,
    help="Compare the new parameter with the old and only restore what's changed.",
)
@option_decorator
def restore(
    backup_file: TextIO,
    filter: Optional[re.Pattern],
    compare: bool,
    socket: str,
    baud_rate: int,
):
    click.echo("Restoring parameters...")
    craft = CraftCommunication(socket, baud_rate)
    backup = load_backup_from_file(backup_file)
    backup.filter(filter)
    if compare:
        counter = 0
        with TablePrinter("Parameter name", "Old value", "New value") as p:
            for name, new_parameter in backup.parameters.items():
                click.echo(" " + r"-\|/"[counter % 4] + "\r", nl=False)
                counter += 1
                try:
                    old_parameter = craft.get_param(Parameter(name=name))
                except ValueError:
                    click.echo(f"Parameter {name} does not exist, skipping...")
                    continue
                if new_parameter.value == old_parameter.value:
                    continue
                p(new_parameter.name, old_parameter.value, new_parameter.value)
                craft.set_param(new_parameter)
    else:
        with TablePrinter("Parameter name", "New value") as p:
            for name, new_parameter in backup.parameters.items():
                p(new_parameter.name, new_parameter.value)
                craft.set_param(new_parameter)


@cli.command(help="Back up all the parameters from a craft to a file.")
@click.argument("craft_name")
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.option(
    "-o",
    "--outdir",
    default=".",
    show_default=True,
    type=click.Path(exists=True, file_okay=False, writable=True),
    help="Directory to write the backup file to.",
)
@option_decorator
def backup(
    craft_name: str,
    socket: str,
    baud_rate: int,
    outdir: str,
    filter: Optional[re.Pattern],
):
    click.echo("Reading parameters...")
    backup = read_backup_from_craft(socket, baud_rate)
    click.echo("Writing to file...")
    filename = Path(outdir) / (
        f"{craft_name.replace(' ', '_')}_"
        f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
        ".chute"
    )

    backup.filter(filter)

    # Write the actual backup.
    with filename.open("w") as outfile:
        save_backup_to_file(backup, outfile)
    click.echo("Done.")


@cli.command(help="Filter parameters by a regular expression.")
@click.argument("regex", type=RegexType())
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def filter(regex: Optional[re.Pattern], backup_file: TextIO, output_file: TextIO):
    click.echo("Filtering based on regular expression...")
    backup = load_backup_from_file(backup_file)
    backup.filter(regex)
    save_backup_to_file(backup, output_file)
    click.echo("Done.")


@cli.command(help="Print parameters from either a backup file or a craft.")
@click.argument("backup_file", type=click.File("r"), required=False)
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@option_decorator
def show(
    backup_file: TextIO,
    filter: Optional[re.Pattern],
    socket: str,
    baud_rate: int,
):
    click.echo("Retrieving parameters...", err=True)

    if backup_file:
        backup = load_backup_from_file(backup_file)
    else:
        backup = read_backup_from_craft(socket, baud_rate)

    backup.filter(filter)

    with TablePrinter("Parameter name", "Value") as p:
        for name, parameter in sorted(backup.parameters.items()):
            p(name, parameter.value)


@cli.command(name="get", help="Get and print parameters.")
@click.argument("params", nargs=-1, type=ParamType())
@click.option(
    "-b",
    "--binary",
    is_flag=True,
    help="Show the value as a binary value.",
)
@option_decorator
def get_params(params: Iterable[str], binary: bool, socket: str, baud_rate: int):
    click.echo("Retrieving parameters...", err=True)
    craft = CraftCommunication(socket, baud_rate)

    with TablePrinter("Parameter name", "Bits" if binary else "Value") as p:
        for parameter in sorted(params):
            try:
                param = craft.get_param(Parameter(name=parameter))
            except ValueError as e:
                sys.exit(str(e))
            if binary and (param.value != int(param.value)):
                sys.exit(
                    f"Parameter {param.name} is not an integer, are you "
                    "sure you have the right name?"
                )
            p(
                param.name,
                bitmask_int_to_str(param.value) if binary else param.value,
            )


@cli.command(name="set", help="Set parameters.")
@click.argument("params", nargs=-1, type=ParamType())
@option_decorator
def set_params(params: Iterable[str], socket: str, baud_rate: int):
    craft = CraftCommunication(socket, baud_rate)

    with TablePrinter("Parameter name", "Old value", "New value") as p:
        for param in params:
            match = PARAM_REGEX.search(param)
            if not match:
                click.echo(
                    f"Wrong parameter syntax: {param} (should be `NAME=VALUE` "
                    "or `NAME:bit=VALUE`).",
                    err=True,
                )
                continue

            name = match.groups()[0]
            bit_index: Union[None, str, int] = match.groups()[1]
            value: Union[str, int, bool] = match.groups()[2]

            try:
                old_parameter = craft.get_param(Parameter(name=name))
            except ValueError as e:
                sys.exit(str(e))

            if bit_index:
                bit_index = int(bit_index)
                value = set_bit(
                    int(old_parameter.value),
                    bit_index,
                    False if value == "0" else True,
                )

            new_parameter = Parameter(name=name, value=value)

            if bit_index:
                p(
                    name,
                    bitmask_int_to_str(old_parameter.value),
                    bitmask_int_to_str(new_parameter.value),
                )
            else:
                p(name, old_parameter.value, new_parameter.value)

            craft.set_param(new_parameter)


@cli.group(help="Convert a Parachute backup into another format.")
@click.option(
    "-f",
    "--filter",
    type=RegexType(),
    help="Filter commands to process based on a regex.",
)
@click.pass_context
def convert(ctx, filter: Optional[re.Pattern]):
    ctx.ensure_object(dict)

    ctx.obj["FILTER"] = filter


@convert.command(help='Convert into a QGroundControl ".params" file.')
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.pass_context
def qgc(ctx, backup_file: TextIO, output_file: TextIO):
    click.echo("Converting to a QGroundControl compatible file...")
    backup = load_backup_from_file(backup_file)
    backup.filter(ctx.obj["FILTER"])

    output_file.write("# Vehicle-Id Component-Id Name Value Type\n")
    output_file.writelines(
        f"1\t1\t{name}\t{parameter.value:.18g}\t{parameter.type}\n"
        for name, parameter in sorted(backup.parameters.items())
    )
    output_file.close()


@convert.command(help='Convert into a Mission Planner ".param" file.')
@click.argument("backup_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
@click.pass_context
def mp(ctx, backup_file: TextIO, output_file: TextIO):
    click.echo("Converting to a Mission Planner compatible file...")
    backup = load_backup_from_file(backup_file)
    backup.filter(ctx.obj["FILTER"])

    output_file.writelines(
        f"{name},{parameter.value:.9f}\n"
        if parameter.is_float
        else f"{name},{parameter.value}\n"
        for name, parameter in sorted(backup.parameters.items())
    )
    output_file.close()


if __name__ == "__main__":
    cli()
