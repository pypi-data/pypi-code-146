testinfra_hosts = ['ansible://bind-host']


def test_bind_delegate(host):
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run(f"dig +short A ns1-xxx.{domain}")
    assert 0 == cmd.rc
    ns1_ip = cmd.stdout.strip()
    assert ns1_ip != ""

    cmd = host.run(f"dig +short A otherbind-host.{domain}")
    assert 0 == cmd.rc
    otherbind_ip = cmd.stdout.strip()

    assert ns1_ip == otherbind_ip

    cmd = host.run(f"dig +short NS xxx.{domain}")
    assert 0 == cmd.rc
    assert f'ns1.xxx.{domain}.' == cmd.stdout.strip()
