import requests
import json
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from sca3s_cli.parser import get_token
from datetime import datetime, timezone
from classes.middleware_status import MWStatus

def submit_job(args):
    """
    Submit job to SCA3S
    :param args: Arguments passed to argparser.
    """
    with open(args.file, 'r') as fd:
        json_data = json.load(fd)
    res = requests.post(url="https://sca3s.scarv.org/api/acquire/job",
                        headers=_header_builder(args.scope),
                        json=json_data)
    if res.status_code != 200:
        return 1
    rprint('Job successfully created.')


def list_jobs(args):
    """
    List jobs on SCA3S
    :param args: Arguments passed to argparser.
    """
    res = requests.get(url="https://sca3s.scarv.org/api/acquire/jobs",
                       headers=_header_builder(args.scope))
    if res.status_code != 200:
        return 1
    jobs = res.json()['jobs']
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim")
    table.add_column("Job Type")
    table.add_column("Device ID")
    table.add_column("Driver ID")
    table.add_column("Major Count")
    table.add_column("Submit Time")
    table.add_column("Expiry Time")
    table.add_column("Status")
    for job in jobs:
        table.add_row(
            job['job_id'][:10],
            job['job_type'],
            job['device_id'],
            job['driver_id'],
            str(job['trace_spec']['count_major']),
            _timestamp_parser(job['submit_time']),
            _timestamp_parser(job['expiry_time']),
            str(MWStatus.build(job['status']).describe())
        )
    console.print(table)


def get_job(args):
    """
    List jobs on SCA3S
    :param args: Arguments passed to argparser.
    """
    res = requests.get(url="https://sca3s.scarv.org/api/acquire/job/" + args.job,
                       headers=_header_builder(args.scope))
    if res.status_code != 200:
        return 1
    job = res.json()
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim")
    table.add_column("Job Type")
    table.add_column("Device ID")
    table.add_column("Driver ID")
    table.add_column("Major Count")
    table.add_column("Submit Time")
    table.add_column("Expiry Time")
    table.add_column("Status")
    table.add_row(
        job['job_id'][:10],
        job['job_type'],
        job['device_id'],
        job['driver_id'],
        str(job['trace_spec']['count_major']),
        _timestamp_parser(job['submit_time']),
        _timestamp_parser(job['expiry_time']),
        str(MWStatus.build(job['status']).describe())
    )
    console.print(table)


def delete_job(args):
    """
    Delete job from SCA3S
    :param args: Arguments passed to argparser.
    """
    res = requests.delete(url="https://sca3s.scarv.org/api/acquire/job/" + args.job,
                          headers=_header_builder(args.scope))
    if res.status_code != 200:
        return 1
    rprint('Job successfully deleted.')


def _header_builder(scope):
    """
    Builds a header for requests for SCA3S.
    """
    return {
        'Authorization': 'token ' + get_token(scope),
        'Accept-Version': '2.0'
    }


def _timestamp_parser(timestamp):
    """
    Convert timestamp into human readable string.
    :param timestamp: timestamp integer.
    :return: human readable text string.
    """
    if timestamp is None:
        return None
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.strftime('%d-%m-%Y %H:%M GMT')
