import pytest

testinfra_hosts = ['ansible://bind-host']


def expected_backups(host, count):
    cmd = host.run("""
    export OS_CLIENT_CONFIG_FILE=/usr/lib/backup/clouds.yml
    export OS_CLOUD=production
    openstack ${OS_INSECURE} image list | grep -c pet-host
    """)
    print(cmd.stderr)
    assert count == cmd.stdout.strip()
    assert 0 == cmd.rc


def test_backup(request, host):
    driver = request.session.infrastructure.driver
    if driver != 'openstack':
        pytest.skip("only valid if the driver is openstack, not {driver}")
    # we need --insecure during tests otherwise going back in time a few days
    # may invalidate some certificates and result in errors such as:
    # SSL exception connecting to
    #    https://auth.cloud.ovh.net/v2.0/tokens: [SSL: CERTIFICATE_VERIFY_FAILED]
    with host.sudo():
        cmd = host.run("OS_INSECURE=--insecure /etc/cron.daily/prune-backup 0")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        try:
            host.run("timedatectl set-ntp 0")
            cmd = host.run("""
            set -x
            export OS_INSECURE=--insecure
            date -s '-15 days'
            bash -x /etc/cron.daily/backup
            date -s '-30 days'
            bash -x /etc/cron.daily/backup
            """)
            host.run("timedatectl set-ntp 1")
            print(cmd.stdout)
            print(cmd.stderr)
            assert 0 == cmd.rc
            expected_backups(host, '2')
            host.run("OS_INSECURE=--insecure bash -x /etc/cron.daily/prune-backup 30")
            expected_backups(host, '1')
        finally:
            host.run("timedatectl set-ntp 1")
            host.run("OS_INSECURE=--insecure bash -x /etc/cron.daily/prune-backup 0")
