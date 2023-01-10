import pytest
import yaml

testinfra_hosts = ['ansible://debian-host']


def test_libvirt(request, host):
    if request.session.infrastructure.driver != 'libvirt':
        pytest.skip("only when running tests on libvirt")

    variables = yaml.safe_load(open(
        'playbooks/misc/inventory/host_vars/debian-host.yml'))

    cmd = host.run("nproc")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    assert variables['libvirt_cpus'] == int(cmd.stdout.strip())

    with host.sudo():
        cmd = host.run("blockdev --getsize64 /dev/vda")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert variables['libvirt_disk'][-1] == 'G'
        giga = 1024 * 1024 * 1024
        disk = int(variables['libvirt_disk'][:-1]) * giga
        assert disk == int(cmd.stdout.strip())

    with host.sudo():
        cmd = host.run("dmidecode -t 17")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        giga = int(variables['libvirt_ram'] / 1024)
        assert f"Size: {giga} GB" in cmd.stdout
