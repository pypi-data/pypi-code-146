testinfra_hosts = ['ansible://icinga-host']


def test_openvpnclient_installed(host):
    cmd = host.run("systemctl list-units --all openvpn*")
    print(cmd.stdout)
    print(cmd.stderr)
    assert cmd.rc == 0
    assert 'client@lan' in cmd.stdout
