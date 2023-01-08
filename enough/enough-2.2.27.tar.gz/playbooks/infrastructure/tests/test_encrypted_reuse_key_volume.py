import logging

testinfra_hosts = ['ansible://infrastructure2-host']
logger = logging.getLogger(__name__)


def test_infrastructure2_encrypted_volume(host):
    cmd = host.run("""
    set -xe
    test -e /dev/mapper/spare
    grep -q /opt /etc/fstab
    test -e /opt/docker/image
    test -e /opt/snap/hello-world
    grep -q snap /etc/fstab
    """)
    logger.debug('stdout %s', cmd.stdout)
    logger.debug('stderr %s', cmd.stderr)
    assert 0 == cmd.rc

    # set by infrastructure/test-encrypted-volume.yml
    with host.sudo():
        host.file("/etc/cryptsetup/keyfile").content == "PASSWORD"
