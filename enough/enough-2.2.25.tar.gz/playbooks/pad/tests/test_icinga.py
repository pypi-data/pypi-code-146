from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'website-host' in self.get_hosts(host='website-host')

    def test_service(self):
        assert self.is_service_ok('website-host!Pad')
