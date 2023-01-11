'''
Implementation of the Optilogic Pioneer Rest API.

Pioneer Product Suite 
Encompasses Atlas and Andromeda products.

Atlas 
Web Application with cornerstone IDE, Jobs Dashboard, Account Management, and more.
https://atlas.optilogic.app

Andromeda
On demand hyper-scaling machinery that provisions required resources for job management and run execution.

API Documentation
https://api-docs.optilogic.app/documentation

API Authentication Methods
User Pass: legacy auth method that requires time to live key management
App Key: preferred auth method for API usage

App Key Management
https://atlas.optilogic.app/dashboard/#/user-account?tab=appkey

Glossary:
account file storage: can be standard disk or premium ssd available to all user workspaces
file storage: generic storage reference to encompass workspace and account file storage types
stack: software environment configuration used to build a a workspace from ie linux based pythonic world with specific configuration
ws,wksp,workspace: software environment instance built from a stack and has associated file storage
workspace file storage: standard file storage that is bound to specific workspace instance
'''

import os
import pickle
import requests
import time
from cachetools import cached, TTLCache
from datetime import datetime
from getpass import getpass
from json import loads
from os import getenv
from sys import platform
from tempfile import gettempdir
from types import FrameType
from typing import Tuple, Optional
from warnings import warn, warn_explicit

if platform == 'linux':
    from signal import alarm, signal, SIGALRM

class Api():
    '''Optilogic API is to pilot Andromeda system
    
    EXAMPLE CONFIG
    :{'un': 'username', 'pw': 'password', 'auth_legacy': True}
    :{'un': 'username', 'app_key': 'base64str'}

    :param un: str: username that has the API role
    :param pw: str: password of the user to authenticate and generate api key
    :param auth_legacy: bool: true for conventional username password or false for appkey
    :param cfg: dict: addition config to unpack and setup for api use
    :param apikey: str: username password authentication with one hour time to live
    :param appkey: str: authentication key generated in product without time to live restrictions
    '''

    DATABASE_TEMPLATES: Tuple[str, ...] = ('empty', 'anura_2_4_clean', 'anura_2_5_clean', 'anura_2_4_blast_off_to_space', 'anura_2_5_blast_off_to_space')
    GEO_PROVIDERS: Tuple[str, ...] = ('bing', 'google' ,'mapbox', 'pcmiler','ptv')
    JOBSTATES: Tuple[str, ...] = ('submitted','starting','started','running','done','stopping','stopped','canceling','cancelled','error')
    JOBSTATES_TERMINAL: Tuple[str, ...] = ('done','stopped','cancelled','error')
    JOBSTATES_TERMINAL_RUNTIME: Tuple[str, ...] = ('done','cancelled','error')

    def __init__(self, auth_legacy = True, version: int = 0, appkey: Optional[str] = None, un: Optional[str] = None, pw: Optional[str] = None, **cfg):
        env_domain: Optional[str] = getenv('OPTILOGIC_API_URL')
        env_username: Optional[str] = getenv('OPTILOGIC_USERNAME')
        self._domain = 'https://api.optilogic.app'
        self.api_crash_count: int = 0
        self.auth_apikey_expiry: int = 0
        self.auth_apikey_mins_left: float = 0.0
        self.auth_apikey: Optional[str] = None
        self.auth_appkey: Optional[str] = appkey
        self.auth_method_legacy: bool = auth_legacy
        self.auth_req_header: dict = {'x-api-key': self.auth_apikey, 'x-app-key': self.auth_appkey}
        self.auth_username: Optional[str] = un
        
        if env_domain and env_domain != self._domain:
            self._domain = env_domain
        elif cfg.get('test_system'):
                self._domain = 'https://dev-api.optilogic.app'

        self.api_version = f'{self._domain}/v{version}/'
        if version > 0:
            warn('Only API version zero is supported', UserWarning, stacklevel=1)
        
        if self.auth_method_legacy:
            self.auth_req_header.pop('x-app-key')
            warn_explicit('legacy userpass authentication, please use modern appkey auth https://optilogic.app/#/user-account?tab=appkey', FutureWarning, __file__, 73)

            if self.auth_username is None:
                self.auth_username = env_username if env_username else self.__input_timed('REQUIRED API Username')
            assert(len(self.auth_username) > 0)
            
            self.auth_userpass = pw if pw else self.__input_timed('REQUIRED API User Password', pw=True)
            assert(len(self.auth_userpass) > 0)
        else:
            self.auth_req_header.pop('x-api-key') # auth legacy header does not apply
             
            if appkey:
                self.auth_appkey = appkey
            else:
                env_appkey: Optional[str] = getenv('OPTILOGIC_JOB_APPKEY')
                self.auth_appkey = env_appkey if env_appkey else self.__input_timed('REQUIRED API AppKey')
            
            if len(self.auth_appkey) != 51 or self.auth_appkey.startswith('op_') is False:
                raise ValueError('Valid appkey is required: https://optilogic.app/#/user-account?tab=appkey')
            
            self.auth_req_header['x-app-key'] = self.auth_appkey

        self.debug_requests = True
        self.dir_tmp = os.path.join(gettempdir(), 'optilogic')
        self.file_cache_auth = os.path.join(self.dir_tmp, f'auth_{self.auth_username}.pkl')

        if os.path.exists(self.dir_tmp) is False:
            os.makedirs(self.dir_tmp)
        if os.path.exists(self.file_cache_auth) is False and self.auth_method_legacy:
            self.authenticate_legacy()
        
        self.job_start_recent_key: str = ''
        self.STORAGE_DEVICE_TYPES: Tuple[str, ...] = ('azure_afs', 'azure_workspace', 'onedrive', 'postgres_db')

    def __alarm_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        '''timeout expired'''
        raise TimeoutError('timeout expired waiting for user input')

    def __batch_input_validation(self, batch: dict, find = False) -> None:
        '''assert batch input structure'''

        if batch.get('batchItems') is None:
            raise KeyError('batchItems key is missing')

        if len(batch['batchItems']) == 0:
            raise IndexError('batchItems list is empty')

        for item in batch['batchItems']:
            if find and item.get('pySearchTerm') is None:
                raise KeyError('pySearchTerm key is missing')
            if find is False and item.get('pyModulePath') is None:
                raise KeyError('pyModulePath key is missing')

    def __does_storage_exist(self, type: str, name: Optional[str] = None) -> bool:
        '''does the account have a specific storage type and optionally by name
        
        :param type: str: storage type
        :param name: str: storage name of type, defaults to None 
        '''

        assert(type in self.STORAGE_DEVICE_TYPES)        
        devices = self.account_storage_devices()
        # BUG storage name is not exclusive to type
        # was to allow users to not have to know the type

        if name is None:
            exists = [True for d in devices['storages'] if d['type'] == type]
        else:
            exists = [True for d in devices['storages'] if d['type'] == type and d['name'] == name]

        return True if len(exists) >= 1 else False

    def __input_timed(self, question: str, max_secs: int = 60, pw: bool = False) -> str:
        '''linux only user input prompt with max time in seconds to complete'''
        
        answer: str = ''
        question = f'\n{question.strip()} -> '
        
        if platform == 'linux':
            signal(SIGALRM, self.__alarm_handler)
            alarm(max_secs)
            try:
                answer = getpass(question) if pw else input(question)
            finally:
                alarm(0)
        else:
            answer = getpass(question) if pw else input(question)
        
        return answer

    def __storage_type(self, type: str) -> list:
        '''specific storage type list
        
        :param type: str: storage type
        '''

        assert(type in self.STORAGE_DEVICE_TYPES)        
        resp = self.account_storage_devices()
        devices = [d for d in resp['storages'] if d['type'] == type]
        return devices

    @cached(cache=TTLCache(maxsize=5, ttl=10))
    def _account_jobs(self, max_jobs: int = 100) -> dict:
        '''any user job from any workspace'''
        
        warn('_account_jobs method is experimental', UserWarning, stacklevel=3)
        url = f'{self.api_version}jobs-dashboard/jobs?maxResults={max_jobs}'
        resp = self._fetch_json('get', url)
        return resp
    
    @property
    def _account_jobs_count(self) -> int:
        '''all-time user jobs ran'''
        resp = self._account_jobs(1)
        return resp.get('totalCount', 0)

    def _cache_apikey(self) -> dict:
        '''read auth api from cache'''

        with open(self.file_cache_auth, 'rb') as f:
            cache_auth_pickle: dict = pickle.load(f)
        
        return cache_auth_pickle

    def _cache_apikey_bad(self) -> bool:
        '''check if api cache is incomplete or expired'''

        bad = False
        cache = self._cache_apikey()

        # error on safety refresh before last two minutes
        now_time = datetime.now().timestamp() + 120

        if (cache.get('apikey') is None
            or cache.get('user') is None
            or cache.get('user') != self.auth_username
            or now_time > cache.get('expiration_time', 0)):
                bad = True

        return bad
    
    def _check_apikey_expiration_time(self) -> None:
        '''userpass key is only valid for 1 hour, ensure it is refreshed'''

        key_bad = self._cache_apikey_bad()
        if key_bad:
            self.authenticate_legacy()
        else:
            # if cache has time left on the clock, reuse cached apikey
            cache = self._cache_apikey()
            now_time = datetime.now().timestamp() + 120
            mins_left = round((cache['expiration_time'] - now_time) / 60, 2)
            self.auth_apikey_mins_left = mins_left
            self.auth_apikey = cache['apikey']
            self.auth_apikey_expiry = cache['expiration_time']
            self.auth_req_header.update({'x-api-key': cache['apikey']})

    def _fetch_json(self, method: str, url: str, json: Optional[dict] = None, data = None, extra_headers: Optional[dict] = None) -> dict:
        '''API calls that return a JSON response

        :param method: str: http request methods
        :param url: str: api server endpoint
        :param json: dict: payload in body of post call
        :param data: dictionary or list of tuples or bytes, or file-like object, defaults to None
        :param extra_headers: dict: extend the request headers, defaults to None
        '''

        if self.auth_method_legacy is True:
            self._check_apikey_expiration_time()

        if extra_headers:
            extra_headers.update(self.auth_req_header)
            headers = extra_headers
        else:
            headers = self.auth_req_header

        resp = requests.Response()
        ret: dict = {}
        try:
            resp = requests.request(method, url, headers=headers, json=json, data=data)
            resp.raise_for_status()
            ret = resp.json()
            if self.debug_requests and resp.status_code == 200 and ret.get('result') == 'error':
                print(url, ret)
        except requests.HTTPError as he:
            self.api_crash_count += 1
            if self.debug_requests:
                print(f"\nException: {resp.status_code} {method} {url}\n\nResponse Body Text:\n\n{resp.text}\n\n{he}\n")
            ret = {'crash': True, 'url': url, 'resp': resp, 'response_body': resp.text, 'exception': he}
        except requests.ConnectionError as ce:
            if self._domain != 'https://api.optilogic.app':
                print(f'{self._domain} != https://api.optilogic.app')
                ret = {'crash': True, 'url': url, 'exception': ce}
        except ValueError as ve:
            #JSONDecodeError
            ret = {'crash': True, 'url': url, 'exception': ve, 'text': resp.text}

        return ret

    def _secret_exist(self, name: Optional[str] = None, category: Optional[str] = None, desc: Optional[str] = None) -> bool:
        '''Does secret store contain any matches
        
        TRUE IF
        :no params and secret store is not empty.
        :one param if any param matches.
        :many params will result in an and operation where all must match.

        :param name: str: name of secret, defaults to None
        :param category: str: type of secret such as geocode, ssh, custom, defaults to None
        :param desc: str: substring to match a secret description, defaults to None
        '''

        secret_list: list = self._secret_select_all(name, category, desc)
        return True if len(secret_list) >= 1 else False 
    
    def _secret_select_all(self, name: Optional[str] = None, category: Optional[str] = None, desc: Optional[str] = None) -> list:
        '''Return all secrets that match criteria
        
        RETURNS 
        :no params will return first item in secret store or none if store is empty.
        :one param will return all secrets that match the param.
        :many params will result in an and operation where all must match.

        :param name: str: name of secret, defaults to None
        :param category: str: type of secret such as geocode, ssh, custom, defaults to None
        :param desc: str: substring to match a secret description, defaults to None
        '''

        resp = self.secrets()
        params: int = 0
        params += 1 if name and len(name) > 0 else 0
        params += 1 if category and len(category) > 0 else 0
        params += 1 if desc and len(desc) > 0 else 0
        matches: list = []
        
        if params == 0:
            return resp['secrets'][0] if resp['count'] >= 1 else matches
            
        for s in resp['secrets']:
            n = s['name']
            t = s.get('type')
            d = s.get('description')
            if (params == 3) and (n == name) and (t == category) and (d and d.find(desc) > -1):
                matches.append(s)
            elif (params == 2):
                if (name and category) and (n == name) and (t and t == category):
                    matches.append(s)
                if (name and desc) and (n == name) and (d and desc and d.find(desc) > -1):
                    matches.append(s)
                if (category and desc) and (t and t == category) and (d and d.find(desc) > -1):
                    matches.append(s)
            elif (params == 1):
                if (n == name) or (t and t == category) or (d and desc and d.find(desc) > -1):
                    matches.append(s)
        
        return matches
    
    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def account_info(self) -> dict:
        '''GET v0/account - Get wksp and user information about the account'''

        url = self.api_version + 'account'
        resp = self._fetch_json('get', url)
        return resp

    def account_storage_device(self, type: str, name: Optional[str] = None) -> dict:
        '''get the first storage device by type or with optional name
        
        :param type: str: storage device type
        :param name: str: storage device name, defaults to None
        '''
        
        device: dict = {}
        if self.__does_storage_exist(type, name) is True:
            devices = self.account_storage_devices()
            for d in devices['storages']:
                if d['type'] == type and name is None:
                    device = d
                    break
                elif d['type'] == type and d['name'] == name:
                    device = d
                    break
        
        return device
    
    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def account_storage_devices(self) -> dict:
        '''GET ​/v0​​/storage - Get a list of available storage devices in an account'''

        url = self.api_version + 'storage'
        resp = self._fetch_json('get', url)
        return resp

    def account_workspace_create(self, name: str, stack: str = 'Gurobi') -> dict:
        '''POST /v0​/workspace - Create a new workspace'''

        url = self.api_version + f'workspace?name={name}&stack={stack}'
        resp = self._fetch_json('post', url)
        return resp 

    def account_workspace_delete(self, wksp: str) -> dict:
        '''DELETE /v0​/workspace/runtime - Delete a workspace'''

        raise NotImplementedError
        url = self.api_version + f'{wksp}/runtime'
        resp = self._fetch_json('delete', url)
        return resp 

    @property
    def account_workspace_count(self) -> int:
        '''total number of workspaces'''
        
        resp = self.account_workspaces()
        return resp['count']
    
    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def account_workspaces(self) -> dict:
        '''GET ​/v0​​/workspaces - Get a list of available workspaces in an account'''

        url = self.api_version + 'workspaces'
        resp = self._fetch_json('get', url)
        return resp

    @property
    def api_server_online(self) -> bool:
        '''check if API service is up and running'''
        
        response = requests.request('get', f'{self.api_version}ping')
        return True if response.status_code == 200 else False

    def authenticate_legacy(self) -> None:
        '''POST ​/refreshApiKey - Legacy auth method that will create an Api Key via username and password

        App Key is the preferred auth method for API usage
        https://atlas.optilogic.app/dashboard/#/user-account?tab=appkey
        
        '''

        # do a fetch, process response, then set
        url = self.api_version + 'refreshApiKey'
        headers: dict = {'x-user-id': self.auth_username, 'x-user-password': self.auth_userpass}

        response = requests.request('post', url, headers=headers)
        response.raise_for_status()
        resp = response.json()

        # set instance members
        self.auth_apikey = resp['apiKey']
        self.auth_apikey_expiry = int(resp['expirationTime'])
        self.auth_apikey_mins_left = round((self.auth_apikey_expiry - datetime.now().timestamp()) / 60, 2)
        self.auth_req_header.update({'x-api-key': resp['apiKey']})

        # cache to disk to avoid unnecessary calls to api server
        auth_pickle = {'apikey': self.auth_apikey,
                       'expiration_time': self.auth_apikey_expiry,
                       'user': self.auth_username}
        
        with open(self.file_cache_auth, 'wb') as f:
            pickle.dump(auth_pickle, f)

    def database_create(self, name: str, desc: Optional[str] = None, template='anura_2_5_clean') -> dict:
        '''POST /storage/{database_name} - create a postgres database
        
        :param name: str: name of postgres database to create
        :param desc: str describe the new database use case
        :param template: str
            empty,  
            anura_2_4_clean, 
            anura_2_5_clean,
            anura_2_4_blast_off_to_space,
            anura_2_5_blast_off_to_space
        '''

        assert(template in self.DATABASE_TEMPLATES)
        if self.storagename_database_exists(name):
            raise AssertionError(f'storage of name {name} already exists')
        
        db_count = self.database_count
        emp = True if self.account_info()['email'].find('@optilogic.com') > 0 else False
        if emp and db_count > 85:
            warn(f'{db_count} databases, approaching limit of 100', UserWarning, stacklevel=2)
        # TODO warn per each subscription level limit
        
        d: dict = {'type': 'sql', 'template': template, 'description': desc}
        if desc is None:
            d.pop('description')

        url = f'{self.api_version}storage/{name}'
        resp = self._fetch_json('post', url, json=d)
        return resp
    
    @property
    def database_count(self) -> int:
        ''''quanity of a postgres databases in account'''
        return self.storagetype_count('postgres_db')

    def database_delete(self, name: str) -> dict:
        '''wrapper for storage_delete'''
        return self.storage_delete(name)

    def database_tables(self, name: str) -> dict:
        '''GET /storage/{database_name}/tables - returns list of schemas and tables
        
        :param name: str: postgres database name
        '''

        url = f'{self.api_version}storage/{name}/tables'
        resp = self._fetch_json('get', url)
        return resp

    def database_templates(self) -> dict:
        '''GET /v0/storage-templates - available postgres schemas'''

        url = f'{self.api_version}storage-templates'
        resp = self._fetch_json('get', url)
        return resp

    def ip_address_allow(self, database_name: str, ip: Optional[str] = None ) -> dict:
        '''PUT /v0/storage/{database_name}/ip-in-firewall - an ip address to be whitelisted
        
        :param database_name: str: postgres database name
        :param ip: str: ip address to allow through the firewall, defaults to None

        omitted ip address will use the client's ip address that is making the request
        '''

        exists = self.storagename_database_exists(database_name)
        if exists is False:
            raise AssertionError(f'postgress database {database_name} does not exist')

        url = f'{self.api_version}storage/{database_name}/ip-in-firewall'
        if ip:
            url += f'?ipAddress={ip}'

        time.sleep(1)
        resp = self._fetch_json('put', url)
        return resp

    def ip_address_allowed(self, database_name: str, ip: Optional[str] = None ) -> dict:
        '''GET /v0/storage/{database_name}/ip-in-firewall - is this ip address whitelisted
        
        :param database_name: str: postgres database name
        :param ip: str: ip address to allow through the firewall, defaults to None
        
        omitted ip address will use the client's ip address that is making the request
        '''

        exists = self.storagename_database_exists(database_name)
        if exists is False:
            raise AssertionError(f'postgress database {database_name} does not exist')

        url = f'{self.api_version}storage/{database_name}/ip-in-firewall'
        if ip:
            url += f'?ipAddress={ip}'

        time.sleep(1)
        resp = self._fetch_json('get', url)
        return resp
    
    def onedrive_push(self, path: str) -> dict:
        '''POST /v0​/Studio/onedrive/push - Push Optilogic files to OneDrive
        
        :param path: str: file or subtree path
        '''

        raise NotImplementedError
        url = f'{self.api_version}Studio/onedrive/push?path={path}'
        resp = self._fetch_json('post', url)
        return resp

    def secret(self, name: str) -> dict:
        '''GET /v0/secret - get confidential value'''
        
        url = f'{self.api_version}secret/{name}'
        resp = self._fetch_json('get', url)
        return resp
    
    def secret_add(self, name: str, value: str, category: str = 'custom', desc: Optional[str] = None, meta: Optional[str] = None) -> dict:
        '''POST /v0/secret - set confidential key value
        
        :param name: str: name of secret
        :param value: str: value of secret
        :param type: str: category ie geocode, ssh, custom, defaults to custom
        :param desc: str: description of secret, defaults to None
        :param meta: str: serialized dict of additional custom data, defaults to None
        '''
        
        if category == 'geocode':
            assert(meta)
            meta_dict = loads(meta)
            if isinstance(meta_dict, dict) is False:
                raise TypeError("system secret type geocode expects {'isDefault': False,'provider': 'mapbox'}")
            assert(isinstance(meta_dict.get('isDefault'), bool))
            assert(meta_dict.get('provider'))
            assert(isinstance(meta_dict.get('provider'), str))
            assert(meta_dict.get('provider') in self.GEO_PROVIDERS)

        url = f'{self.api_version}secret/{name}?value={value}&type={category}'
        url += f'&description={desc}' if desc else ''
        url += f'&meta={meta}' if meta else ''        
        resp = self._fetch_json('post', url)
        return resp
        
    def secret_delete(self, name: str) -> dict:
        '''POST /v0/secret - set confidential key value
        
        :param name: str: name of secret
        '''
        
        url = f'{self.api_version}secret/{name}'
        resp = self._fetch_json('delete', url)
        return resp
    
    def secret_update(self, name: str, new_name: Optional[str] =  None, value: Optional[str] =  None, 
                        type: Optional[str] =  None, desc: Optional[str] = None, meta: Optional[str] = None) -> dict:
        '''PUT /v0/secret - update confidential key value
        
        :param name: str: name of secret
        :param new_name: str: change secret name to a new name, defaults to None
        :param value: str: value of secret, defaults to None
        :param type: str: category geocode, ssh, custom, defaults to custom
        :param desc: str: description of secret, defaults to None
        :param meta: str: serialized dict of additional custom data, defaults to None
        '''
        
        url = f'{self.api_version}secret/{name}'
        query = ''
        query += f'&name={new_name}' if new_name else ''
        query += f'&value={value}' if value else ''
        query += f'&type={type}' if type else ''
        query += f'&description={desc}' if desc else ''
        query += f'&meta={meta}' if meta else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('put', url)
        return resp

    def secrets(self, category: Optional[str] = None) -> dict:
        '''GET /v0/secrets - List of confidential key value store
        
        :param type: str: category type ie geocode, ssh, custom, defaults to None
        '''
        
        url = f'{self.api_version}secrets?type={category}' if category else f'{self.api_version}secrets'
        resp = self._fetch_json('get', url)
        return resp

    def storage(self, name: str) -> dict:
        '''GET /v0/storage/{storageName} - storage device info
        
        :param name: str: storage device name
        '''

        url = f'{self.api_version}storage/{name}'
        resp = self._fetch_json('get', url)
        return resp
    
    def storage_delete(self, name: str) -> dict:
        '''DELETE /v0/storage/{storageName}
        
        :param name: str: storage device name
        '''
        
        warn('storage_delete method is experimental', UserWarning, stacklevel=2)
        url = f'{self.api_version}storage/{name}'
        response = requests.delete(url=url, headers=self.auth_req_header)
        response.raise_for_status()
        #TODO currently always returns 200 status code and empty response body
        return {'result': 'success'}

    def storage_disk_create(self, name: str, type: str = 'hdd', size_gb: int = 10) -> dict:
        '''POST /v0/storage/{storageName} - create a new file storage device
        
        :param name: str: name of new file storage device
        :param type: str: hdd or ssd
        :param size_gb: int: storage capacity in gigabytes, defaults to 10
        '''

        raise NotImplementedError
        # TODO check if storagename is already taken
        type = 'transaction-optimized' if type == 'hdd' else 'premium'
        url = f'{self.api_version}storage/{name}?type={type}&size={size_gb}'
        resp = self._fetch_json('post', url)
        return resp
    
    def storagename_onedrive_exists(self, name: str) -> bool:
        '''does the account have OneDrive file storage by name'''
        return self.__does_storage_exist('onedrive', name)
    
    def storagename_wkspfiles_exists(self, name: str) -> bool:
        '''does the account have workspace file storage by name'''
        return self.__does_storage_exist('azure_workspace', name)
    
    def storagename_accountfiles_exists(self, name: str) -> bool:
        '''does the account have account file storage by name'''
        return self.__does_storage_exist('azure_afs', name)
    
    def storagename_database_exists(self, name: str) -> bool:
        '''does the account have postgres database by name'''
        return self.__does_storage_exist('postgres_db', name)
    
    def storagetype_count(self, type: str) -> int:
        '''quanity of a storage type'''
        count: int = len(self.__storage_type(type))
        return count
        
    @property
    def storagetype_accountfiles_exists(self) -> bool:
        '''does the account have account file storage'''
        return self.__does_storage_exist('azure_afs')

    @property
    def storagetype_database_exists(self) -> bool:
        '''does the account have postgres database'''
        return self.__does_storage_exist('postgres_db')

    @property
    def storagetype_onedrive_exists(self) -> bool:
        '''does the account have OneDrive file storage'''
        return self.__does_storage_exist('onedrive')
    
    @property
    def storagetype_wkspfiles_exists(self) -> bool:
        '''does the account have workspace file storage'''
        return self.__does_storage_exist('azure_workspace')
    
    @cached(cache=TTLCache(maxsize=25, ttl=300))
    def sql_connection_info(self, storage_name: str) -> dict:
        '''GET /storage​/{storageName}​/connection-string
        Get the connection information for a SQL storage item
        
        :param storage_name: str: postgres database friendly name
        '''

        assert(self.storagename_database_exists(storage_name)) 
        url = f'{self.api_version}storage/{storage_name}/connection-string'
        resp = self._fetch_json('get', url)
        return resp

    def sql_query(self, database_name: str, query: str) -> dict:
        '''POST ​/v0​/storage/{storagename}​/query-sql - retrieves data from one or more tables
        
        :param database_name: str: postgres database friendly name
        :param query: str: sql statement
        '''
        
        assert(self.storagename_database_exists(database_name))       
        d = {'query': query}
  
        url = f'{self.api_version}storage/{database_name}/query-sql'
        resp = self._fetch_json('post', url, json=d)
        return resp

    def util_job_monitor(self, wksp: str, job_key: str, stop_when: str = 'running', secs_max: int = 120) -> bool:
        '''poll a job for status'
        
        :param wksp: str: workspace where relevant jobs belong to
        :param job_key: str: which job to monitor
        :param stop_when: str: return when job state matches, defaults to running
        :param secs_max: int: hard stop then return when wait time is exhausted, defaults to 100
        
        STOP WHEN STATES
        'submitted','starting','started','running','done','stopping','stopped','canceling','cancelled','error'

        fail-safe stop will occur when job is in a terminal state
        '''

        stop_when = stop_when.lower()
        assert(stop_when in self.JOBSTATES)
        
        time_start = time.time()
        while True:
            time.sleep(5)
            resp = self.wksp_job_status(wksp, job_key)
            time_delta = time.time() - time_start
            if time_delta >= secs_max:
                return False
            elif resp['status'] in self.JOBSTATES_TERMINAL or resp['status'] == stop_when:
                return True

    def wksp_file_copy(self, wksp: str, file_path_src: str, file_path_dest: str, overwrite: bool = False) -> dict:
        '''POST ​/v0​/{workspace}​/file​/copy - Copy a file within a workspace

        :param wksp: str: workspace to download from
        :param file_path_src: str: file to copy from
        :param file_path_dest: str: where to copy to
        :param overwrite: bool: overwrite existing file if exists, defaults to False
        '''

        src_path, src_filename = os.path.split(file_path_src)
        dest_path, dest_filename = os.path.split(file_path_dest)

        # if targetDirectoryPath is not provided, path will be defaulted to src directory
        url = f'{self.api_version }{wksp}/file/copy?sourceDirectoryPath={src_path}&sourceFilename={src_filename}'
        url += f'&targetDirectoryPath={dest_path}&targetFilename={dest_filename}&overwrite={overwrite}'
        resp = self._fetch_json('post', url)
        return resp

    def wksp_file_delete(self, wksp: str, file_path: str) -> dict:
        '''DELETE ​/v0​/{workspace}​/file​/{directoryPath}​/{filename} -Delete a specific file from a workspace

        :param wksp: str: workspace to delete from
        :param file_path: str: file to delete in wksp
        '''

        dir_path, file_name = os.path.split(file_path)
        url = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}'
        resp = self._fetch_json('delete', url)
        return resp

    def wksp_file_download(self, wksp: str, file_path: str) -> str:
        '''GET ​/v0​/{workspace}​/file​/{directoryPath}​/{filename} - Get a file from a specific workspace

        :param wksp: str: workspace to download from
        :param file_path: str: file to download
        '''

        dir_path, file_name = os.path.split(file_path)
        url = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}?op=download'
        response = requests.get(url=url, headers=self.auth_req_header)
        return response.text

    def wksp_file_download_status(self, wksp: str, file_path: str) -> dict:
        '''GET ​/v0​/{workspace}​/file​/{directoryPath}​/{filename} - Get a file metadata

        :param wksp: str: workspace to download from
        :param file_path: str: file to download
        '''

        dir_path, file_name = os.path.split(file_path)
        url = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}?op=status'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_file_upload(self, wksp: str, file_path_dest: str, file_path_local: Optional[str] = None,
                        overwrite: bool = False, filestr: Optional[str] = None) -> dict:
        '''POST ​/v0​/{workspace}​/file​/{directoryPath}​/{filename} - Upload a file to a workspace

        :param wksp: str: workspace to upload to
        :param file_path_dest: str: where to write file on optilogic file storage
        :param file_path_local: str: file to read from on local machine, defaults to None
        :param overwrite: bool: change existing file, defaults to False
        :param filestr: str: alternative file contents, defaults to None
        '''

        dir_path, file_name = os.path.split(file_path_dest)
        url = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}?overwrite={overwrite}'
        data: str = ''
        
        if filestr:
            data = filestr
        elif file_path_local:
            assert os.path.exists(file_path_local)
            with open(file_path_local) as file:
                data = file.read()
        elif filestr is None and file_path_local is None:
            raise ValueError('must provide a file_path_local or filestr')

        headers = {'content-type': 'application/octet-stream',
                   'content-length': f'{len(data)}'}

        if len(data) == 0:
            raise ValueError('file_path_local or filestr cannot be zero length str')
        
        resp = self._fetch_json('post', url, data=data, extra_headers=headers)
        return resp

    def wksp_files(self, wksp: str, filter: Optional[str] = None) -> dict:
        '''GET ​/v0​/{workspace}​/files - List all user files in the workspace
        
        :param wksp: str: where your files live
        :param filter: str: regex str on full file path, defaults to None
        '''

        url = self.api_version + f'{wksp}/files'
        url += f'?filter={filter}' if filter else ''
        resp = self._fetch_json('get', url)
        return resp

    def wksp_folder_delete(self, wksp: str, dir_path: str, force: bool = False) -> dict:
        '''DELETE ​/v0/{workspace}​/folder​/{directoryPath} Delete a folder from a workspace

        :param dir_path: str: folder to delete
        '''

        url = f'{self.api_version}{wksp}/folder/{dir_path}?recursive={str(force).lower()}'
        resp = self._fetch_json('delete', url)
        return resp

    def wksp_info(self, wksp: str) -> dict:
        '''GET ​/v0​/{workspace} - Get information about a workspace

        :param wksp: str: where your files live
        '''

        url = self.api_version + wksp
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_back2back(self, wksp: str, batch: dict, verboseOutput: bool = False, 
                      resourceConfig: Optional[str] = None, tags: Optional[str] = None, timeout: Optional[int] = None) -> dict:
        '''POST /v0/{workspace}/jobBatch/backToBack - Queue one job to run many python modules in a row
        
        :param batch: dict: payload in body of post call
        :param resourceConfig: str: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: str: earmark the job record, defaults to None
        :param timeout: int: max job runtime in secs
        :param verboseOutput: bool: emit python module info to stdout, defaults to False
        :param wksp: str: workspace scope 
        
        INPUT DIRECTIVE
        :batch: dict: payload to send in body of the request
        :batchItems: list: find python modules to execute
        :pyModulePath: str: absolute file path of the python module to execute
        :commandArgs: str: arguments to pass to associated python module
        :timeout: int: max run time of the associated python module
        {"batchItems":[
            {
                "pyModulePath":"/projects/My Models/Transportation/France.py",
                "commandArgs":"diesel",
                "timeout": 100
            }]
        } 
        '''

        self.__batch_input_validation(batch)
        url = f'{self.api_version}{wksp}/jobBatch/backToBack'
        query = ''
        query += '&verboseOutput' if verboseOutput else ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        query += f'&timeout={timeout}' if timeout else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_job_back2back_findnrun(self, wksp: str, batch: dict, verboseOutput: bool = False, 
                      resourceConfig: Optional[str] = None, tags: Optional[str] = None, timeout: Optional[int] = None) -> dict:
        '''POST /v0/{workspace}/jobBatch/backToBack/searchNRun - Run many python modules back to back
        
        :param batch: dict: list of py regex search terms to discover py modules to run
        :param resourceConfig: str: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: str: earmark the job record, defaults to None
        :param timeout: int: max job runtime in secs, defaults to None
        :param verboseOutput: bool: emit python module info to stdout, defaults to False
        :param wksp: str: workspace scope 

        INPUT DIRECTIVE
        :batch: dict: payload to send in body of the request
        :batchItems: list: find python modules to execute
        :pySearchTerm: str: regex search file paths yields python modules to execute
        :commandArgs: str: arguments to pass into matching python modules
        :timeout: int: max run time for matching python modules
        {"batchItems":[
            {"pySearchTerm":"My Models/Transportation", "commandArgs":"", "timeout": 0},
            {"pySearchTerm":"network-\d{3,}", "commandArgs":"", "timeout": 0}
        ]}
        '''

        self.__batch_input_validation(batch, find=True)
        url = f'{self.api_version}{wksp}/jobBatch/backToBack/searchNRun'
        query = ''
        query += '&verboseOutput' if verboseOutput else ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        query += f'&timeout={timeout}' if timeout else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_job_file_error(self, wksp: str, jobkey: str) -> str:
        '''GET ​/v0​/{workspace}​/job​/{jobKey} - Get job error file

        :param wksp: str: workspace where job exists
        :param jobkey: str: unique id
        '''

        url = f'{self.api_version}{wksp}/job/{jobkey}?op=error'
        resp = requests.request('get', url, headers=self.auth_req_header)
        return resp.content.decode('utf-8')

    def wksp_job_file_result(self, wksp: str, jobkey: str) -> str:
        '''GET ​/v0​/{workspace}​/job​/{jobKey} - Get job result file

        :param wksp: str: workspace where job exists
        :param jobkey: str: unique id
        '''

        url = f'{self.api_version }{wksp}/job/{jobkey}?op=result'
        resp = requests.request('get', url, headers=self.auth_req_header)
        return resp.content.decode('utf-8')

    def wksp_job_ledger(self, wksp: str, jobkey: str, keys: Optional[str] = None) -> dict:
        '''GET /{workspace}/job/{jobKey}/ledger - Get records from a specified job
        
        :param wksp: str: workspace scope
        :param jobkey: str: unique id
        :param keys: str: return only ledger records that match csv string, defaults to None
        '''
        
        url = f'{self.api_version}{wksp}/job/{jobkey}/ledger'
        if keys:
            url += f'?keys={keys}'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_metrics(self, wksp: str, jobkey: str) -> dict:
        '''GET /{workspace}/job/{jobKey}/metrics - Get one second cpu and memory sampling of a job
        
        :param wksp: str: workspace scope
        :param jobkey: str: unique id
        '''

        url = f'{self.api_version}{wksp}/job/{jobkey}/metrics'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_metrics_max(self, wksp: str, jobkey: str) -> dict:
        '''GET /{workspace}/job/{jobKey}/metrics/stats - Get peak cpu and memory stats of a job
        
        :param wksp: str: workspace scope
        :param jobkey: str: unique id
        '''

        url = f'{self.api_version}{wksp}/job/{jobkey}/metrics/stats'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_start(self, wksp: str, file_path: str, commandArgs: Optional[str] = None, tags: Optional[str] = None,
                      timeout: Optional[int] = None, resourceConfig: Optional[str] = None) -> dict:
        '''POST ​/v0​/{workspace}​/job - Queue a job to run

        :param wksp: str: workspace scope
        :param file_path: str: python module to run
        :param commandArgs: str: positional args for py module, defaults to None
        :param tags: str: earmark the job record, defaults to None
        :param timeout: int: kill job if still running after duration, defaults to None
        :param resourceConfig: str: mini, 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl defaults to None
        '''
        
        assert(file_path.endswith('.py'))            
        dir_path, file_name = os.path.split(file_path)

        url = f'{self.api_version}{wksp}/job?directoryPath={dir_path}&filename={file_name}'
        url += f'&commandArgs={commandArgs}' if commandArgs else ''
        url += f'&tags={tags}' if tags else ''
        url += f'&timeout={timeout}' if timeout else ''
        url += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        
        now = datetime.utcnow()
        resp = self._fetch_json('post', url)
        self.job_start_recent_key = resp['jobKey']
        resp['apiRequestTime'] = now # burn in the req time the call was initiated
        return resp

    def wksp_job_status(self, wksp: str, jobkey: str) -> dict:
        '''GET ​/v0​/{workspace}​/job​/{jobKey} - Get job status

        :param wksp: str: workspace where job exists
        :param jobkey: str: unique id
        '''

        url = f'{self.api_version}{wksp}/job/{jobkey}?op=status'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_stop(self, wksp: str, jobkey: str) -> dict:
        '''DELETE ​/v0​/{workspace}​/job​/{jobKey} -Stop a queued or running job

        :param wksp: str: workspace where job exists
        :param jobkey: str: unique id
        '''

        url = f'{self.api_version}{wksp}/job/{jobkey}'
        resp = self._fetch_json('delete', url)
        return resp

    def wksp_jobify(self, wksp: str, batch: dict, resourceConfig: Optional[str] = None, tags: Optional[str] = None) -> dict:
        '''POST /v0/{workspace}/jobBatch/jobify - batch queue many jobs

        Will create a job for each python module provided.

        :param batch: dict: list of py modules to run and their config
        :param resourceConfig: str: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: str: earmark the job record, defaults to None
        :param wksp: str: workspace scope 

        INPUT DIRECTIVE
        :batch: dict: payload to send in body of the request
        :batchItems: list: find python modules to execute
        :pyModulePath: str: absolute file path of the python module to execute
        :commandArgs: str: arguments to pass to associated python module
        :timeout: int: max run time of the associated python module
        {"batchItems":[
            {
                "pyModulePath":"/projects/My Models/Transportation/France.py",
                "commandArgs":"diesel",
                "timeout": 100
            }]
        }
        '''

        self.__batch_input_validation(batch)
        url = f'{self.api_version}{wksp}/jobBatch/jobify'
        query = ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_jobify_findnrun(self, wksp: str, batch: dict, resourceConfig: Optional[str] = None, tags: Optional[str] = None) -> dict:
        '''POST /v0/{workspace}/jobBatch/jobify/searchNRun - Batch queue many jobs per search results

        :param batch: dict: list of py regex search terms to discover py modules to run
        :param resourceConfig: str: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: str: earmark the job record, defaults to None
        :param wksp: str: workspace scope

        INPUT DIRECTIVE
        :batch: dict: payload to send in body of the request
        :batchItems: list: find python modules to execute
        :pySearchTerm: str: regex search file paths yields python modules to execute
        :commandArgs: str: arguments to pass into matching python modules
        :timeout: int: max run time for matching python modules
        {"batchItems":[
            {"pySearchTerm":"My Models/Transportation", "commandArgs":"", "timeout": 0},
            {"pySearchTerm":"network-\d{3,}", "commandArgs":"", "timeout": 0}
        ]}
        '''

        self.__batch_input_validation(batch, find=True)
        url = f'{self.api_version}{wksp}/jobBatch/jobify/searchNRun'
        query = ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_jobs(self, wksp: str, command: Optional[str] = None, history: Optional[str] = None, status: Optional[str] = None,
                      runSecsMin: Optional[int] = None, runSecsMax: Optional[str] = None, tags: Optional[str] = None) -> dict:
        '''GET ​/v0​/{workspace}​/jobs - List the jobs for a specific workspace

        :param wksp: str: where your files live

        QUERYSTRING PARAMETERS
        :param command: str: run, presolve, run_custom, run_default, supplychain-3echelon, estimate, accelerate, supplychain-2echelon, defaults to None
        :param history: str: all, or n days ago, defaults to None
        :param runSecsMax: int: maximum runtime in secs, defaults to None
        :param runSecsMin: int: minimum runtime in secs, defaults to None
        :param status: str: done, error, submitted, starting, running, cancelled, stopped, cancelling, stopping, defaults to None
        :param tags: str: filter jobs where csv string matches, defaults to None
        '''

        url = f'{self.api_version}{wksp}/jobs'
        query = ''
        query += f'&command={command}' if command else ''
        query += f'&history={history}' if history else ''
        query += f'&status={status}' if status else ''
        query += f'&tags={runSecsMin}' if runSecsMin else ''
        query += f'&tags={runSecsMax}' if runSecsMax else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('get', url)
        return resp

    def wksp_jobs_stats(self, wksp: str, command: Optional[str] = None, history: Optional[str] = None, status: Optional[str] = None,
                      runSecsMin: Optional[int] = None, runSecsMax: Optional[str] = None, tags: Optional[str] = None) -> dict:
        '''GET ​/v0​/{workspace}​/jobs/stats - Get the stats for jobs for a specific workspace

        :param wksp: str:  where your files live

        QUERYSTRING PARAMETERS
        :param command: str: run, presolve, run_custom, run_default, supplychain-3echelon, estimate, accelerate, supplychain-2echelon, defaults to None
        :param history: str: all, or n days ago, defaults to None
        :param runSecsMax: int: maximum runtime in secs, defaults to None
        :param runSecsMin: int: minimum runtime in secs, defaults to None
        :param status: str: done, error, submitted, starting, running, cancelled, stopped, cancelling, stopping, defaults to None
        :param tags: str: filter jobs where csv string matches, defaults to None
        '''

        url = f'{self.api_version}{wksp}/jobs'
        query = ''
        query += f'&command={command}' if command else ''
        query += f'&history={history}' if history else ''
        query += f'&status={status}' if status else ''
        query += f'&tags={runSecsMin}' if runSecsMin else ''
        query += f'&tags={runSecsMax}' if runSecsMax else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('get', url)
        return resp

    def wksp_share_file(self, wksp: str, file_path: str, targetUsers: str) -> dict:
        '''POST ​/v0​/{workspace}​/file​/share - Share a specific file from a workspace to other users

        :param wksp: str: workspace to copy from
        :param file_path: str: file to share
        :param targetUsers: str: csv string of usernames or email
        '''

        dir_path, file_name = os.path.split(file_path)
        url = f'{self.api_version}{wksp}/file/share?sourceDirectoryPath={dir_path}&sourceFilename={file_name}&targetUsers={targetUsers}'
        resp = self._fetch_json('post', url)
        return resp

    def wksp_share_folder(self, wksp: str, dir_path: str, targetUsers: str, includeHidden: bool = False) -> dict:
        '''POST ​/v0​/{workspace}​/folder/share - Share a specific subtree from a workspace to other users

        :param wksp: str: workspace to copy from
        :param dir_path: str: subtree to share
        :param targetUsers: str: csv list of usernames or email
        :param includeHidden: bool: include hidden files in folder, defaults to False
        '''

        url = f'{self.api_version}{wksp}/folder/share?sourceDirectoryPath={dir_path}&targetUsers={targetUsers}&includeHidden={includeHidden}'
        resp = self._fetch_json('post', url)
        return resp

if __name__ == '__main__':
    api = Api(auth_legacy=False)
    pass # set a breakpoint here
