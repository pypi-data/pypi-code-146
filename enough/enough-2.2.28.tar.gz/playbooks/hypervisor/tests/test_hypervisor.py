testinfra_hosts = ['ansible://hypervisor-host']


def test_hypervisor(host):
    # see playbooks/hypervisor/files/inventory/group_vars/all/libvirt.yml
    r = host.run("ping -W 5 -c 1 10.10.10.65")
    assert r.rc == 0
    assert ', 0% packet loss' in r.stdout
