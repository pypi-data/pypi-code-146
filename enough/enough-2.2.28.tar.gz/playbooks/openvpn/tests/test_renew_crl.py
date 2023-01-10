testinfra_hosts = ['ansible://website-host']


def test_renew_crl(host):
    with host.sudo():
        cmd = host.run("rm -f /etc/openvpn/crl.pem ; /srv/openvpn/easy-rsa/renew-crl.sh")
        print(cmd.stdout)
        print(cmd.stderr)
        assert cmd.rc == 0
        assert host.file("/etc/openvpn/crl.pem").exists
