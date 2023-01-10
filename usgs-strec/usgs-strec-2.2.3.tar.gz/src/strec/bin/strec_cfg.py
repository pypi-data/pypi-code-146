#!/usr/bin/env python

# stdlib imports
import logging
import pathlib
import sys
from enum import Enum
from io import StringIO

# third party imports
import typer

# local imports
from strec.database import fetch_dataframe, read_datafile, stash_dataframe
from strec.gcmt import fetch_gcmt
from strec.slab import get_slab_grids
from strec.utils import create_config, get_config, get_config_file_name

app = typer.Typer()


# I hoped making an enum of string = loglevel would be clear, but typer prints the integer values
# of the log levels instead of CRITICAL, ERROR, etc. Making an enum and then a dict to make this
# clearer.
class LoggingLevel(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


LOGDICT = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


def config_exists():
    config_file = get_config_file_name()
    return config_file.exists()


def get_datafolder():
    try:
        config = get_config()
        datafolder = config["DATA"]["folder"]
        return datafolder
    except Exception:
        return None


@app.command()
def info():
    if not config_exists():
        print("No config file exists at. Run the update command.")
        sys.exit(1)
    config_file = get_config_file_name()
    print(f"Config file {config_file}:")
    print("------------------------")
    config = get_config()
    config_str = StringIO()
    config.write(config_str)
    config_str.seek(0)
    print(config_str.getvalue().rstrip())
    print("------------------------\n")
    dbfile = config["DATA"]["dbfile"]
    dataframe = fetch_dataframe(dbfile)
    nsources = len(dataframe["source"].unique())
    print(
        (
            f"Moment Tensor Database ({dbfile}) contains {len(dataframe)} "
            f"events from {nsources} sources.\n"
        )
    )
    slabfolder = config["DATA"]["slabfolder"]
    slab_files = list(pathlib.Path(slabfolder).glob("*.grd"))
    names = [slab_file.name for slab_file in slab_files]
    slabs = set([name.split("_")[0] for name in names])
    print(
        (
            f"There are {len(slab_files)} slab grids from {len(slabs)} "
            f"unique slab models located in {slabfolder}."
        )
    )
    sys.exit(0)


@app.command()
def update(
    datafolder: str = typer.Option(
        get_datafolder,
        help=(
            "Folder where slab data and moment tensor data will be stored. "
            "Defaults to previously configured value."
        ),
    ),
    slab: bool = typer.Option(False, help="Download slab data"),
    gcmt: bool = typer.Option(False, help="Download GCMT moment tensor data"),
    moment_data: str = typer.Option(None, help="Supply moment data as CSV/Excel"),
    moment_data_source: str = typer.Option(
        "unknown", help="Supply moment data source (US, CI, etc.)"
    ),
    log: LoggingLevel = typer.Option(
        "INFO",
        help=(
            "Set logging level (https://docs.python.org/3/"
            "library/logging.html#logging-levels)"
        ),
    ),
):
    if log:
        logging.basicConfig(level=LOGDICT[log])
    if datafolder is None:
        print("Config file does not exist. Please specify a datafolder.")
        sys.exit(1)
    if gcmt and (moment_data is not None or moment_data_source != "unknown"):
        print(
            (
                "You may either choose to download GCMT "
                "moment tensors or install your own source, not both."
            )
        )
        sys.exit(1)
    datafolder = pathlib.Path(datafolder)
    if not config_exists():
        config = create_config(datafolder)
    else:
        config = get_config()
        if str(datafolder) != config["DATA"]["folder"]:
            # TODO - update or raise error?
            print("datafolder is already configured. Exiting.")
            sys.exit(1)

    messages = []
    if slab:
        slabfolder = pathlib.Path(config["DATA"]["slabfolder"])
        if not slabfolder.exists():
            slabfolder.mkdir(parents=True)
        slab_result, slab_msg = get_slab_grids(slabfolder)
        if not slab_result:
            messages.append(slab_msg)
    if gcmt:
        try:
            gcmt_dataframe = fetch_gcmt()
            dbfile = config["DATA"]["dbfile"]
            source = "GCMT"
            stash_dataframe(gcmt_dataframe, dbfile, source, create_db=True)
        except Exception as e:
            gcmt_msg = f"Failed to download GCMT data: {str(e)}"
            messages.append(gcmt_msg)

    if moment_data:
        try:
            moment_dataframe = read_datafile(moment_data)
            stash_dataframe(
                moment_dataframe, dbfile, moment_data_source, create_db=True
            )
        except Exception as e:
            moment_msg = f"Could not parse moment datafile {moment_data}: {str(e)}"
            messages.append(moment_msg)
    if len(messages):
        print("Errors were encountered during the course of downloading/loading data:")
        for message in messages:
            print(f"'{message}'")
    sys.exit(0)


if __name__ == "__main__":
    app()
