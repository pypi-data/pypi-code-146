testinfra_hosts = ['ansible://bind-host']


def test_spf(host):
    with host.sudo():
        host.run("apt-get install -y dnsutils")
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run("dig +short TXT " + domain)
    assert 0 == cmd.rc
    assert "v=spf1" in cmd.stdout.strip()
