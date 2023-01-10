from __future__ import unicode_literals

import base64
import logging
import time
import traceback
import random
import requests
from datetime import datetime, timezone

from MammothAnalytics import const
from MammothAnalytics.const import REQUEST_STATUS, USER_PERMISSIONS, RESERVED_BATCH_COLUMN_INTERNAL_NAMES_AND_KEYS
from MammothAnalytics.errors import AuthError, UnknownError
from MammothAnalytics.errors import MalformedRequestError, AuthenticationError, \
    NotFoundError, AuthorizationError
from .urls import get_url
import pydash

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)

MAX_RETRIES = 80
RETRY_DELAY_IN_SEC = 2
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


def handleError(f):
    def new_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (AuthError, UnknownError, NotFoundError, AuthenticationError,
                AuthorizationError, MalformedRequestError) as e:
            raise e
        except Exception as e:
            fname = f.__name__
            log.error({
                'function_name': fname,
                'args': args,
                'kwrgs': kwargs
            })
            log.error(''.join(traceback.format_exc()))
            raise UnknownError(0, 'Error in: {0}'.format(fname))

    new_function.__name = f.__name__
    new_function.__doc__ = f.__doc__
    return new_function


def encode_integration_key(key):
    """encrypt the base 64 encrypted integration key to escape adblocker
    Args:
        key (string): base 64 encrypted integration key of the connector
    Returns:
        string: integration string of the connector
    """
    return base64.b64encode(key.encode('ascii')).decode()


class MammothConnector(object):
    def __init__(self, account_id=None, api_url=None, api_key=None, api_secret=None):
        """
        The main class for handling Mammoth Analytics API
        Args:
            :account_id: Account ID.
            :api_url: API server url
            :api_key: API key for an account user
            :api_secret: API secret for an account user
        """
        if not api_url:
            api_url = const.API
        self.api_url = api_url
        self.__account_id = account_id

        if api_key and api_secret:
            self.__api_key = api_key
            self.__api_secret = api_secret
        else:
            raise AuthError("Apikey Apisecret needed!")

    def __del__(self):
        pass

    def _make_signed_request(self, rtype, api, **kwargs):
        log.info((rtype, api))
        headers = {'X-API-KEY': self.__api_key}
        headers['X-API-SECRET'] = self.__api_secret
        if 'headers' in kwargs.keys():
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers
        method_maps = {
            'get': requests.get,
            'post': requests.post,
            'delete': requests.delete,
            'patch': requests.patch,
            'put': requests.put
        }
        api_url = get_url(api, self.api_url)
        response = method_maps[rtype](api_url, **kwargs)
        resp = {'ERROR_CODE': 0, 'ERROR_MESSAGE': 'Unknown'}
        try:
            resp = response.json()
            log.debug('response json :{0}'.format(resp))
        except Exception as e:
            raise UnknownError(resp['ERROR_CODE'], 'Server responded with status code :{0}'.format(response.status_code,
                                                                                                   resp[
                                                                                                       'ERROR_MESSAGE']))
        if response.status_code == 200:
            return response
        elif response.status_code == 500:
            if resp['ERROR_CODE'] == 0:
                raise UnknownError(resp['ERROR_CODE'],
                                   'Server responded with status code :{0} and message:'.format(response.status_code,
                                                                                                resp['ERROR_MESSAGE']))
            else:
                raise UnknownError(resp.get('ERROR_CODE'), resp.get('ERROR_MESSAGE'))
        else:
            exc_class = UnknownError
            if response.status_code == 400:
                exc_class = MalformedRequestError
            elif response.status_code == 401:
                exc_class = AuthenticationError
            elif response.status_code == 403:
                exc_class = AuthorizationError
            elif response.status_code == 404:
                exc_class = NotFoundError
            raise exc_class(resp['ERROR_CODE'], resp['ERROR_MESSAGE'])

    @handleError
    def list_accounts(self):
        """
        Returns a list of accounts user has access to
        :return: List of dictionaries. Each dictionary contains id, name and other properties associated with an account
        """
        response = self._make_signed_request('get', '/accounts')
        return response.json()['accounts']

    @handleError
    def list_users(self):
        """
        Returns a list of accounts user has access to
        :return: List of dictionaries. Each dictionary contains id, name and other properties associated with an account
        """
        response = self._make_signed_request('get', '/accounts/{account_id}/users'.format(account_id=self.__account_id))
        return response.json()['users']

    @handleError
    def add_user_to_account(self, email, full_name, user_permission=USER_PERMISSIONS.ANALYST,
                            get_access_token=False):
        log.info("Account id is {0}".format(self.__account_id))
        response = self._make_signed_request('post',
                                             '/accounts/{account_id}/users'.format(account_id=self.__account_id),
                                             json={
                                                 'email': email,
                                                 'full_name': full_name,
                                                 'perm_name': user_permission,
                                                 'get_access_token': get_access_token
                                             })
        return response.json()

    @handleError
    def remove_user_from_account(self, user_id):
        self._make_signed_request('delete', '/accounts/{account_id}/users/{user_id}'.format(
            account_id=self.__account_id, user_id=user_id
        ))

    @handleError
    def list_datasets(self):
        """
        Returns a list of datasets in the system
        :return: List of dictionaries containing info about the datasets in the system. Contains info such as id, name etc.
        """
        response = self._make_signed_request('get', '/datasets')
        return response.json()['datasets']

    @handleError
    def refresh_dataset(self, ds_id):
        response = self._make_signed_request('patch', '/datasets/{0}'.format(ds_id), json={
            "patch": [{"op": "replace", "path": "data", "value": "refresh"}]})
        return response.json()

    @handleError
    def delete_dataset(self, ds_id):
        log.debug(f"Deleting dataset {ds_id}")
        response = self._make_signed_request('delete', '/datasets/{0}'.format(ds_id))
        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        log.debug(f"Dataset {ds_id} deleted successfully")
        return future_response

    @handleError
    def delete_identity(self, identity_key, integration_key):
        integration_key = encode_integration_key(integration_key)
        response = self._make_signed_request('delete',
                                             '/integrations/{0}/identities/{1}'.format(integration_key, identity_key))
        return response.json()

    @handleError
    def create_dataset(self, name, metadata, display_properties=None):
        """
        Create a dataset in Mammoth Analytics.

        TODO: explain metadata and display properties somewhere and put links here

        :param name: Name of the dataset
        :param metadata: Metadata for the given dataset. This is a list of dict objects. Each dict should contain `display_name`,
            `internal_name` and `type`. `type` should be one of `NUMERIC`, `TEXT` or `DATE`
        :param display_properties: A dictionary of display properties.
        :return: Datasource id
        """
        if not display_properties:
            display_properties = {'FORMAT_INFO': {}, "SORT": []}
        response = self._make_signed_request(
            'post', '/datasets',
            json={'name': name, 'metadata': metadata,
                  'display_properties': display_properties})
        return response.json()['id']

    @handleError
    def create_dataset_from_url(self, file_url):
        """
        Create a dataset from file url
        :params: file url
        :return: dataset id
        """

        file_url_ds_param = {"url": file_url}
        r = self._make_signed_request('post', '/weburls', json=file_url_ds_param)
        response = r.json()

        if response.get('STATUS') == 'SUCCESS':
            file_id = response.get('id')
            self.wait_till_file_processing_get_ds(file_id)
            ds_id = self.get_ds_for_file(file_id)['id']
            return ds_id
        else:
            raise UnknownError(response.get('ERROR_MESSAGE'))

    @handleError
    def create_webhook_dataset(self, name, is_secure=False, ds_mode="Replace"):
        """
        Create a webhook dataset in Mammoth Analytics.
        Args:
            name: Name of the dataset
            is_secure: Is secure True/False
            ds_mode: Dataset mode of the dataset Replace/Combine
        Return:
            response.json(): Datasource id
        """
        webhook_ds_param = {"name": name, "origins": "*", "is_secure": is_secure, "mode": ds_mode}
        response = self._make_signed_request(
            'post', '/webhooks',
            json=webhook_ds_param)
        return response.json()

    @handleError
    def get_webhook_by_uri(self, webhook_uri):
        webhook_details = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            all_webhooks = self.list_webhooks()
            for wh in all_webhooks:
                if wh.get('url') == webhook_uri:
                    webhook_details = wh
                    break
            if webhook_details is not None:
                break
            retry_count += 1
        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max retry limit reached to get webhook details.")
        return webhook_details

    @handleError
    def list_webhooks(self):
        response = self._make_signed_request('get', 'webhooks').json()
        webhooks = response.get('webhooks', [])
        return webhooks

    @handleError
    def post_data_to_webhook(self, uri, data):
        if not isinstance(uri, str):
            raise TypeError("webhook uri should be of string type. found {0} instead".format(type(uri)))
        response = self._make_signed_request('post', uri, json=data)
        return response.json()

    @handleError
    def list_batches(self, ds_id):
        log.debug(f"Fetching batches for ds {ds_id}")
        response = self._make_signed_request('get', '/datasets/{0}/batches'.format(ds_id))
        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        log.debug(f"Batches for ds {ds_id} fetched successfully")
        return future_response

    @handleError
    def delete_batches(self, ds_id, batches, wait_till_ready=True):
        response = self._make_signed_request('patch', '/datasets/{0}/batches'.format(ds_id), json={
            "patch": [{"op": "remove", "path": "datasources", "value": batches}]})
        response = response.json()
        if wait_till_ready:
            future_id = response['future_id']
            response = self.track_future_id(future_id)
        return response

    @handleError
    def get_dataset(self, ds_id, include_row_count=True):
        """
        Returns a dataset information dictionary for the given ID
        :param ds_id: The datasource id
        :return: dictionary containing information on the dataset
        """
        log.debug("Get dataset for id: {0}".format(ds_id))
        response = self._make_signed_request('get',
                                             '/datasets/{0}?INCLUDE_ROW_COUNT={1}'.format(ds_id, include_row_count))
        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        log.debug(f"Dataset fetched successfully: {future_response}")
        return future_response

    @handleError
    def get_batch(self, ds_id, batch_id, columns=None, condition=None, limit=None, offset=None):
        """
        Method to get paginated data for a particular batch of a dataset
        """
        log.debug(f"Get batch info for dataset {ds_id} and batch {batch_id}")
        paging_params = {
            'columns': columns,
            'condition': condition,
            'limit': limit,
            'offset': offset
        }
        response = self._make_signed_request('get',
                                             '/ datasets / {dataset_id} / batches / {batch_id}'.format(dataset_id=ds_id,
                                                                                                       batch_id=batch_id),
                                             json=paging_params)

        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        get_batch_response = future_tracking_response['response']
        log.debug(f"successfully fetched batch {batch_id} for ds {ds_id} :- {get_batch_response}")
        return get_batch_response

    @handleError
    def get_task(self, view_id):
        log.debug(f"Fetch tasks for view {view_id}")
        response = self._make_signed_request('get', '/workspaces/{0}/tasks'.format(view_id))
        future_id = response.json()['future_id']
        future_req_tracking_response = self.track_future_id(future_id)
        future_response = future_req_tracking_response['response']
        task_response = future_response.get('tasks')
        log.debug(f"Successfully fetched tasks for view {view_id}")
        return task_response

    @handleError
    def add_task(self, view_id, params, wait_till_ready=True):
        log.debug("Adding task for view_id: {0}".format(view_id))
        r = self._make_signed_request('post', '/workspaces/{0}/tasks'.format(view_id), json={'param': params})
        response = r.json()
        log.debug("Response of adding task to view_id {} is {}".format(view_id, response))
        if wait_till_ready and response['information']['status'] == 'processing':
            response = self.track_future_id(response['information']['future_id'])
        log.debug(f"Task added to view {view_id} successfully with response: {response}")
        return response

    @handleError
    def update_task(self, view_id, task_id, params, wait_till_ready=True):
        log.debug("Updating task for view_id: {0}".format(view_id))
        r = self._make_signed_request('patch', '/workspaces/{0}/tasks/{1}'.format(view_id, task_id),
                                      json={"patch": [{"op": "replace", "path": "params", "value": params}]})
        response = r.json()
        if wait_till_ready and response['information']['status'] == 'processing':
            response = self.track_future_id(response['information']['future_id'])
        log.debug(f"Successfully updated task {task_id} in view {view_id} with response: {response}")
        return response

    @handleError
    def delete_task(self, view_id, task_id, wait_till_ready=True, skip_validation=False):
        log.debug("Deleting task for view_id: {0}".format(view_id))
        skip_validation_arg = 'true' if skip_validation else 'false'
        r = self._make_signed_request('delete', '/workspaces/{0}/tasks/{1}?skip_validation={2}'.format(view_id, task_id,
                                                                                                       skip_validation_arg))
        response = r.json()
        if wait_till_ready and response['information']['status'] == 'processing':
            response = self.track_future_id(response['information']['future_id'])
        log.debug(f"Successfully deleted task {task_id} in view {view_id} with response: {response}")
        return response

    @handleError
    def refresh_webhook_data(self, webhook_id):
        response = self._make_signed_request('post', 'webhooks/{0}'.format(webhook_id))
        return response.json()

    @handleError
    def get_task_statuses(self, view_id):
        response = self._make_signed_request('get', 'workspaces/{0}/task-statuses'.format(view_id))
        return response.json().get('statuses')

    @handleError
    def add_data_to_dataset(self, ds_id, data, end_batch=False):
        """
        Add data to a dataset as a list of dictionaries.

        :param ds_id: The target dataset id
        :param data: a list of dictionaries. Each dictionary represents a row of data where key is the column internal name and value is the value of the cell.
        :param end_batch: If true , this would be considered an end of batch.
        :return: A processing response dictionary
        """
        response = self._make_signed_request('post', '/datasets/{0}/data'.format(ds_id),
                                             json={"rows": data, "endBatch": end_batch})
        return response.json()

    @handleError
    def add_data_to_dataset_as_csv(self, ds_id, file_path, has_header):
        """
        To add clean data to a dataset as a csv. Should contain a csv that has the same structure has the metadata.
        use this only if you are sure that all the rows of the right format. That is, each row should contain comma
        separated values in the same order as dataset metadata

        :param has_header: If the file has a header row.
        :param ds_id: the destination ds id
        :param file_path: the path of the file where you want to upload
        """
        header_string = 'true'
        if not has_header:
            header_string = 'false'
        files = {'file': open(file_path, 'rb')}
        response = self._make_signed_request('post', '/datasets/{0}/data'.format(ds_id),
                                             files=files, data={"has_header": header_string})
        return response.json()

    @handleError
    def upload_csv(self, file_path, target_datasource_id=None, replace=False, file_name=None,
                   ds_with_no_header=False, label_resource_id=None):
        """
        To upload an arbitrary csv file to the system. The system would return a file id based on which one can track
        the progress of the file through the mammoth system.
        Args:
            file_path - The file path
            target_datasource_id - if this is set to a dataset id, the arbitrary csv would be appended to the
            data of the dataset.
            replace - mode for which the file should be appended
            file_name - file name for .xlsx, .xls, .zip
            ds_with_no_header - if the given file has header or not
            label_resource_id - resource id of the label/folder
        Return:
            ds - A ds object.
        """
        log.debug("Uploading csv file: {0}".format(file_path))
        files = {'file': open(file_path, 'rb')}
        post_data = {}
        if label_resource_id:
            post_data['label_resource_id'] = label_resource_id
        if target_datasource_id:
            post_data['append_to_ds_id'] = target_datasource_id
            if replace:
                post_data['replace'] = "true"
        response = self._make_signed_request('post', '/files', files=files, data=post_data)
        log.debug(f"Response of files: {response.json()}")
        file_id = response.json()['id']
        ds = self.wait_till_file_processing_get_ds(file_id, file_name, ds_with_no_header)
        ds_id = ds['id']
        if ds_with_no_header is False:
            self.wait_till_ds_ready(ds_id)
            views = self.list_views(ds_id)
            if len(views) > 0:
                view_ids = [view['id'] for view in views]
                workspace_id = max(view_ids)
                self.wait_for_view_to_finish_processing(workspace_id)
            else:
                retry_count = 0
                while retry_count < MAX_RETRIES:
                    if retry_count != 0:
                        time.sleep(RETRY_DELAY_IN_SEC)
                    views = self.list_views(ds_id)
                    if len(views) > 0:
                        view_ids = [view['id'] for view in views]
                        workspace_id = max(view_ids)
                        self.wait_for_view_to_finish_processing(workspace_id)
                        break
                    retry_count += 1
        return ds

    @handleError
    def append_datasets(self, source_dataset_id, target_dataset_id, column_mapping, change_map=None,
                        new_ds_params=None, replace=False, wait_for_views_to_update=True, wait_till_ready=True):
        """
        Method to combine two datasets While appending datasets, target ds gets combined and new rows gets added.At
        this point, ds updated_at will change. Thereafter, the pipeline re-run happens in all workspaces and
        updated_at gets modified for all the workspace once after pipeline re-run. Therefore, we need wait till
        all workspaces updated_at gets changed. -
        1. Loop until updated_at not greater than last_updated_at. Once updated_at is greater than
        last_updated_at break the loop and return the response
        2. Try until retry_count is less than 50, to avoid stuck issue in worse case
        """
        log.debug(f"Appending datasets -  source: {source_dataset_id}, target - {target_dataset_id}")
        wksp_data = []
        date_format = '%Y-%m-%dT%H:%M:%S.%f%z'
        params = {
            "source": "datasource",
            "source_id": source_dataset_id,
            "mapping": column_mapping,
            "replace": replace
        }
        if change_map:
            params.update({"change_map": change_map})
        if new_ds_params:
            params.update({"new_ds_params": new_ds_params})

        # List all workspaces of target dataset
        wksps = self.list_views(target_dataset_id)
        for wksp in wksps:
            view_id = int(wksp["id"])
            res = self.get_view_details(view_id)
            last_updated_at = res['updated_at']
            # store all workspace id and last_data_updated_at time into a dictionary
            wksp_data.append({'view_id': view_id, 'last_updated_at': last_updated_at})
        log.debug(f"wksp_data before: {wksp_data}")
        # append dataset
        response = self._make_signed_request('post', '/datasets/{0}/batches'.format(target_dataset_id), json=params)
        response = response.json()
        if response['STATUS'] == 'SUCCESS':
            future_id = response['result']['future_id']
            if wait_till_ready:
                res = self.track_future_id(future_id)
            if wait_for_views_to_update:
                time.sleep(35)
                self.sync_now(target_dataset_id)
                log.debug(f"Wait for 5 sec to sync ds {target_dataset_id} 's data to views")
                time.sleep(35)
                for view_details in wksp_data:
                    view_id = view_details['view_id']
                    last_updated_at = view_details['last_updated_at']
                    log.debug(
                        f"Iterating over view {view_details['view_id']} whose last_updated_at stored is {last_updated_at}")
                    res = self.get_view_details(view_id)
                    updated_at = res['updated_at']
                    log.debug(f"Fetched updated at for view {view_details['view_id']} with current value: {updated_at}")

                    # convert string to datetime
                    last_updated_at = datetime.strptime(last_updated_at, date_format)
                    updated_at = datetime.strptime(updated_at, date_format)
                    retry_count = 0

                    while not (updated_at > last_updated_at) and retry_count < MAX_RETRIES:
                        # iterate until data_updated_at is not greater than last_data_updated_at
                        retry_count += 1
                        log.debug(f"Wait for 5 more secs for view to be updated after appending data to dataset")
                        time.sleep(5)
                        res = self.get_view_details(view_id)
                        updated_at = res['updated_at']
                        log.debug(f"Fetched updated at for view {view_id} in while loop with value: {updated_at}")
                        updated_at = datetime.strptime(updated_at, date_format)

                    if retry_count == MAX_RETRIES:
                        raise RuntimeError(f"Max retry limit reached to combine datasets.")

                self.sync_now(target_dataset_id)
                log.debug(f"Another Wait for 15 secs to sync ds {target_dataset_id} 's data to views")
                time.sleep(15)
                r = self._make_signed_request('get', '/datasets/{0}/batches'.format(target_dataset_id))
                future_id = r.json().get('future_id')
                future_tracking_response = self.track_future_id(future_id)
                future_response = future_tracking_response['response']
                self.wait_till_ds_ready(target_dataset_id)
                return future_response
        return response

    def wait_till_file_processing_get_ds(self, file_id, file_name=None, ds_with_no_header=False):
        """
        Method will wait till the file with given id has finished processing.
        Works for csv,txt,tsv files right now.
        Also if we pass file_name to the method it works fine for .xslx, .xls
        TODO: Write logic to support .zip file.
        :param file_id:
        :return: A dataset dictionary
        """
        log.debug(f"Waiting till file: {file_id} is processing")
        retry_count = 0
        while retry_count < MAX_RETRIES * 4:
            response = self._make_signed_request('get', '/files/{0}'.format(file_id))
            file_info = response.json()['file']
            status = file_info['status']
            if status != 'processing':
                log.debug(f"Current info of file - {file_id} is {file_info}")
                break
            else:
                time.sleep(RETRY_DELAY_IN_SEC)
            retry_count += 1
        if retry_count == MAX_RETRIES * 4:
            raise RuntimeError(f"Max time limit reached to get processed file .")
        response = self._make_signed_request('get', '/files/{0}'.format(file_id))
        file_info = response.json()['file']
        log.debug(f"File info finally: {file_info}")
        final_ds_id = file_info["additional_data"].get("final_ds_id")
        append_to_ds_id = file_info["additional_data"].get("append_to_ds_id")
        if final_ds_id is None and file_name is None:
            raise UnknownError(f"File name required for .xls, .xlsx, .zip file extensions.")
        log.debug(f"Wait 5 seconds till the file reflects in resources to get dataset id by filtering resources")
        time.sleep(5)
        if final_ds_id is None and file_name is not None:
            resources = self.list_resources()
            resource_keys = resources.keys()
            ds_resources = list(filter(lambda x: resources[x]['resource_type'] == "datasource", resource_keys))
            for ds_resource in ds_resources:
                data = resources[ds_resource]['object_properties']['name']
                if data == file_name:
                    ds_id = resources[ds_resource]['object_properties']['id']
                    final_ds_id = ds_id
        try:
            self._wait_for_ds_status(final_ds_id, 'processing', check_for_status_equality=False)
        except UnknownError as e:
            # in case there is a append to ds id, final ds may get deleted before status check
            log.error(e)
        if append_to_ds_id and ds_with_no_header is False:
            self._wait_for_ds_status(append_to_ds_id, 'ready')
            ds = self.get_dataset(append_to_ds_id)
        else:
            ds = self.get_dataset(final_ds_id)
        return ds

    @handleError
    def _wait_for_ds_status(self, ds_id, status, check_for_status_equality=True):
        intention = 'equal' if check_for_status_equality else 'not_equal'
        log.debug(f"Waiting for dataset {ds_id} status to {intention} {status}")
        retry_count = 0
        while ds_id and retry_count < MAX_RETRIES * 4:
            ds = self.get_dataset(ds_id)
            ds_status = ds['status']
            if check_for_status_equality:
                if ds_status == status:
                    break
                else:
                    time.sleep(RETRY_DELAY_IN_SEC)
            else:
                if ds_status != status:
                    break
                else:
                    time.sleep(RETRY_DELAY_IN_SEC)
            retry_count += 1
        if retry_count == MAX_RETRIES * 4:
            raise RuntimeError(f"Max time limit reached in _wait_for_ds_status")

    @handleError
    def sync_now(self, ds_id, wait_till_ready=False):
        r = self._make_signed_request('post', '/datasets/{}/apply-data'.format(ds_id))
        log.debug("The response of sync now i.e apply data is {}".format(r.json()))
        response = r.json()
        if wait_till_ready:
            response = self.wait_till_batch_data_is_synced(ds_id)
        return response

    @handleError
    def get_ds_for_file(self, file_id):
        """
        Will return the dataset for the given file.
        :param file_id: The file id
        :return: A ds information dictionary
        """
        datasets = self.list_datasets()
        for i in range(len(datasets)):
            ds = datasets[len(datasets) - 1 - i]
            if 'source_id' in list(ds.keys()):
                if ds['source_id'] == file_id and ds['source_type'] == 'file':
                    return ds

    @handleError
    def list_views(self, ds_id):
        """
        Returns a list of views a dataset has
        :param ds_id: Dataset ID
        :return: list of workspace dictionaries
        """
        response = self._make_signed_request('get', '/datasets/{0}/workspaces'.format(ds_id))
        return response.json()['workspaces']

    @handleError
    def create_view(self, ds_id, duplicate_from_view_id=None):
        """
        Returns a workspace_id of the dataset
        :param ds_id: Dataset ID
        :param duplicate_from_view_id: duplicate existing view
        :return: workspace_id
        """
        try:
            params = {}
            if duplicate_from_view_id:
                params = {'clone_config_from': duplicate_from_view_id}
            response = self._make_signed_request('post', '/datasets/{0}/workspaces'.format(ds_id), json=params)

            # View duplication takes a while to reflect the data
            if 'workspace_id' not in response.json():
                time.sleep(10)
                views = self.list_views(ds_id)
                view_ids = [view['id'] for view in views]
                workspace_id = max(view_ids)
                self.wait_for_view_to_finish_processing(workspace_id)
            else:
                workspace_id = response.json()['workspace_id']
        except Exception as e:
            raise e
        return workspace_id

    @handleError
    def delete_view(self, view_id, wait_till_ready=True):
        """
        Safe deletes a workspace
        :param ds_id: Workspace id
        :return: response
        """
        params = {}
        r = self._make_signed_request('post', '/workspaces/{}/safe-delete-request'.format(view_id), json=params)
        response = r.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def reset_view(self, view_id, wait_till_ready=True):
        """
        Make API call to reset the view - Resetting the View will remove all Transformations, Elements and Filters
        :param view_id: workspace_id
        :return: response
        """
        r = self._make_signed_request('post', '/workspaces/{0}/reset'.format(view_id), json={})
        response = r.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def rerun_pipeline(self, view_id, force_run_pipeline=False):
        params = {'force_run': force_run_pipeline}
        response = self._make_signed_request('post', '/workspaces/{}/rerun'.format(view_id), json=params)
        return response.json()

    def reorder_tasks(self, view_id, param, wait_till_ready=True):
        log.debug("Reordering tasks for view_id: {0}".format(view_id))
        r = self._make_signed_request('patch', '/workspaces/{0}/tasks'.format(view_id),
                                      json={"patch": [{"op": "replace", "path": "tasks", "value": param}]})
        response = r.json()
        if wait_till_ready and response['information']['status'] == 'processing':
            response = self.track_future_id(response['information']['future_id'])
        log.debug(f"Successfully reordered tasks in view {view_id} with response: {response}")
        return response

    @handleError
    def get_view_data(self, view_id, columns=None, condition=None, limit=None, offset=None):
        """
        Makes api call to get view data which creates a future request
        Then calls future request tracker method to get future requets's response
        Finally returns the data of the wksp as per params passed
        """
        log.debug(f"Get data for view {view_id}")
        paging_params = {
            'columns': columns,
            'condition': condition,
            'limit': limit,
            'offset': offset
        }

        response = self._make_signed_request('post', 'workspaces/{workspace_id}/data'.format(workspace_id=view_id),
                                             json=paging_params)
        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        view_data = future_response['data']
        log.debug(f"Successfully fetched data for view  {view_id} : {future_response}")
        return view_data

    @handleError
    def run_transform(self, view_id, param):
        r = self._make_signed_request('post', '/workspaces/{0}/tasks'.format(view_id), json={'param': param})
        return r.json()

    @handleError
    def get_view_details(self, view_id):
        log.debug(f"Get details for view {view_id}")
        r = self._make_signed_request('get', '/workspaces/{0}'.format(view_id))
        future_id = r.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        log.debug(f"Successfully fetched details for view {view_id}")
        return future_tracking_response['response']

    @handleError
    def set_view_properties(self, view_id, properties):
        log.debug(f"Set properties for view {view_id}")
        r = self._make_signed_request('post', '/workspaces/{0}'.format(view_id), json=properties)
        future_id = r.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        log.debug(f"Successfully updated properties for view {view_id}")
        return future_tracking_response['response']

    @handleError
    def wait_for_view_to_finish_processing(self, view_id):
        retry_count = 0
        while retry_count < MAX_RETRIES * 2:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            view = self.get_view_details(view_id)
            if view['status'] != 'processing':
                break
            retry_count += 1
        if retry_count == MAX_RETRIES * 2:
            raise RuntimeError(f"Max retry limit reached to get view in ready state")

    @handleError
    def wait_till_view_is_ready(self, view_id):
        retry_count = 0
        while retry_count < MAX_RETRIES * 2:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            view = self.get_view_details(view_id)
            if view['status'] == 'ready':
                break
            retry_count += 1
        if retry_count == MAX_RETRIES * 2:
            raise RuntimeError(f"Max retry limit reached to get view in ready state")

    @handleError
    def copy_template_from_view(self, ds_id, view_id):
        """
        use this method to copy template from another view and apply to the dataset's view. If the dataset has an
        empty view, it will be reused. Else, a new view will get created.

        :param ds_id: The dataset id
        :param view_id: The view ID from which you want to copy the template from.
        :return: Nothing
        """
        self._make_signed_request('post',
                                  '/datasets/{0}/workspaces'.format(ds_id),
                                  json={'clone_config_from': view_id})

    @handleError
    def add_action(self, view_id, param, wait_till_ready=False):
        """
        Adds an action.
        :param view_id: The view on which the action is to be performed
        :param param: The param for the action.
        :return: Request Id for the action
        """
        r = self._make_signed_request('post', '/workspaces/{0}/actions'.format(view_id), json={'param': param})
        response = r.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def run_action(self, view_id, action_id, param, wait_till_ready=False):
        """
        Runs an action.
        :param view_id: The view on which the action is to be performed
        :param action_id:The param to get applied action id
        :param param: The param for the action.
        :return: Request Id for the action
        """
        r = self._make_signed_request('post', '/workspaces/{0}/actions/{1}'.format(view_id, action_id),
                                      json={'param': param})
        response = r.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def edit_action(self, view_id, action_id, param, wait_till_ready=False):
        """
        edit an action.
        :param wait_till_ready:
        :param view_id: The view on which the action is to be performed
        :param action_id:The param to get applied action id
        :param param: The param for the action.
        :return: Request Id for the action
        """

        r = self._make_signed_request('patch', '/workspaces/{0}/actions/{1}'.format(view_id, action_id),
                                      json={"patch": [{"op": "replace", "path": "params", "value": param}]})
        response = r.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def list_actions(self, view_id):
        log.debug(f"Fetching actions for view {view_id}")
        response = self._make_signed_request('get', '/workspaces/{0}/actions'.format(view_id))
        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        actions = future_response['triggers']
        log.debug(f"Actions fetched for view {view_id} are: {actions}")
        return actions

    @handleError
    def delete_action(self, view_id, action_id):
        """
        Deletes action by action id
        :param view_id:
        :param param
        :param action_id:
        :param wait_till_ready:
        :return:
        """
        r = self._make_signed_request('delete', '/workspaces/{0}/actions/{1}'.format(view_id, action_id))
        return r.json()

    @handleError
    def push_view_data_to_mysql(self, view_id, host, username, password, port, database, target_table=None):
        action_param = {
            'run_immediately': True,
            # 'validate_only': True,
            'target_properties': {
                'username': username,
                'password': password,
                'database': database,
                'host': host,
                'table': target_table,
                'port': port
            },
            'trigger_type': 'none',
            'additional_properties': {},
            'handler_type': 'mysql'
        }
        response = self.add_action(view_id, action_param, wait_till_ready=True)
        return response

    @handleError
    def download_view_as_csv(self, view_id, file_prefix=None, condition=None):
        if not isinstance(file_prefix, str):
            file_prefix = 'file_{0}'.format(random.randint(1000, 2000))

        action_param = {
            "handler_type": "s3",
            "trigger_type": "none",
            "run_immediately": True,
            "sequence": None,
            "additional_properties": {},
            "WORKSPACE_ID": view_id,
            "target_properties": {
                "file": file_prefix,
                "use_format": True,
                "include_hidden": False
            }
        }
        action_response = self.add_action(view_id, action_param, wait_till_ready=True)
        log.debug("The response of download_view_as_csv is {}".format(action_response))
        notifications = self.list_notifications()
        for n in notifications:
            url = pydash.get(n, 'details.data.additional_data.url')
            if isinstance(url, str):
                if file_prefix in url:
                    return url

    @handleError
    def list_notifications(self):
        r = self._make_signed_request('get', '/resources')
        data = r.json()
        return data['notifications']['items']

    @handleError
    def _get_async_request_data(self, request_id):
        url = '/async/{0}'.format(request_id)
        r = self._make_signed_request('get', url)
        return r.json()

    @handleError
    def add_third_party_identity(self, integration_key, identity_config):
        integration_key = encode_integration_key(integration_key)
        url = '/integrations/{0}/identities'.format(integration_key)
        r = self._make_signed_request('post', url, json=identity_config)
        request_id = r.json()['request_id']
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            data = self._get_async_request_data(request_id)
            if data['STATUS'] == 'SUCCESS':
                return data['response']['identity_key']
            elif data['STATUS'] == 'PROCESSING':
                retry_count += 1
                continue
            else:
                raise AuthError(data['message'])

        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max retry limit reached to get third party identity created.")

    @handleError
    def get_third_party_identity_key_by_name(self, integration_key, name):
        integration_key = encode_integration_key(integration_key)
        url = "/integrations/{0}/identities".format(integration_key)
        r = self._make_signed_request('get', url)
        data = r.json()
        for identity in data['identities']:
            if identity['name'] == name:
                return identity['value']

    @handleError
    def get_third_party_identities(self, integration_key):
        integration_key = encode_integration_key(integration_key)
        url = "/integrations/{0}/identities".format(integration_key)
        r = self._make_signed_request('get', url)
        data = r.json()
        return data['identities']

    @handleError
    def validate_third_party_ds_config(self, integration_key, identity_key, ds_config):
        integration_key = encode_integration_key(integration_key)
        url = '/integrations/{0}/identities/{1}/dsConfigs'.format(integration_key, identity_key)
        r = self._make_signed_request('post', url, json=ds_config)
        data = r.json()
        # return data['is_valid']
        return data

    @handleError
    def create_third_party_dataset(self, ds_param, wait_till_ready=False):
        url = '/datasets'
        r = self._make_signed_request('post', url, json=ds_param)
        data = r.json()
        # if the response json(data) contains datasource_id it returns ds_id otherwise returns none(only in case of file type dataset creation such as sftp, google drive, dropbox)
        ds_id = data.get('datasource_id')
        if wait_till_ready:
            if ds_id is not None:
                self.wait_till_ds_ready(ds_id)
        return ds_id

    def wait_till_ds_ready(self, ds_id):
        retry_count = 0
        while retry_count < MAX_RETRIES * 4:
            datasets = self.list_datasets()
            ds_ready = False
            for i in range(len(datasets)):
                ds = datasets[len(datasets) - 1 - i]
                log.debug(ds)
                if ds['id'] == ds_id:
                    if ds['status'] == 'processing':
                        time.sleep(RETRY_DELAY_IN_SEC)
                        continue
                    if ds['status'] in ['ready', 'error']:
                        time.sleep(RETRY_DELAY_IN_SEC)
                        ds_ready = True
                        break
                    log.debug(ds['status'])
            if ds_ready:
                break
            retry_count += 1
        if retry_count == MAX_RETRIES * 4:
            raise RuntimeError(f"Max time limit reached to get ds ready.")

    @handleError
    def apply_template_to_view(self, view_id, template_config, wait_till_ready=False):
        url = '/workspaces/{0}/exportable-config'.format(view_id)
        r = self._make_signed_request('post', url, json={"config": template_config})
        response = r.json()
        if wait_till_ready:
            self.wait_till_view_is_ready(view_id)
        return response

    @handleError
    def track_future_id(self, future_id):
        """
        Future request tracker that send GET request to Future API
        and returns response as JSON object when status is not in
        processing (i.e. SUCCESS/FAILED)
        """
        log.debug("Tracking fututre request with id: {}".format(future_id))
        if not isinstance(future_id, int):
            raise RuntimeError(f"Future id should be a numeric value")

        response = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            resource_resp = self._make_signed_request('get', f'/future/{future_id}')
            resource_resp_json = resource_resp.json()
            future_object = resource_resp_json['future']
            response = future_object
            if future_object['status'] != 'processing':
                break
            retry_count += 1

        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to future request response.")
        log.debug("Response from future request: {}".format(response))
        return response

    @handleError
    def add_batch_columns(self, ds_id, param, wait_till_ready=True, ds_column_count=None):
        """
        Method to add batch columns to the Dataset
        :param ds_id:
        :param param - List of batch column/s to be added to the dataset
        :param ds_column_count - expected column count for ds after batch column edition
        """
        res = self._make_signed_request('patch', f'/datasets/{ds_id}',
                                        json={"patch": [{"op": "replace", "path": "batch_columns",
                                                         "value": {"add_columns": param, "remove_columns": []}}]})
        response = res.json()
        if wait_till_ready:
            future_id = response.get('future_id')
            self.track_future_id(future_id)
            self.wait_till_ds_ready(ds_id)
            if ds_column_count is not None:
                self.wait_till_batch_columns_are_updated_in_ds(ds_id, ds_column_count=ds_column_count)
        return response

    @handleError
    def get_batch_column_keys(self, ds_id):
        """
        Method to get batch columns of the dataset
        :param ds_id:
        :return - List of batch column/s keys
        """
        batch_column_keys = []
        metadata = self.get_dataset(ds_id)['metadata']
        for value in metadata:
            if value['internal_name'] in RESERVED_BATCH_COLUMN_INTERNAL_NAMES_AND_KEYS.keys():
                batch_col_key = RESERVED_BATCH_COLUMN_INTERNAL_NAMES_AND_KEYS[value['internal_name']]
                batch_column_keys.append(batch_col_key)

        return batch_column_keys

    @handleError
    def remove_batch_columns(self, ds_id, rem_cols, wait_till_ready=True, ds_column_count=None):
        """
        Method to remove batch columns from the Dataset
        :param ds_id:
        :param rem_cols - List of batch column/s (keys) to be removed from the dataset
        :param ds_column_count - expected column count for ds after batch column deletion
        """
        # Get batch columns of the dataset
        batch_column_keys = self.get_batch_column_keys(ds_id)
        add_cols = list(set(batch_column_keys) - set(rem_cols))

        res = self._make_signed_request('patch', '/datasets/{0}'.format(ds_id),
                                        json={"patch": [{"op": "replace", "path": "batch_columns",
                                                         "value": {"add_columns": add_cols,
                                                                   "remove_columns": rem_cols}}]})
        response = res.json()
        if wait_till_ready:
            future_id = response.get('future_id')
            self.track_future_id(future_id)
            self.wait_till_ds_ready(ds_id)
            if ds_column_count is not None:
                self.wait_till_batch_columns_are_updated_in_ds(ds_id, ds_column_count=ds_column_count)
        return response

    @handleError
    def add_publish(self, view_id, params, wait_till_ready=True):
        r = self._make_signed_request('post', '/workspaces/{0}/publish'.format(view_id), json={'param': params})

        response = r.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def delete_publish(self, view_id, publish_trigger_id):
        log.debug(f"Deleting publish trigger with id: {publish_trigger_id} from view {view_id}")
        response = self._make_signed_request('delete', f'/workspaces/{view_id}/publish/{publish_trigger_id}')

        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        log.debug(f"Deleted publish from view {view_id} successfully")
        return future_response

    @handleError
    def regenerate_publish_password(self, view_id, publish_odbc_type):
        log.debug(f"Regenerating password for publish in view {view_id}")
        param = {
            "patch": [{
                "op": "replace", "path": "reset_password",
                "value": {
                    "odbc_type": publish_odbc_type
                }
            }]
        }
        response = self._make_signed_request('patch', \
                                             f'/workspaces/{view_id}/publish', \
                                             json=param)

        future_id = response.json()['future_id']
        future_tracking_response = self.track_future_id(future_id)
        future_response = future_tracking_response['response']
        log.debug(f"Successfully regenerated password for publish in view {view_id}")
        return future_response['password']

    @handleError
    def get_publish_credentials(self, odbc_type):
        response = self._make_signed_request('get', f'/publish_credentials?odbc_type={odbc_type}')
        return response.json()

    @handleError
    def create_folder(self, params):
        """
        Method to create folder
        :param params - params for the create folder
        """
        r = self._make_signed_request('post', '/labels', json=params)
        response = r.json()
        return response

    @handleError
    def move_file_to_folder(self, destination_folder_id, params, wait_till_ready=True):
        """
        Method to move files from one folder to another
        :param destination_folder_id - id of the folder to which files are moving
        :param params - params which contains files to be moved
        """
        log.debug(f"Moving file to folder: {destination_folder_id}")
        response = self._make_signed_request('post', '/labels/{0}/resources'.format(destination_folder_id), json=params)
        future_id = response.json()['future_id']
        if wait_till_ready:
            future_tracking_response = self.track_future_id(future_id)
            future_response = future_tracking_response['response']
        log.debug(f"File  moved successfully")
        return future_response

    @handleError
    def list_folders(self):
        """
        Method to list all the folders
        """
        response = self._make_signed_request('get', '/labels')
        return response.json().get('labels')

    @handleError
    def delete_folder(self, folder_id):
        """
        Method to delete folder
        :param folder_id - id of the folder to be deleted
        """
        r = self._make_signed_request('delete', '/labels/{0}'.format(folder_id))
        response = r.json()
        return response

    @handleError
    def list_resources(self):
        """
        Method to list all the resources
        """
        response = self._make_signed_request('get', '/resources')
        response = response.json()
        resources = response['core_list_items']['items']
        return resources

    @handleError
    def rename_dataset(self, ds_id, dataset_name):
        """
        method to rename dataset
        :param
            ds_id: dataset id
            dataset_name: dataset name to be changed
        """
        res = self._make_signed_request('patch', '/datasets/{0}'.format(ds_id),
                                        json={"patch": [{"op": "replace", "path": "name",
                                                         "value": dataset_name}]})
        response = res.json()
        return response

    @handleError
    def rename_view(self, wksp_id, wksp_name):
        """
        method to rename view
        :param
            wksp_id: workspace id
            wksp_name: dataset name to be changed
        """
        res = self._make_signed_request('patch', '/workspaces/{0}'.format(wksp_id),
                                        json={"patch": [{"op": "replace", "path": "name",
                                                         "value": wksp_name}]})
        response = res.json()
        return response

    @handleError
    def apply_template(self, view_id, params):
        """
        method to apply template to the view
        :param
            view_id: workspace id
            params: pipeline to be added
        """
        res = self._make_signed_request('post', 'workspaces/{0}/exportable-config'.format(view_id),
                                        json={'config': params})
        response = res.json()
        return response

    @handleError
    def suspend_action(self, view_id, action_id):
        """
        method to suspend action
        :param
            view_id: workspace id
            action_id: action id
        """
        r = self._make_signed_request('patch', '/workspaces/{0}/actions/{1}'.format(view_id, action_id),
                                      json={"patch": [{"op": "replace", "path": "updateState", "value": "suspend"}]})
        response = r.json()
        return response

    @handleError
    def restore_action(self, view_id, action_id):
        """
        method to restore action
        :param
            view_id: workspace id
            action_id: action id
        """
        r = self._make_signed_request('patch', '/workspaces/{0}/actions/{1}'.format(view_id, action_id),
                                      json={"patch": [{"op": "replace", "path": "updateState", "value": "active"}]})
        response = r.json()
        return response


    @handleError
    def fix_schema_header(self, ds_id, params, wait_till_ready=True):
        """
        method to fix the uploaded file which needs user input (ex: csv file does not have header)
        :param
            ds_id: datasest id,
            params: input params for the file to process
        """
        res = self._make_signed_request('post', '/datasets/{ds_id}/csvfile'.format(ds_id=ds_id), json=params)
        response = res.json()
        request_id = response.get('request_id')
        if wait_till_ready:
            response = self.track_async_request_id(request_id)
        return response

    @handleError
    def track_async_request_id(self, request_id):
        """
        Async request tracker that send GET request to Async API
        and returns response as JSON object when status is not in
        processing (i.e. SUCCESS/FAILED)
        """
        if not isinstance(request_id, int):
            raise RuntimeError(f"Request id should be a numeric value")

        response = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            resp_json = self._get_async_request_data(request_id)
            if resp_json['STATUS'] != 'PROCESSING':
                response = resp_json
                break
            retry_count += 1

        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to future request response.")
        return response

    @handleError
    def wait_till_batch_is_updated(self, ds_id, batch_count=None, batch_creation_timestamp=None):
        """
        Method to wait until the batch is updated
        Args:
            ds_id: datasest id
            batch_count: expected task count in case of combined mode
            batch_creation_timestamp: previous batch addition timestamp in case of replace mode
            (either batch_count or batch_creation_timestamp should be passed)
        Return:
            batch_details: updated batch details
        """
        batch_details = None

        if not batch_count and not batch_creation_timestamp:
            raise RuntimeError(f"Either of batch_count or batch_creation_timestamp should be passed")

        retry_count = 0
        if batch_creation_timestamp:
            batch_creation_timestamp = datetime.strptime(batch_creation_timestamp, DATE_FORMAT)

        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            batches = self.list_batches(ds_id)
            if batch_count and len(batches) == batch_count:
                break
            elif batch_creation_timestamp:
                if len(batches) > 0:
                    current_batch_date = batches[-1]['created_at']
                    current_batch_date = datetime.strptime(current_batch_date, DATE_FORMAT)
                    if current_batch_date > batch_creation_timestamp:
                        break
            retry_count += 1
            batch_details = batches
        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to update batch details.")
        return batch_details

    @handleError
    def wait_till_task_details_updated(self, view_id, task_count):
        """
        Method to wait until the task details updated
        Args:
            view_id: workspace id
            task_count: expected task count
        Return:
            task_details: updated task details
        """
        task_details = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            tasks = self.get_task(view_id)
            if len(tasks) == task_count:
                task_details = tasks
                break
            retry_count += 1
        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to update task details.")
        return task_details

    @handleError
    def wait_till_pipeline_status_is_updated(self, view_id, status):
        """
        Method to wait until the pipeline status changes
        Args:
            view_id: workspace id
            status: expected status
        Return:
            pipeline_status: status of the pipeline
        """
        pipeline_status = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            view_details = self.get_view_details(view_id)
            if view_details['pipeline_status'] == status:
                pipeline_status = view_details['pipeline_status']
                break
            retry_count += 1
        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to update pipeline status.")
        return pipeline_status

    @handleError
    def wait_till_batch_columns_are_updated_in_ds(self, ds_id, ds_column_count):
        """
        Method to wait until the pipeline status changes
        Args:
            ds_id: dataset id
            ds_column_count: expected column count for dataset
        Return:
            dataset_details: dataset details
        """
        dataset_details = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            ds_details = self.get_dataset(ds_id)
            if ds_details['column_count'] == ds_column_count:
                dataset_details = ds_details
                break
            retry_count += 1
        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to add/edit batch columns.")
        return dataset_details

    @handleError
    def wait_till_batch_data_is_synced(self, ds_id):
        """
        Method to wait until the added batch data is synced
        Args:
            ds_id: dataset id
        Return:
            dataset_details: dataset details
        """
        dataset_details = None
        ds_row_count = 0
        retry_count = 0

        batches = self.list_batches(ds_id)
        for batch in batches:
            ds_row_count += batch['count']

        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            ds_details = self.get_dataset(ds_id)
            if ds_details['row_count'] == ds_row_count:
                dataset_details = ds_details
                break
            retry_count += 1
        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to sync dataset.")
        return dataset_details

    @handleError
    def get_explore_data(self, view_id, params, wait_till_ready=True):
        """
        Method to add explore card data
        Args:
            view_id: workspace id
            params: params for adding explore card
        """
        r = self._make_signed_request('post', '/workspaces/{0}/data/query'.format(view_id), json=params)
        response = r.json()
        if wait_till_ready:
            future_tracking_response = self.track_future_id(response['future_id'])
            response = future_tracking_response['response']
        return response

    @handleError
    def create_api_token(self, params):
        """
        Method to create api token
        Args:
            params: params for creating api token
        """
        response = self._make_signed_request('post', '/clientapps', json=params)
        return response.json()

    @handleError
    def edit_api_token(self, params):
        """
        Method to edit api token
        Args:
            params: params for editing api token name and description
        """
        response = self._make_signed_request('put', '/clientapp', json=params)
        return response.json()

    @handleError
    def delete_api_token(self, api_token_id):
        """
        Method to delete api token
        Args:
            api_token_id: id of the token to be deleted
        """
        response = self._make_signed_request('delete', '/clientapp?id=' + str(api_token_id))
        return response.json()

    @handleError
    def list_api_tokens(self):
        """
        Method to list all the api tokens of an account
        """
        response = self._make_signed_request('get', '/clientapps')
        return response.json()

    @handleError
    def change_user_role(self, account_id, user_id, user_role):
        """
        Method to change user role
        Args:
            account_id: id of the account
            user_id: id of the user for which role to be changed
            user_role: role to be assigned to the user
        """
        response = self._make_signed_request('patch', '/accounts/{0}/users/{1}'.format(account_id, user_id), json={
            "patch": [{"op": "replace", "path": "user_permission", "value": user_role}]})
        return response.json()

    @handleError
    def suspend_unsuspend_batches(self, ds_id, params, wait_till_ready=True):
        """
        Method to suspend/un-suspend batches
        Args:
            ds_id: dataset id
            params: params for suspend/unsuspend batches
        """
        response = self._make_signed_request('patch', '/datasets/{0}/batches'.format(ds_id), json={
            "patch": [{"op": "replace", "path": "batches", "value": params}]})
        response = response.json()
        if wait_till_ready:
            future_id = response['future_id']
            future_tracking_response = self.track_future_id(future_id)
            response = future_tracking_response['response']
        return response

    @handleError
    def toggle_autosync(self, ds_id, auto_sync):
        """
        Method to toggle auto sync for a dataset
        Args:
            ds_id: dataset id
            auto_sync: toggle value of auto sync on or off (True/False)
        """
        response = self._make_signed_request('patch', '/datasets/{0}'.format(ds_id), json={
            "patch": [{"op": "replace", "path": "autosync", "value": auto_sync}]})
        return response.json()

    @handleError
    def add_user(self, add_user_param):
        """
        Method to add user to an account
        Args:
            add_user_param: params for adding a user
        """
        response = self._make_signed_request('post', '/accounts/{0}/users'.format(self.__account_id),
                                             json=add_user_param)
        return response.json()

    @handleError
    def remove_user(self, user_id):
        """
        Method to remove user from an account
        Args:
            user_id: id of the user to be removed from account
        """
        response = self._make_signed_request('delete', '/accounts/{0}/users/{1}'.format(self.__account_id, user_id))
        return response.json()

    @handleError
    def get_current_plan_details(self):
        """
        Method to get current plan details of account
        Args:
            NA
        """
        plan_details = {'message': 'This account is not associated with any plan'}
        response = self._make_signed_request('get', '/accounts/{0}/sms-details'.format(self.__account_id))
        current_plan_details = response.json().get('current_plan')
        if current_plan_details is not None:
            return current_plan_details
        else:
            return plan_details

    @handleError
    def get_user_app_usage(self, user_id):
        """
        Method to get app usage of the give user
        Args:
            user_id: user id
        """
        response = self._make_signed_request('get', '/accounts/{0}/app-usage/{1}'.format(self.__account_id, user_id))
        return response.json()

    @handleError
    def edit_organization_name(self, organization_name):
        """
        Method to edit organization name
        Args:
            organization_name: name of the organization to be changed to
        """
        response = self._make_signed_request('patch', '/accounts/{0}'.format(self.__account_id), json={
            "patch": [{"op": "replace", "path": "name", "value": organization_name}]})
        return response.json()

    @handleError
    def update_pipeline_inbound_updates(self, view_id, disable=False):
        """
        Method to snooze/unsnooze pipeline updates
        """
        response = self._make_signed_request('post', 'workspaces/{0}/inbound-updates'.format(view_id),
                                             json={'disable': disable})
        return response.json()

    def add_metric(self, view_id, params, condition=None, limit=None, wait_till_ready=True):
        """
        Method to add a metric
        Args:
            view_id: workspace id
            param: param for adding a metric
        """
        res = self._make_signed_request('post', '/workspaces/{0}/derivatives'.format(view_id), json=params)
        response = res.json()
        if wait_till_ready:
            response = self.wait_till_metric_is_ready(view_id, response.get('id'), condition, limit)
        return response

    @handleError
    def delete_metric(self, view_id, metric_id, wait_till_ready=True):
        """
        Method to delete a metric
        Args:
            view_id: workspace id
            metric_id: id of the metric
        """
        res = self._make_signed_request('delete', '/workspaces/{0}/derivatives/{1}'.format(view_id, metric_id))
        response = res.json()
        if wait_till_ready and 'future_id' in response and response["STATUS"] == REQUEST_STATUS.PROCESSING:
            response = self.track_future_id(response['future_id'])
        return response

    @handleError
    def list_metrics(self, view_id):
        """
        Method to list all the metrics of the given view
        Args:
            view_id: workspace id
        """
        res = self._make_signed_request('get', '/workspaces/{0}/derivatives'.format(view_id))
        return res.json().get('derivatives')

    @handleError
    def wait_till_metric_is_ready(self, view_id, metric_id, condition=None, limit=None):
        """
        Method to wait until the metric is ready
        Args:
            view_id: workspace id
            metric_id: id of the metric
            condition: condition for the metric
            limit: row limit
        """
        response = None
        retry_count = 0
        while retry_count < MAX_RETRIES:
            if retry_count != 0:
                time.sleep(RETRY_DELAY_IN_SEC)
            metric_res = self._make_signed_request('post', '/workspaces/{0}/derivatives/{1}'.format(view_id, metric_id),
                                                   json={"CONDITION": condition, "LIMIT": limit})
            metric_resp_json = metric_res.json()
            if metric_resp_json['STATUS'] == 'READY':
                response = metric_resp_json
                break
            retry_count += 1

        if retry_count == MAX_RETRIES:
            raise RuntimeError(f"Max limit reached to add a metric")
        return response

    @handleError
    def toggle_draft_mode(self, view_id, mode):
        """
        Method to enter or exit draft mode for given view
        Returns:
            response: return response json of API request contains account details
        """
        res = self._make_signed_request('post', '/workspaces/{0}/draft-mode'.format(view_id),
                                        json={'draft_operation': mode})
        response = res.json()
        return response

    @handleError
    def modify_password(self, params):
        """
        Method to modify user password
        Args:
            params: modify password post request params
        """
        response = self._make_signed_request('post', '/modify-password', json=params)
        return response.json()

    @handleError
    def suspend_task(self, view_id, task_id, skip_validation=False, wait_till_ready=True):
        """
        method to suspend action
        :param
            view_id: workspace id
            task_id: task id
        """
        r = self._make_signed_request('patch', '/workspaces/{0}/tasks/{1}'.format(view_id, task_id),
                                      json={"patch": [{"op": "suspend", "path": "status",
                                                       "value": {"skip_validation": skip_validation}}]})
        response = r.json()
        if wait_till_ready:
            future_id = int(response.get('information').get('future_id'))
            response = self.track_future_id(future_id)
        return response

    @handleError
    def restore_task(self, view_id, task_id, skip_validation=False):
        """
        method to restore action
        :param
            view_id: workspace id
            task_id: task id
        """
        r = self._make_signed_request('patch', '/workspaces/{0}/tasks/{1}'.format(view_id, task_id),
                                      json={"patch": [
                                          {"op": "restore", "path": "status",
                                           "value": {"skip_validation": skip_validation}}]})
        response = r.json()
        return response

    @handleError
    def get_account_details(self):
        """
        Method to get account details
        """
        r = self._make_signed_request('get', '/accounts/{account_id}'.format(account_id=self.__account_id))
        response = r.json()
        return response

    @handleError
    def send_forgot_password_email(self, email_id):
        """
        Method to send mail for forgot password
        Args:
            :email_id: email id for which email to be sent
        """
        res = self._make_signed_request('post', '/reset-password',
                                           json={"email": email_id, "recaptcha_response": ""})
        response = res.json()
        return response

    @handleError
    def reset_password(self, password, token):
        """
        Method to send mail for forgot password
        Args:
            :password: password to be changed to
            :token: token sent on email for resetting password
        """
        res = self._make_signed_request('post', '/change-password',
                                        json={"password": password, "token": token})
        response = res.json()
        return response

    @handleError
    def download_template(self, view_id):
        """
        Method to download/get template details
        Args:
            :view_id: workspace id
        Return:
            :template_details: list of task details in a template format
        """
        r = self._make_signed_request('get', '/workspaces/{view_id}/exportable-config'.format(view_id=view_id))
        response = r.json()
        template_details = self._get_async_request_data(response['request_id'])
        return template_details

    @handleError
    def get_resource_dependency_details(self, resource_id):
        """
        Method to get the dependency details for the given resource id
        Args:
            :resource_id: resource id of workspace/dataset
        """
        res = self._make_signed_request('get', '/resource_dependencies?resource_ids={resource_id}'.format(
            resource_id=resource_id))
        response = res.json()
        return response

    @handleError
    def update_data_pass_through(self, dependency_update_params):
        """
        Method to update data_pass_through/data_update_pending for a given params
        dependency_update_params structure
        [{
            "context_id": workspace/task/action id,
            "context_type": workspace/task/action,
            "data_pass_through"/"run_pending_update": True/False
        }]
        Args:
            :dependency_update_params: params for updating data_pass_through/data_update_pending details
        """
        res = self._make_signed_request('patch', '/resource_dependencies', json=dependency_update_params)
        response = res.json()
        return response
