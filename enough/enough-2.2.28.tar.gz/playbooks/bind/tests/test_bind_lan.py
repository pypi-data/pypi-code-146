testinfra_hosts = ['ansible://bind-host']


def test_bind_lan(host):
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run(f"dig +norec @127.0.0.1 lan.{domain}. NS")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    assert '10.23.10.2' in cmd.stdout.strip()
