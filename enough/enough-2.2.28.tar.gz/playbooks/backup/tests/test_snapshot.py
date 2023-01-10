testinfra_hosts = ['ansible://bind-host']


def openstack(host, cmd):
    cmd = host.run(f"""
    docker run --rm -v $HOME/.enough:/root/.enough --entrypoint enough \
       enoughcommunity/enough:latest --domain $(hostname -d) \
       openstack -- {cmd}
    """)
    print(cmd.stderr)
    assert 0 == cmd.rc
    return cmd.stdout


def expected_snapshots(host, count):
    assert count == openstack(
        host, "volume snapshot list -f value -c Name 2>&1 | grep pet-volume | wc -l").strip()


HOST = 'fakepet-host'


def expected_images(host, count):
    assert count == openstack(
        host, f"image list --private -f value -c Name 2>&1 | grep {HOST} | wc -l").strip()


def test_backup(request, host):
    driver = request.session.infrastructure.driver
    if driver == 'openstack':
        expected = expected_snapshots
    elif driver == 'libvirt':
        domain = host.run("hostname -d").stdout.strip()
        with host.sudo():
            cmd = host.run(f"""
            mkdir -p /var/lib/libvirt/images/enough/{domain}
            all=/root/.enough/{domain}/inventory/group_vars/all
            echo 'libvirt_pets: ["{HOST}"]' > $all/libvirt.yml
            docker run --rm \
              -v /var/lib/libvirt/images/enough:/var/lib/libvirt/images/enough \
              --entrypoint qemu-img enoughcommunity/enough:latest \
              create -f qcow2 /var/lib/libvirt/images/enough/{domain}/{HOST}.qcow2 1M
            """)
            print(cmd.stdout)
            print(cmd.stderr)
            assert 0 == cmd.rc
        expected = expected_images

    with host.sudo():
        cmd = host.run("/etc/cron.daily/snapshot")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        expected(host, '1')

        cmd = host.run("/etc/cron.daily/snapshot 0")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        expected(host, '0')
