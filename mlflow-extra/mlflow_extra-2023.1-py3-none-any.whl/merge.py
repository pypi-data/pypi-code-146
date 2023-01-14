#!/usr/bin/env python3
'''
Merge experiments into a common directory.
'''

import argparse
import logging
import pathlib
import shutil

import yaml

from mlflow_extra.common import configure_logging
from mlflow_extra.metadata import Metadata

LOGGER = logging.getLogger(__name__)


def update_experiment_ids(path, new_id):
    '''
    Update the experiment ID in all metadata files under the given path.

    Args:
        path:
            The path under which to update the experiment IDs.

        new_id:
            The new experiment ID.
    '''
    for data in Metadata().find_meta(path):
        old_id = data.experiment_id
        if old_id != new_id:
            LOGGER.info(
                'Replacing experiment ID %s with %s in %s',
                old_id,
                new_id,
                data.path
            )
            data.experiment_id = new_id
            data.save()


def fix_experiment_ids(path):
    '''
    Fix the experiment IDs for the experiment and all runs under the given path.
    This will ensure that the experiment ID is a non-negative integer and that
    the ID matches the experiment's directory name. The directory will be moved
    if necessary.

    Args:
        path:
            The path to the experiment directory.
    '''
    path = pathlib.Path(path).resolve()

    # Experiment ID according to current directory path.
    try:
        dir_id = Metadata.non_negative_int(path.name)
    except ValueError:
        pass
    else:
        update_experiment_ids(path, dir_id)
        return

    # Invalid experiment ID in directory name.
    metadata = Metadata(path=path)
    try:
        exp_id = metadata.non_negative_int(metadata.experiment_id)
    except ValueError:
        pass
    else:
        # Check if the directory can be renamed to the current ID.
        new_path = path.parent / str(exp_id)
        if not new_path.exists():
            shutil.move(path, new_path)
            update_experiment_ids(new_path, exp_id)
            return

    # Find the first available directory path to set a new experiment ID.
    exp_id = 0
    while True:
        new_path = path.parent / str(exp_id)
        if new_path.exists():
            exp_id += 1
            continue
        shutil.move(path, new_path)
        update_experiment_ids(new_path, exp_id)
        return


def reorder_experiment_ids(path):
    '''
    Reorder all of the experiment IDs in a directory by their creation time.
    '''
    path = pathlib.Path(path).resolve()
    metadatas = (
        Metadata(path=mpath)
        for mpath in path.glob(f'*/{Metadata.FILENAME}')
    )
    metadatas = sorted(metadatas, key=lambda dat: (dat.creation_time, dat.name))
    prefix = 'tmp_'
    i = 0
    while list(path.glob(f'{prefix}*')):
        prefix = f'tmp_{i:d}_'
        i += 1
    for i, metadata in enumerate(metadatas):
        tmp_path = path / f'{prefix}{i:d}'
        LOGGER.info('moving %s to temporary path %s', metadata.path.parent, tmp_path)
        shutil.move(metadata.path.parent, tmp_path)
    for tmp_path in path.glob(f'{prefix}*'):
        new_path = tmp_path.parent / tmp_path.name[len(prefix):]
        LOGGER.info('moving temporary path %s to %s', tmp_path, new_path)
        shutil.move(tmp_path, new_path)
        fix_experiment_ids(new_path)


def collect_experiment_names(path):
    '''
    Collect all experiment names from the experiment directories under the given
    path.

    Args:
        path:
            The directory path containing the experiment directories.

    Returns:
        A dict mapping experiment names to lists of experiment directory paths.
    '''
    experiments = {}
    path = pathlib.Path(path).resolve()
    for metadata_path in path.glob(f'*/{Metadata.FILENAME}'):
        metadata = Metadata(path=metadata_path)
        experiments.setdefault(metadata.name, []).append(metadata)
    return experiments


def merge_experiments_by_name(path):
    '''
    Merge runs from experiments with the same name into a single experiment.

    Args:
        path:
            The directory path containing the experiment directories.
    '''
    experiments = collect_experiment_names(path)
    for name, metadatas in experiments.items():
        if len(metadatas) < 2:
            continue
        target_md = metadatas[0]
        for metadata in metadatas[1:]:
            exp_dir = metadata.path.parent
            if target_md.lifecycle_stage != metadata.lifecycle_stage:
                LOGGER.warning(
                    (
                        'Refusing to merge experiments named %s in different lifecycle stages:'
                        '%s [%s] and %s [%s]'
                    ),
                    name,
                    target_md.path, target_md.lifecycle_stage,
                    metadata.path, metadata.lifecycle_stage
                )
                continue
            target_md.creation_time = min(target_md.creation_time, metadata.creation_time)
            target_md.last_update_time = min(target_md.last_update_time, metadata.last_update_time)
            for run_dir in exp_dir.glob('*'):
                if not run_dir.is_dir():
                    continue
                new_run_dir = target_md.path.parent / run_dir.name
                if new_run_dir.exists():
                    LOGGER.warning(
                        'Run %s already exists in %s: %s will not be merged',
                        run_dir.name, new_run_dir.parent, run_dir
                    )
                    continue
                LOGGER.info('Moving run from %s to %s', run_dir, new_run_dir)
                shutil.move(run_dir, new_run_dir)
            shutil.rmtree(exp_dir)
        update_experiment_ids(target_md.path.parent, target_md.experiment_id)


def copy_experiments(src_path, dst_path):
    '''
    Copy experiments from one path to another.

    Args:
        src_path:
            The source directory from which to move the experiments.

        dst_path:
            The target directory to which to move the experiments.
    '''
    src_path = pathlib.Path(src_path).resolve()
    dst_path = pathlib.Path(dst_path).resolve()

    next_exp_id = 0
    for path in dst_path.glob('*'):
        try:
            exp_id = int(path.name)
        except ValueError:
            continue
        next_exp_id = max(next_exp_id, exp_id)
    next_exp_id += 1

    for path in src_path.glob('*'):
        if not path.is_dir() or path.name == '.trash':
            continue
        new_path = dst_path / path.name
        while new_path.exists():
            new_path = dst_path / str(next_exp_id)
            next_exp_id += 1
        LOGGER.info('Copying %s to %s', path, new_path)
        shutil.copytree(path, new_path)


def fix_artifact_uris(path, map_path=None):
    '''
    Update artifact URIs for all experiments and runs under the given path.

    Args:
        path:
            The path containing the experiments to fix.

        map_path:
            An optional path to a YAML file that maps old paths to new ones.
    '''
    path_map = {}
    if map_path is not None:
        with open(map_path, 'rb') as handle:
            data = yaml.safe_load(handle)
        for old, new in data.items():
            old = pathlib.Path(old).resolve()
            new = pathlib.Path(new).resolve()
            path_map[old] = new

    for data in Metadata().find_meta(path):
        uri = data.artifact_uri
        # Skip anything that isn't a local path.
        if not uri.is_local_file:
            continue

        current_path = uri.path
        new_path = None

        # Update from the path map.
        for old, new in path_map.items():
            if current_path.is_relative_to(old):
                subpath = current_path.relative_to(old)
                new_path = new / subpath
                break

        else:
            # Assume that an artifact directory in the same directory is the
            # intended target.
            artifact_dir = data.path.parent / 'artifacts'
            if artifact_dir.exists():
                new_path = artifact_dir

            # Assume that experiments point to their own directory be default.
            elif data.is_experiment and not uri.path.exists():
                new_path = data.path.parent

        if new_path is not None and new_path != current_path:
            LOGGER.info('Updating artifact URI to %s in %s', new_path, data.path)
            uri.path = new_path
            data.artifact_uri = uri
            data.save()
            continue

        # Warn about missing paths.
        if not current_path.exists():
            LOGGER.warning(
                'Artifacts URI does not exist: %s [%s]',
                uri,
                data.path
            )


def script_merge_experiments(args=None):
    '''
    Copy experiments into a common MLflow directory. Runs from experiments with
    the same name will be merged.
    '''
    configure_logging()

    parser = argparse.ArgumentParser(description=script_merge_experiments.__doc__)
    parser.add_argument(
        'target',
        help='The directory into which to merge the experiments. Default: %(default)s'
    )
    parser.add_argument(
        'dirs',
        nargs='+',
        help='The directories with the experiments to merge.'
    )
    pargs = parser.parse_args(args=args)

    target_path = pathlib.Path(pargs.target).resolve()
    target_path.mkdir(parents=True, exist_ok=True)

    for path in pargs.dirs:
        copy_experiments(path, target_path)
    merge_experiments_by_name(target_path)
    reorder_experiment_ids(target_path)
    fix_artifact_uris(target_path)


def script_fix_artifact_uris(args=None):
    '''
    Attempt to fix broken artifact URIs in experiments and runs.
    '''
    configure_logging()

    parser = argparse.ArgumentParser(description=script_fix_artifact_uris.__doc__)
    parser.add_argument(
        'path',
        help='A path to a directory with experiments and runs.'
    )
    parser.add_argument(
        '-m', '--map',
        help='A path to a YAML file that maps old paths to new paths.'
    )
    pargs = parser.parse_args(args=args)
    fix_artifact_uris(pargs.path, map_path=pargs.map)


def script_fix_experiment_ids(args=None):
    '''
    Attempt to fix experiment IDs so that the experiment's directory and all of
    its runs match its ID.
    '''
    configure_logging()

    parser = argparse.ArgumentParser(description=script_fix_experiment_ids.__doc__)
    parser.add_argument(
        'paths',
        nargs='+',
        help='Experiment directory paths.'
    )
    pargs = parser.parse_args(args=args)
    for path in pargs.paths:
        try:
            fix_experiment_ids(path)
        except FileNotFoundError as err:
            LOGGER.error('failed to fix IDs in %s: %s', path, err)


if __name__ == '__main__':
    script_merge_experiments()
