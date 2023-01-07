testinfra_hosts = ['ansible://website-host']


def test_openvpnclient_route(host):
    cmd = host.run("systemctl list-units vpn-route.service")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert 'vpn-route' in cmd.stdout
    cmd = host.run("ip r")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert '10.123.1.0/24 via' in cmd.stdout
