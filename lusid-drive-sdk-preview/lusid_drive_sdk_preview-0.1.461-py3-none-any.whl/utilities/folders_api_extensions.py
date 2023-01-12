import lusid_drive
import lusid_drive.models as models
import json
import logging

logger = logging.getLogger("drive-logger")
logger.setLevel("INFO")


def create_folder(api_factory, folder_path, folder_name):
    """
    This function creates a new folder on LUSID Drive.

    param api_factory ApiClientFactory: A LUSID Drive API Factory
    param folder_path str: The folder path on LUSID Drive
    param folder_path str: The new folder name on LUSID Drive

    returns: a CreateFolder responses

    """

    folder_api = api_factory.build(lusid_drive.api.FoldersApi)

    try:

        create_folder_request = folder_api.create_folder(
            create_folder=models.CreateFolder(folder_path, folder_name))

        return create_folder_request

    except lusid_drive.ApiException as e:

        if json.loads(e.body)["code"] == 664:

            return json.loads(e.body)["detail"]


def create_all_folders_in_path(api_factory, folder_path):
    """
    This function create a folder recursively.
    For example, we can pass a new path "/a/b/c/d", and the function will recursively create the four API calls
    to create:
        /a
        /a/b
        /a/b/c
        /a/b/c/d

    :param api_factory ApiClientFactory: A LUSID Drive API Factory
    :param folder_path str: The new folder path on LUSID Drive

    returns: A list of CreateFolder responses
    """

    folder_path = drive_path_formatter(folder_path)

    if len(folder_path) > 1024:

        raise ValueError("Path length must be less than 1024 characters")

    sub_dirs = [i for i in folder_path.split("/") if i != ""]

    path = "/"

    create_folder_requests = []

    for elem in sub_dirs:

        resp = create_folder(api_factory, path, elem)

        create_folder_requests.append(resp)

        path += elem + "/"

    return create_folder_requests


def path_to_search_api_parms(drive_path):
    """
    Function to conver path of format /abc/def/text1 to a format suitable for the SearchApi

    :param drive_path str: The path on LUSID Drive

    returns: a tuple of (folder_path, folder_name). For example, the string "/abc/def/text1"
    would return ("/abc/def", "text1")
    """

    drive_path = drive_path_formatter(drive_path)

    if drive_path.count("/") == 1:

        folder_path = "/"

        f_name = drive_path[1:]

    else:

        folder_path = drive_path[:drive_path.rfind("/")]

        f_name = drive_path[drive_path.rfind("/") + 1:]

    return (folder_path, f_name)


def delete_folder(api_factory, drive_path):
    """
    Function to delete folder on Drive

    :param api_factory ApiClientFactory: A LUSID Drive API Factory
    :param folder_path str: The folder path on LUSID Drive
    """

    drive_path = drive_path_formatter(drive_path)
    drive_ids = drive_object_to_id(api_factory, drive_path)

    folder_api = api_factory.build(lusid_drive.api.FoldersApi)

    if len(drive_ids) > 0:

        folder_ids = [i for i in drive_ids]

        folder_to_delete = []

        for i in folder_ids:

            delete_response = folder_api.delete_folder(id=i)

            folder_to_delete.append(delete_response)

        return folder_to_delete

    else:

        logger.info(f"The folder {drive_path} does not exist in LUSID Drive")



def drive_path_formatter(drive_path):

    if not drive_path.startswith("/"):

        drive_path = "/" + drive_path

    if drive_path.endswith("/"):

        drive_path = drive_path[:-1]

    return drive_path


def drive_object_to_id(api_factory, drive_path):

    """
    Function to return a list of IDs for a given LUSID Drive path.

    :param api_factory ApiClientFactory: A LUSID Drive API Factory
    :param drive_path str: The path to a file or folder on Drive

    returns a List of Drive IDs

    """

    search_api = api_factory.build(lusid_drive.api.SearchApi)

    drive_path = path_to_search_api_parms(drive_path)

    with_path_for_search = drive_path[0]
    name_for_search = drive_path[1]

    search_drive = search_api.search(search_body=models.SearchBody(
        with_path=with_path_for_search, name=name_for_search)).values

    drive_ids = [i.id for i in search_drive]

    return drive_ids






