testinfra_hosts = ['ansible://bind-host']


def test_another(host):
    cmd = host.run("dig +norec @127.0.0.1 another.tld. NS")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    assert '1.2.3.4' in cmd.stdout.strip()
