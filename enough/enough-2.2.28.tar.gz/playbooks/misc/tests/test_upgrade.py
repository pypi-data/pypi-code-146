import sh

from enough.common import retry


testinfra_hosts = ['ansible://debian-host']


def test_upgrade(host):
    with host.sudo():
        reboot = "Unattended-Upgrade::Automatic-Reboot-Time"
        cmd = host.run(f"""
        set -x ; sed -i -e 's/.*{reboot} .*/{reboot} "now";/' \
                 /etc/apt/apt.conf.d/50unattended-upgrades
        """)
        assert 0 == cmd.rc

        cmd = host.run("set -x ; touch /var/run/reboot-required")
        assert 0 == cmd.rc

        before = host.run("uptime --since").stdout.strip()
        print(f'debian-host is up since {before}')

        #
        # It will most likely fail because reboot will interrupt the connection
        #
        try:
            cmd = host.run("unattended-upgrade")
            print(cmd.stdout)
            print(cmd.stderr)
        except RuntimeError:
            pass

        variables = host.ansible.get_variables()
        address = variables['ansible_host']
        private_key_file = variables['ansible_ssh_private_key_file']

        @retry.retry((sh.ErrorReturnCode_255, AssertionError), tries=7)
        def run():
            r = sh.ssh('-oStrictHostKeyChecking=no',
                       '-i', private_key_file, 'debian@' + address,
                       'uptime', '--since')
            after = r.stdout.decode('utf-8').strip()
            assert before < after, f'debian-host did not reboot since {before}'

        run()
