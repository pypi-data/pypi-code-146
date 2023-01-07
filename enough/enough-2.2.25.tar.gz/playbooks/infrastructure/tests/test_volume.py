import json
import logging

testinfra_hosts = ['ansible://infrastructure4-host']
logger = logging.getLogger(__name__)


def test_volume(host):
    cmd = host.run("""
    set -xe
    ! test -e /dev/mapper/spare
    """)
    logger.debug('stdout %s', cmd.stdout)
    logger.debug('stderr %s', cmd.stderr)
    assert 0 == cmd.rc

    lsblk = host.run('lsblk --tree --json')
    logger.debug('stdout %s', lsblk.stdout)
    logger.debug('stdout %s', lsblk.stderr)
    assert 0 == lsblk.rc
    blockdevices = json.loads(lsblk.stdout)['blockdevices']
    # check that there are two disks and one unused disk
    assert 2 == len([unused for unused in blockdevices if unused['type'] == 'disk'])
    assert 1 == len([unused for unused in blockdevices
                     if not unused.get('children', False) and unused['type'] == 'disk'])
