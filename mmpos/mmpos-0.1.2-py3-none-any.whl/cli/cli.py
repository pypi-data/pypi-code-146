import click
import os
from mmpos.cli.rigs import commands as rigs
from mmpos.cli.farms import commands as farms
from mmpos.cli.profiles import commands as profiles
import sys


@click.group()
@click.version_option(version="0.1.2", prog_name="mmpos cli")
def entry_point():
    pass


entry_point.add_command(rigs.entry_point, "rigs")
entry_point.add_command(farms.entry_point, "farms")
entry_point.add_command(profiles.entry_point, "profiles")


def main(prog_name="mmpos"):
    try:
        os.environ["MMPOS_API_TOKEN"]
        entry_point()
    except KeyError as e:
        if "MMPOS_API_TOKEN" in "f{e}":
            print("MMPOS_API_TOKEN environment variable not set")
        else:
            print(e)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
