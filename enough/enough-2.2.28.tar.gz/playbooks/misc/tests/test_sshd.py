testinfra_hosts = ['ansible://debian-host']


def test_ssh(host):
    cmd = host.run("ssh-keyscan debian-host")
    assert 0 == cmd.rc
    assert 'ssh-rsa' in cmd.stdout
    assert 'ssh-ed25519' in cmd.stdout
