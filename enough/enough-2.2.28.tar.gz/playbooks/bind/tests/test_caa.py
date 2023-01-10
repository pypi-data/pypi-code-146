testinfra_hosts = ['ansible://bind-client-host']


def test_caa(host):
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run("dig +short CAA " + domain)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    assert '"letsencrypt.org"' in cmd.stdout.strip()
