testinfra_hosts = ['ansible://letsencryptstaging-host']


def test_can_curl_locally(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    assert host.run("curl -m 5 -I https://letsencryptstaging-host.$(hostname -d)").rc == 0
    assert host.run("grep 'SOMETHING TESTS CAN GREP' /etc/nginx/sites-enabled/*.conf").rc == 0


def test_bind_fails_because_no_lestencrypt_staging_ca_installed(host):
    bind_host = host.get_host('ansible://bind-host',
                              ansible_inventory=host.backend.ansible_inventory)
    with bind_host.sudo():
        bind_host.run("apt-get install -y curl")
    assert bind_host.run("curl -m 5 -I -k https://letsencryptstaging-host.$(hostname -d)").rc == 0
    assert bind_host.run("curl -m 5 -I https://letsencryptstaging-host.$(hostname -d)").rc == 60


def test_client_succeeds_because_lestencrypt_staging_ca_installed(host):
    client_host = host.get_host('ansible://client-host',
                                ansible_inventory=host.backend.ansible_inventory)
    with client_host.sudo():
        client_host.run("apt-get install -y curl")
    assert client_host.run("curl -m 5 -I https://letsencryptstaging-host.$(hostname -d)").rc == 0


def test_reverse_can_curl_locally(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    assert host.run("curl -m 5 -I https://reverse.$(hostname -d)").rc == 0


def test_reverse_file_behind_the_reverse_proxy_is_read(host):
    r = host.run("curl -s -m 5 https://reverse.$(hostname -d)/index.html")
    assert r.rc == 0
    assert 'REVERSEPROXY' in r.stdout


def test_reverse_bind_fails_because_no_lestencrypt_staging_ca_installed(host):
    bind_host = host.get_host('ansible://bind-host',
                              ansible_inventory=host.backend.ansible_inventory)
    with bind_host.sudo():
        bind_host.run("apt-get install -y curl")
    assert bind_host.run("curl -m 5 -I -k https://reverse.$(hostname -d)").rc == 0
    assert bind_host.run("curl -m 5 -I https://reverse.$(hostname -d)").rc == 60


def test_reverse_client_succeeds_because_lestencrypt_staging_ca_installed(host):
    client_host = host.get_host('ansible://client-host',
                                ansible_inventory=host.backend.ansible_inventory)
    with client_host.sudo():
        client_host.run("apt-get install -y curl")
    assert client_host.run("curl -m 5 -I https://reverse.$(hostname -d)").rc == 0
