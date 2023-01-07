from enough.common import retry
import sh


def test_localhost_vpn_route():
    sh.sudo('apt-get', 'install', '-y', 'openvpn')
    sh.sudo.openvpn('/etc/openvpn/localhost.conf',
                    _cwd='/etc/openvpn', _bg=True, _truncate_exc=False)

    @retry.retry(AssertionError, tries=5)
    def check_route():
        output = sh.ip.route()
        assert '10.30.20' in output

    check_route()
