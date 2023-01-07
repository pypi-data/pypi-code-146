import json
import os
import pytest
import sh
import shutil
import yaml

from enough import settings
from enough.common import Enough
from enough.common.openstack import OpenStack
from enough.common.ssh import SSH

from tests import prepare_config_dir


@pytest.mark.openstack_integration
def test_clone_and_destroy(tmpdir):

    clone_override_dir = f'{tmpdir}/clone-override'
    shutil.copytree('tests/enough/common/test_init/clone-override',
                    clone_override_dir)
    original_domain = 'original.com'

    # TODO: swap the two instructions below once Python 3.8 is used
    # and update copytree parameters:
    # 1. add dirs_exist_ok=True parameter
    # 2. use original_config_dir instead of f'{tmpdir}/{original_domain}
    shutil.copytree('tests/enough/common/test_init/backup',
                    f'{tmpdir}/{original_domain}')
    original_config_dir = prepare_config_dir(original_domain, tmpdir)

    password = 'PASSWORD'
    open(f'{original_config_dir}.pass', 'w').write(password)

    original_all_dir = f'{original_config_dir}/inventory/group_vars/all'
    assert not os.path.exists(f'{original_all_dir}/internal_network.yml')

    original = Enough(original_config_dir, settings.SHARE_DIR,
                      domain=original_domain,
                      driver='openstack')
    assert original.openstack.o.server.list().strip() == ''

    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, 'clone', True)

    assert password == open(f'{clone.config_dir}.pass').read()
    assert 'REPLACED CONTENT' == open(
        f'{clone.config_dir}/inventory/host_vars/to-replace.yml').read().strip()
    assert clone.openstack.o.server.list().strip() == ''
    clone_all_dir = f'{clone.config_dir}/inventory/group_vars/all'
    assert os.path.exists(f'{clone_all_dir}/internal_network.yml')

    assert os.path.exists(clone.config_dir)
    clone.destroy()
    assert not os.path.exists(clone.config_dir)


def create_enough(tmpdir, dotenough, **kwargs):

    enough_domain = 'enough.com'

    # TODO: swap the two instructions below once Python 3.8 is used
    # and update copytree parameters:
    # 1. add dirs_exist_ok=True parameter
    # 2. use config_dir instead of f'{tmpdir}/{enough_domain}
    shutil.copytree(f'tests/enough/common/test_init/{dotenough}',
                    f'{tmpdir}/{enough_domain}')
    config_dir = prepare_config_dir(enough_domain, tmpdir)

    enough = Enough(config_dir, settings.SHARE_DIR,
                    domain=enough_domain,
                    driver='openstack',
                    **kwargs)
    return enough


def test_clone_clobber(tmpdir):
    original = create_enough(tmpdir, 'copy')
    shutil.copyfile('tests/enough/common/test_init/clone-clobber/clouds.yml',
                    f'{original.config_dir}/inventory/group_vars/all/clouds.yml')
    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, 'clone', False)
    assert os.path.exists(f'{clone.config_dir}')
    stone = f'{clone.config_dir}/STONE'
    open(stone, 'w').write('INSIDE')

    assert os.path.exists(stone)
    clone = original.clone(clone_domain, 'clone', False)
    assert os.path.exists(stone)
    clone = original.clone(clone_domain, 'clone', True)
    assert not os.path.exists(stone)


def create_and_clone_server_and_volume(tmpdir):
    original = create_enough(tmpdir, 'backup')
    original.set_args(name='sample', playbook='enough-playbook.yml')
    original.service.create_or_update()

    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, 'clone', True)
    clone.set_args(name='sample', playbook='enough-playbook.yml')
    clone.service.create_or_update()

    return (original, clone)


@pytest.mark.openstack_integration
def test_clone_create_service(tmpdir):
    try:
        (original, clone) = create_and_clone_server_and_volume(tmpdir)
        assert 'sample-host' in original.openstack.o.server.list()
        assert 'sample-volume' in original.openstack.o.volume.list()
        assert 'sample-host' in clone.openstack.o.server.list()
        assert 'sample-volume' in clone.openstack.o.volume.list()
    finally:
        for cloud in ('production', 'clone'):
            o = OpenStack(original.config_dir, cloud=cloud)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_copy_host(tmpdir):
    try:
        enough = create_enough(tmpdir, 'copy')
        if 'copy-volume' not in enough.openstack.o.volume.list():
            enough.openstack.o.volume.create('--size', '1', 'copy-volume')
        ip = enough.create_copy_host('copy-from-host', 'some-volume', 'copy-volume')
        sh.ssh_keygen('-R', ip, _ok_code=(0, 255))
        r = sh.ssh('-oStrictHostKeyChecking=no',
                   '-i', enough.dotenough.private_key(), f'root@{ip}', 'id')
        assert 'uid=0(root)' in r
        r = sh.ssh('-oStrictHostKeyChecking=no',
                   '-i', enough.dotenough.private_key(), f'root@{ip}', 'mountpoint', '/srv').strip()
        assert r == '/srv is a mountpoint'
    finally:
        o = OpenStack(enough.config_dir)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_volume_from_snapshot(tmpdir):
    try:
        e = create_enough(tmpdir, 'backup')
        e.set_args(name='sample', playbook='enough-playbook.yml')
        e.service.create_or_update()
        e.openstack.backup_create(['sample-volume'])
        snapshot = f'{e.openstack.backup_name_create("sample-volume")}'
        assert snapshot in e.openstack.o.volume.snapshot.list()

        volume = 'test-volume'
        e.openstack.create_volume_from_snapshot(snapshot, volume)

        assert volume in e.openstack.o.volume.list()

    finally:
        o = OpenStack(e.config_dir)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_clone_volume_from_snapshot(tmpdir):
    try:
        original = create_enough(tmpdir, 'backup')
        original.set_args(name='sample', playbook='enough-playbook.yml')
        original.service.create_or_update()
        ip = original.hosts.load().get_ip('sample-host')
        sh.ssh_keygen('-R', ip, _ok_code=(0, 255))
        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', original.dotenough.private_key(), f'debian@{ip}', 'touch', '/srv/STONE')
        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', original.dotenough.private_key(), f'debian@{ip}', 'sync')
        original.openstack.backup_create(['sample-volume'])
        snapshot = f'{original.openstack.backup_name_create("sample-volume")}'
        assert snapshot in original.openstack.o.volume.snapshot.list()

        clone_domain = 'clone.com'
        clone = original.clone(clone_domain, 'clone', True)

        (from_ip, to_ip, from_volume, to_volume) = original._clone_volume_from_snapshot_body(
            clone, snapshot)

        sh.ssh_keygen('-R', from_ip, _ok_code=(0, 255))
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', original.dotenough.private_key(), f'root@{from_ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0
        sh.ssh_keygen('-R', to_ip, _ok_code=(0, 255))
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', clone.dotenough.private_key(), f'root@{to_ip}',
                      'test', '!', '-e', '/srv/STONE').exit_code == 0
        original._rsync_copy_host(from_ip, to_ip)
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', clone.dotenough.private_key(), f'root@{to_ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0

        original._clone_volume_from_snapshot_cleanup(clone, from_volume)

    finally:
        for cloud in ('production', 'clone'):
            o = OpenStack(original.config_dir, cloud=cloud)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_service_matching_snapshot(tmpdir):
    try:
        enough = create_enough(tmpdir, 'backup')
        host = enough.create_service_matching_snapshot('2020-02-20-sample-volume')
        assert host == 'sample-host'
        assert 'sample-volume' in enough.openstack.o.volume.list()

    finally:
        o = OpenStack(enough.config_dir)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_restore_remote(tmpdir):
    try:
        original = create_enough(tmpdir, 'backup')
        original.set_args(name='sample', playbook='enough-playbook.yml')
        original.service.create_or_update()
        hosts = original.hosts.load()
        ip = hosts.get_ip('sample-host')
        port = hosts.get_port('sample-host')

        sh.ssh_keygen('-R', ip, _ok_code=(0, 255))
        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', original.dotenough.private_key(), f'-p{port}',
               f'debian@{ip}', 'touch', '/srv/STONE')
        original.openstack.backup_create(['sample-volume'])
        snapshot = f'{original.openstack.backup_name_create("sample-volume")}'
        assert snapshot in original.openstack.o.volume.snapshot.list()

        # original host isn't needed anymore
        original.openstack.o.server.stop('sample-host')
        original.openstack.server_wait_shutoff('sample-host')

        clone = original.restore_remote('test.com', 'clone', True, snapshot)
        assert 'sample-volume' in clone.openstack.o.volume.list()
        clone_hosts = clone.hosts.load()
        clone_ip = clone_hosts.get_ip('sample-host')
        clone_port = clone_hosts.get_port('sample-host')

        assert ip != clone_ip

        SSH.wait_for_ssh(clone_ip, clone_port)
        sh.ssh_keygen('-R', clone_ip, _ok_code=(0, 255))
        res = sh.ssh('-oStrictHostKeyChecking=no',
                     '-i', clone.dotenough.private_key(), f'-p{clone_port}',
                     f'debian@{clone_ip}',
                     'test', '-e', '/srv/STONE')
        assert res.exit_code == 0, f'Unexpected SSH exit code: {res.exit_code}'

    finally:
        for cloud in ('production', 'clone'):
            o = OpenStack(original.config_dir, cloud=cloud)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_restore_local(tmpdir):
    try:
        e = create_enough(tmpdir, 'backup')
        e.set_args(name='sample', playbook='enough-playbook.yml')
        e.service.create_or_update()
        hosts = e.hosts.load()
        ip = hosts.get_ip('sample-host')
        port = hosts.get_port('sample-host')

        sh.ssh_keygen('-R', ip, _ok_code=(0, 255))
        sh.ssh('-oStrictHostKeyChecking=no', '-i', e.dotenough.private_key(),
               f'-p{port}', f'debian@{ip}', 'touch', '/srv/STONE')
        e.openstack.backup_create(['sample-volume'])
        sh.ssh('-oStrictHostKeyChecking=no', '-i', e.dotenough.private_key(),
               f'-p{port}', f'debian@{ip}', 'rm', '/srv/STONE')
        snapshot = f'{e.openstack.backup_name_create("sample-volume")}'
        assert snapshot in e.openstack.o.volume.snapshot.list()

        assert e == e.restore_local(snapshot)
        assert 'sample-volume' in e.openstack.o.volume.list()
        SSH.wait_for_ssh(ip, port)
        sh.ssh_keygen('-R', ip, _ok_code=(0, 255))
        res = sh.ssh('-oStrictHostKeyChecking=no', '-i', e.dotenough.private_key(),
                     f'-p{port}', f'debian@{ip}', 'test', '-e', '/srv/STONE')
        assert res.exit_code == 0, f'Unexpected SSH exit code: {res.exit_code}'

    finally:
        o = OpenStack(e.config_dir)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_missings(tmpdir):
    try:
        enough = create_enough(tmpdir, 'create-missings')
        r = enough.create_missings(['bind-host'])
        assert 'bind-host' in r
        internal_dns = enough.openstack.o.subnet.show(
            '--format=json', '-c', 'dns_nameservers', 'internal')
        internal_dns = json.loads(internal_dns.stdout)
        assert len(internal_dns['dns_nameservers']) == 1
        bind_internal_ip = enough.openstack.server_ip_in_network('bind-host', 'internal')
        assert bind_internal_ip == internal_dns['dns_nameservers'][0]
    finally:
        o = OpenStack(enough.config_dir)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


def test_replace_production(tmpdir):
    target_cloud = 'clone'
    clouds = {
        'clouds': {
            target_cloud: 'CLONE',
            'production': 'PRODUCTION',
        }
    }
    clouds_path = f'{tmpdir}/clouds.yml'
    open(clouds_path, 'w').write(yaml.dump(clouds))
    Enough.replace_production(clouds_path, target_cloud)
    clouds = yaml.safe_load(open(clouds_path))
    assert clouds['clouds']['production'] == 'CLONE'
    assert target_cloud not in clouds['clouds']


def test_volume_from_snapshot():
    volume = 'NAME'
    snapshot = f'2010-07-08-{volume}'
    assert Enough.volume_from_snapshot(snapshot) == volume


def test_host_from_snapshot(tmpdir):
    e = create_enough(tmpdir, 'backup')
    host = 'sample-host'
    snapshot = '2010-07-08-sample-volume'
    assert e.host_from_snapshot(snapshot) == host


@pytest.mark.openstack_integration
def test_volume_resize(tmpdir):
    try:
        enough = create_enough(tmpdir, 'resize')
        enough.set_args(name='sample', playbook='enough-playbook.yml')
        enough.service.create_or_update()
        # False because the size does not change
        assert enough.volume_resize('sample-host', 'sample-volume') is False
        with pytest.raises(Enough.VolumeResizeUndefined):
            enough.volume_resize('other-host', 'other-volume')
        with pytest.raises(Enough.VolumeResizeNoSize):
            enough.volume_resize('nosize-host', 'nosize-volume')
    finally:
        o = OpenStack(enough.config_dir)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.parametrize("service,expected", [
    ('chat', 'chat\thttps://chat.enough.com'),
    ('cloud', 'cloud\thttps://cloud.enough.com nextcloud_admin_user=admin'),
    ('forum', 'forum\thttps://forum.enough.com'),
    ('gitlab', 'gitlab\thttps://lab.enough.com user=root'),
    ('website', 'website\thttps://www.enough.com'),
    ('icinga', 'icinga\thttps://icinga.enough.com icingaweb2_user=icingaadmin'),
    ('jitsi', 'jitsi\thttps://jitsi.enough.com jitsi_startAudioOnly=true'),
    ('openedx', 'openedx\thttps://openedx.enough.com https://studio.enough.com'),
    ('pad', 'pad\thttps://pad.enough.com user=admin'),
    ('psono', 'psono\thttps://psono.enough.com psono_contact=admin@enough.community'),
    ('gitea', 'gitea\thttps://gitea.enough.com gitea_version=1'),
    ('securedrop', 'securedrop\tsecuredrop_admin_user=admin'),
    ('wazuh', 'wazuh\twazuh_mailto=(unknown value)'),
    ('weblate', 'weblate\thttps://weblate.enough.com user=admin'),
    ('wekan', 'wekan\thttps://wekan.enough.com user=admin'),
    ('wordpress', 'wordpress\thttps://wordpress.enough.com wordpress_admin_user=admin'),
])
def test_info_service(tmpdir, service, expected):
    enough_domain = 'enough.com'
    config_dir = prepare_config_dir(enough_domain, tmpdir)
    f = f'{config_dir}/inventory/hosts.yml'
    open(f, 'w').write(yaml.dump({
        'live': {
            'hosts': {
                'some-host': {
                    'ansible_host': '1.2.3.4',
                }
            }
        }
    }))
    f = f'{config_dir}/inventory/services.yml'
    open(f, 'w').write(yaml.dump({
        f'{service}-service-group': {
            'hosts': {
                'some-host': None,
            }
        }
    }))
    e = Enough(config_dir, settings.SHARE_DIR,
               domain=enough_domain,
               driver='openstack')
    info = e.info()
    assert expected in info[1]


def test_info_internal(tmpdir):
    enough_domain = 'enough.com'
    config_dir = prepare_config_dir(enough_domain, tmpdir)
    f = f'{config_dir}/inventory/hosts.yml'
    open(f, 'w').write(yaml.dump({
        'live': {
            'hosts': {
                'some-host': {
                    'ansible_host': '1.2.3.4',
                }
            }
        }
    }))
    f = f'{config_dir}/inventory/services.yml'
    open(f, 'w').write(yaml.dump({
        'bind-service-group': {
            'hosts': {
                'some-host': None,
            }
        }
    }))
    e = Enough(config_dir, settings.SHARE_DIR,
               domain=enough_domain,
               driver='openstack')
    info = e.info()
    assert info[1] == '\tbind\t'


def test_info_general(tmpdir):
    e = create_enough(tmpdir, 'info')
    info = e.info()
    assert info.pop(0) == 'other-host ip=10.20.30.40 port=55'
    assert info.pop(0) == '\tbackup\t'
    assert info.pop(0) == ('\tcloud\thttps://cloud.enough.com '
                           'nextcloud_admin_user=admin '
                           'enough_nextcloud_version=23 '
                           'nextcloud_admin_pass=*****')
    assert info.pop(0) == 'some-host ip=1.2.3.4 port=22'
    assert info.pop(0) == ('\tcloud\thttps://cloud.enough.com '
                           'nextcloud_admin_user=NEXTCLOUD_ADMIN_USER '
                           'enough_nextcloud_version=ENOUGH_NEXTCLOUD_VERSION '
                           'nextcloud_admin_pass=*****')
    assert info.pop(0) == '\tunknown\t(unknown service)'

    e.args['show_passwords'] = True
    info = e.info()
    assert info.pop(0) == 'other-host ip=10.20.30.40 port=55'
    assert info.pop(0) == '\tbackup\t'
    assert info.pop(0) == ('\tcloud\thttps://cloud.enough.com '
                           'nextcloud_admin_user=admin '
                           'enough_nextcloud_version=23 '
                           'nextcloud_admin_pass=mynextcloud')


#
# Host
#
@pytest.mark.openstack_integration
@pytest.mark.libvirt_integration
def test_host_create_or_update(tmpdir, dotenough_fixture):
    enough = Enough(dotenough_fixture.config_dir, settings.SHARE_DIR,
                    domain=dotenough_fixture.domain,
                    driver=dotenough_fixture.driver)
    enough.set_args(name=dotenough_fixture.prefix)
    info = enough.host.create_or_update()
    assert 'ipv4' in info
