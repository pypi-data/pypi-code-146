import logging
from shutil import rmtree
from vxbase.vtypes import is_iterable
from os import path, remove


_logger = logging.getLogger(__name__)


def clean_files(files):
    """Remove unnecessary and temporary files.

    :param files: A list or a str of absolute or relative paths thar will be erased
    """
    if not files:
        return
    items = files if is_iterable(files) else [files]
    for item in items:
        fname = item[0] if is_iterable(item) else item
        if fname != "/":
            _logger.info('Removing %s', fname)
            if path.isfile(fname):
                remove(fname)
            elif path.isdir(fname):
                rmtree(fname)
        else:
            _logger.error(
                "Invalid target path: '/'. Are you trying to delete your root path?")
