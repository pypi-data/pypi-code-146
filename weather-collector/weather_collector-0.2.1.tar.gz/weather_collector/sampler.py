"""
Module for formatting Python files

:author: Julian M. Kleber
"""
import os
import click
import time
import datetime

from typing import Any, Optional

from amarium.utils import make_full_filename
from bulkhead.sampler.sampler import SamplerEndpoints

from weather_collector.weather_collection import get_collection


@click.command()
@click.option("-i", help="Sample interval")
@click.option("-n", default=None, help="Number of iterations")
@click.option("-l", help="Longitude")
@click.option("-o", help="Output file name")
@click.option("-t", help="Latitude")
def sample(
    o: str, i: float, l: float, t: float, n: Optional[int] = None
) -> None:  # pragma: no cover
    """
    The sample function is a wrapper for the sample_infinite_intervall function.
    It takes in an output file path, and an interval as parameters. The output file
    path is used to create a directory where the sampled data will be saved, and
    the interval is used to determine how often sampling should occur. The sample
    wrapper function then calls the sample_infinite_intervall function with these two
    parameters along with some other parameters that are specific to this project.

    :param o:str: Used to Define the output file name and location.
    :param i:float: Used to Set the interval in seconds.
    :return: A nonetype object.

    :doc-author: Julian M. Kleber
    """
    lon = l
    lat = t

    save_dir = os.path.dirname(o)
    file_name = os.path.basename(o)

    header = [
        "time_stamp",
        "OpenWeatherMap",
        "Tomorrow.io",
        "WeatherAPI",
        "mean",
        "lon",
        "lat",
    ]

    value_name = "cloud_cover"
    method_name = "get_time_mean_atomic_vals"
    method_parameters = {"value_name": value_name}
    interval = i
    num_runs = n

    ec = get_collection()
    sampler = SamplerEndpoints(object_instance=ec)
    if num_runs is None:
        sample_infinite_interval(
            file_name=file_name,
            save_dir=save_dir,
            header=header,
            method_name=method_name,
            interval=interval,
            sampler=sampler,
            method_parameters=method_parameters,
            lon=lon,
            lat=lat,
        )
    else:
        sample_finite_interval(
            file_name=file_name,
            save_dir=save_dir,
            header=header,
            method_name=method_name,
            interval=interval,
            sampler=sampler,
            method_parameters=method_parameters,
            lon=lon,
            lat=lat,
            num_runs=num_runs,
        )


def sample_finite_interval(**kwargs: Any) -> None:
    """
    The sample_finite_interval function samples data from the specified source at a fixed interval.

    :param **kwargs:Any: Used to Pass in the parameters of the function.
    :return: Nothing, but it does print the data to the console.

    :doc-author: Julian M. Kleber
    """

    num_runs = int(kwargs["num_runs"])
    interval = float(kwargs["interval"])

    for i in range(num_runs):
        try:
            one_step(**kwargs)
        except Exception as e:  # pragma no cover
            print(
                "Could not sample data at time {time}".format(
                    time=str(datetime.datetime.now())
                )
            )
            print(e)
            continue
        finally:
            time.sleep(interval)


def sample_infinite_interval(**kwargs: Any) -> None:  # pragma no-cover
    """
    The sample_infinite_intervall function samples the data from a given interval and saves it to a csv file.
        The function is called in an infinite loop, so that the sampling can be done continuously.

    :param **kwargs:Any: Used to Pass in a dictionary of arguments.
    :return: Nothing.

    :doc-author: Julian M. Kleber
    """
    interval = int(kwargs["interval"])

    while True:
        try:
            one_step(**kwargs)
        except Exception as e:
            print(
                "Could not sample data at time {time}".format(
                    time=str(datetime.datetime.now())
                )
            )
            print(e)
            continue
        finally:
            time.sleep(interval)


def one_step(**kwargs) -> None:
    """
    The one_step function is a wrapper for the sampler.sample_intervall function, which is used to sample data.
    The one_step function takes in several arguments and returns nothing. It does however save
    the sampled data to a csv file with the name specified by the user.

    :param **kwargs: Used to Pass a variable number of keyword arguments to a function.
    :return: A list of values.

    :doc-author: Julian M. Kleber
    """

    file_name = str(kwargs["file_name"])
    save_dir = str(kwargs["save_dir"])
    header = list(kwargs["header"])
    method_name = str(kwargs["method_name"])
    sampler = kwargs["sampler"]
    method_parameters = kwargs["method_parameters"]
    lon = float(kwargs["lon"])
    lat = float(kwargs["lat"])

    data = sampler.sample_intervall(
        method_name=method_name,
        interval=0,
        num=1,
        method_parameters=method_parameters,
        lon=lon,
        lat=lat,
    )[0]
    data.append(lon)
    data.append(lat)
    print(data)
    check_name = make_full_filename(save_dir, file_name)
    if os.path.isfile(check_name):
        sampler.save_to_csv(save_dir, file_name, data)
    else:
        sampler.save_to_csv(save_dir, file_name, data, header)


if __name__ == "__main__":
    sample()
