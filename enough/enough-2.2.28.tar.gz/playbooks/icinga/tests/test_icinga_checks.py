import re

from bs4 import BeautifulSoup
from tests.icinga_helper import IcingaHelper
from enough.common import retry
import requests
import testinfra
import yaml

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_icinga_host(self):
        hosts = self.get_hosts()
        assert 'bind-host' in hosts
        assert 'deleted-host' not in hosts

    def test_icinga_version(self, pytestconfig):
        url = f'{self.get_api_url()}/status/IcingaApplication'
        answer = requests.get(url, **self.connection_params())
        answer.raise_for_status()
        results = answer.json().get('results', [])
        assert len(results) == 1
        version = results[0]['status']['icingaapplication']['app']['version']

        host = testinfra.get_host(f'ansible://{TestChecks.icinga_host}',
                                  ansible_inventory=self.inventory)
        host_vars = host.ansible.get_variables()
        expected_version = host_vars.get('icinga_version')
        if not expected_version:
            icinga2_common_defaults = 'playbooks/icinga/roles/icinga2_common/defaults/main.yml'
            expected_version = yaml.safe_load(open(icinga2_common_defaults))['icinga_version']

        expected_version = expected_version.rsplit('.', 1)[0]
        assert re.search(expected_version, version)

    def test_disk(self):
        assert self.is_service_ok('website-host!disk')
        assert self.is_service_ok('packages-host!disk')

    def test_icinga_ntp_time(self):
        assert self.is_service_ok('website-host!systemd-timesyncd is working')

    def test_memory(self):
        assert self.is_service_ok('icinga-host!memory')
        assert self.is_service_ok('website-host!memory')

    def test_grafana(self, request):
        (s, a) = self.get_web_session(request.session.infrastructure.certs())

        @retry.retry(AssertionError, tries=8)
        def has_image():
            r = s.get(
                f'https://{a}/icingaweb2/monitoring/service/show?host=icinga-host&service=load')
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            module_selector = '.module-grafana'
            assert len(soup.select(module_selector)) > 0, f"select('{module_selector}') not found"
            img_selector = '.grafana-img'
            img = soup.select(img_selector)
            assert len(img) > 0, f"select('{img_selector}') not found"
            img = img[0]
            assert hasattr(img, 'width'), f"select('{img_selector}') not width attribute"
            return True

        assert has_image()
