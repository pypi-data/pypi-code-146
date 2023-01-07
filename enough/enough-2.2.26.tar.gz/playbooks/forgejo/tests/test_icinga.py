from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'forgejo-host' in self.get_hosts(host='forgejo-host')
        assert 'otherforgejo-host' in self.get_hosts(host='otherforgejo-host')

    def test_service(self, host):
        assert self.is_service_ok('forgejo-host!Forgejo')
        assert self.is_service_ok('otherforgejo-host!Forgejo')
