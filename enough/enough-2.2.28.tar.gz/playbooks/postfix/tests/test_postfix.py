import testinfra

from enough.common import retry

testinfra_hosts = ['ansible://postfix-host']


def test_sendmail(host):
    domain = host.run("hostname -d").stdout.strip()

    postfix_host = host
    with postfix_host.sudo():
        host.run("postsuper -d ALL")

    postfix_client_host = testinfra.host.Host.get_host(
        'ansible://bind-host',
        ansible_inventory=host.backend.ansible_inventory)

    cmd = postfix_client_host.run("""
    ( echo 'To: loic+doomtofail@dachary.org' ; echo POSTFIX TEST ) |
    /usr/sbin/sendmail -v -F 'NO REPLY' -f 'noreply@{}' -t
    """.format(domain))
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc

    @retry.retry(AssertionError, tries=5)
    def wait_for_mail():
        with postfix_host.sudo():
            cmd = host.run("""
            grep -q doomtofail /var/spool/postfix/hold/*
            """)
        assert cmd.rc == 0, f'{cmd.stdout} {cmd.stderr}'
    wait_for_mail()


def test_encryption(host):
    with host.sudo():
        cmd = host.run("""
        set -ex
        postsuper -d ALL
        ( echo Subject: encrypted ; echo ; echo ENCRYPTED CONTENT ) | \
          mail -r debian@localhost debian@localhost
        for d in 0 1 2 4 ; do
           sleep $d
           grep -q 'PGP MESSAGE' /var/spool/postfix/hold/* || continue
           grep -q 'ENCRYPTED CONTENT' /var/spool/postfix/hold/* && exit 1
           ls /var/spool/postfix/hold | while read m ; do
              postcat -q $m | sudo -u zeyple gpg --homedir /var/lib/zeyple/keys --decrypt | \
                grep -q 'ENCRYPTED CONTENT' && echo FOUND && break
           done
        done
        """)
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert 'FOUND' in cmd.stdout

        cmd = host.run("""
        set -ex
        postsuper -d ALL
        ( echo Subject: encrypted ; echo ; echo CLEAR TEXT ) | \
          mail -r debian@localhost debian+notencrypted@localhost
        for d in 0 1 2 4 ; do
           sleep $d
           grep -q 'CLEAR TEXT' /var/spool/postfix/hold/* && echo FOUND && break
        done
        """)
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert 'FOUND' in cmd.stdout
