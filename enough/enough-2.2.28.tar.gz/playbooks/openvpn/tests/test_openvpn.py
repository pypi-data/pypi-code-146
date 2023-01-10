testinfra_hosts = ['ansible://internal-host']


def test_vpn_route(host):
    cmd = host.run("hostname")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert 'internal-host' in cmd.stdout
