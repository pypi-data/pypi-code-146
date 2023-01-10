testinfra_hosts = ['ansible://website-host']


def test_retirement(host):
    with host.sudo():
        assert host.file("/srv/openvpn/easy-rsa/pki/issued/localhost.crt").exists
        assert not host.file("/srv/openvpn/easy-rsa/pki/issued/retired.crt").exists
