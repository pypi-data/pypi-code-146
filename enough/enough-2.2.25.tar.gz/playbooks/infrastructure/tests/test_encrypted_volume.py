import logging

testinfra_hosts = ['ansible://infrastructure1-host']
logger = logging.getLogger(__name__)


def test_encrypted_volume(host):
    cmd = host.run("""
    set -xe
    test -e /dev/mapper/spare
    grep -q /srv /etc/fstab
    test ! -e /srv/docker
    test ! -e /srv/snap
    """)
    logger.debug('stdout %s', cmd.stdout)
    logger.debug('stderr %s', cmd.stderr)
    assert 0 == cmd.rc
