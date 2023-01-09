import requests
import pandas as pd
import json
from typing import List


def post_effective_volumes_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function enables posting of effective volumes to the database. The function firstly checks that the
    input arguments are of the correct type, followed by modifying the dataset to a list of dictionaries. The
    function then attempts to post the dictionaries to the API, recording the status code for each post request
    as a printed value, if verbose=True.

    :param dataset: data in the correct schema to be posted to the Effective Volumes table. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: failed_uploads: the information which failed to upload. (pd.DataFrame)
    """
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError("The 'dataset' argument must be a Pandas DataFrame.")
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' argument must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    failed_uploads = []
    dict_list = dataset.to_dict('records')
    url = "https://www.samsonrockapis.com/effective_volumes"
    header = {'Authorization': 'Bearer ' + access_token}
    for item in dict_list:
        response = requests.post(url, data=json.dumps(item), headers=header)
        if response.status_code in [200, 201]:
            if verbose:
                print("Status Code: {}, Uploaded.".format(response.status_code))
        else:
            failed_uploads.append(item)
            if verbose:
                print("Status Code: {}, {}.".format(response.status_code, response.text))
    return pd.DataFrame.from_records(failed_uploads)


def post_many_effective_volumes_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts effective volumes data to the date table of the database. The function firstly checks that the
    input arguments are of the correct type, followed by modifying the dataset into a json information packet. The
    json information is then passed to the endpoint, with a status code and error message printed if appropriate,
    and verbose=True.

    :param dataset: a Pandas DataFrame containing the data to upload within a given schema. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    dict_list = dataset.to_json(orient='records')
    url = "https://www.samsonrockapis.com/effective_volumes/bulk"
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.post(url, data=dict_list, headers=header)
    if response.status_code in [200, 201, 202, 203, 204]:
        if verbose:
            print("Status Code: {}, data posted to effective volumes table.".format(response.status_code))
    elif response.status_code in [401, 403]:
        if verbose:
            print("Status Code: {}, user not authenticated for endpoint.".format(response.status_code))
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))


def collect_multiple_historical_effective_volumes(ticker_list: List[str], access_token: str, verbose: bool = True):
    """
    This function collects multiple historical effective volumes by ticker data from the database. The function firstly
    checks that the input arguments are of the correct type, followed by collecting the main information from the
    effective volume mapping data table. The information is returned with a status code and error message printed if
    appropriate, and verbose=True.

    :param ticker_list: the list of tickers to be considered by the database. (List[str])
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: the Pandas DataFrame containing the data requested. (pd.DataFrame)
    """
    if not isinstance(ticker_list, list):
        raise TypeError("The 'ticker_list' argument must be a list type.")
    if not all(isinstance(x, str) for x in ticker_list):
        raise TypeError("Each ticker in 'ticker_list' must be a string type.")
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/effective_volumes&multiple_tickers"
    header = {'Authorization': 'Bearer ' + access_token}
    payload = {"ticker_list": ticker_list}
    response = requests.get(url, headers=header, params=payload)
    if response.status_code == 200:
        if verbose:
            print("Status Code: {}".format(response.status_code))
        return pd.read_json(response.text)
    elif response.status_code == 404:
        if verbose:
            print("Status Code: {}, cannot find date data.".format(response.status_code))
        return pd.DataFrame()
    elif response.status_code in [401, 403]:
        if verbose:
            print("Status Code: {}, user not properly authenticated for endpoint.".format(response.status_code))
        return pd.DataFrame()
    else:
        if verbose:
            print("Status Code: {}, {}.".format(response.status_code, response.text))
        return pd.DataFrame()


def collect_effective_volumes_by_ticker(ticker: str, access_token: str, verbose: bool = True):
    """
    This function collects the historical effective volume of a specific ticker from the database. The function firstly
    checks that the input arguments are of the correct type, followed by collecting the main information from the
    effective volume mapping data table. The information is returned with a status code and error message printed if
    appropriate, and verbose=True.

    :param ticker: the ticker of interest, can be composite or local, Equity extension or not. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: the Pandas DataFrame containing the data requested. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [ticker]):
        raise TypeError("The 'ticker' argument must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")

    url = "https://www.samsonrockapis.com/effective_volumes&ticker={}".format(ticker)
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


def collect_effective_volumes_by_date(date: str, access_token: str, verbose: bool = True):
    """
    This function collects the historical effective volumes recorded on a specific date. The function firstly
    checks that the input arguments are of the correct type, followed by collecting the main information from the
    effective volume mapping data table. The information is returned with a status code and error message printed if
    appropriate, and verbose=True.

    :param date: the date of interest, in the format YYYY-MM-DD. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: the Pandas DataFrame containing the data requested. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [date]):
        raise TypeError("The 'date' argument must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")

    url = "https://www.samsonrockapis.com/effective_volumes&date={}".format(date)
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


def collect_all_effective_volumes(access_token: str, verbose: bool = True):
    """
    This function collects all of the historical effective volumes recorded. The function firstly checks that the input
    arguments are of the correct type, followed by collecting the main information from the effective volume mapping
    data table. The information is returned with a status code and error message printed if appropriate, and verbose=True.

    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: the Pandas DataFrame containing the data requested. (pd.DataFrame)
    """
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/effective_volumes&all"
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
