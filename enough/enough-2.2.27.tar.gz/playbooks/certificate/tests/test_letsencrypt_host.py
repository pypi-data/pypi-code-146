testinfra_hosts = ['ansible://bind-host']


def test_can_curl_locally(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    assert host.run("curl -m 5 -I https://bind-host.$(hostname -d)").rc == 0


def test_ownca_can_curl(host):
    ownca_host = host.get_host('ansible://ownca-host',
                               ansible_inventory=host.backend.ansible_inventory)
    with ownca_host.sudo():
        ownca_host.run("apt-get install -y curl")
    assert ownca_host.run("curl -m 5 -I https://bind-host.$(hostname -d)").rc == 0
