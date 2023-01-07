import json
import logging

testinfra_hosts = ['ansible://infrastructure5-host']
logger = logging.getLogger(__name__)


def test_no_volume(host):
    logger = logging.getLogger(__name__)
    cmd = host.run('lsblk --list --json')
    logger.debug("stdout: %s", cmd.stdout)
    logger.debug("stderr: %s", cmd.stderr)
    blockdevices = json.loads(cmd.stdout)['blockdevices']
    # check that there is only one disk device
    assert 1 == len([disk for disk in blockdevices if disk['type'] == 'disk'])
    # check that there is only one partition (root)
    assert 1 == len([disk for disk in blockdevices
                     if disk['type'] == 'part' and disk['mountpoint'] == '/'])
    assert 0 == cmd.rc
