from pprint import pprint
import testinfra
import requests
import yaml
from enough.common import ansible_utils
from enough.common import retry

testinfra_hosts = ['ansible://wazuh-host']


class Wazuh(object):

    def __init__(self, config):
        inventory = config.getoption("--ansible-inventory")
        url = self.get_address(inventory)
        p = ansible_utils.Ansible('.', '.', ['playbooks/wazuh/inventory'])
        username = p.get_variable('wazuh_api_username', 'wazuh-host')
        password = p.get_variable('wazuh_api_password', 'wazuh-host')
        self.url = f'https://{url}:55000'
        self.s = requests.session()
        self.s.verify = None
        self.s.headers = {
            'Accept': 'application/json',
        }
        r = self.s.get(f'{self.url}/security/user/authenticate',
                       auth=(username, password))
        print(r.text)
        r.raise_for_status()
        self.s.headers['Authorization'] = f"Bearer {r.json()['data']['token']}"

    def get_info(self):
        r = self.s.get(self.url, params={'pretty': 'true'})
        print(r.text)
        r.raise_for_status()
        return r.json()

    def get_agents(self):
        r = self.s.get(f'{self.url}/agents')
        print(r.text)
        r.raise_for_status()
        return r.json()

    def get_agent_id(self, host):
        agents = self.get_agents()['data']['affected_items']
        for agent in agents:
            if agent['name'].startswith(host):
                return agent['id']
        raise Exception(f'{host} not found in {agents}')

    def get_address(self, inventory):
        vars_dir = f'{inventory}/group_vars/all'
        return 'wazuh.' + yaml.safe_load(
            open(vars_dir + '/domain.yml'))['domain']

    def get_check_times(self, agent):
        r = self.s.get(f'{self.url}/syscheck/{agent}/last_scan')
        print(r.text)
        r.raise_for_status()
        d = r.json()['data']['affected_items'][0]
        return (d['start'], d['end'])

    @retry.retry(AssertionError, tries=8)
    def wait_for_checks(self, agent):
        # start time > end time means the check is ongoing
        (start, end) = self.get_check_times(agent)
        assert start < end

    def get_syscheck_end(self, agent):
        return self.get_check_times(agent)[1]

    def run_syscheck(self, host):
        agent = self.get_agent_id(host)
        last = self.get_syscheck_end(agent)
        r = self.s.put(self.url + '/syscheck', params={'agents_list': agent})
        r.raise_for_status()
        d = r.json()
        pprint(d)
        assert d['error'] == 0

        @retry.retry(AssertionError, tries=8)
        def wait_for_syscheck():
            current_last = self.get_syscheck_end(agent)
            assert current_last is not None, 'syscheck in progress'
            assert current_last > last, f'{current_last} > {last}'
        wait_for_syscheck()

    @retry.retry(AssertionError, tries=8)
    def get_syscheck_md5(self, host, path):
        agent = self.get_agent_id(host)
        r = self.s.get(f'{self.url}/syscheck/{agent}', params={'file': path})
        print(r.text)
        r.raise_for_status()
        r = r.json()
        assert len(r['data']['affected_items']) > 0, f'{r} has no information yet about {path}'
        d = r['data']['affected_items'][0]
        assert d['file'] == path
        return d['md5']


def test_wazuh_api(host, pytestconfig):
    w = Wazuh(pytestconfig)
    info = w.get_info()
    assert info['error'] == 0
    assert info['data']['title'] == "Wazuh API REST"


def test_wazuh_syscheck(host, pytestconfig):
    try:
        w = Wazuh(pytestconfig)
        w.run_syscheck('postfix-host')
        good_md5 = w.get_syscheck_md5('postfix-host', '/etc/issue')
        with host.sudo():
            host.run("""
            postsuper -d ALL
            sed -i -e '/email_alert_level/s/>12</>6</' /var/ossec/etc/ossec.conf
            systemctl restart wazuh-manager
            """)
        # postfix_host is a wazuh agent
        postfix_host = testinfra.host.Host.get_host(
            'ansible://postfix-host',
            ansible_inventory=host.backend.ansible_inventory)

        #
        # modify /etc/issue and verify wazuh sees it
        #
        with postfix_host.sudo():
            postfix_host.run("date +%s >> /etc/issue")
        w.run_syscheck('postfix-host')
        bad_md5 = w.get_syscheck_md5('postfix-host', '/etc/issue')
        assert good_md5 != bad_md5

        #
        # verify a notification is sent regarding this change
        #
        @retry.retry(AssertionError, tries=5)
        def wait_for_mail():
            with host.sudo():
                cmd = host.run("""
                ls /var/spool/postfix/hold
                grep -qw /etc/issue /var/spool/postfix/hold/*
                """)
            print(cmd.stdout)
            assert cmd.rc == 0, f'{cmd.stdout} {cmd.stderr}'
        wait_for_mail()

    finally:
        with host.sudo():
            host.run("""
            sed -i -e '/email_alert_level/s/>.*</>12</' /var/ossec/etc/ossec.conf
            systemctl restart wazuh-manager
            """)


@retry.retry(AssertionError, tries=5)
def test_wazuh_vulnerability_detector(host):
    with host.sudo():
        host.file("/var/ossec/queue/vulnerabilities/cve.db").exists
        host.file("/var/ossec/logs/ossec.log").contains('Finished vulnerability assessment')


def test_wazuh_vulnerability_ignored(host):
    with host.sudo():
        host.run("""
        systemctl stop wazuh-manager
        rm /var/ossec/logs/alerts/alerts.log
        rm /var/ossec/queue/vulnerabilities/cve.db
        apt-get install -y libbsd0=0.9.1-2
        systemctl start wazuh-manager
        """)

        @retry.retry(AssertionError, tries=8)
        def get_alert():
            host.file("/var/ossec/logs/alerts/alerts.log").contains('non-upgradeable packages')
            host.file("/var/ossec/logs/alerts/alerts.log").contains('libbsd0')
        get_alert()
