import os
import xarray as xr
import itertools
import click
import yaml
from dask.diagnostics import ProgressBar


# Créer un dataset par chunk dask
def split_by_chunks(dataset):
    chunk_slices = {}
    for dim, chunks in dataset.chunks.items():
        slices = []
        start = 0
        for chunk in chunks:
            if start >= dataset.sizes[dim]:
                break
            stop = start + chunk
            slices.append(slice(start, stop))
            start = stop
        chunk_slices[dim] = slices
    for slices in itertools.product(*chunk_slices.values()):
        selection = dict(zip(chunk_slices.keys(), slices))
        yield dataset[selection]


@click.command(
    help="""
    Cut datasets in multiple files
    """
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Specify configuration file",
)
def cut(config: str):
    conf = yaml.safe_load(open(config, "r"))

    lat = conf["cut"]["nb_lat"]
    lon = conf["cut"]["nb_lon"]

    for datas in conf["data"]:

        path = conf["data"][datas]["path"]
        ds = xr.open_dataset(path)

        if "latitude" in ds.coords:
            chunks = {"latitude": lat, "longitude": lon}
        else:
            chunks = {"lat": lat, "lon": lon}

        ds = xr.open_dataset(path, chunks=chunks)

        chunked_ds = list(split_by_chunks(ds))

        p = [
            os.path.dirname(path) + "/Cut_" + str(i + 1) + ".nc"
            for i in range(len(chunked_ds))
        ]
        print("Saving in " + os.path.dirname(path))
        delayed = xr.save_mfdataset(datasets=chunked_ds, paths=p, compute=False)
        with ProgressBar():
            delayed.compute()
        print(str(len(chunked_ds)) + " files saved.")


if __name__ == "__main__":
    cut()
