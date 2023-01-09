import requests
import pandas as pd
import json


def post_index_name_acronyms_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts index name - index acronym relationship data to the index name component of the database.
    The function firstly checks that the input arguments are of the correct type, followed by modifying the dataset
    into a list of dictionaries. Each dictionary is passed to the endpoint, with a status code and error message
    printed if appropriate, and verbose=True.

    :param dataset: a Pandas DataFrame containing the data to upload within a given schema. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: failed_uploads: the information which failed to upload. (pd.DataFrame)
    """
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError("The 'dataset' argument must be a Pandas DataFrame.")
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean argument.")
    failed_uploads = []
    dict_list = dataset.to_dict('records')
    url = "https://www.samsonrockapis.com/namemapping/upload"
    header = {'Authorization': 'Bearer ' + access_token}
    for item in dict_list:
        response = requests.post(url, data=json.dumps(item), headers=header)
        if response.status_code in [200, 201, 202, 203, 204]:
            if verbose:
                print("Status Code: {}, data posted to date table.".format(response.status_code))
        elif response.status_code == 401:
            failed_uploads.append(item)
            if verbose:
                print("Status Code: {}, user not authenticated for endpoint.".format(response.status_code))
        else:
            failed_uploads.append(item)
            if verbose:
                print("Status Code: {}, {}.".format(response.status_code, response.text))
    return pd.DataFrame.from_records(failed_uploads)


def post_many_index_name_acronyms_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts index name - index acronym relationship data to the index name component of the database.
    The function firstly checks that the input arguments are of the correct type, followed by modifying the dataset
    into a json information packet. The json information is then passed to the endpoint, with a status code and error
    message printed if appropriate, and verbose=True.

    :param dataset: a Pandas DataFrame containing the data to upload within a given schema. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    dict_list = dataset.to_json(orient='records')
    url = "https://www.samsonrockapis.com/namemapping/bulk"
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.post(url, data=dict_list, headers=header)
    if response.status_code in [200, 201, 202, 203, 204]:
        if verbose:
            print("Status Code: {}, data posted to date table.".format(response.status_code))
    elif response.status_code in [401, 403]:
        if verbose:
            print("Status Code: {}, user not authenticated for endpoint.".format(response.status_code))
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))


def get_index_name_acronyms_from_database(access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all date information held in the database relating to index name - index
    acronym mappings. The function firstly checks that the arguments are of the correct type, followed by attempting
    to collect the requested information from the database. If the information is available, it is returned as a
    Pandas DataFrame, otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' arguments must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/namemapping"
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        if verbose:
            print("Status Code: {}".format(response.status_code))
        return pd.read_json(response.text)
    elif response.status_code == 404:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))
        return pd.DataFrame()
    elif response.status_code == 401:
        if verbose:
            print("Status Code: {}, user not properly authenticated for endpoint.".format(response.status_code))
        return pd.DataFrame()
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))
        return pd.DataFrame()
