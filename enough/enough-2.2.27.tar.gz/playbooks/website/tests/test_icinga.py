import website
import testinfra
from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'website-host' in self.get_hosts(host='website-host')

    def test_service(self):
        website.update(testinfra.get_host('ansible://website-host',
                                          ansible_inventory=self.inventory))
        assert self.is_service_ok('website-host!Website')

    def test_proxy_host(self):
        assert 'proxy-host' in self.get_hosts(host='proxy-host')

    def test_proxy_service(self):
        assert self.is_service_ok('proxy-host!Proxy othername.website.test')
        assert self.is_service_ok('proxy-host!Proxy theproxy.website.test')
