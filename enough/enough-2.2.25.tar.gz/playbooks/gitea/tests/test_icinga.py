from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'gitea-host' in self.get_hosts(host='gitea-host')
        assert 'othergitea-host' in self.get_hosts(host='othergitea-host')

    def test_service(self, host):
        assert self.is_service_ok('gitea-host!Gitea')
        assert self.is_service_ok('othergitea-host!Gitea')
