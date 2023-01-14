#!/usr/bin/env python3

'''
Delete suboptimal runs.
'''

import argparse
import logging
import pathlib
import subprocess
import tempfile

import pandas as pd

from mlflow.tracking import _get_store

from mlflow_extra.common import configure_logging


LOGGER = logging.getLogger(__name__)
METRIC_PREFIX = 'metrics.'


def export_csv(experiment_id, path):
    '''
    Export experiment data to a CSV file.

    Args:
        experiment_id:
            The experiment ID.

        path:
            The output path.
    '''
    path = pathlib.Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.debug('Exporting data from experiment %d', experiment_id)
    subprocess.run(
        ('mlflow', 'experiments', 'csv', '-x', str(experiment_id), '-o', str(path)),
        stdout=subprocess.DEVNULL,
        check=True
    )


def list_metrics(data):
    '''
    Print metric data to STDOUT.

    Args:
        data:
            The data loaded from the CSV file.
    '''
    data = data.filter(regex=f'^{METRIC_PREFIX}', axis=1)
    data.columns = [col[len(METRIC_PREFIX):] for col in data.columns]
    data = data[sorted(data.columns)]
    for _metric, values in data.iteritems():
        print(values.describe())
        print()


def filter_by_threshold(data, thresholds, ascending=False):
    '''
    Filter rows in data by threshold values.

    Args:
        data:
            The data to filter.

        thresholds:
            A dict mapping column names to threshold values.


        ascending:
            If True, keep values less than or equal to the thresold values,
            otherwise keep values greater than or equal to the threshold values.
    '''
    for name, value in thresholds.items():
        if ascending:
            data = data[data[name] <= value]
        else:
            data = data[data[name] >= value]
    return data


def filter_by_number(data, columns, number, ascending=False):
    '''
    Filter rows to only keep a selected number.

    Args:
        data:
            The data to filter.

        columns:
            The columns by which to filter the data before selecting the rows.

        number:
            The number of rows to keep.

        ascending:
            If True, sort the data in ascending order before selecting the rows
            to keep, otherwise sort in descending order.
    '''
    return data.sort_values(by=columns, ascending=ascending).head(n=number)


def delete_runs(run_ids, total_runs, confirm=False):
    '''
    Delete the selected runs

    Args:
        run_ids:
            An iterable of run IDs to delete.

        total_runs:
            The total number of runs in the data, only used for display.

        confirm:
            If True, delete the run, else perform a dryrun.

    Returns:
        True if anything was deleted, False otherwise.
    '''
    LOGGER.debug('Loading MLflow data store')
    store = _get_store()
    n_runs = len(run_ids)
    LOGGER.info(
        '%d / %d run%s selected for deletion',
        n_runs,
        total_runs,
        '' if n_runs == 1 else 's'
    )
    prefix = '' if confirm else '[DRYRUN] '
    deleted = False
    for i, run_id in enumerate(run_ids, start=1):
        LOGGER.info('%sDeleting run %s [%d / %d]', prefix, run_id, i, n_runs)
        if confirm:
            #  subprocess.run(
            #      ('mlflow', 'runs', 'delete', '--run-id', str(run_id)),
            #      stdout=subprocess.DEVNULL,
            #      check=True
            #  )
            store.delete_run(run_id)
            deleted = True
    if deleted:
        print('Runs can be restored with mlflow runs restore --run-id <run_id>')

    return deleted


def script_filter_runs(args=None):  # pylint: disable=too-many-locals
    '''
    Delete runs from experiment based on thresholds.
    '''
    configure_logging()

    parser = argparse.ArgumentParser(description=script_filter_runs.__doc__)
    parser.add_argument(
        'experiment_id',
        type=int,
        nargs='+',
        help='The MLflow experiment ID (see mlflow experiments list).'
    )
    parser.add_argument(
        '-a', '--ascending',
        action='store_true',
        help='Keep the first n runs in ascending order instead of descending.'
    )
    parser.add_argument(
        '-c', '--confirm',
        action='store_true',
        help='Confirm the deletion. Without this only a dryrun is performed.'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List metrics and their statistics.'
    )
    parser.add_argument(
        '-m', '--metrics',
        nargs='+',
        action='extend',
        help='The metrics by which to filter runs.'
    )
    parser.add_argument(
        '-n', '--number',
        type=int,
        help='The number of runs to keep.'
    )
    parser.add_argument(
        '-t', '--thresholds',
        nargs='+',
        action='extend',
        type=float,
        help=('''
            The threshold values for the selected metrics. In descending order
            the threshold values are a lower limit. In ascending order they are
            an upper limit.
        ''')
    )
    pargs = parser.parse_args(args=args)
    has_req_args = pargs.metrics and (pargs.thresholds or pargs.number is not None)
    if not (has_req_args or pargs.list):
        LOGGER.warning('You must select either a number of a threshold value.')
        return

    run_ids = set()
    total_runs = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        for experiment_id in pargs.experiment_id:
            # Extract the run data to a temporary CSV file.
            tmpdir = pathlib.Path(tmpdir)
            csv_path = tmpdir / 'run.csv'
            export_csv(experiment_id, csv_path)
            data = pd.read_csv(csv_path)
            if not data:
                LOGGER.warning('no data for experiment %s', experiment_id)
                continue

            # List data and exit if requested.
            if pargs.list:
                list_metrics(data)
                continue

            total_runs += data.shape[0]
            data_to_keep = data
            metrics = [METRIC_PREFIX + m for m in pargs.metrics]

            # Filter by selected metrics.
            if pargs.thresholds:
                data_to_keep = filter_by_threshold(
                    data_to_keep,
                    dict(zip(metrics, pargs.thresholds)),
                    ascending=pargs.ascending
                )

            # Filter to the selected number of runs.
            if isinstance(pargs.number, int) and pargs.number >= 0:
                data_to_keep = filter_by_number(
                    data_to_keep, metrics, pargs.number, ascending=pargs.ascending
                )
            run_ids.update(set(data['run_id']) - set(data_to_keep['run_id']))

    delete_runs(run_ids, total_runs, confirm=pargs.confirm)


if __name__ == '__main__':
    script_filter_runs()
