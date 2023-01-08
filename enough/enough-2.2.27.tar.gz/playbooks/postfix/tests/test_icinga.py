from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'postfix-host' in self.get_hosts(host='postfix-host')

    def test_service(self, host):
        #  r = self.get_client().objects.list('Service', joins=['host.name'])
        with host.sudo():
            host.run("systemctl restart icinga2")
        assert self.is_service_ok('postfix-host!Check smtps TLS certificate')
