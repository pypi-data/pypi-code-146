testinfra_hosts = ['ansible://infrastructure1-host']


def test_static_ips_hypervisor(host):
    # see playbooks/hypervisor/inventory/host_vars/hypervisor-host/static_ips.yml
    for i in (1, 2):
        r = host.run(f"ping -W 5 -c 1 10.100.100.1{i}")
        assert r.rc == 0
        assert ', 0% packet loss' in r.stdout
