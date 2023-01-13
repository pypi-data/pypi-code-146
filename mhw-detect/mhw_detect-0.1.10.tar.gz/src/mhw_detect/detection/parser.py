import os
import glob
import xarray as xr


def check_precalc_clim_thresh(data):
    if not {"clim", "percent"} <= data.keys():
        print(
            "Precalculated mean and/or percentile have not been referenced in config file. \n\
        They will be recalculated by Hobday's method."
        )


def check_file_exist(conf):
    for datas in conf["data"]:
        if not os.path.exists(conf["data"][datas]["path"]):
            raise ValueError("This file does not exist: ", conf["data"][datas]["path"])


def parse_data(conf, cut=True):
    if cut:
        parse_path = lambda p: os.path.join(os.path.dirname(p), "Cut_")
    else:
        parse_path = lambda p: p

    data = {
        datas: [parse_path(conf["data"][datas]["path"]), conf["data"][datas]["var"]]
        for datas in conf["data"]
    }
    check_precalc_clim_thresh(data)
    return data


def parse_param(conf):
    return {params: conf["params"][params] for params in conf["params"]}


def count_files(conf):
    return (
        len(
            [
                name
                for name in glob.glob(
                    os.path.dirname(conf["data"]["data"]["path"]) + "/Cut_*.nc"
                )
            ]
        )
        + 1
    )


def check_climato_period(conf):
    ds = xr.open_dataset(conf["data"]["data"]["path"])
    period = conf["params"]["climatologyPeriod"]

    min = ds.time.min().values.astype("datetime64[Y]").astype(int) + 1970
    max = ds.time.max().values.astype("datetime64[Y]").astype(int) + 1970

    assert (period[0] >= min) or (
        period[1] <= max
    ), "The dataset does not cover the climatologyPeriod."
