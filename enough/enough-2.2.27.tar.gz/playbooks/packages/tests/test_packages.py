testinfra_hosts = ['ansible://packages-host']


def test_packages(host):
    cmd = host.run("""
    set -xe

    ! test -f /var/log/update-packages.log.1.gz
    echo >> /var/log/update-packages.log
    sudo /usr/sbin/logrotate --force /etc/logrotate.d/packages-logrotate
    test -f /var/log/update-packages.log.1.gz
    test debian = $(stat --format=%U /var/log/update-packages.log)
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc


def test_displayed_packages(host):
    with host.sudo():
        host.run("apt-get install -y curl")

    assert host.run("curl -s -m 5 https://packages.$(hostname -d)").rc == 0
