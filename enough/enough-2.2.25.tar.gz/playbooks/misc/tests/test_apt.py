testinfra_hosts = ['ansible://debian-host']


def test_apt(host):
    with host.sudo():
        cmd = host.run("apt update")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
