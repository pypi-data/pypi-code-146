import os
import sys
import multiprocessing as mp
from functools import partial
import pandas as pd
import xarray as xr
import yaml
import click
from typing import Tuple

from src.mhw_detect.detection.parser import (
    check_climato_period,
    check_file_exist,
    parse_data,
    parse_param,
    count_files,
)
from src.mhw_detect.detection.detect import prepare_data


@click.command(
    help="""
    Detect extreme events
    """
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Specify configuration file",
)
@click.option(
    "--geographical-subset",
    "-g",
    type=(
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-180, max=180),
        click.FloatRange(min=-180, max=180),
    ),
    help="The geographical subset as "
    + "minimal latitude, maximal latitude, "
    + "minimal longitude and maximal longitude.\n\n"
    + "If set, the detection will be done on the subsetted global dataset given in config file (not the cuts) and sequentially.",
)
@click.option(
    "--categ-map/--no-categ-map",
    type=bool,
    help="Generate category map in a netcdf file.",
    default=False,
    show_default=True,
)
def extreme_events(
    config: str,
    geographical_subset: Tuple[float, float, float, float],
    categ_map: bool,
):
    conf = yaml.safe_load(open(config, "r"))

    output = conf["output_detection"]

    try:
        check_file_exist(conf)
    except Exception as error:
        print(repr(error))
        sys.exit()

    param = parse_param(conf)

    if geographical_subset != None:
        data = parse_data(conf, False)

        lat = geographical_subset[0:2]
        lon = geographical_subset[2:4]

        prepare_data(
            0,
            output,
            mask=categ_map,
            lat=lat,
            lon=lon,
            p=param["pctile"],
            **data,
            **param
        )

        print("Creating csv")
        df = pd.read_csv(os.path.join(output, "0.txt"), sep=";")
        df.to_csv(os.path.join(output, "data.csv"), sep=";")

        if categ_map:
            os.rename(output + "/0.txt.nc", output + "/mask.nc")

    else:
        data = parse_data(conf)
        nfile = count_files(conf)

        if "clim" not in data:
            check_climato_period(conf)

        pool = mp.Pool()
        pool.map(
            partial(
                prepare_data,
                outdir=output,
                mask=categ_map,
                p=param["pctile"],
                **data,
                **param
            ),
            range(1, nfile),
        )
        pool.close()
        pool.join()

        print("Computation done")

        print("Creating csv")

        def f(i):
            return pd.read_csv(i, sep=";")

        filepaths = [os.path.join(output, str(i) + ".txt") for i in range(1, nfile)]
        df = pd.concat(map(f, filepaths))
        df.to_csv(os.path.join(output, "data.csv"), sep=";")

        if categ_map:
            print("Creating mask")
            mask = xr.open_mfdataset(output + "/*.nc")
            comp = dict(zlib=True)
            encoding = {var: comp for var in mask.data_vars}
            mask.to_netcdf(output + "/mask.nc", encoding=encoding)
            p = [os.path.join(output, str(g) + ".txt.nc") for g in range(1, nfile)]

            for path in p:
                try:
                    os.remove(path)
                except OSError:
                    click.echo("Error while deleting file: ", path)


if __name__ == "__main__":
    extreme_events()
