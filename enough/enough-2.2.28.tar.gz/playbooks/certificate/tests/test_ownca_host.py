testinfra_hosts = ['ansible://ownca-host']


def test_can_curl_locally(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    assert host.run("curl -m 5 -I https://ownca-host.$(hostname -d)").rc == 0
    assert host.run("grep 'SOMETHING TESTS CAN GREP' /etc/nginx/sites-enabled/*.conf").rc == 0


def test_letsencryptstaging_fails_because_no_ownca_installed(host):
    letsencryptstaging_host = host.get_host('ansible://letsencryptstaging-host',
                                            ansible_inventory=host.backend.ansible_inventory)
    with letsencryptstaging_host.sudo():
        letsencryptstaging_host.run("apt-get install -y curl")
    assert letsencryptstaging_host.run("curl -m 5 -I -k https://ownca-host.$(hostname -d)").rc == 0
    assert letsencryptstaging_host.run("curl -m 5 -I https://ownca-host.$(hostname -d)").rc == 60


def test_client_succeeds_because_ownca_installed(host):
    client_host = host.get_host('ansible://client-host',
                                ansible_inventory=host.backend.ansible_inventory)
    with client_host.sudo():
        client_host.run("apt-get install -y curl")
    assert client_host.run("curl -m 5 -I https://ownca-host.$(hostname -d)").rc == 0
