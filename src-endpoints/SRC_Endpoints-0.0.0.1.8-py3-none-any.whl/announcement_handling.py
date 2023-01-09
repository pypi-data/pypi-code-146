import requests
import pandas as pd
import json


def post_announcements_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts announcement data to the announcement table of the database. The function firstly
    checks that the input arguments are of the correct type, followed by modifying the dataset into a list
    of dictionaries. Each dictionary is passed to the endpoint, with a status code and error message printed
    if appropriate, and verbose=True.

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
    url = "https://www.samsonrockapis.com/announcement"
    header = {'Authorization': 'Bearer ' + access_token}
    for item in dict_list:
        response = requests.post(url, data=json.dumps(item), headers=header)
        if response.status_code in [200, 201, 202, 203, 204]:
            if verbose:
                print("Status Code: {}, data posted to announcements.".format(response.status_code))
        elif response.status_code == 401:
            failed_uploads.append(item)
            if verbose:
                print("Status Code: {}, user not authenticated for endpoint.".format(response.status_code))
        else:
            if verbose:
                print("Status Code: {}, {}.".format(response.status_code, response.text))
            failed_uploads.append(item)
    return pd.DataFrame.from_records(failed_uploads)


def post_many_announcements_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts announcement data to the date table of the database. The function firstly checks that the
    input arguments are of the correct type, followed by modifying the dataset into a json information packet. The
    json information is then passed to the endpoint, with a status code and error message printed if appropriate,
    and verbose=True.

    :param dataset: a Pandas DataFrame containing the data to upload within a given schema. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    dict_list = dataset.to_json(orient='records')
    url = "https://www.samsonrockapis.com/announcement/bulk"
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


def get_all_index_announcements_from_db(index: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all announcement information held in the database relating to a specific
    index. The function firstly checks that the arguments are of the correct type, followed by attempting to collect
    the requested information from the database. If the information is available, it is returned as a Pandas DataFrame,
    otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, access_token]):
        raise TypeError("The 'index' and 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/announcement&index={}".format(index)
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


def get_multiple_index_announcement_data_from_db(index: str, review_type: str, access_token: str, verbose: bool = True):
    """
    This function collects announcement data for a specific index and review type, but is agnostic to the review date.
    The function firstly checks that the arguments are of the correct type, followed by calling the API endpoint,
    passing the index and review_type arguments to the API. If the information is available, it is returned as a Pandas
    DataFrame, otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param review_type: the type of review. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, review_type, access_token]):
        raise TypeError("The 'index', 'review_type' and 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/announcement&index={}&review_name={}".format(index, review_type)
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


def get_index_announcement_data_from_db(index: str, review_year: int, review_month: int, review_type: str,
                                        access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all announcement information held in the database relating to a specific
    index review. The function firstly checks that the arguments are of the correct type, followed by attempting to
    collect the requested information from the database. If the information is available, it is returned as a Pandas
    DataFrame, otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param review_year: the year at which the review event took place. (int)
    :param review_month: the month at which the review took place. (int)
    :param review_type: the type of review. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, review_type, access_token]):
        raise TypeError("The 'index', 'review_type' and 'access_token' arguments must be string types.")
    if not all(isinstance(v, int) for v in [review_year, review_month]):
        raise TypeError("The 'review_year' and 'review_month' arguments must be integer types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/announcement&index={}&review_year={}&" \
          "review_month={}&review_name={}".format(index, review_year, review_month, review_type)
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
