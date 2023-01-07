import testinfra

from enough.common import retry

testinfra_hosts = ['ansible://forgejo-host']


def test_admin_user(host):
    with host.sudo():
        cmd = host.run("docker exec --user 1000 forgejo gitea admin user list --admin")
        print(cmd.stdout)
        print('--------------------------')
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert "root" in cmd.stdout


def test_send_email(host):
    forgejo_host = host

    postfix_host = testinfra.host.Host.get_host(
        'ansible://postfix-host',
        ansible_inventory=host.backend.ansible_inventory)

    with postfix_host.sudo():
        postfix_host.run("postsuper -d ALL")

    content = "THECONTENT"

    with forgejo_host.sudo():
        command = (
            "docker exec --user 1000 forgejo "
            f"gitea admin sendmail --title TITLE --content '{content}' --force"
        )
        cmd = host.run(command)
        print(cmd.stdout)
        print('--------------------------')
        print(cmd.stderr)
        assert 0 == cmd.rc

    @retry.retry(AssertionError, tries=5)
    def wait_for_mail():
        with postfix_host.sudo():
            cmd = postfix_host.run(f"""
            grep -q {content} /var/spool/postfix/hold/*
            """)
        assert cmd.rc == 0, f'{cmd.stdout} {cmd.stderr}'
    wait_for_mail()
