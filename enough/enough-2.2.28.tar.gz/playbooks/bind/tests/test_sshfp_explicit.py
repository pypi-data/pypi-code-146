testinfra_hosts = ['ansible://bind-host']


def test_sshfp(host):
    domain = host.run('hostname -d').stdout.strip()
    #
    # expected side effect of
    #
    #     - role: install_ssh_records
    #       vars:
    #         install_ssh_records_host: ns1
    #
    cmd = host.run('dig sshfp +noall +answer @ns1.{domain} ns1.{domain}'.format(
        domain=domain))
    assert cmd.rc == 0
    assert 'SSHFP' in cmd.stdout
    assert 'ns1.' + domain in cmd.stdout
