import testinfra
from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


def update(host):
    with host.sudo():
        cmd = host.run("""
        set -xe
        apt-get install -y curl
        curl -v --location 'http://localhost:5000/api/v1/update' \
                --header 'Content-Type: application/json' \
                --data-raw '{"secret":"mysecret", "branch":"main"}'
        grep --quiet -i Enough /usr/share/nginx/html/index.html
        """)
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc


class TestChecks(IcingaHelper):

    def test_host(self):
        assert 'pages-host' in self.get_hosts(host='pages-host')

    def test_service(self):
        update(testinfra.get_host('ansible://pages-host',
                                  ansible_inventory=self.inventory))
        assert self.is_service_ok('pages-host!Pages')
