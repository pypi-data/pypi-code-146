from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'cloud-host' in self.get_hosts(host='cloud-host')

    def test_service(self, host):
        assert self.is_service_ok('cloud-host!cloud-host')
