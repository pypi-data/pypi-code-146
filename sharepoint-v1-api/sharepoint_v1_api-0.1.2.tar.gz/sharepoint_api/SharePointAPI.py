import sys
import os
import getpass
import json
import requests
from requests_ntlm import HttpNtlmAuth
from typing import List

from .SharePointUser import SharePointUser
from .SharePointUserList import SharePointUserList
from .SharePointListItem import SharePointListItem, SharepointSiteCase
from .SharePointList import SharePointList, CasesList, TimeRegistrationList
from .SharePointLists import SharePointLists


class SharePointAPI:

    @classmethod
    def _compact_init(cls, credentials: dict):
        '''
        Takes credentials in the form of a dict
        {
            "username": "",
            "password": "",
            "sharepoint_url": ""
        }
        '''

        username = credentials['username']
        password = credentials['password']
        sharepoint_url = credentials['sharepoint_url']
        proxies = {} if 'proxies' not in credentials else credentials['proxies']

        sharepoint_api = object.__new__(SharePointAPI)
        sharepoint_api.__init__(username, password, sharepoint_url, proxies)

        return sharepoint_api

    def __init__(self, username: str, password: str, sharepoint_url: str, proxies: dict):
        '''

        '''

        self.username = username
        self.password = password
        self.sharepoint_url = sharepoint_url
        self.proxies = proxies

    def _api_post_call(self, url, post_data, form_digest_value=None, merge=False):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'accept': 'application/json;odata=verbose',
            'Content-type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Length': str(len(f'{post_data}')),
            'X-RequestDigest': f'{form_digest_value}',
            'If-Match': '*'
        }
        if merge:
            headers['X-HTTP-Method'] = 'MERGE'

        r = requests.post(url,
                          auth=HttpNtlmAuth(self.username, self.password), headers=headers, json=post_data, proxies=self.proxies)

        if r.status_code == 400:
            print('Failed to connect: ', r.status_code)
            print(r.text)
            print('Exiting.')
            raise ConnectionError
        elif r.status_code == 404:
            print('Failed to connect: ', r.status_code)
            print(r.request.url)
            print(r.request.body)
            print('Exiting.')
            raise ConnectionError
        elif r.status_code not in [200, 201, 204]:
            print('Failed to connect: ', r.status_code)
            print('Exiting.')
            raise ConnectionError
        return r

    def _api_attachment_call(self, url, post_data, form_digest_value=None, overwrite=False, x_http_method=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'accept': 'application/json;odata=verbose',
            'X-RequestDigest': f'{form_digest_value}'
        }
        if overwrite:
            headers['X-HTTP-Method'] = "PUT"
        if x_http_method:
            if x_http_method.lower() == 'delete':
                headers['X-HTTP-Method'] = "DELETE"
            elif x_http_method.lower() == 'put':
                headers['X-HTTP-Method'] = "PUT"
            else:
                print(f'X-HTTP-Method "{x_http_method}" is not implemented')

        if post_data:
            headers['Content-Length'] = str(len(f'{post_data}'))
            r = requests.post(url,
                              auth=HttpNtlmAuth(self.username, self.password), data=post_data, headers=headers, proxies=self.proxies)
        else:
            r = requests.post(url,
                              auth=HttpNtlmAuth(self.username, self.password), headers=headers, proxies=self.proxies)

        if r.status_code == 404:
            print('Failed to connect: ', r.status_code)
            print(r.request.url)
            # print(r.request.body)
            print(str(r.content))
            print('Exiting.')
            raise ConnectionError
        if r.status_code == 400:
            print('Failed to connect: ', r.status_code)
            print(r.reason)
            # print(r.request.body)
            print(str(r.content))
            print('Exiting.')
            raise ConnectionError
        elif r.status_code not in [200, 204]:
            print('Failed to connect: ', r.status_code)
            try:
                print(r.json()['error']['message']['value'])
            except:
                print('No error message found')
            print('Exiting.')
            raise ConnectionError
        return r

    def _api_get_call(self, url, *args, **kwargs):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
            'accept': 'application/json;odata=verbose',
            'Content-type': 'application/json; charset=utf-8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br'
        }

        r = requests.get(url,
                         auth=HttpNtlmAuth(self.username, self.password), headers=headers, proxies=self.proxies)

        if r.status_code == 404:
            print('Failed to process request with status code ', r.status_code)
            print(r.json()['error']['message']['value'])
            raise ConnectionError
        elif r.status_code != 200:
            print('Failed to connect: ', r.status_code)
            try:
                print(json.loads(r.text)['error']['message']['value'])
            except:
                pass
            try:
                print(json.loads(r.text)['error']['code'])
            except:
                pass
            json.loads(r.text)
            print('Exiting.')
            raise ConnectionError
        return r

    def get_users(self, sharepoint_site):
        '''
            Returns a list of users from a given sharepoint_site
        '''
        r = self._api_get_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/siteusers')

        users = []

        for user_settings in r.json()["d"]["results"]:
            users.append(SharePointUser(user_settings))

        return SharePointUserList(sharepoint_site, users)

    def get_user(self, sharepoint_site, user_id):
        '''
            Returns a list of users from a given sharepoint_site
        '''
        if user_id is None:
            return SharePointUser()
        r = self._api_get_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/siteusers?$filter=( Id eq {user_id} )')

        user_settings = r.json()["d"]["results"][0]
        return SharePointUser(user_settings)

    # SP Lists

    def get_lists(self, sharepoint_site):
        '''
            Returns a list of lists from a given sharepoint_site
        '''
        r = self._api_get_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists')

        _lists = []
        for list_props in r.json()["d"]["results"]:
            _lists.append(SharePointList(sharepoint_site, list_props))

        return SharePointLists(_lists)

    def get_list(self, sharepoint_site, sp_list, filters=None, top=1000, view_path=None, SPListType: SharePointList = SharePointList) -> SharePointList:
        '''
            Returns a list from a given sharepoint_site using its guid

            Returns a subset of items from a list

            sharepoint_site:
            guid: the guid of the list to retrieve items from
        '''

        # Uses either guid or SharePointList
        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid
            r = self._api_get_call(
                f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')')
            sp_list = SPListType(sharepoint_site, r.json()["d"])

        elif isinstance(sp_list, str):
            guid = sp_list
            r = self._api_get_call(
                f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')')
            sp_list = SPListType(sharepoint_site, r.json()["d"])
        else:
            sys.exit(1)

        arguments = []

        if filters is not None:
            if not isinstance(filters, list):
                filter_string = self.py2sp_conditional(filters)
                # print(filters)
                # raise('invalid search filters')
            else:

                filter_string = self.py2sp_conditional(' and '.join(filters))
            arguments.append(f'$filter={filter_string}')

        if view_path is not None:
            # Shows top x items
            arguments.append(f'$ViewPath={view_path}')

        if top is not None:
            # Shows top x items
            arguments.append(f'$top={top}')

        r = self._api_get_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items?{"&".join(arguments)}')

        items = [SPListType.SPItem(self, sharepoint_site, guid, item_settings)
                 for item_settings in r.json()["d"]["results"]]
        sp_list.append_items(items)
        return sp_list

    def get_list_by_name(self, sharepoint_site, sp_list_name: str, filters=None, top=1000, view_path=None, SPListType: SharePointList = SharePointList) -> SharePointList:
        '''
            Returns a list from a given sharepoint_site filtering by list name

            Returns a subset of items from a list

            sharepoint_site: The sharepoint_site containing the list
            sp_list_name: the name of the list
            filters: query filters
            top: Maximum items to query from the list
        '''

        sp_lists = self.get_lists(sharepoint_site)

        if sp_list_name in sp_lists.all_list_titles:
            return self.get_list(sharepoint_site, sp_lists.get_list(sp_list_name), filters, top, view_path, SPListType=SPListType)
        else:
            print(
                f"List '{sp_list_name}' does not exist in sharepoint_site {sharepoint_site}'")
            sys.exit(1)

    def get_list_from_json(self, file_name, SPListType: SharePointList = SharePointList) -> SharePointList:
        '''
            Returns a list from a sharepoint_site based on a json file.

            file_name: the json file to load the list from

        '''
        try:
            with open(file_name, 'r') as fp:
                data_dict = json.load(fp)

            sharepoint_site = data_dict['sharepoint_site']
            guid = data_dict['GUID']

            cases = []
            for case in data_dict['cases']:
                settings = case["settings"]
                versions = None if "versions" not in case else case["versions"]
                cases.append(SPListType.SPItem(
                    self, sharepoint_site, guid, settings, versions))

            return SPListType(sharepoint_site, data_dict['Settings'], cases)
        except FileNotFoundError as err:
            print(f"File '{file_name}' was not found")
            raise err
        except Exception as err:
            raise err

    # SP Item

    def get_item(self, sharepoint_site, sp_list, item_id) -> SharePointListItem:
        '''
            Returns a list of users from a given sharepoint_site
        '''

        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid

        elif isinstance(sp_list, str):
            guid = sp_list
        else:
            sys.exit(1)

        r = self._api_get_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items({item_id})')

        settings = r.json()["d"]
        return SharePointListItem(self, sharepoint_site, guid, settings)

    def create_item(self, sharepoint_site, sp_list, data) -> SharePointListItem:
        # Uses either guid or SharePointList
        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid
        elif isinstance(sp_list, str):
            guid = sp_list
            r = self._api_get_call(
                f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')')
            sp_list = SharePointList(
                sharepoint_site, r.json()["d"]["results"][0])

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})

        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items', data, form_digest_value)

        settings = r.json()["d"]
        return SharePointListItem(self, sharepoint_site, guid, settings)

    def update_item(self, sharepoint_site, sp_list, item_id, data) -> None:
        '''
            Update a sharepoint item

            sharepoint_site: The sharepoint_site containing the item
            sp_list: The list containing the item
            item_id: The id of the item
            data: Data to push to the item
        '''
        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid
        elif isinstance(sp_list, str):
            guid = sp_list
            r = self._api_get_call(
                f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')')
            sp_list = SharePointList(
                sharepoint_site, r.json()["d"]["results"][0])
        else:
            raise TypeError(
                'Only "SharePointList" and "str" types are allowed')

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})

        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items({item_id})', data, form_digest_value, merge=True)

    def attach_file(self, sharepoint_site, sp_list, item, file_name, file_content) -> dict:
        # Uses either guid or SharePointList
        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid
        elif isinstance(sp_list, str):
            guid = sp_list
        else:
            raise TypeError(
                'Only "SharePointList" and "str" types are allowed')

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})
        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        r = self._api_attachment_call(
            f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items({item.Id})/AttachmentFiles/ add(FileName='{file_name}')", file_content, form_digest_value)

        return r.json()

    def get_item_versions(self, sharepoint_site, sp_list, item_id, select_fields=[]) -> list:
        '''
            Returns a list of users from a given sharepoint_site
        '''

        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid

        elif isinstance(sp_list, str):
            guid = sp_list
        else:
            sys.exit(1)

        if select_fields:
            r = self._api_get_call(
                f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items({item_id})/versions?$select={",".join(select_fields)}')
        else:
            r = self._api_get_call(
                f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items({item_id})/Versions')

        versions = r.json()["d"]['results']
        return versions

    # Cases

    def get_cases_list_from_json(self, file_name) -> CasesList:
        '''
            Returns a cases list from a sharepoint_site based on a json file.

            file_name: the json file to load the list from

        '''

        return self.get_list_from_json(file_name, SPListType=CasesList)

    def get_cases_list(self, sharepoint_site, sp_list, filters=None, top=1000, view_path=None) -> CasesList:
        '''
            Returns a cases list from a given sharepoint_site using its guid

            Returns a subset of items from a list

            sharepoint_site: The sharepoint_site containing the list
            sp_list: the guid of the list to retrieve items from
            filters: query filters
            top: Maximum items to query from the list
        '''

        return self.get_list(sharepoint_site, sp_list, filters, top, view_path, SPListType=CasesList)

    def get_cases_list_by_name(self, sharepoint_site, sp_list_name: str, filters=None, top=1000, view_path=None) -> CasesList:
        '''
            Returns a cases list from a given sharepoint_site filtering by list name

            sharepoint_site: The sharepoint_site containing the list
            sp_list_name: the name of the list
            filters: query filters
            top: Maximum items to query from the list
        '''
        return self.get_list_by_name(sharepoint_site, sp_list_name, filters, top, view_path, SPListType=CasesList)

    def get_case(self, sharepoint_site, sp_list, item_id) -> SharePointListItem:
        '''
            Returns a list of users from a given sharepoint_site
        '''

        if isinstance(sp_list, SharePointList):
            guid = sp_list.guid

        elif isinstance(sp_list, str):
            guid = sp_list
        else:
            sys.exit(1)

        r = self._api_get_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/Lists(guid\'{guid}\')/items({item_id})')

        settings = r.json()["d"]
        return SharepointSiteCase(self, sharepoint_site, guid, settings)

    # Time Registration

    def get_time_registration_list_from_json(self, file_name) -> TimeRegistrationList:
        '''
            Returns a Time Registration list from a sharepoint_site based on a json file.

            file_name: the json file to load the list from

        '''

        return self.get_list_from_json(file_name, SPListType=TimeRegistrationList)

    def get_time_registration_list(self, sharepoint_site, sp_list, filters=None, top=1000, view_path=None) -> TimeRegistrationList:
        '''
            Returns a Time Registration list from a given sharepoint_site using its guid

            Returns a subset of items from a list

            sharepoint_site: The sharepoint_site containing the list
            sp_list: the guid of the list to retrieve items from
            filters: query filters
            top: Maximum items to query from the list
        '''

        return self.get_list(sharepoint_site, sp_list, filters, top, view_path, SPListType=TimeRegistrationList)

    def get_time_registration_list_by_name(self, sharepoint_site, sp_list_name: str, filters=None, top=1000, view_path=None) -> TimeRegistrationList:
        '''
            Returns a Time Registration list from a given sharepoint_site filtering by list name

            sharepoint_site: The sharepoint_site containing the list
            sp_list_name: the name of the list
            filters: query filters
            top: Maximum items to query from the list
        '''
        return self.get_list_by_name(sharepoint_site, sp_list_name, filters, top, view_path, SPListType=TimeRegistrationList)

    # SP Files

    def folder_exists(self, sharepoint_site, folder, in_doc_lib=True):
        '''
            Returns a boolean to indicate whether a folder exists
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        r = self._api_get_call(
            f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/GetFolderByServerRelativeUrl('/cases/{sharepoint_site}/{folder}')/ListItemAllFields")

        return False if ("ListItemAllFields" in r.json()["d"] and r.json()["d"]["ListItemAllFields"] is None) else True

    def create_new_folder(self, sharepoint_site, folder, new_folder, in_doc_lib=True):
        '''
            Creates a new folder
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})
        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        r = self._api_post_call(f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/web/folders",
                                form_digest_value=form_digest_value,
                                post_data={
                                    "ServerRelativeUrl": f'/cases/{sharepoint_site}/{folder}/{new_folder}',
                                }
                                )

        return r.status_code

    def get_files(self, sharepoint_site, folder, in_doc_lib=True):
        '''
            Returns a list of files from a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        r = self._api_get_call(
            f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/GetFolderByServerRelativeUrl('/cases/{sharepoint_site}/{folder}')/Files")

        return r.json()["d"]["results"]

    def get_file_content(self, sharepoint_site, folder, file, in_doc_lib=True):
        '''
            Downloads and saves a file from a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        r = self._api_get_call(
            f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/GetFolderByServerRelativeUrl('/cases/{sharepoint_site}/{folder}')/Files('{file}')/$value")
        return r._content

    def download_file(self, sharepoint_site, folder, file, out_file=None, in_doc_lib=True):
        '''
            Downloads and saves a file from a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        if not out_file:
            out_file = file

        file_content = self.get_file_content(
            sharepoint_site, folder, file, in_doc_lib)

        with open(out_file, 'wb') as f:
            f.write(file_content)

    def upload_file_content(self, sharepoint_site, folder, file, file_content, overwrite=False, in_doc_lib=True):
        '''
            Uploads a file to a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})
        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        r = self._api_attachment_call(
            f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/GetFolderByServerRelativeUrl('/cases/{sharepoint_site}/{folder}')/Files/add(url='{file}',overwrite={str(overwrite).lower()})",
            file_content,
            form_digest_value)
        return r.json()

    def upload_file(self, sharepoint_site, folder, file, in_file=None, overwrite=False, in_doc_lib=True):
        '''
            Uploads a file to a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        if not in_file:
            in_file = file
        with open(in_file, 'rb') as f:
            file_content = f.read()

        return self.upload_file_content(sharepoint_site, folder, file, file_content, overwrite, False)

    def delete_file(self, sharepoint_site, folder, file, in_doc_lib=True):
        '''
            Uploads a file to a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})
        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        r = self._api_attachment_call(
            url=f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/GetFolderByServerRelativeUrl('/cases/{sharepoint_site}/{folder}')/Files('{file}')",
            post_data=None,
            form_digest_value=form_digest_value,
            x_http_method='DELETE')

    def copy_file(self, sharepoint_site, folder, file, out_folder=None, out_file=None, overwrite=False, in_doc_lib=True):
        '''
            Downloads and saves a file from a folder in a given sharepoint_site
        '''

        if in_doc_lib:
            folder = os.path.join("DocumentLibrary", folder)

        if not out_file:
            out_file = 'copy of '+file

        if not out_folder:
            out_folder = folder

        r = self._api_post_call(
            f'{self.sharepoint_url}/cases/{sharepoint_site}/_api/contextinfo', {})
        form_digest_value = r.json(
        )["d"]["GetContextWebInformation"]["FormDigestValue"]

        in_path = f"/cases/{sharepoint_site}/{folder}"
        out_path = f"/cases/{sharepoint_site}/{out_folder}/{out_file}"

        r = self._api_attachment_call(
            f"{self.sharepoint_url}/cases/{sharepoint_site}/_api/Web/GetFolderByServerRelativeUrl('{in_path}')/Files('{file}')/copyto(strnewurl='{out_path}',boverwrite={str(overwrite).lower()})",
            None,
            form_digest_value)

    # STATIC METHODS

    @staticmethod
    def py2sp_conditional(conditional: str):
        ''''''
        return conditional.replace('==', 'eq').replace('!=', 'ne').replace('>=', 'ge').replace('<=', 'le').replace('>', 'gt').replace('<', 'lt')
