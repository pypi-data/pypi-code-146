testinfra_hosts = ['ansible://bind-host', 'ansible://bind-client-host', 'ansible://icinga-host']


def test_sshfp(host):
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run("ssh -v "
                   "-o BatchMode=yes "
                   "-o VerifyHostKeyDNS=yes "
                   f"debian@bind-host.{domain} true || true")
    assert "debug1: matching host key fingerprint found in DNS" in cmd.stderr
