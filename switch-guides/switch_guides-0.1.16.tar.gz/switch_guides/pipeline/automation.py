# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Module defining the Automation extensions which contains deployment.
---------------------
Automation Extensions
---------------------
This class contains the helper methods extensions used to register, deploy, and test the created tasks. Additional helper functions
 for retrieving details of existing tasks on the Switch Automation Platform are also included in this module.
"""
import logging
import sys
import pandas
import requests
import uuid
from io import StringIO
from switch_api._utils._utils import _column_name_cap
from ..utils.utils import ApiInputs
from switch_api._utils._constants import (
    EXPECTED_DELIVERY, QUEUE_NAME, SCHEDULE_TIMEZONE)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  switch_api.%(module)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)


def deploy_as_upload_data_feed(driver_id: str,
                               api_inputs: ApiInputs, data_feed_id: uuid.UUID, expected_delivery: EXPECTED_DELIVERY,
                               queue_name: QUEUE_NAME = 'task', data_feed_name: str = None):
    """Deploy the custom driver as a REST API end point Datafeed.
    To upload a file to the deployed data feed, use the UploadUrl from the response dataframe (with request type
    POST) with the following two headers:
    - 'Ocp-Apim-Subscription-Key' - set to the value of ``api_inputs.subscription_key``
    - 'Authorization' - set to the value 'Bearer ``api_inputs.bearer_token``'
    For example, to upload a file using the ``requests`` package:
    >>> import requests
    >>> url = df.loc[0,'UploadUrl']
    >>> payload={}
    >>> file_path = 'C:/xxyyzz.txt'
    >>> files={'file': open(file_path, 'rb')}
    >>> headers = {'Ocp-Apim-Subscription-Key': api_inputs.subscription_key, 'Authorization': f'Bearer {api_inputs.bearer_token}'}
    >>> response = requests.request("POST", url, headers=headers, data=payload, files=files)
    >>> print(response.text)
    Parameters
    ----------
    taskId : str
        Id of the custom driver class created from the Abstract Base Class 'Task'
    api_inputs : ApiInputs
        Object returned by the initialize() function.
    data_feed_id : uuid.UUID
        The DataFeedId to update if existing, else will create a new record with the given value.
    expected_delivery : EXPECTED_DELIVERY
        The expected delivery frequency of the data.
    queue_name : QUEUE_NAME, optional
        The queue name (Default value = 'task').
    data_feed_name : str, Optional
        The name of the data feed (to be displayed in Task Insights UI).
    Returns
    -------
    df : pandas.DataFrame
        Dataframe containing the details of the deployed https endpoint data feed.
    """
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()
    if data_feed_name == '' and data_feed_name == None:
        logger.error('Data Feed Name must be provided.')
        return pandas.DataFrame()
    headers = api_inputs.api_headers.default
    if not set([expected_delivery]).issubset(set(EXPECTED_DELIVERY.__args__)):
        logger.error('expected_delivery parameter must be set to one of the allowed values defined by the '
                     'EXPECTED_DELIVERY literal: %s', EXPECTED_DELIVERY.__args__)
        return pandas.DataFrame()
    if not set([queue_name]).issubset(set(QUEUE_NAME.__args__)):
        logger.error('queue_name parameter must be set to one of the allowed values defined by the '
                     'QUEUE_NAME literal: %s', QUEUE_NAME.__args__)
        return pandas.DataFrame()
    logger.info(
        f'Deploy Driver with Id {driver_id} as a data feed for ApiProjectID: {api_inputs.api_project_id}')
    payload = {
        "dataFeedId": str(data_feed_id),
        "driverId": str(driver_id),
        "name": data_feed_name,
        "feedType": 'Readings',  # Default
        "expectedDelivery": expected_delivery,
        "sourceType": "Upload",
        "queueName": queue_name,
        "upload": {
            "placeholder": ""
        },
    }
    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/tasks/deployment"
    logger.info("Sending request: POST %s", url)
    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error(
            'No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()
    df = pandas.read_json(StringIO(response.text),
                          typ='Series').to_frame().T
    df.columns = _column_name_cap(df.columns)
    return response_status, df


def deploy_on_timer(driver_id: str,
                    api_inputs: ApiInputs, data_feed_id: uuid.UUID, expected_delivery: EXPECTED_DELIVERY,
                    cron_schedule: str, queue_name: QUEUE_NAME = "task", settings: dict = None,
                    schedule_timezone: SCHEDULE_TIMEZONE = 'Local', timezone_offset_minutes: int = None,
                    data_feed_name: str = None):
    """Deploy driver to run on timer.
    Parameters
    ----------
    task : Task
        The custom driver class created from the Abstract Base Class `Task`.
    api_inputs : ApiInputs
        Object returned by initialize.initialize() function
    data_feed_id : uuid.UUID
        The DataFeedId to update if existing, else will create a new record with the given value.
    expected_delivery : EXPECTED_DELIVERY
        The expected delivery frequency.
    cron_schedule : str
        The CRONOS cron object containing the required schedule for the driver to be run. For details on the
        required format, see: https://crontab.cronhub.io/
    queue_name : QUEUE_NAME, optional
        The queue name (Default value = 'task').
    settings : dict, Optional
        List of settings used to deploy the driver. For example, may contain the user_name and password required to
        authenticate calls to a third-party API (Default value = None).
    schedule_timezone : SCHEDULE_TIMEZONE, optional
        Whether the ``cron_schedule`` should be applied based on Local or Utc timezone. If set to `Local`, this is
        taken as the timezone of the western-most site in the given portfolio (Default value = 'Local').
    timezone_offset_minutes: int, Optional
        Timezone offset in minutes (from UTC) to be used when applying the ``cron_schedule`` (Default value = None).
    data_feed_name : str, Optional
        The name of the data feed (to be displayed in Task Insights UI). If not provided, will default to the
        task name.
    Returns
    -------
    pandas.Dataframe
        A dataframe containing the details of the deployed data feed.
    """
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()
    if data_feed_name == '' and data_feed_name == None:
        logger.error('Data Feed Name must be provided.')
        return pandas.DataFrame()
    if timezone_offset_minutes is None:
        timezone_offset_minutes = 0
    headers = api_inputs.api_headers.default
    if not set([expected_delivery]).issubset(set(EXPECTED_DELIVERY.__args__)):
        logger.error('expected_delivery parameter must be set to one of the allowed values defined by the '
                     'EXPECTED_DELIVERY literal: %s', EXPECTED_DELIVERY.__args__)
        return pandas.DataFrame()
    if not set([schedule_timezone]).issubset(set(SCHEDULE_TIMEZONE.__args__)):
        logger.error('schedule_timezone parameter must be set to one of the allowed values defined by the '
                     'SCHEDULE_TIMEZONE literal: %s', SCHEDULE_TIMEZONE.__args__)
        return pandas.DataFrame()
    if not set([queue_name]).issubset(set(QUEUE_NAME.__args__)):
        logger.error('queue_name parameter must be set to one of the allowed values defined by the '
                     'QUEUE_NAME literal: %s', QUEUE_NAME.__args__)
        return pandas.DataFrame()
    if 5 > len(cron_schedule.split(' ')) > 6:
        logger.error(
            "cron_schedule parameter must be in the format * * * * *")
        return pandas.DataFrame()
    logger.info(
        f'Deploy for Driver Id {driver_id} on timer for ApiProjectID: {api_inputs.api_project_id} and schedule: {cron_schedule}.')
    logger.info(
        f'Settings to be passed to the driver on start are: {str(settings)}')
    payload = {
        "dataFeedId": str(data_feed_id),
        "driverId": driver_id,
        "name": data_feed_name,
        "feedType": "Readings",  # Default
        "expectedDelivery": expected_delivery,
        "sourceType": "Timer",
        "queueName": queue_name,
        "timer": {
            "cronSchedule": cron_schedule,
            "timezoneOffsetMinutes": timezone_offset_minutes,
            "scheduleTimezone": schedule_timezone
        },
        "settings": settings
    }
    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/tasks/deployment"
    logger.info("Sending request: POST %s", url)
    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    if response.status_code != 200 and len(response.text) > 0:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        error_df = pandas.read_json(response.text)
        return response_status, error_df
    elif response.status_code != 200 and len(response.text) == 0:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error(
            'No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()
    df = pandas.read_json(response.text, typ='Series').to_frame().T
    df.columns = _column_name_cap(df.columns)
    return df


def reschedule_timer(api_inputs: ApiInputs, data_feed_id: uuid.UUID, queue_on_schedule: bool = False):
    """Rescedule Timer driver.
    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize.initialize() function
    data_feed_id : uuid.UUID
        The DataFeedId of the Timer Task to reschedule
    Returns
    -------
    pandas.Dataframe
        A dataframe containing the details of the deployed data feed.
    """
    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using API.")
        return pandas.DataFrame()

    headers = api_inputs.api_headers.default
    payload = {
        "dataFeedId": str(data_feed_id),
        "queueJobOnSchedule": queue_on_schedule
    }

    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/data-ingestion/tasks/reschedule"
    logger.info("Sending request: POST %s", url)
    response = requests.post(url, json=payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)

    if response.status_code != 200 and len(response.text) > 0:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        error_df = pandas.read_json(response.text)
        return response_status, error_df
    elif response.status_code != 200 and len(response.text) == 0:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.", response.status_code,
                     response.reason)
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error(
            'No data returned for this API call. %s', response.request.url)
        return response_status, pandas.DataFrame()

    df = pandas.read_json(response.text, typ='Series').to_frame().T
    df.columns = _column_name_cap(df.columns)

    return df
