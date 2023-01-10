#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pathlib
import subprocess
from io import BytesIO
from zipfile import ZipFile

import requests
from poppy.core.logger import logger
from poppy.core.task import Task

__all__ = ['InstallIdbTask']

from roc.idb.constants import TIMEOUT, \
    IDB_SVN_URL, IDB_SVN_USER, IDB_SVN_PASSWORD, \
    MIB_ARCHIVE_URL_PATTERN, MIB_GITLAB_TOKEN


class IdbInstallError(Exception):
    pass


def download_palisade(
    raw_idb_version,
    install_dir,
    user=IDB_SVN_USER,
    password=IDB_SVN_PASSWORD,
    svn_url=IDB_SVN_URL,
    timeout=TIMEOUT,
    force=False,
):
    """
    Download a IDB PALISADE version.

    :param raw_idb_version: string with PALISADE IDB version
    :param install_dir: string with the IDB installation main directory path
    :param user: login user
    :param password: login password
    :param svn_url: SVN host URL
    :param timeout: process timeout in seconds
    :param force: Force installation even if IDB folder is already found locally
    :return: Path of the directory where the IDB has been downloaded
    """
    idb_version = (
        raw_idb_version
        if raw_idb_version.startswith('V')
        else 'V' + raw_idb_version
    )

    # build the url with the idb version
    url = f'{svn_url}/{idb_version}'

    # create the intermediate-level directories needed to contain the idb
    idb_dir_path = os.path.join(install_dir, idb_version)

    if os.path.exists(idb_dir_path) and not force:
        logger.warning(f'IDB [PALISADE-{idb_version}] already found in {idb_dir_path}: cancelling task! '
                       f'(Use --force keyword to force installation)')
        raise FileExistsError

    # Create IDB local folder
    os.makedirs(idb_dir_path, exist_ok=True)

    # build the command
    cmd = 'svn checkout --no-auth-cache'
    if user:
        cmd += f' --username {user} '
    if password:
        cmd += f' --password {password} '
    cmd += f'{url} {idb_dir_path}'

    p = subprocess.run(cmd,
                       stdout=subprocess.PIPE,
                       shell=True,
                       timeout=timeout,
                       check=True)
    return idb_dir_path


def download_mib(
    idb_version,
    install_dir,
    access_token=MIB_GITLAB_TOKEN,
    url=MIB_ARCHIVE_URL_PATTERN,
    force=False,
):
    """
    Download the MIB using the gitlab API

    :param idb_version: The tag, branch reference, or SHA of the MIB
    :param install_dir: The directory where the mib will be unzipped
    :param access_token: The private access token
    :param url: The gitlab API url
    :param force: Force installation even if local files are already found
    :return: Path where the IDB has been downloaded
    """

    # call the gitlab API using the user token
    headers = None
    if access_token:
        headers = {'PRIVATE-TOKEN': access_token}
    response = requests.get(
        url.format(version=idb_version),
        headers=headers,
    )

    # if the response was successful, no Exception will be raised
    response.raise_for_status()

    # create the intermediate-level directories needed to contain the idb
    idb_dir_path = os.path.join(install_dir, idb_version)

    if os.path.exists(idb_dir_path) and not force:
        logger.warning(f'IDB [MIB-{idb_version}] already found in {idb_dir_path}: cancelling task! '
                       f'(Use --force keyword to force installation)')
        raise FileExistsError

    # Create IDB local folder
    os.makedirs(idb_dir_path, exist_ok=True)

    # extract the zip
    try:
        with ZipFile(BytesIO(response.content)) as zip_file:
            for zip_info in zip_file.infolist():
                # skip the root dir of the zip
                zip_path = pathlib.Path(zip_info.filename)
                if len(zip_path.parts[1:]) == 0:
                    continue

                # the zip lib use trailing slash to determine if it's a dir or a file
                if zip_info.filename[-1] == '/':
                    # it's a directory, add a trailing slash to the pathlib output
                    zip_info.filename = (
                        pathlib.Path(*zip_path.parts[1:]).as_posix() + '/'
                    )
                else:
                    zip_info.filename = pathlib.Path(
                        *zip_path.parts[1:]
                    ).as_posix()

                # extract the file
                zip_file.extract(zip_info, idb_dir_path)
    except:
        logger.exception(f'Installing IDB [MIB-{idb_version}] has failed!')
        raise IdbInstallError

    return idb_dir_path


@Task.as_task(plugin_name='roc.idb', name='idb_install')
def InstallIdbTask(self):
    if self.pipeline.args.idb_source in ['SRDB', 'PALISADE']:
        logger.debug(
            f'Downloading PALISADE IDB version: "{self.pipeline.args.idb_version}"'
            f' in "{self.pipeline.args.install_dir}"'
        )
        try:
            download_palisade(
                self.pipeline.args.idb_version, self.pipeline.args.install_dir,
                user=self.pipeline.args.svn_user[0], password=self.pipeline.args.svn_password[0]
            )
        except subprocess.CalledProcessError:
            logger.exception(f'Downloading PALISADE IDB {self.pipeline.args.idb_version} has failed!')
            self.pipeline.exit()
        except subprocess.TimeoutExpired:
            logger.exception(f'Time to download PALISADE IDB {self.pipeline.args.idb_version} has expired!')
            self.pipeline.exit()
        except FileExistsError:
            pass
        except IdbInstallError:
            pass

    elif self.pipeline.args.idb_source == 'MIB':
        logger.debug(
            f'Downloading MIB IDB version: "{self.pipeline.args.idb_version}"'
            f' in "{self.pipeline.args.install_dir}"'
        )
        try:
            download_mib(
                self.pipeline.args.idb_version, self.pipeline.args.install_dir,
                access_token=self.pipeline.args.access_token[0]
            )
        except FileExistsError:
            pass
        except IdbInstallError:
            pass
    else:
        raise IdbInstallError(
            f"Wrong IDB source '{self.pipeline.args.idb_source}'"
        )
