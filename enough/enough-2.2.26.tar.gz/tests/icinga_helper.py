from bs4 import BeautifulSoup
from functools import lru_cache
import json
import re
import urllib.parse
from enough.common import retry
from enough.common import ansible_utils
import requests
import urllib3
import yaml
import testinfra

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IcingaHelper(object):

    icinga_host = 'icinga-host'

    # set by ../conftest.py
    @staticmethod
    def set_ansible_inventory(inventory):
        IcingaHelper.inventory = inventory

    @lru_cache(maxsize=1)
    def get_auth(self):
        host = testinfra.get_host(f'ansible://{IcingaHelper.icinga_host}',
                                  ansible_inventory=self.inventory)
        with host.sudo():
            f = host.file("/etc/icinga2/conf.d/api-users.conf")
            return (
                re.search('ApiUser "(.*)"', f.content_string).group(1),
                re.search('password = "(.*)"', f.content_string).group(1)
            )

    def get_web_session(self, certs='certs'):
        p = ansible_utils.Playbook('.', '.', [self.inventory])
        username = list(p.get_role_variables('icinga2', 'icingaweb2_user').values())[0]
        password = list(p.get_role_variables('icinga2', 'icingaweb2_user_pass').values())[0]
        address = self.get_address()
        session = requests.Session()
        session.verify = certs

        r = session.get(f'https://{address}/icingaweb2/authentication/login')
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        CSRFToken = soup.select('#CSRFToken')[0]['value']

        r = session.post(f'https://{address}/icingaweb2/authentication/login',
                         allow_redirects=False,
                         data={'username': username, 'password': password, 'CSRFToken': CSRFToken,
                               'formUID': 'form_login', 'redirect': '', 'btn_submit': 'Login'})
        r.raise_for_status()
        return (session, address)

    @lru_cache(maxsize=1)
    def get_address(self):
        vars_dir = f'{self.inventory}/group_vars/all'
        host = 'icinga.' + yaml.safe_load(
            open(vars_dir + '/domain.yml'))['domain']
        return host

    def get_api_url(self):
        host = self.get_address()
        return f'https://{host}:5665/v1'

    def connection_params(self):
        return dict(
            headers={'Accept': 'application/json'},
            auth=self.get_auth(),
            timeout=5,
            verify=False,
        )

    def get_hosts(self, host=None):
        url = self.get_api_url()
        if host:
            url += f'/objects/hosts/{host}?attrs=name&attrs=state'
        else:
            url += '/objects/hosts?attrs=name&attrs=state'

        answer = requests.get(url, **self.connection_params())
        answer.raise_for_status()
        results = answer.json().get('results', [])
        if host:
            assert len(results) == 1
        return {x['attrs']['name']: x['attrs']['state'] for x in results}

    @retry.retry((AssertionError, requests.exceptions.HTTPError), tries=7)
    def wait_for_service(self, name):
        self.schedule_check(name)

        name = urllib.parse.quote(name)
        url = f'{self.get_api_url()}/objects/services/{name}'
        answer = requests.get(url, **self.connection_params())
        answer.raise_for_status()

        results = answer.json().get('results', [])
        assert len(results) == 1

        attrs = results[0]['attrs']
        assert attrs['last_check'] > 0, f'{name} has not been checked yet'
        state = attrs['state']
        assert int(state) == 0, f"{name}: unexpected state ({state}: " \
            "{results[0]['attrs']})"
        return True

    def schedule_check(self, name):
        """force the check to reduce the waiting time"""
        data = {
            'type': 'Service',
            'filter': f'service.__name=="{name}"',
            'force': True,
        }
        url = f'{self.get_api_url()}/actions/reschedule-check'
        answer = requests.post(url, data=json.dumps(data),
                               **self.connection_params())

        answer.raise_for_status()
        results = answer.json().get('results', [])
        assert len(results) == 1
        assert int(results[0]['code']) == 200

    def is_service_ok(self, name):
        return self.wait_for_service(name)
