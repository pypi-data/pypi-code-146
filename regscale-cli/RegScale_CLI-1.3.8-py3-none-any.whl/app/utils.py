#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
import csv
import glob
import ntpath
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import rich.progress
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from app.application import Application
from app.login import is_licensed
from app.logz import create_logger
from exceptions.license_exception import LicenseException

logger = create_logger()


def check_license():
    """Check RegScale License

    Raises:
        LicenseException: Custom Exception

    Returns:
        Application: application instance
    """
    app = Application()
    if not is_licensed(app):
        raise LicenseException(
            "This feature is limited to RegScale Enterprise, please check RegScale license."
        )
    return app


def validate_mac_address(mac_address: str) -> bool:
    """Simple validation of a mac address input

    Args:
        mac_address (str): mac address

    """
    if re.match(
        "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()
    ):
        return True
    return False


def str_to_date(date_str: str) -> datetime:
    """
    function to convert string into a date object
    """
    # replace the T with a space and create list of result
    date_str = date_str.replace("T", " ").split(" ")

    # convert the first part of the date list into a date
    date = datetime.strptime(date_str[0], "%Y-%m-%d")

    # return date result
    return date


def uncamel_case(camel_str: str) -> str:
    """
    function to convert camelCase strings to Title Case
    """
    # check to see if a string with data was passed
    if camel_str != "":
        # split at any uppercase letters
        result = re.sub("([A-Z])", r" \1", camel_str)

        # use title to Title Case the string
        result = result.title()
        return result
    return ""


def get_css(file_path: str) -> str:
    """
    function to load the css properties from the given file_path
    """
    # create variable to store the string and return
    css = ""

    # check if the filepath exists before trying to open it
    if os.path.exists(file_path):
        # file exists so open the file
        with open(file_path, "r", encoding="utf-8") as file:
            # store the contents of the file in the css str variable
            css = file.read()
    # return the css variable
    return css


def send_email(api, domain: str, payload: dict) -> bool:
    """
    function to use the RegScale email API
    """
    # use the api to post the dict payload passed
    response = api.post(url=f"{domain}/api/email", json=payload)
    # see if api call was successful and return boolean
    return response.status_code == 200


def epoch_to_datetime(epoch: str, format="%Y-%m-%d %H:%M:%S") -> str:
    """Return datetime from unix epoch.

    Args:
        epoch (str): unix epoch
        format (str): datetime string format
    Returns:
        datetime string

    """
    return datetime.fromtimestamp(int(epoch)).strftime(format)


def get_current_datetime(format="%Y-%m-%d %H:%M:%S") -> str:
    """Return current datetime.

    Args:
        format : datetime string format
    Returns:
        datetime string

    """
    return datetime.now().strftime(format)


def check_config_for_issues(config, issue: str, key: str):
    """Function to check config keys and return the default if no value"""
    return (
        config["issues"][issue][key]
        if "issues" in config.keys() and config["issues"][issue][key] is not None
        else None
    )


def cci_control_mapping(file_path: Path):
    """Simple function to read csv artifact to help with STIG mapping"""
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        return list(reader)


def create_progess_object() -> rich.progress.Progress:
    """
    function to create and return a progress object
    """
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    )
    return job_progress


def get_file_type(file_name: str) -> str:
    """
    function to get the file type of the provided file_path and returns it as a string
    """
    file_type = Path(file_name).suffix
    return file_type.lower()


def get_file_name(file_path: str) -> str:
    """
    function to parse the provided file path and returns the file's name as a string
    """
    # split the provided file_path with ntpath
    directory, file_name = ntpath.split(file_path)
    # return the file_path or directory
    return file_name or ntpath.basename(directory)


def create_regscale_file(
    file_path: str, parent_id: int, parent_module: str, api
) -> dict:
    """
    function to create a file within RegScale via API
    """
    # get the file type of the provided file_path
    file_type = get_file_type(file_path)

    # get the file name from the provided file_path
    file_name = get_file_name(file_path)

    # set up file headers
    file_headers = {"Authorization": api.config["token"], "Accept": "application/json"}

    # see file_type is an acceptable format and set the file_type_header accordingly
    if file_type == ".csv":
        file_type_header = "text/csv"
    elif file_type in [".xlsx", ".xls"]:
        file_type_header = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        # let user know it was an unaccepted file_type
        logger.error("Unaccepted file type to upload!")
        sys.exit(1)

    # set the files up for the RegScale API Call
    files = [("file", (file_name, open(file_path, "rb").read(), file_type_header))]

    # configure data payload
    data = {"id": parent_id, "module": parent_module}

    # make the api call
    file_response = api.post(
        url=f"{api.config['domain']}/api/files/file",
        headers=file_headers,
        data=data,
        files=files,
    )
    # set the regscale_file to the json response if it was a successfull API call
    regscale_file = file_response.json() if file_response.status_code == 200 else None

    # return the regscale_file
    return regscale_file


def upload_file_to_regscale(
    file_name: str, parent_id: int, parent_module: str, api
) -> bool:
    """
    function that will create and upload a file to RegScale to the provided parent_module and parent_id
    """

    # first create the file in RegScale
    regscale_file = create_regscale_file(
        file_path=file_name, parent_id=parent_id, parent_module=parent_module, api=api
    )

    # verify the file creation was successful
    if regscale_file:
        # set up headers for file upload
        file_headers = {
            "Authorization": api.config["token"],
            "accept": "application/json, text/plain, */*",
        }

        # set up file_data payload with the regscale_file dictionary
        file_data = {
            "uploadedBy": "",
            "parentId": parent_id,
            "parentModule": parent_module,
            "uploadedById": api.config["userId"],
            "id": regscale_file["id"],
            "fullPath": regscale_file["fullPath"],
            "trustedDisplayName": regscale_file["trustedDisplayName"],
            "trustedStorageName": regscale_file["trustedStorageName"],
            "uploadDate": regscale_file["uploadDate"],
            "fileHash": regscale_file["fileHash"],
            "size": os.path.getsize(file_name),
        }

        # post the regscale_file data via RegScale API
        file_res = api.post(
            url=f"{api.config['domain']}/api/files",
            headers=file_headers,
            json=file_data,
        )
    else:
        logger.error("Unable to create %s as a RegScale file.", file_name)
        return False
    # return whether the api call was successful or not
    # right now there is a bug in the main application where it returns a 204 error code
    # which means there is no content on the file, but the file does upload successfully and has data
    return file_res.status_code in [200, 204]


def create_regscale_assessment(url: str, new_assessment: dict, api) -> int:
    """
    function to create a new assessment in RegScale and returns the new assessment's ID
    """
    assessment_res = api.post(url=url, json=new_assessment)
    asset_id = (
        assessment_res.json()["id"] if assessment_res.status_code == 200 else None
    )
    return asset_id


def get_recent_files(file_path: Path, file_count: int, file_type: str = None) -> list:
    """
    function to go to the provided file_path and get the x number of recent items
    optional argument of file_type to filter the directory
    """
    # verify the provided file_path exists
    if os.path.exists(file_path):
        # get the list of files from the provided path, get the desired
        # file_type if provided
        file_list = (
            glob.glob(f"{file_path}/*{file_type}")
            if file_type
            else glob.glob(f"{file_path}/*")
        )

        # sort the file_list by modified date in descending order
        file_list.sort(key=os.path.getmtime, reverse=True)

        # check if file_list has more items than the provided number, remove the rest
        if len(file_list) > file_count:
            file_list = file_list[:file_count]
    else:
        logger.error("The provided file path doesn't exist! Provided: %s", file_path)
        sys.exit(1)
    # return the list of files
    return file_list


def check_file_path(file_path: Path):
    # see if the provided directory exists, if not create it
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        # notify user directory has been created
        logger.info("%s didn't exist, but has been created.", file_path)
