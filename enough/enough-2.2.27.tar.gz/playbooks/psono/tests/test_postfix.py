import logging
from enough.common import retry

testinfra_hosts = ['ansible://psono-host']
logger = logging.getLogger(__name__)


def test_psono_send_mail(host):

    with host.sudo():
        host.run("postsuper -d ALL")

    cmd = host.run("""
    cd /srv/psono
    sudo docker-compose run server python3 \
        ./psono/manage.py sendtestemail loic-doomtofail@dachary.org
    """)
    logger.debug('stdout %s', cmd.stdout)
    logger.debug('stderr %s', cmd.stderr)
    assert 0 == cmd.rc

    @retry.retry(AssertionError, tries=5)
    def wait_for_mail():
        with host.sudo():
            cmd = host.run("""
            grep -q doomtofail /var/spool/postfix/hold/*
            """)
        assert cmd.rc == 0, f'{cmd.stdout} {cmd.stderr}'
    wait_for_mail()
