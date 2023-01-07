from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'weblate-host' in self.get_hosts(host='weblate-host')

    def test_service(self, host):
        assert self.is_service_ok('weblate-host!Weblate')
