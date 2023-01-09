import requests
import pandas as pd
import json


def announcement_ticker_search(ticker: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to search historical announcements for a given ticker. The function
    firstly checks that the arguments are of the correct type, followed by attempting to collect historical
    announcement information from the database. If the information is available, it is returned as a Pandas DataFrame,
    otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param ticker: the local or composite ticker to search for. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [ticker, access_token]):
        raise TypeError("The 'ticker' and 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/search&announcement&ticker={}".format(ticker)
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


def forecast_flows_ticker_search(ticker: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to search historical forecast flows for a given ticker. The function
    firstly checks that the arguments are of the correct type, followed by attempting to collect historical
    announcement information from the database. If the information is available, it is returned as a Pandas DataFrame,
    otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param ticker: the local or composite ticker to search for. (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [ticker, access_token]):
        raise TypeError("The 'ticker' and 'access_token' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/search&flows&ticker={}".format(ticker)
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
