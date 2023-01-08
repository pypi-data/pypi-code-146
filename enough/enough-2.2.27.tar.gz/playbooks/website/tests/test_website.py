import website
testinfra_hosts = ['ansible://website-host']


def test_website(host):
    website.update(host)
    with host.sudo():
        cmd = host.run("""
        set -xe

        ! test -f /var/log/update-website.log.1.gz
        /usr/sbin/logrotate --force /etc/logrotate.d/website-logrotate
        test -f /var/log/update-website.log.1.gz
        test debian = $(stat --format=%U /var/log/update-website.log)
        """)
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc

        host.run("apt-get install -y curl")

        assert host.run("curl -m 5 -I https://$(hostname -d)").rc == 0
        assert host.run("curl -m 5 -I https://www.$(hostname -d)").rc == 0
