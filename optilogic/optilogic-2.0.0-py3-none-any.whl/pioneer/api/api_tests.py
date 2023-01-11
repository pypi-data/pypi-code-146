'''
This module performs unit tests on the Pioneer REST API

Usage:
  api_tests.py [--authlegacy=<bool>] [--user=<str>] [--pass=<str>] [--appkey=<str>] [--wksp=<str>]
  api_tests.py (-h | --help)

Examples:
  api_tests.py --user=username --pass=secret
  api_tests.py --user=username --appkey=op_guid --wksp=sqa

Options:
  -h, --help
  -a, --authlegacy=<bool>  true for legacy username password method [default: False]
  -u, --user=<str>         API user [default:]
  -p, --pass=<str>         API password [default:]
  -k, --appkey=<str>       non expiring auth key [default:]
  -w, --wksp=<str>         wksp to use [default: Studio]
'''

import api
import os
import time
import unittest
from dateutil.parser import parse
from datetime import datetime
from docopt import docopt
from json import dumps, loads
from typing import Optional
from uuid import uuid4

class TestApi(unittest.TestCase):
    '''A series of Pioneer REST API unit tests

    OVERRIDE   
    docopt configuration passed into the module will override the default static members  

    STATIC MEMBERS  
    USERNAME    required to be issued api key  
    USERPASS    required to be issued api key  
    WORKSPACE   defines what storage account to use for IO operations  
    APPKEY      non expiring authentication key
    AUTH_LEGACY true for legacy username password authentication method
    '''

    USERNAME: Optional[str] = None
    USERPASS: Optional[str] = None
    WORKSPACE: str = 'Studio'
    APPKEY: Optional[str] = None
    AUTH_LEGACY: bool = False

    # method execution order - unittest.TestLoader.sortTestMethodsUsing
    # default string sort of class method names startswith test_{method-name}, ie dir(self)

    @classmethod
    def setUpClass(self):
        '''called before test methods are ran
        ensure cache directories and test data inputs are available in target wksp
        '''

        self.API = api.Api(auth_legacy=TestApi.AUTH_LEGACY, appkey=TestApi.APPKEY, un=TestApi.USERNAME, pw=TestApi.USERPASS)
        self.API.debug_requests = False

        # directory references
        self.dir_local_current = os.path.dirname(__file__)
        self.dir_testdata_local = os.path.join(self.dir_local_current, 'quick_tests')
        assert(os.path.exists(self.dir_testdata_local))
        assert(len(os.listdir(self.dir_testdata_local)) >= 1)
        self.dir_testdata_remote = 'quick_tests'
        self.files_testdata_local = []
        self.files_testdata_remote = []
        self.py_runme = ''
        self.py_runme_quick = ''

        # get all directories from wksp
        resp = self.API.wksp_files(self.WORKSPACE, '/quick_tests/')
        files_remote: list[str] = [f['filePath'] for f in resp['files']]

        # comb over local test data and map to destination file structure
        for f in os.listdir(self.dir_testdata_local):
            local = os.path.join(self.dir_testdata_local, f)
            if os.path.isfile(local) is False:
                continue
            elif os.path.getsize(local) == 0:
                continue
            dest = os.path.join(self.dir_testdata_remote, f)
            self.files_testdata_local.append(local)
            self.files_testdata_remote.append(dest)
            if dest.endswith('sleep.py'):
                self.py_runme = dest
            elif dest.endswith('quick.py'):
                self.py_runme_quick = dest

        # upload local test data to destination
            for idx, local in enumerate(self.files_testdata_local):
                dest = self.files_testdata_remote[idx]
            res = [f for f in files_remote if dest in f]
            if len(res) == 0:
                print(f'uploading {dest}')
                resp = self.API.wksp_file_upload(self.WORKSPACE, file_path_dest=dest, file_path_local=local)

    def test_000_prereqs(self):
        '''first test to ensure job data is available to test against'''

        self.API.wksp_job_start(self.WORKSPACE, self.py_runme_quick, tags='unittest_preseed')
        stime = time.time()
        print('Preseeding by running a new job')
        res = self.API.util_job_monitor(self.WORKSPACE, self.API.job_start_recent_key, stop_when='done', secs_max=300)
        delta = time.time() - stime
        print(f'Job completed {res}, time spent {delta}')
        self.assertLessEqual(delta, 180.0)

    @unittest.skipIf(AUTH_LEGACY is False, 'not applicable to appkey authentication')
    def test_auth_apikey(self):
        '''api key is required for all api calls with legacy authentication'''

        self.assertTrue(self.API.auth_apikey)

    @unittest.skipIf(AUTH_LEGACY is False, 'not applicable to appkey authentication)')
    def test_auth_apikey_expiration(self):
        '''ensure api key is refreshed and not expired'''

        self.assertGreater(self.API.auth_apikey_expiry, datetime.now().timestamp())

    def test_auth_header(self):
        '''request header must have valid apikey or appkey'''

        if self.AUTH_LEGACY:
            self.assertEqual(self.API.auth_req_header['x-api-key'], self.API.auth_apikey)
        else:
            self.assertEqual(self.API.auth_req_header['x-app-key'], self.API.auth_appkey)

    def test_account_info(self):
        '''account properties'''

        resp = self.API.account_info()
        self.assertEqual(resp['result'], 'success')
        if self.API.auth_username:
            self.assertEqual(resp['username'], self.API.auth_username)
        else:
            self.assertIsInstance(resp['username'], str)
        self.assertGreaterEqual(resp['apiConcurrentSolvesMax'], 1)
        self.assertGreaterEqual(resp['workspaceCount'], 1)

    @unittest.skip('api has not implemented')
    def test_account_info_changes(self):
        '''change account properties to see if they auto update'''

        # name, email, username, and rename wksp cannot be changed atm.
        # BUG a new refresh apikey is required to see new wksp created
        raise NotImplementedError

    def test_account_jobs(self):
        ''''any user job from any workspace'''

        job_count: int = 50
        resp = self.API._account_jobs(max_jobs=job_count)
        self.assertIsInstance(resp['jobs'], list)
        self.assertIsInstance(resp['result'], str)
        self.assertIsInstance(resp['subsetCount'], int)
        self.assertIsInstance(resp['totalCount'], int)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['subsetCount'], job_count)
        for job in resp['jobs']:
            self.assertIsInstance(job['canHaveResult'], bool)
            self.assertIsInstance(job['jobInfo'], dict)
            self.assertIsInstance(job['jobInfo']['command'], str)
            if job['jobInfo']['command'] != 'run_custom':
                self.assertIsInstance(job['jobInfo']['directoryPath'], str)
                self.assertIsInstance(job['jobInfo']['filename'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig'], dict)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['cpu'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['name'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['ram'], str)
            self.assertIsInstance(float(job['jobInfo']['resourceConfig']['run_rate']), float) # BUG OE-6710 float or int
            self.assertIsInstance(job['jobInfo']['tags'], str)
            self.assertIsInstance(int(job['jobInfo']['timeout']), int) # BUG OE-6710 str or int
            self.assertIsInstance(job['jobInfo']['workspace'], str)
            self.assertIsInstance(job['jobKey'], str)
            self.assertIsInstance(float(job['runRate']), float) # BUG OE-6710 float or int
            self.assertIsInstance(job['status'], str)
            self.assertIsInstance(job['submittedDatetime'], str)
            self.assertIsInstance(job['submittedTimeStamp'], int)

            if job['status'] in ('done','cancelled','error'):
                self.assertTrue(job['canHaveResult'])
                self.assertIsInstance(job['billedTime'], str)
                self.assertIsInstance(float(job['billedTimeMs']), float) # BUG OE-6710 float or int
                self.assertIsInstance(job['endDatetime'], str)
                self.assertIsInstance(job['endTimeStamp'], int)
                self.assertIsInstance(job['runTime'], str)
                self.assertIsInstance(job['runTimeMs'], int)
                self.assertIsInstance(job['startDatetime'], str)
                self.assertIsInstance(job['startTimeStamp'], int)
            else:
                #self.assertFalse(job['canHaveResult']) # BUG OE-6710 stopped cant have a result
                pass

    def test_account_storage_devices(self):
        '''get a list of available storage devices in an account'''

        resp = self.API.account_storage_devices()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['storages'], list)
        with self.subTest():
            for device in resp['storages']:
                if device['type'] == 'azure_afs':
                    self.assertEqual(len(device), 11)
                    self.assertIsInstance(device['bytesUsed'], int)
                    self.assertIsInstance(device['capacity'], int)
                    self.assertIsInstance(device['created'], int)
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertIsInstance(device['id'], str)
                    self.assertIsInstance(device['internal'], bool)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['tier'], str)
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                if device['type'] == 'azure_workspace':
                    self.assertEqual(len(device), 12)
                    self.assertIsInstance(device['bytesUsed'], int)
                    self.assertIsInstance(device['capacity'], int)
                    self.assertIsInstance(device['created'], int)
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertIsInstance(device['id'], str)
                    self.assertIsInstance(device['internal'], bool)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['tier'], str)
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                    self.assertIsInstance(device['workspaceKey'], str)
                elif device['type'] == 'onedrive':
                    self.assertEqual(len(device), 18)
                    self.assertIsInstance(device['accountName'], str)
                    self.assertIsInstance(device['authenticated'], int)
                    self.assertTrue(device['bytesUsed'] is None or isinstance(device['bytesUsed'], int))
                    self.assertIsInstance(device['capacity'], int)
                    self.assertIsInstance(device['created'], int)
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertIsInstance(device['endpointSuffix'], str)
                    self.assertIsInstance(device['homeAccountId'], str)
                    self.assertIsInstance(device['id'], str)
                    self.assertIsInstance(device['internal'], bool)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['protocol'], str)
                    self.assertIsInstance(device['tier'], str)
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                    self.assertIsInstance(device['username'], str)
                elif device['type'] == 'postgres_db':
                    self.assertEqual(len(device), 16)
                    self.assertTrue(device['bytesUsed'] is None or isinstance(device['bytesUsed'], int))
                    self.assertTrue(device['bytesUsedLastUpdated'] is None or isinstance(device['bytesUsedLastUpdated'], int))
                    self.assertIsInstance(device['created'], int)
                    self.assertIsInstance(device['dbname'], str)
                    self.assertTrue(device['defaultSchema'] is None or isinstance(device['defaultSchema'], str))
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertTrue(device['flywayVersion'] is None or isinstance(device['flywayVersion'], str))
                    self.assertIsInstance(device['host'], str)
                    self.assertIsInstance(device['id'], str)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['port'], int)
                    self.assertIsInstance(device['schemaVersion'], str)
                    self.assertEqual(device['schemaVersion'], 'coming soon')
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                    self.assertIsInstance(device['user'], str)

    def test_account_workspaces(self):
        '''check all worskpaces properties'''

        resp = self.API.account_workspaces()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)

        wksp_exists = False
        for wksp in resp['workspaces']:
            self.assertRegex(wksp['name'], '^[\\w-]+$')
            self.assertEqual(len(wksp['key']), 25)
            self.assertIn(wksp['stack'], ['Optilogic', 'Gurobi'])            
            self.assertIn(wksp['status'], ['STARTING', 'RUNNING', 'STOPPING', 'STOPPED'])
            self.assertRegex(wksp['status'], '\\w{3,}')

            # https://en.wikipedia.org/wiki/ISO_8601
            dt_wksp_creation = parse(wksp['createdon'])
            self.assertGreaterEqual(dt_wksp_creation.year, 2020)

            if wksp['name'] == self.WORKSPACE:
                wksp_exists = True

        self.assertTrue(wksp_exists)

    def test_account_worksapce_count(self):
        '''account info and workspaces both return wksp count'''

        resp = self.API.account_info()
        ws_count: int = self.API.account_workspace_count
        self.assertEqual(resp['workspaceCount'], ws_count)

    @unittest.skip('cant delete a wksp atm')
    def test_account_workspace_create(self):
        '''creating a new workspace'''

        resp = self.API.account_workspace_create('delme')
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['name'], 'delme')
        self.assertEqual(resp['stack'], 'Gurobi')

    def test_account_workspace_create_crash(self):
        '''expected to not create the same workspace twice'''

        resp = self.API.account_workspace_create('Studio')
        self.assertEqual(resp['crash'], True)
        self.assertEqual(resp['exception'].response.status_code, 400)

    @unittest.skip('api has not implemented')
    def test_account_workspace_delete(self):
        '''deleting a newly created workspace'''

        raise NotImplementedError
        resp = self.API.account_workspace_delete('delme')

    def test_api_server_online(self):
        '''check if api service is up and running'''

        self.assertTrue(self.API.api_server_online)

    def test_api_version(self):
        '''only version zero is supported'''

        self.assertTrue(self.API.api_version.endswith('v0/'))

    def test_database_create_delete(self):
        '''create a postgres database then delete'''

        # get the latest version anura_2_n_blast_off_to_space template
        bots = [t for t in self.API.DATABASE_TEMPLATES if t.find('blast') > 0]
        bots = sorted(bots)
        dbname = f'pg_{time.perf_counter_ns}'

        resp = self.API.database_create(dbname, desc=f'unittest {dbname}', template=bots[0])
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['storageId'], str)
        self.assertEqual(len(resp['storageId']), 36)

        resp = self.API.storage_delete(dbname)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')

    def test_database_tables(self):
        '''list of schemas and tables'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.database_tables(db['name'])
        self.assertIsInstance(resp['result'], str)
        for schema in resp['schemas']:
            self.assertIsInstance(schema['name'], str)
            self.assertIsInstance(schema['tables'], int)
            self.assertIsInstance(schema['is_default_schema'], bool)
        self.assertIsInstance(resp['tables'], list)

        if len(resp['tables']) >= 1:
            self.assertIsInstance(resp['tables'][0]['name'], str)
            self.assertIsInstance(resp['tables'][0]['rows'], int)
            self.assertIsInstance(resp['tables'][0]['schema'], str)

    def test_database_templates(self):
        '''empty db or anura schemas'''

        resp = self.API.database_templates()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(resp['count'], 5)
        self.assertIsInstance(resp['templates'], list)
        self.assertEqual(len(resp['templates']), 5)
        for t in resp['templates']:
            #self.assertEqual(t['serverName'], 'default') TODO OE-7040
            self.assertIsInstance(t['role'], str)
            self.assertTrue(t['id'] in self.API.DATABASE_TEMPLATES)
            if t['id'] == 'empty':
                self.assertEqual(t['schema'], '')
            else:
                self.assertTrue(t['name'].startswith('Anura - '))
                self.assertTrue(t['schema'].startswith('anura_2_'))

    def test_ip_address_allow(self):
        '''whitelist ip address'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.ip_address_allow(database_name=db['name'], ip='127.0.0.0')

        self.assertIsInstance(resp['ip'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['ip'], '127.0.0.0')
        self.assertEqual(resp['result'], 'accepted')
        self.assertIn('five-minute delay', resp['message'])

    def test_ip_address_allow_invalid(self):
        '''unable to whitelist, ip address is invalid'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        r = self.API.ip_address_allow(database_name=db['name'], ip='alpha.0.0.0')
        resp = r['resp'].json()
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['message'], 'ipAddress is missing or invalid')

    def test_ip_address_allowed(self):
        '''ip address is whitelisted'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.ip_address_allowed(database_name=db['name'], ip='127.0.0.0')
        self.assertIsInstance(resp['allowed'], bool)
        self.assertIsInstance(resp['ip'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['allowed'], True)
        self.assertEqual(resp['ip'], '127.0.0.0')
        self.assertEqual(resp['result'], 'success')
        self.assertIn('is in the firewall', resp['message'])

    def test_ip_address_allowed_invalid(self):
        '''ip address is invalid'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        db = self.API.account_storage_device(type='postgres_db')
        r = self.API.ip_address_allowed(database_name=db['name'], ip='alpha.0.0.0')
        resp = r['resp'].json()

        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['message'], 'ipAddress is missing or invalid')

    @unittest.skip('OE-7039 API: OneDrive Push Broke')
    def test_onedrive_push(self):
        '''push optilogic files to onedrive'''

        # does account even have onedrive storage?
        onedrive = self.API.storagetype_onedrive_exists
        if onedrive is False:
            self.skipTest('OneDrive device not available')

        # storage device info cached, grab the first onedrive device name
        devices = self.API.account_storage_devices()
        onedrives = [d for d in devices['storages'] if d['type'] == 'onedrive']

        # upload a file to onedrive device
        file_contents = f'{datetime.now()} unittest test_onedrive_push {time.time()}'
        file_path = f"/{onedrives[0]['name']}/unittest.txt"
        self.API.wksp_file_upload('Studio', file_path, overwrite=True, filestr=file_contents)

        # initiate push to onedrive
        resp = self.API.onedrive_push(file_path)
        self.assertEqual(resp['result'], 'success')
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['storageId'], str)
        self.assertIsInstance(resp['storageName'], str)
        self.assertTrue(resp['storageId'], onedrives[0]['id'])
        self.assertTrue(resp['storageName'], onedrives[0]['name'])

    def test_secret_add(self):
        '''create a new secret'''

        nano_secs = str(time.perf_counter_ns())
        n = 'unittest_secret_last_added'
        prereq = self.API.secret(n)
        if prereq.get('crash'):
            self.API.secret_add(n, value=nano_secs, category='unittest')
        else:
            self.API.secret_update(n, value=nano_secs)

        cat = 'geocode'
        desc = f'unittest {nano_secs}'
        for provider in self.API.GEO_PROVIDERS:
            meta_dict: dict = {'isDefault': False, 'provider': provider}
            meta_str = dumps(meta_dict)
            name: str = f'ut_{provider}_{nano_secs}'
            value: str = str(uuid4())
        
            resp = self.API.secret_add(name, value, cat, desc, meta=meta_str)
            self.assertIsInstance(resp['created'], str)
            self.assertIsInstance(resp['description'], str)
            self.assertIsInstance(resp['id'], str)
            self.assertIsInstance(resp['meta'], str)
            self.assertIsInstance(resp['name'], str)
            self.assertIsInstance(resp['result'], str)
            self.assertIsInstance(resp['type'], str)
            self.assertIsInstance(resp['value'], str)
            self.assertEqual(resp['description'], desc)
            self.assertEqual(resp['meta'], meta_str)
            self.assertEqual(resp['name'], name)
            self.assertEqual(resp['result'], 'success')
            self.assertEqual(resp['type'], cat)
            self.assertEqual(resp['value'], value)
            self.assertTrue(resp['created'].endswith('Z'))
            dt = parse(resp['created'])
            self.assertTrue(dt.tzname(), 'UTC')
            now = datetime.utcnow()
            self.assertEqual(dt.year, now.year)
            self.assertEqual(dt.month, now.month)
            self.assertEqual(dt.day, now.day)
        
        self.added_secrets = True

    def test_secret_alter(self):
        '''modify a secret'''

        secrets = self.API._secret_select_all(desc='unittest') # no values returned too sensitive
        sec = None
        sname = None
        for secret in secrets:
            if secret['name'].find('bing') > -1:
                sec = secret
                sname = secret['name']
                break

        secret = self.API.secret(sname)
        newname = 'ut_altered'

        resp = self.API.secret_update(sname, new_name=newname)
        self.assertEqual(resp['created'], sec['created'])
        self.assertEqual(resp['id'], sec['id'])
        self.assertEqual(resp['description'], sec['description'])
        self.assertEqual(resp['meta'], sec['meta'])
        self.assertEqual(resp['name'], newname)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['type'], sec['type'])

        old = self.API.secret(sname)
        self.assertTrue(old['crash'])
        d: dict = loads(old['response_body'])
        self. assertIsInstance(d, dict)
        self.assertEqual(d['result'], 'error')
        self.assertGreater(d['message'].find('no secret found'), -1)
        self.assertEqual(secret['value'], resp['value'])
        
        new = self.API.secret('ut_altered')
        self.assertEqual(resp['id'], new['id'])
        self.assertEqual(resp['name'], newname)

    def test_secrets(self):
        '''check all secrets'''

        resp = self.API.secrets()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['secrets'], list)
        self.assertGreaterEqual(len(resp['secrets']), 1)
        
        for s in resp['secrets']:
            self.assertEqual(len(s['id']), 36)
            self.assertIsInstance(s['created'], str)
            self.assertIsInstance(s['id'], str)
            self.assertIsInstance(s['name'], str)
            
            if s.get('description'):
                self.assertIsInstance(s['description'], str)
            if s.get('meta'):
                self.assertIsInstance(s['meta'], str)
            if s.get('type'):
                self.assertIsInstance(s['type'], str)
            
            dt = parse(s['created'])
            self.assertTrue(dt.tzname(), 'UTC')
            now = datetime.utcnow()
            self.assertEqual(dt.year, now.year)

    def test_secrets_exist(self):
        '''check newly created unittest secrets'''

        prereq = self.API.secret('unittest_secret_last_added')
        if prereq.get('crash'):
            self.skipTest('must first run method test_secret_add')
        nano_secs = prereq['value']

        self.assertFalse(self.API._secret_exist(name='dontexist', category='geocode', desc='unittest'))
        self.assertFalse(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', category='geocode', desc='dontexist'))
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', category='geocode', desc='unittest'))
        
        self.assertFalse(self.API._secret_exist(name='dontexist', category='geocode'))
        self.assertFalse(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', category='dontexist'))
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', category='geocode'))
        
        self.assertFalse(self.API._secret_exist(name='dontexist', desc='unittest'))
        self.assertFalse(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', desc='dontexist'))
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}', desc='unittest'))
        
        self.assertFalse(self.API._secret_exist(category='geocode', desc='dontexist'))
        self.assertTrue(self.API._secret_exist(category='geocode', desc='unittest'))
        
        self.assertFalse(self.API._secret_exist(name='dontexist'))
        self.assertTrue(self.API._secret_exist(name=f'ut_pcmiler_{nano_secs}'))
        
        self.assertFalse(self.API._secret_exist(category='dontexist'))
        self.assertTrue(self.API._secret_exist(category='geocode'))
        
        self.assertFalse(self.API._secret_exist(desc='dontexist'))
        self.assertTrue(self.API._secret_exist(desc='unittest'))

    def test_secrets_remove(self):
        '''remove all unittest secrets'''
        
        secrets = self.API._secret_select_all(desc='unittest')

        for s in secrets:
            resp = self.API.secret_delete(s['name'])
            self.assertEqual(resp['result'], 'success')
            self.assertEqual(resp['id'], s['id'])
            self.assertEqual(resp['name'], s['name'])

    def test_sql_connect_info(self):
        '''get the connecton information for a sql storage item'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have a postgres database')

        pg = self.API.account_storage_device('postgres_db')
        resp = self.API.sql_connection_info(pg['name'])
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['raw']), 6)
        self.assertIsInstance(resp['raw']['host'], str)
        self.assertTrue(resp['raw']['host'].endswith('postgres.database.azure.com'))
        self.assertIsInstance(resp['raw']['dbname'], str)
        self.assertIsInstance(resp['raw']['password'], str)
        self.assertIsInstance(resp['raw']['port'], int)
        self.assertIsInstance(resp['raw']['sslmode'], str)
        self.assertIsInstance(resp['raw']['user'], str)
        self.assertIsInstance(resp['connectionStrings'], dict)
        self.assertEqual(len(resp['connectionStrings']), 5)
        self.assertTrue(resp['connectionStrings']['jdbc'].startswith('jdbc:postgresql://'))
        self.assertTrue(resp['connectionStrings']['libpq'].startswith('host='))
        self.assertTrue(resp['connectionStrings']['net'].startswith('Server='))
        self.assertTrue(resp['connectionStrings']['psql'].startswith('psql \'host='))
        self.assertTrue(resp['connectionStrings']['url'].startswith('postgresql://'))

    def test_storage(self):
        '''storage device info'''

        devices = self.API.account_storage_devices()
        self.assertEqual(devices['result'], 'success')
        with self.subTest():
            for device in devices['storages']:
                device = self.API.storage(device['name'])
                self.assertEqual(device['result'], 'success')
                if device['type'] == 'azure_afs':
                    self.assertEqual(len(device), 12)
                    self.assertIsInstance(device['bytesUsed'], int)
                    self.assertIsInstance(device['capacity'], int)
                    self.assertIsInstance(device['created'], int)
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertIsInstance(device['id'], str)
                    self.assertIsInstance(device['internal'], bool)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['tier'], str)
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                if device['type'] == 'azure_workspace':
                    self.assertEqual(len(device), 13)
                    self.assertIsInstance(device['bytesUsed'], int)
                    self.assertIsInstance(device['capacity'], int)
                    self.assertIsInstance(device['created'], int)
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertIsInstance(device['id'], str)
                    self.assertIsInstance(device['internal'], bool)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['tier'], str)
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                    self.assertIsInstance(device['workspaceKey'], str)
                elif device['type'] == 'onedrive':
                    self.assertEqual(len(device), 20)
                    self.assertIsInstance(device['accountName'], str)
                    self.assertIsInstance(device['authenticated'], int)
                    self.assertTrue(device['bytesUsed'] is None or isinstance(device['bytesUsed'], int))
                    self.assertIsInstance(device['capacity'], int)
                    self.assertIsInstance(device['created'], int)
                    self.assertIsInstance(device['connected'], bool)
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertIsInstance(device['endpointSuffix'], str)
                    self.assertIsInstance(device['homeAccountId'], str)
                    self.assertIsInstance(device['id'], str)
                    self.assertIsInstance(device['internal'], bool)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['protocol'], str)
                    self.assertIsInstance(device['tier'], str)
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                    self.assertIsInstance(device['userId'], str)
                    self.assertIsInstance(device['username'], str)
                elif device['type'] == 'postgres_db':
                    self.assertEqual(len(device), 17)
                    self.assertTrue(device['bytesUsed'] is None or isinstance(device['bytesUsed'], int))
                    self.assertTrue(device['bytesUsedLastUpdated'] is None or isinstance(device['bytesUsedLastUpdated'], int))
                    self.assertIsInstance(device['created'], int)
                    self.assertIsInstance(device['dbname'], str)
                    self.assertTrue(device['defaultSchema'] is None or isinstance(device['defaultSchema'], str))
                    self.assertTrue(device['description'] is None or isinstance(device['description'], str))
                    self.assertTrue(device['flywayVersion'] is None or isinstance(device['flywayVersion'], str))
                    self.assertIsInstance(device['host'], str)
                    self.assertIsInstance(device['id'], str)
                    self.assertTrue(device['lockoutReason'] is None or isinstance(device['lockoutReason'], str))
                    self.assertIsInstance(device['name'], str)
                    self.assertIsInstance(device['port'], int)
                    self.assertIsInstance(device['schemaVersion'], str)
                    self.assertEqual(device['schemaVersion'], 'coming soon')
                    self.assertIsInstance(device['type'], str)
                    self.assertIsInstance(device['updated'], int)
                    self.assertIsInstance(device['user'], str)

    @unittest.skip('api has not implemented')
    def test_storage_disk_create(self):
        '''create a new file storage device'''

        raise NotImplementedError

    @unittest.skip('api is incomplete')
    def test_storage_delete(self):
        '''delete storage device'''

        raise NotImplementedError

    def test_sql_query(self):
        '''test sql statement execution'''

        if self.API.storagetype_database_exists is False:
            self.skipTest('account does not have postgres database')

        pg = self.API.account_storage_device(type='postgres_db')
        resp = self.API.sql_query(database_name=pg['name'], query='SELECT datname FROM pg_database;')
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['rowCount'], int)
        self.assertGreaterEqual(resp['rowCount'], 1)
        self.assertIsInstance(resp['queryResults'], list)
        self.assertGreaterEqual(len(resp['queryResults']), 1)

    def test_wksp_file_copy(self):
        '''make a copy of a file within a workspace'''

        src = self.py_runme
        dest = f'{self.dir_testdata_remote}/cp_test.txt'
        resp = self.API.wksp_file_copy(self.WORKSPACE, file_path_src=src, file_path_dest=dest, overwrite=True)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['copyStatus'], 'success')
        self.assertEqual(resp['message'], 'Copy complete')
        src_result = f"{resp['sourceFileInfo']['directoryPath']}/{resp['sourceFileInfo']['filename']}"
        dest_result = f"{resp['targetFileInfo']['directoryPath']}/{resp['targetFileInfo']['filename']}"
        self.assertEqual(src, src_result)
        self.assertEqual(dest, dest_result)

    def test_wksp_file_delete(self):
        '''delete a copied file with a workspace'''

        f = f'{self.dir_testdata_remote}/cp_test.txt'
        resp = self.API.wksp_file_delete(self.WORKSPACE, file_path=f)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'File deleted')
        file_result = f"{resp['fileInfo']['directoryPath']}/{resp['fileInfo']['filename']}"
        self.assertEqual(f, file_result)

    def test_wksp_file_download(self):
        '''download a file from a given workspace'''

        download = self.API.wksp_file_download(self.WORKSPACE, file_path=self.py_runme)
        self.assertGreaterEqual(len(download), 1)
        self.assertIsInstance(download, str)

    def test_wksp_file_download_crash(self):
        '''download a file from a given workspace'''

        resp = self.API.wksp_file_download(self.WORKSPACE, file_path='I_DONT_EXIST')
        self.assertIsInstance(resp, str)
        r = loads(resp)
        self.assertEqual(r['result'], 'error')
        self.assertIsInstance(r['error'], str)
        self.assertEqual(len(r['correlationId']), 36)

    def test_wksp_file_download_meta(self):
        '''file metadata'''

        resp = self.API.wksp_file_download_status(self.WORKSPACE, file_path=self.py_runme)
        self.assertEqual(resp['result'], 'success')
        keys = ['result', 'workspace', 'filename', 'directoryPath', 'filePath', 'lastModified', 'contentLength', 'date', 'fileCreatedOn', 'fileLastWriteOn', 'fileChangeOn']
        for key in resp.keys():
            self.assertIn(key, keys)
        self.assertEqual(resp['filePath'], self.py_runme)
        self.assertEqual(resp['workspace'], self.WORKSPACE)
        self.assertIsInstance(resp['contentLength'], int)
        dt = parse(resp['lastModified'])
        self.assertEqual(dt.tzname(), 'UTC')

    def test_wksp_file_upload(self):
        '''upload a file to a workspace'''

        dest = f'{self.dir_testdata_remote}/str2file.txt'
        resp = self.API.wksp_file_upload(self.WORKSPACE, file_path_dest=dest, overwrite=True, filestr='test')
        self.assertEqual(resp['result'], 'success')
        self.assertIn(resp['message'], ['File created', 'File replaced'])

    def test_wksp_files(self):
        '''file structure from a given worskpace and must have atleast one file'''

        resp = self.API.wksp_files(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['files'], list)
        self.assertGreaterEqual(len(resp['files']), 1)
        self.assertTrue(resp['files'][0].get('filename'))
        self.assertTrue(resp['files'][0].get('directoryPath'))
        self.assertTrue(resp['files'][0].get('filePath'))
        self.assertTrue(resp['files'][0].get('contentLength'))

    def test_wksp_folder_delete(self):
        '''delete a folder from a workspace'''

        folder = 'delmenow'
        fp = os.path.join(folder, 'delme.txt')
        self.API.wksp_file_upload(self.WORKSPACE, fp, filestr='first file line')
        resp = self.API.wksp_folder_delete(self.WORKSPACE, dir_path=folder, force=True)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Directory and all contents deleted')
        self.assertEqual(resp['directoryPath'], folder)

    def test_wksp_info(self):
        '''properties of a given worskpace'''

        resp = self.API.wksp_info(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['name'], self.WORKSPACE)
        self.assertEqual(len(resp['key']), 25)
        self.assertRegex(resp['key'], '^workspace')
        self.assertIn(resp['stack'], ['Optilogic', 'Simulation', 'Gurobi'])
        self.assertTrue(resp['status'].isupper())

    def test_wksp_job_back2back(self):
        '''one job to run many python modules in a row'''

        item_one: dict = {'pyModulePath': '/projects/quick_tests/sleep.py', 'commandArgs': 'not_used', 'timeout': 90}
        item_two: dict = {'pyModulePath': '/projects/quick_tests/airline_hub_location_cbc.py', 'timeout': 30}
        batch = {'batchItems': [item_one, item_two]}

        tag = 'unittest_batch_back2back'
        resp = self.API.wksp_job_back2back(self.WORKSPACE, batch=batch, verboseOutput=True, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['batch'], dict)
        self.assertEqual(len(resp['batch']), 1)
        
        # batchItems
        self.assertIsInstance(batch['batchItems'], list)
        self.assertEqual(len(batch['batchItems']), 2)
        # item_one
        self.assertIsInstance(resp['batch']['batchItems'][0], list)
        self.assertEqual(len(resp['batch']['batchItems'][0]), 3)
        self.assertEqual(resp['batch']['batchItems'][0][0], item_one['pyModulePath'])
        self.assertEqual(resp['batch']['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(resp['batch']['batchItems'][0][2], item_one['timeout'])
        # item_two
        self.assertIsInstance(resp['batch']['batchItems'][1], list)
        self.assertEqual(len(resp['batch']['batchItems'][1]), 3)
        self.assertEqual(resp['batch']['batchItems'][1][0], item_two['pyModulePath'])
        self.assertIsNone(resp['batch']['batchItems'][1][1])
        self.assertEqual(resp['batch']['batchItems'][1][2], item_two['timeout'])
        
        # jobInfo
        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(len(resp['jobInfo']), 4)
        self.assertEqual(resp['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(resp['jobInfo']['tags'], tag)
        self.assertEqual(resp['jobInfo']['timeout'], -1)
        self.assertIsInstance(resp['jobInfo']['resourceConfig'], dict)
        self.assertEqual(len(resp['jobInfo']['resourceConfig']), 4)
        self.assertEqual(resp['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(resp['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(resp['jobInfo']['resourceConfig']['run_rate'], 2)

        # verify new batch job
        job = self.API.wksp_job_status(self.WORKSPACE, resp['jobKey'])
        self.assertEqual(job['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(job['jobInfo']['directoryPath'], '/usr/bin')
        self.assertEqual(job['jobInfo']['filename'], 'batch_run.py')
        self.assertEqual(job['jobInfo']['command'], 'run')
        self.assertIsInstance(job['jobInfo']['commandArgs'], str)
        args: dict = loads(job['jobInfo']['commandArgs'][1:-1])
        self.assertIsInstance(args, dict)
        self.assertIsInstance(args['batchItems'], list)
        self.assertEqual(args['batchItems'][0][0], item_one['pyModulePath'])
        self.assertEqual(args['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(args['batchItems'][0][2], item_one['timeout'])
        self.assertEqual(args['batchItems'][1][0], item_two['pyModulePath'])
        self.assertEqual(args['batchItems'][1][1], item_two.get('commandArgs'))
        self.assertEqual(args['batchItems'][1][2], item_two['timeout'])
        self.assertEqual(job['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(job['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(job['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(job['jobInfo']['resourceConfig']['run_rate'], 2)

    def test_wksp_job_back2back_findnrun(self):
        '''search file paths yields one job to run many python modules in a row'''

        item_one: dict = {'pySearchTerm': '/projects/quick_tests/sleep.py', 'commandArgs': 'not_used', 'timeout': 90}
        item_two: dict = {'pySearchTerm': '/projects/quick_tests/airline_hub_location_cbc.py', 'timeout': 30}
        batch = {'batchItems': [item_one, item_two]}

        tag = 'unittest_batch_back2back_find'
        resp = self.API.wksp_job_back2back_findnrun(self.WORKSPACE, batch=batch, verboseOutput=True, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['batch'], dict)
        self.assertEqual(len(resp['batch']), 2)
        self.assertTrue(resp['batch']['search'])
        
        # batchItems        
        self.assertIsInstance(batch['batchItems'], list)
        self.assertEqual(len(batch['batchItems']), 2)
        # item_one
        self.assertIsInstance(resp['batch']['batchItems'][0], list)
        self.assertEqual(len(resp['batch']['batchItems'][0]), 3)
        self.assertEqual(resp['batch']['batchItems'][0][0], item_one['pySearchTerm'])
        self.assertEqual(resp['batch']['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(resp['batch']['batchItems'][0][2], item_one['timeout'])
        # item_two
        self.assertIsInstance(resp['batch']['batchItems'][1], list)
        self.assertEqual(len(resp['batch']['batchItems'][1]), 3)
        self.assertEqual(resp['batch']['batchItems'][1][0], item_two['pySearchTerm'])
        self.assertIsNone(resp['batch']['batchItems'][1][1])
        self.assertEqual(resp['batch']['batchItems'][1][2], item_two['timeout'])
        
        # jobInfo
        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(len(resp['jobInfo']), 4)
        self.assertEqual(resp['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(resp['jobInfo']['tags'], tag)
        self.assertEqual(resp['jobInfo']['timeout'], -1)
        self.assertIsInstance(resp['jobInfo']['resourceConfig'], dict)
        self.assertEqual(len(resp['jobInfo']['resourceConfig']), 4)
        self.assertEqual(resp['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(resp['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(resp['jobInfo']['resourceConfig']['run_rate'], 2)

         # verify new batch job
        job = self.API.wksp_job_status(self.WORKSPACE, resp['jobKey'])
        self.assertEqual(job['jobInfo']['workspace'], self.WORKSPACE)
        self.assertEqual(job['jobInfo']['directoryPath'], '/usr/bin')
        self.assertEqual(job['jobInfo']['filename'], 'batch_search_n_run.py')
        self.assertEqual(job['jobInfo']['command'], 'run')
        self.assertIsInstance(job['jobInfo']['commandArgs'], str)
        args: dict = loads(job['jobInfo']['commandArgs'][1:-1])
        self.assertIsInstance(args, dict)
        self.assertIsInstance(args['batchItems'], list)
        self.assertEqual(args['batchItems'][0][0], item_one['pySearchTerm'])
        self.assertEqual(args['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(args['batchItems'][0][2], item_one['timeout'])
        self.assertEqual(args['batchItems'][1][0], item_two['pySearchTerm'])
        self.assertEqual(args['batchItems'][1][1], item_two.get('commandArgs'))
        self.assertEqual(args['batchItems'][1][2], item_two['timeout'])
        self.assertEqual(job['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(job['jobInfo']['resourceConfig']['name'], '3XS')
        self.assertEqual(job['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(job['jobInfo']['resourceConfig']['run_rate'], 2)

    def test_wksp_job_file_error(self):
        '''get job error file'''

        resp = self.API.wksp_job_file_error(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertIsInstance(resp, str)
        if resp.startswith('{\"result\":\"error\"'):
            err = loads(resp)
            self.assertEqual(err['result'], 'error')
            self.assertIsInstance(err['error'], str)
            self.assertIsInstance(err['correlationId'], str)
            self.assertEqual(len(err['correlationId']), 36)
        else:
            self.assertGreater(len(resp), 0)

    def test_wksp_job_file_result(self):
        '''get job result file'''

        resp = self.API.wksp_job_file_result(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertIsInstance(resp, str)
        if resp.startswith('{\"result\":\"error\"'):
            err = loads(resp)
            self.assertEqual(err['result'], 'error')
            self.assertIsInstance(err['error'], str)
            self.assertIsInstance(err['correlationId'], str)
            self.assertEqual(len(err['correlationId']), 36)
        else:
            self.assertGreater(len(resp), 0)

    def test_wksp_job_ledger(self):
        '''get job ledger that has realtime messages'''

        resp = self.API.wksp_job_ledger(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['records'], list)
        self.assertGreaterEqual(len(resp['records']), 1)
        self.assertIsInstance(resp['records'][0]['timestamp'], int)
        self.assertIsInstance(resp['records'][0]['datetime'], str)
        # job was created during init, assert same day
        self.assertTrue(resp['records'][0]['datetime'].endswith('Z'))
        dt = parse(resp['records'][0]['datetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)

    def test_wksp_job_metrics(self):
        '''get one second cpu and memory sampling of a job'''

        resp = self.API.wksp_job_metrics(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['max'], dict)
        self.assertEqual(len(resp['max']), 7)
        self.assertIsInstance(resp['max']['memoryPercent'], float)
        self.assertIsInstance(resp['max']['memoryResident'], float)
        self.assertIsInstance(resp['max']['memoryAvailable'], int)
        self.assertIsInstance(resp['max']['cpuPercent'], float)
        self.assertIsInstance(resp['max']['cpuUsed'], float)
        self.assertIsInstance(resp['max']['cpuAvailable'], int)
        self.assertIsInstance(resp['max']['processCount'], int)
        self.assertIsInstance(resp['records'], list)
        self.assertGreaterEqual(len(resp['records']), 1)
        self.assertIsInstance(resp['records'][0]['timestamp'], int)
        self.assertIsInstance(resp['records'][0]['datetime'], str)
        self.assertTrue(resp['records'][0]['datetime'].endswith('Z'))
        dt = parse(resp['records'][0]['datetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)
        self.assertIsInstance(resp['records'][0], dict)
        self.assertIsInstance(resp['records'][0]['cpuAvailable'], int)
        self.assertIsInstance(resp['records'][0]['cpuPercent'], float)
        self.assertIsInstance(resp['records'][0]['cpuUsed'], float)
        self.assertIsInstance(resp['records'][0]['memoryAvailable'], int)
        self.assertIsInstance(resp['records'][0]['memoryPercent'], float)
        self.assertIsInstance(resp['records'][0]['memoryResident'], float)
        self.assertIsInstance(resp['records'][0]['processCount'], int)

    def test_wksp_job_metrics_max(self):
        ''' get peak cpu and memory stats of a job'''

        resp = self.API.wksp_job_metrics_max(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['max'], dict)
        self.assertEqual(len(resp['max']), 7)
        self.assertIsInstance(resp['max']['memoryPercent'], float)
        self.assertIsInstance(resp['max']['memoryResident'], float)
        self.assertIsInstance(resp['max']['memoryAvailable'], int)
        self.assertIsInstance(resp['max']['cpuPercent'], float)
        self.assertIsInstance(resp['max']['cpuUsed'], float)
        self.assertIsInstance(resp['max']['cpuAvailable'], int)
        self.assertIsInstance(resp['max']['processCount'], int)

    def test_wksp_job_metrics_mia(self):
        '''
        OE-5276 Job Metrics are Missing Sometimes
        OE-5369 Job Metrics Missing v3
        '''

        # spin up a few jobs to create load and evaluate all
        jobs_max = 9
        tag_time = time.time()
        tag = f'metrics_{tag_time}'
        secs = 15
        for job in range(jobs_max):
            self.API.wksp_job_start(self.WORKSPACE, self.py_runme, tags=tag, timeout=secs)

        # check the jobs that are about to run
        d = {}
        check = True
        loops = 0
        while check:
            loops += 1

            jobs = self.API.wksp_jobs(self.WORKSPACE, tags=tag)

            # jobs all finished?
            terminal = 0
            for t in self.API.JOBSTATES_TERMINAL:
                terminal += jobs['statusCounts'].get(t)

            if terminal == jobs_max:
                check = False
                break

            # check running jobs for metrics
            active = self.API.wksp_jobs(self.WORKSPACE, status='running', tags=tag)

            if active['statusCounts']['running'] >= 1:
                for job in active['jobs']:
                    resp = self.API.wksp_job_metrics(self.WORKSPACE, job['jobKey'])
                    self.assertEqual(resp['result'], 'success')
                    self.assertIsInstance(resp['count'], int)
                    with self.subTest():
                        self.assertGreaterEqual(resp['count'], 1)

                    # missing metrics!
                    if resp['count'] == 0:
                        st = str(job['startDatetime'])
                        st = st.replace('T', ' ')
                        st = st.replace('Z', '')
                        job_start = datetime.fromisoformat(st)
                        now = datetime.utcnow()
                        delta = now - job_start
                        d[job['jobKey']] = str(delta) # store jobkey and elapsed time without metrics

                        print(f"{str(delta)} secs elapsed and metrics missing for job {job['jobKey']}")

            time.sleep(1)

        # were there any jobs that failed metric check?
        if len(d) >= 1:
            print(f"\n\nJob Submitted: {jobs_max}, Job Duration: {secs}, Job Tag: {tag}")
            print('\n JobKey, LastSeenWithMissingMetricCount_RunDuration')
            for k in d.items():
                print(k[1], k[0])

    def test_wksp_job_start(self):
        '''creating a job '''

        resp = self.API.wksp_job_start(self.WORKSPACE, file_path=self.py_runme, tags='unittest_start')
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['jobKey']), 36)
        jobinfo_keys = ['workspace', 'directoryPath', 'filename', 'command', 'resourceConfig', 'tags', 'timeout']
        for key in resp['jobInfo'].keys():
            self.assertIn(key, jobinfo_keys)

    def test_wksp_job_status(self):
        '''get job status for explicit state'''

        resp = self.API.wksp_job_status(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['submittedDatetime'], str)
        self.assertTrue(resp['submittedDatetime'].endswith('Z'))
        dt = parse(resp['submittedDatetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)
        self.assertIn(resp['status'], self.API.JOBSTATES)
        jobinfo_keys = ['workspace', 'directoryPath', 'filename', 'command',
                        'errorFile', 'resultFile', 'resourceConfig', 'tags', 'timeout']
        for key in resp['jobInfo'].keys():
            self.assertIn(key, jobinfo_keys)
        self.assertEqual(resp['jobInfo']['command'], 'run')
        self.assertIsInstance(resp['jobInfo']['errorFile'], bool)
        self.assertIsInstance(resp['jobInfo']['resultFile'], bool)
        resource_keys = ['name', 'cpu', 'ram', 'run_rate']
        for key in resp['jobInfo']['resourceConfig']:
            self.assertIn(key, resource_keys)

    def test_wksp_job_stop(self):
        '''stop a most recently created job'''

        resp = self.API.wksp_job_stop(self.WORKSPACE, self.API.job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['jobKey'], self.API.job_start_recent_key)
        keys = ['result', 'message', 'jobKey', 'status', 'jobInfo']
        for key in resp.keys():
            self.assertIn(key, keys)

    def test_wksp_jobify(self):
        '''batch queue many jobs'''

        batch = {'batchItems':
                 [
                     {'pyModulePath': '/projects/quick_tests/sleep.py', 'timeout': 90},
                     {'pyModulePath': '/projects/quick_tests/airline_hub_location_cbc.py', 'timeout': 30}
                 ]}

        tag = 'unittest_batch_jobify'
        resp = self.API.wksp_jobify(self.WORKSPACE, batch=batch, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Jobs submitted')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(resp['count'], len(resp['jobKeys']))
        for key in resp['jobKeys']:
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 36)

    def test_wksp_jobify_findnrun(self):
        '''search file paths yields many jobs to run each python module found'''

        batch = {'batchItems':
                 [
                     {'pySearchTerm': '^/quick_tests/sleep.py', 'timeout': 90},
                     {'pySearchTerm': '^/quick_tests/airline_hub_location_cbc.py', 'timeout': 30},
                 ]}

        tag = 'unittest_batch_jobify_find'
        resp = self.API.wksp_jobify_findnrun(self.WORKSPACE, batch=batch, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Jobs submitted')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(len(batch['batchItems']), resp['count'])
        self.assertEqual(resp['count'], len(resp['jobKeys']))
        for key in resp['jobKeys']:
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 36)

    def test_wksp_jobs(self):
        '''list the jobs for a specific workspace'''

        resp = self.API.wksp_jobs(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['statusCounts'], dict)

        status_keys = ['submitted', 'starting', 'started', 'running',
                       'done', 'stopping', 'stopped', 'canceling', 'cancelled', 'error']
        for status in resp['statusCounts']:
            self.assertIn(status, status_keys)
            self.assertGreaterEqual(resp['statusCounts'][status], 0)

        self.assertIsInstance(resp['tagCounts'], dict)
        self.assertIsInstance(resp['filters'], dict)

        filter_keys = ['command', 'history', 'runSecsMax', 'runSecsMin', 'status', 'tags']
        for filter in resp['filters']:
            self.assertIn(filter, filter_keys)

        self.assertGreaterEqual(len(resp['jobs']), 1)
        job_keys = ['jobKey', 'submittedDatetime', 'startDatetime', 'endDatetime',
                    'runTime', 'runRate', 'billedTime', 'status', 'jobInfo', 'waitTime']
        for job in resp['jobs']:
            for key, value in job.items():
                self.assertIn(key, job_keys)
                if key.lower().find('datetime') > -1 and value:
                    with self.subTest():
                        dt = parse(value)
                        self.assertEqual(dt.tzname(), 'UTC')
                if key == 'jobInfo':
                    if job[key]['command'] == 'run':
                        self.assertIsInstance(job[key]['directoryPath'], str)
                        self.assertIsInstance(job[key]['filename'], str)
                    self.assertIsInstance(job[key]['resourceConfig'], dict)
                    self.assertIsInstance(job[key]['workspace'], str)

    def test_wksp_jobs_stats(self):
        '''get the stats for jobs for a specific workspace'''

        resp = self.API.wksp_jobs(self.WORKSPACE)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['statusCounts'], dict)

        status_keys = ['submitted', 'starting', 'started', 'running',
                       'done', 'stopping', 'stopped', 'canceling', 'cancelled', 'error']
        for status in resp['statusCounts']:
            self.assertIn(status, status_keys)
            self.assertGreaterEqual(resp['statusCounts'][status], 0)

        self.assertIsInstance(resp['tagCounts'], dict)
        self.assertIsInstance(resp['filters'], dict)

        filter_keys = ['command', 'history', 'runSecsMax', 'runSecsMin', 'status', 'tags']
        for filter in resp['filters']:
            self.assertIn(filter, filter_keys)

    def test_wksp_share_file(self):
        '''share a file from a workspace to all other workspaces of a user/self'''

        resp = self.API.wksp_share_file(self.WORKSPACE, file_path=self.py_runme, targetUsers=self.API.auth_username)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Share Accepted')
        f = f"{resp['sourceFileInfo']['directoryPath']}/{resp['sourceFileInfo']['filename']}"
        self.assertEqual(f, self.py_runme)
        self.assertEqual(resp['targetUsers'], self.API.auth_username)

    def test_wksp_share_file_sample(self):
        '''OE-5840 API Share File/Folder Results in 500 Internal Server Error'''

        if self.API.account_workspace_count < 2:
            self.skipTest('account does not have required multi-workspaces needed for sharing')

        test_result = False

        # get all not Studio workspaces
        resp: dict = self.API.account_workspaces()
        wksp_names: list[str] = [w['name'] for w in resp['workspaces'] if w['name'] != 'Studio']
        wksp_not_studio: str = wksp_names[0]

        # upload files to share
        filenames: list[str] = []
        filepaths: list[str] = []
        tag: int = time.perf_counter_ns()
        for x in range(10):
            filename = f'{tag}_{x}.txt'
            file_path = f'/My Files/{tag}/{filename}'
            file_contents = f'{datetime.now()} {tag}_{x} unittest test_wksp_share_file_sample'
            resp = self.API.wksp_file_upload('Studio', file_path, filestr=file_contents)
            if resp.get('crash'):
                print(f'{x} {filename} upload attempt failed')
                continue
            filenames.append(filename)
            filepaths.append(file_path)

        # verify uploaded files arrived
        up_arrived = False
        up_count_verified: int = 0
        up_start: float = time.perf_counter()
        while up_arrived is False and time.perf_counter() - up_start < 30:
            resp = self.API.wksp_files('Studio', str(tag))
            if resp.get('crash'):
                continue

            up_count_verified = resp.get('count', 0)
            print(f'{tag} {up_count_verified}/{len(filepaths)} confirmed files uploaded {time.perf_counter() - up_start} secs')
            if resp.get('count') == len(filepaths):
                up_arrived = True
                break
            time.sleep(2)

        if up_arrived is False:
            print(f'verify upload failed {len(filepaths)} - {up_count_verified} files missing')
            print('30 seconds not enough time to veirfy?')

        # share files to other workspaces
        files_failed_sharing: int = 0
        for fp in filepaths:
            resp = self.API.wksp_share_file('Studio', fp, targetUsers=self.API.auth_username)
            if resp.get('crash'):
                print(f'share crash skipping {fp}')
                files_failed_sharing += 1

        # verify shared files arrived to determine test case can pass
        share_arrived = False
        start_share: float = time.perf_counter()
        # TODO verify file share arrived to all non studio workspaces
        diffs = set()
        while share_arrived is False and time.perf_counter() - start_share < 180:
            resp = self.API.wksp_files(wksp_not_studio, str(tag))
            filenames_verified = {f['filename'] for f in resp['files']}
            diffs = set(filenames).symmetric_difference(filenames_verified)
            if resp.get('count') == up_count_verified and len(diffs) == 0:
                share_arrived = True
                break
            elif resp.get('count', 0) > up_count_verified:
                # BUG there might be file share retry logic
                # 1156398951931738_1.txt failed to share due to 500/504 issue but it showed up 5mins later
                # 1156398951931738_1_2022-10-15T021756Z.txt server tried more than once and created a duplicate!
                break
            time.sleep(2)

        if share_arrived:
            test_result = True
        else:
            print(f'verify share file diff: {len(diffs)}\n{sorted(diffs)}')

        # cleanup: remove files used to share out
        self.API.wksp_folder_delete('Studio', f'My Files/{tag}', force=True)

        # cleanup: remove files shared to other workspaces
        share_folders: list[str] = ['Sent to Me', 'sent_to_me']
        for ws in wksp_names:
            for share_folder in share_folders:
                resp = self.API.wksp_files(ws, share_folder)
                if resp.get('count') == 0:
                    continue
                for fn in filenames:
                    self.API.wksp_file_delete(ws, f'{share_folder}/{self.API.auth_username}/{fn}')

        self.assertTrue(test_result)

    def test_wksp_share_folder(self):
        '''share a subtree from a workspace to all other workspaces of a user/self'''

        resp = self.API.wksp_share_folder(self.WORKSPACE, dir_path=self.dir_testdata_remote, targetUsers=self.API.auth_username)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Share Accepted')
        self.assertEqual(resp['sourceDirectoryPath'], self.dir_testdata_remote)
        self.assertEqual(resp['targetUsers'], self.API.auth_username)
        self.assertEqual(resp['includeHidden'], 'False')

if __name__ == '__main__':
    # !! TODO update module docstring to set your user defautls !!
    # apikey auth works with most calls: replace YOUR_USERNAME, YOUR_PASSWORD
    # appkey auth with with some calls: replace YOUR_USERNAME, YOUR_APPLICATION_KEY and remove authlegacy default True value

    args: dict = docopt(__doc__)
    TestApi.APPKEY = args.get('--appkey')
    TestApi.AUTH_LEGACY = args.get('--authlegacy', '').lower() == 'true'
    TestApi.USERNAME = args.get('--user')
    TestApi.USERPASS = args.get('--pass')
    TestApi.WORKSPACE = args.get('--wksp', 'Studio')
    unittest.main(__name__, argv=['main'])
