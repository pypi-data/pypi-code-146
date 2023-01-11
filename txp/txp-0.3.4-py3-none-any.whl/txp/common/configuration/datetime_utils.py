"""This module defines utilities used commonly in the TXP
packages when dealing with datetime module and configuration
values"""

from datetime import datetime, timedelta
from txp.common.configuration.job import SamplingParameters
from typing import Optional
from logging import Logger


def get_num_windows_in_task(
    task_parameters: SamplingParameters
):
    """Return the number of sampling windows that fit in the interval declared
    in the sampling parameters."""
    current_date = datetime.now().date()
    end_date = current_date
    if task_parameters.end_time <= task_parameters.start_time:  # ends next day.
        end_date = (datetime.now() + timedelta(days=1)).date()

    start_datetime = datetime.combine(current_date, task_parameters.start_time)
    end_datetime = datetime.combine(end_date, task_parameters.end_time)
    diff = end_datetime - start_datetime
    num_samplings = int(
        diff.total_seconds() / task_parameters.sampling_window.observation_time
    )

    return num_samplings
