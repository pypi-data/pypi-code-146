import testinfra
from enough.common import retry

testinfra_hosts = ['ansible://weblate-host']


def test_weblate_send_mail(host):

    weblate_host = host
    postfix_host = testinfra.host.Host.get_host(
        'ansible://postfix-host',
        ansible_inventory=host.backend.ansible_inventory)

    with postfix_host.sudo():
        host.run("postsuper -d ALL")

    cmd = weblate_host.run("""
    cd /srv/weblate
    sudo docker-compose -f docker-compose-infrastructure.yml exec -T weblate weblate \
         sendtestemail loic-doomtofail@dachary.org
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc

    @retry.retry(AssertionError, tries=5)
    def wait_for_mail():
        with postfix_host.sudo():
            cmd = postfix_host.run("""
            grep -q doomtofail /var/spool/postfix/hold/*
            """)
        print(cmd.stdout)
        assert cmd.rc == 0, f'{cmd.stdout} {cmd.stderr}'
    wait_for_mail()
