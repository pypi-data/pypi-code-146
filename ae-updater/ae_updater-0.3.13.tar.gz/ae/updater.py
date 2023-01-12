"""
application environment updater
===============================

this module is providing check functions running on app startup for easy deployment of Python application updates.

updater check functions
-----------------------

update any files on the destination machine with the help of the check functions :func:`check_moves` and
:func:`check_overwrites`.

the check function :func:`check_local_updates` checks if your deployment package contains a Python update script that
will be executed (and only one time after an app update) on the next startup of your application.

for a temporary work-around or bug-fix you can deploy your application update with a bootstrap Python script which will
be executed on every startup of your application. the detection and execution of such bootstrap script is done by the
function :func:`check_local_bootstrap`-

the function :func:`check_all` combines all the above checks.

the following skeleton of a main app module demonstrates a typical usage of :func:`check_all`::

    from python_and_3rd_party_libs import ...
    from ae.updater import check_all
    from project_local_libs import ...

    check_all()

    app = WhatEverApp(app_name=...)
    ...
    app.run_app()

replace the :func:`check_all` call with the needed check function(s) if your app only needs certain checks.

.. note::
    make sure that the check function(s) get called before you initialize any app instances if you want to update ony
    :ref:`config-variables`, like :ref:`application status` or user preferences.

..hint: more info you find in the doc-strings of each of the check functions.
"""
import os
from typing import List

from ae.base import PACKAGE_INCLUDE_FILES_PREFIX, PY_EXT, module_attr               # type: ignore
from ae.paths import copy_files, move_files, path_folders, Collector                # type: ignore


__version__ = '0.3.13'


COPIES_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_copies'
MOVES_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_moves'
OVERWRITES_SRC_FOLDER_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater_overwrites'

UPDATER_MODULE_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'updater'
BOOTSTRAP_MODULE_NAME = PACKAGE_INCLUDE_FILES_PREFIX + 'bootstrap'


def check_copies(src_folder: str = COPIES_SRC_FOLDER_NAME, dst_folder: str = "") -> List[str]:
    """ check on new or missing files to be copied from src_folder to the dst_folder.

    :param src_folder:      path to source folder/directory where the files get copied from. If not specified then
                            :data:`COPIES_SRC_FOLDER_NAME` will be used.
    :param dst_folder:      path to destination folder/directory where the files get copied to. If not specified
                            or if you pass an empty string then the user data/preferences path ({usr}) will be used.
    :return:                list of moved files, with their destination path.
    """
    if not dst_folder:
        dst_folder = "{usr}"
    return copy_files(src_folder, dst_folder)


def check_moves(src_folder: str = MOVES_SRC_FOLDER_NAME, dst_folder: str = "") -> List[str]:
    """ check on missing files to be moved from src_folder to the dst_folder.

    :param src_folder:      path to source folder/directory where the files get moved from. If not specified then
                            :data:`MOVES_SRC_FOLDER_NAME` will be used. Please note that the source folder itself will
                            neither be moved nor removed (but will be empty after the operation finished).
    :param dst_folder:      path to destination folder/directory where the files get moved to. If not specified
                            or if you pass an empty string then the user data/preferences path ({usr}) will be used.
    :return:                list of moved files, with their destination path.
    """
    if not dst_folder:
        dst_folder = "{usr}"
    return move_files(src_folder, dst_folder)


def check_overwrites(src_folder: str = OVERWRITES_SRC_FOLDER_NAME, dst_folder: str = "") -> List[str]:
    """ check on files to be moved from the source directory and overwritten within the destination directory.

    :param src_folder:      path to source folder/directory where the files get moved from. If not specified then
                            :data:`MOVES_SRC_FOLDER_NAME` will be used. Please note that the source folder itself will
                            neither be moved nor removed (but will be empty after the operation finished).
    :param dst_folder:      path to destination folder/directory where the files get moved to. If not specified
                            or if you pass an empty string then the user data/preferences path ({usr}) will be used.
    :return:                list of moved and possibly overwritten files, with their destination path.
    """
    if not dst_folder:
        dst_folder = "{usr}"
    return move_files(src_folder, dst_folder, overwrite=True)


def check_local_updates() -> bool:
    """ check if ae_updater script exists in the current working directory to be executed and deleted.

    .. note:
        ff the module :data:`UPDATER_MODULE_NAME` exists, is declaring a :func:`run_updater` function and that
        function is returning a non-empty return value (evaluating as boolean True) then the module will be
        automatically deleted after the execution of the function.

    :return:                return value (True) of executed run_updater method (if module&function exists), else False.
    """
    func = module_attr(UPDATER_MODULE_NAME, attr_name='run_updater')
    ret = func() if func else False
    if ret:
        os.remove(UPDATER_MODULE_NAME + PY_EXT)
    return ret


def check_local_bootstraps() -> bool:
    """ check if ae_bootstrap script exists in the current working directory to be executed on app startup.

    :return:                return value (True) of executed run_updater function (if module&function exists) else False.
    """
    func = module_attr(BOOTSTRAP_MODULE_NAME, attr_name='run_updater')
    return func() if func else False


def check_all(copy_src_folder: str = "", move_src_folder: str = "", over_src_folder: str = "",
              dst_folder: str = "") -> List[str]:
    """ check all outstanding scripts to be executed and files to be moved/overwritten.

    :param copy_src_folder: path to source folder/directory where the files get copied from. if not specified
                            or if you pass an empty string then :data:`COPIES_SRC_FOLDER_NAME` will be used.
    :param move_src_folder: path to source folder/directory where the files get moved from. if not specified
                            or if you pass an empty string then :data:`MOVES_SRC_FOLDER_NAME` will be used.
    :param over_src_folder: path to source folder/directory where the files get moved from and overwritten to.
                            if not specified then :data:`OVERWRITES_SRC_FOLDER_NAME` will be used.
    :param dst_folder:      path to destination folder/directory where the files get moved to. if not specified
                            or if you pass an empty string then the user data/preferences path ({usr}) will be used.
    :return:                list of processed (copied, moved or overwritten) files, with their destination path.
    """
    if not copy_src_folder:
        copy_src_folder = COPIES_SRC_FOLDER_NAME
    if not move_src_folder:
        move_src_folder = MOVES_SRC_FOLDER_NAME
    if not over_src_folder:
        over_src_folder = OVERWRITES_SRC_FOLDER_NAME

    check_local_updates()
    check_local_bootstraps()

    processed = []

    coll = Collector(path_scanner=path_folders)
    coll.collect('{cwd}', append=copy_src_folder, only_first_of='prefix')
    if coll.paths:
        processed += check_copies(src_folder=coll.paths[0], dst_folder=dst_folder)

    coll = Collector(path_scanner=path_folders)
    coll.collect('{cwd}', append=move_src_folder, only_first_of='prefix')
    if coll.paths:
        processed += check_moves(src_folder=coll.paths[0], dst_folder=dst_folder)

    coll = Collector(path_scanner=path_folders)
    coll.collect('{cwd}', append=over_src_folder, only_first_of='prefix')
    if coll.paths:
        processed += check_overwrites(src_folder=coll.paths[0], dst_folder=dst_folder)

    return processed
