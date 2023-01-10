import pytest

testinfra_hosts = ['ansible://external-host']


def test_external_bind(request, host):
    if request.session.infrastructure.driver == 'libvirt':
        pytest.skip("libvirt has no public IP therefore no external host")

    bind_host = host.get_host('ansible://bind-host',
                              ansible_inventory=host.backend.ansible_inventory)
    domain = bind_host.run("hostname -d").stdout.strip()
    address = bind_host.ansible.get_variables()['ansible_host']

    with host.sudo():
        host.run("apt-get install -y dnsutils")

    cmd = host.run(f"dig ns1.{domain}")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc

    cmd = host.run(f"dig axfr {domain} @{address}")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc

    # recursion is prohibited
    cmd = host.run(f"dig fsf.org @{address} | grep -q '^fsf.org'")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 1 == cmd.rc
