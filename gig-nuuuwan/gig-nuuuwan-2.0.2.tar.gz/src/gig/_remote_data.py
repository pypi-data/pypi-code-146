import os

from utils import WWW


def _get_remote_file_path(file):
    return os.path.join(
        'https://raw.githubusercontent.com',
        'nuuuwan/gig-data/master',
        file,
    )


def _get_remote_tsv_data(file):
    return WWW(_get_remote_file_path(file)).readTSV()


def _get_remote_json_data(file):
    return WWW(_get_remote_file_path(file)).readTSV()
