import requests
import pandas as pd
import json


def post_flows_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function enables the posting of data to the database. The function firstly checks that the
    input arguments are of the correct type, followed by modifying the dataset to a list or dictionaries.
    The function then attempts to post the dictionaries to the API, recording the status code for each post
    request as a printed value, if verbose = True.

    :param dataset: data in the correct schema to be posted to the Forecast Flows DB. (pd.DataFrame)
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
    url = "https://www.samsonrockapis.com/forecast_flows"
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


def post_many_flows_to_database(dataset: pd.DataFrame, access_token: str, verbose: bool = True):
    """
    This function posts flows data to the date table of the database. The function firstly checks that the
    input arguments are of the correct type, followed by modifying the dataset into a json information packet. The
    json information is then passed to the endpoint, with a status code and error message printed if appropriate,
    and verbose=True.

    :param dataset: a Pandas DataFrame containing the data to upload within a given schema. (pd.DataFrame)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    dict_list = dataset.to_json(orient='records')
    url = "https://www.samsonrockapis.com/forecast_flows/bulk"
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


def get_all_index_data_from_db(index: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all information held in the database relating to a specific index.
    The function firstly checks that the arguments are of the correct type, followed by attempting to collect the
    requested information from the database. If the information is available, it is returned as a Pandas DataFrame,
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

    url = "https://www.samsonrockapis.com/forecast_flows&index={}".format(index)
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


def get_index_review_data_from_db(index: str, review_year: int, review_month: int, review_type: str,
                                  access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all information held in the database relating to a specific index review.
    The function firstly checks that the arguments are of the correct type, followed by attempting to collect the
    requested information from the database. If the information is available, it is returned as a Pandas DataFrame,
    otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

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

    url = "https://www.samsonrockapis.com/forecast_flows&index={}&" \
          "review_year={}&review_month={}&review_name={}".format(index,
                                                                 review_year,
                                                                 review_month,
                                                                 review_type)
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


def get_index_review_data_single_day(index: str, review_year: int, review_month: int, review_type: str, date: str,
                                     access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all information held in the database relating to a specific index review
    on a given day. The function firstly checks that the arguments are of the correct type, followed by attempting to
    collect the requested information from the database. If the information is available, it is returned as a Pandas
    DataFrame, otherwise, empty data shall be returned, with an appropriate status code printed if verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param review_year: the year at which the review event took place. (int)
    :param review_month: the month at which the review took place. (int)
    :param review_type: the type of review. (str)
    :param date: the date for which the forecast flows should be retrieved, format "YYYY-MM-DD". (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, review_type, date, access_token]):
        raise TypeError("The 'index', 'review_type', 'date' and 'access_token' arguments must be string types.")
    if not all(isinstance(v, int) for v in [review_year, review_month]):
        raise TypeError("The 'review_year' and 'review_month' arguments must be integer types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    date = date.replace("/", "-")
    url = "https://www.samsonrockapis.com/forecast_flows&index={}" \
          "&review_year={}&review_month={}&review_name={}&date={}".format(index, review_year, review_month,
                                                                          review_type, date)
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


def get_index_review_data_daterange(index: str, review_year: int, review_month: int, review_type: str,
                                    start_date: str, end_date: str, access_token: str, verbose: bool = True):
    """
    This function enables the user to collect all information held in the database relating to a specific index review
    for a given date range. The function firstly checks that the arguments are of the correct type, followed by
    attempting to collect the requested information from the database. If the information is available, it is returned
    as a Pandas DataFrame, otherwise, empty data shall be returned, with an appropriate status code printed if
    verbose=True.

    :param index: the index for which the user would like to return data. (str)
    :param review_year: the year at which the review event took place. (int)
    :param review_month: the month at which the review took place. (int)
    :param review_type: the type of review. (str)
    :param start_date: the date for which the forecast flows should be retrieved, format "YYYY-MM-DD". (str)
    :param end_date: the date for which the forecast flows should be retrieved, format "YYYY-MM-DD". (str)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: dataset: a Pandas DataFrame containing all data relating to the index argument. (pd.DataFrame)
    """
    if not all(isinstance(v, str) for v in [index, review_type, start_date, end_date, access_token]):
        raise TypeError("The 'index', 'review_type', 'start_date', 'end_date' and 'access_token' "
                        "arguments must be string types.")
    if not all(isinstance(v, int) for v in [review_year, review_month]):
        raise TypeError("The 'review_year' and 'review_month' arguments must be integer types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    start_date = start_date.replace("/", "-")
    end_date = end_date.replace("/", "-")
    url = "https://www.samsonrockapis.com/forecast_flows&index={}&review_year={}" \
          "&review_month={}&review_name={}&start_date={}&end_date={}".format(index, review_year, review_month,
                                                                             review_type, start_date, end_date)
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
