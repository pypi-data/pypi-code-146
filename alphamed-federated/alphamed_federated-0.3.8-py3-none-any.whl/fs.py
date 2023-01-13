"""File System Utils."""
import os

from .mock import is_mock_mode

__all__ = [
    'get_root_dir',
    'get_runtime_dir',
    'get_share_dir',
    'get_result_dir',
    'get_model_dir',
    'get_dataset_dir',
]


def get_root_dir(task_id: str = None):
    """Return the root FS directory which is writable.

    Task ID is only optional in mock mode.
    """
    assert not task_id or isinstance(task_id, str), f'Invalid task_id: `{task_id}`.'
    if is_mock_mode():
        task_id = task_id or ''
    else:
        assert task_id, 'Must specify the task_id.'

    _root = os.path.curdir if is_mock_mode() else '/data/alphamed-federated'
    return os.path.join(_root, task_id)


def get_runtime_dir(task_id: str = None):
    """Return default runtime data directory which is writable.

    Task ID is only optional in mock mode.
    """
    return os.path.join(get_root_dir(task_id), 'runtime')


def get_share_dir(task_id: str = None):
    """Return default share data directory which is writable.

    Task ID is only optional in mock mode.
    """
    return os.path.join(get_root_dir(task_id), 'share')


def get_result_dir(task_id: str = None):
    """Return default result data directory which is writable.

    Task ID is only optional in mock mode.
    """
    return os.path.join(get_root_dir(task_id), 'result')


def get_model_dir(task_id: str = None):
    """Return default model data directory which is writable.

    Task ID is only optional in mock mode.
    """
    return os.path.join(get_root_dir(task_id), 'model')


def get_dataset_dir(task_id: str = None):
    """Return default dataset data directory which is writable.

    Task ID is only optional in mock mode.
    """
    return os.path.join(get_root_dir(task_id), 'dataset')
