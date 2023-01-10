import datetime
import os
import sh
import time

import pytest
import requests_mock as requests_mock_module

from tests.modified_environ import modified_environ

from enough import settings
from enough.common import openstack
from enough.common.openstack import Stack, Heat, OpenStack


#
# Stack
#
@pytest.mark.openstack_integration
def test_stack_create_or_update(openstack_name, openstack_variables,
                                dot_openstack):
    name = openstack_name
    network = openstack_name
    class_c = '10.101.30'
    cidr = f'{class_c}.0/24'
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    d.update(
        internal_network=network,
        internal_network_cidr=cidr
    )
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    r = s.create_or_update()
    assert r['port'] == '22'
    ipv4 = r['ipv4']
    o = OpenStack(settings.CONFIG_DIR)
    assert o.server_connected_to_network(name, network)
    assert r == s.create_or_update()
    assert o.server_connected_to_network(name, network)
    assert r['ipv4'] == ipv4
    s.delete()
    assert not o.network_exists(network)


#
# Heat
#
def test_heat_definition():
    h = Heat(settings.CONFIG_DIR)
    definitions = h.get_stack_definitions()
    assert 'bind-host' in definitions
    definition = h.get_stack_definition('bind-host')
    assert definition['name'] == 'bind-host'
    assert h.get_stack_definition('unknown') is None


def test_host_from_volume():
    h = Heat(settings.CONFIG_DIR)
    assert h.host_from_volume('cloud-volume') == 'cloud-host'
    assert h.host_from_volume('unknown-volume') is None


def test_heat_definition_encrypted():
    d = 'tests/enough/common/test_openstack/config_dir'
    h = Heat(d)
    definitions = h.get_stack_definitions(share_dir=d)
    assert 'my-host' in definitions
    assert definitions['my-host']['myvariable'] == 'myvalue'


def test_create_test_subdomain_no_bind(mocker):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('enough.common.openstack.Stack.list', return_value=[])
    h = Heat(settings.CONFIG_DIR)
    assert h.create_test_subdomain('my.tld') is None


def test_create_test_subdomain_with_bind(tmpdir, mocker, requests_mock):
    mocker.patch('enough.settings.CONFIG_DIR', str(tmpdir))
    d = f'{tmpdir}/inventory/group_vars/all'
    os.makedirs(d)
    assert not os.path.exists(f'{d}/domain.yml')
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('enough.common.openstack.Stack.list', return_value=['bind-host'])
    mocker.patch('enough.common.openstack.Stack.set_public_key')
    mocker.patch('enough.common.openstack.Stack.create_or_update', return_value={
        'ipv4': '1.2.3.4',
    })
    mocker.patch('enough.common.openstack.Heat.get_stack_definition')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    h = Heat(settings.CONFIG_DIR)
    with modified_environ(ENOUGH_API_TOKEN="TOKEN"):
        fqdn = h.create_test_subdomain('my.tld')
    assert '.test.my.tld' in fqdn
    assert os.path.exists(f'{d}/domain.yml')


#
# OpenStack
#
@pytest.mark.openstack_integration
def test_glance(dot_openstack):
    o = OpenStack(dot_openstack.config_dir)
    assert len(o.glance()('image-list')) > 0


def test_server_ip_in_network_ok(mocker):
    ip = '1.2.3.4'
    mocker.patch('enough.common.openstack.OpenStack.server_port_list',
                 return_value="[{'ip_address': '" + ip + "'}, {'ip_address': '1:2:3:4:5'}]")
    o = OpenStack(settings.CONFIG_DIR)
    assert o.server_ip_in_network('server', 'network') == ip


def test_server_ip_in_network_none(mocker):
    mocker.patch('enough.common.openstack.OpenStack.server_port_list',
                 return_value='[]')
    o = OpenStack(settings.CONFIG_DIR)
    assert o.server_ip_in_network('server', 'network') is None


@pytest.mark.openstack_integration
def test_network(openstack_name, dot_openstack):
    o = OpenStack(settings.CONFIG_DIR)
    o.network_and_subnet_create(openstack_name, '10.11.12.0/24')
    assert o.network_exists(openstack_name)
    assert o.subnet_exists(openstack_name)

    dns_ip = '1.2.3.4'
    o.subnet_update_dns(openstack_name, dns_ip)
    r = o.o.subnet.show('--format=value', '-c', 'dns_nameservers', openstack_name)
    assert r.strip() == f"['{dns_ip}']"


@pytest.mark.openstack_integration
def test_backup_create_with_name(openstack_name, dot_openstack, caplog):
    o = OpenStack(settings.CONFIG_DIR)
    o.o.volume.create('--size=1', openstack_name)
    assert o.backup_create([openstack_name]) == 1
    assert o.backup_create([openstack_name]) == 0
    available_snapshot = f'AVAILABLE {o.backup_name_create(openstack_name)}'
    assert available_snapshot in caplog.text
    assert o.backup_prune(0) == 1
    assert o.backup_prune(0) == 0


@pytest.mark.openstack_integration
def test_volume_prune(openstack_name, dot_openstack, caplog):
    o = OpenStack(settings.CONFIG_DIR)

    volume_precious = openstack_name
    o.o.volume.create('--size=1', volume_precious)
    days = 2

    old = days + 1
    old_date = (datetime.datetime.today() - datetime.timedelta(old)).strftime('%Y-%m-%d')

    old_volume_with_snapshot = f'{old_date}-old-with-snapshot-{openstack_name}'
    o.o.volume.create('--size=1', old_volume_with_snapshot)
    old_volume_snapshot = f'snapshot-{openstack_name}'
    o.o.volume.snapshot.create('--volume', old_volume_with_snapshot, old_volume_snapshot)

    old_volume = f'{old_date}-old-{openstack_name}'
    o.o.volume.create('--size=1', old_volume)

    recent = days - 1
    recent_date = (datetime.datetime.today() - datetime.timedelta(recent)).strftime('%Y-%m-%d')

    recent_volume = f'{recent_date}-{openstack_name}'
    o.o.volume.create('--size=1', recent_volume)

    assert o.volume_prune(days) == {'deleted': [old_volume],
                                    'has_snapshots': [old_volume_with_snapshot],
                                    'no_date_prefix': [volume_precious],
                                    'recent': [recent_volume]}


@pytest.mark.openstack_integration
def test_backup_create_no_names(openstack_name, dot_openstack, caplog):
    o = OpenStack(settings.CONFIG_DIR)
    o.o.volume.create('--size=1', openstack_name)
    backup_name = f'2020-03-22-{openstack_name}'
    o.o.volume.create('--size=1', backup_name)
    o.backup_create([])
    available_snapshot = f'AVAILABLE {o.backup_name_create(openstack_name)}'
    assert available_snapshot in caplog.text
    skipped = f'skipping {backup_name}'
    assert skipped in caplog.text


@pytest.mark.openstack_integration
def test_openstack_replace_volume(openstack_name, dot_openstack,
                                  openstack_variables):
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    d.update({
        'volumes': [
            {
                'size': '1',
                'name': openstack_name,
            },
        ],
    })
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    s.create_or_update()

    o = OpenStack(settings.CONFIG_DIR)
    assert openstack_name in o.o.volume.list('--name', openstack_name)

    other_volume = f'{openstack_name}_other'
    backup_volume = o.backup_name_create(openstack_name)

    o.o.volume.create('--size=1', other_volume)
    o.replace_volume(openstack_name, other_volume, delete_volume=True)
    assert o.o.volume.list('--name', other_volume).strip() == ''
    assert o.o.volume.list('--name', backup_volume).strip() == ''
    assert o.o.volume.list(
        '-f=value', '-c=Name', '--name', openstack_name).strip() == openstack_name

    other_volume = f'{openstack_name}_backedup'
    o.o.volume.create('--size=1', other_volume)
    o.replace_volume(openstack_name, other_volume, delete_volume=False)
    assert o.o.volume.list('--name', other_volume).strip() == ''
    assert o.o.volume.list(
        '-f=value', '-c=Name', '--name', backup_volume).strip() == backup_volume
    assert o.o.volume.list(
        '-f=value', '-c=Name', '--name', openstack_name).strip() == openstack_name


@pytest.mark.openstack_integration
def test_openstack_volume_resize_ok(openstack_name, dot_openstack,
                                    openstack_variables):
    size = 1
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    d.update({
        'volumes': [
            {
                'size': str(size),
                'name': openstack_name,
            },
        ],
    })
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    s.create_or_update()

    o = OpenStack(settings.CONFIG_DIR)

    assert size == int(o.o.volume.show(
        '-c', 'size', '--format=value', openstack_name).strip())

    new_size = 2
    assert o.volume_resize(openstack_name, openstack_name, new_size) is True

    assert new_size == int(o.o.volume.show(
        '-c', 'size', '--format=value', openstack_name).strip())

    assert o.volume_resize(openstack_name, openstack_name, new_size) is False

    with pytest.raises(openstack.OpenStackVolumeResizeMismatch):
        o.volume_resize(openstack_name, 'UNKNOWN', new_size)

    with pytest.raises(openstack.OpenStackVolumeResizeShrink):
        o.volume_resize(openstack_name, openstack_name, 1)


@pytest.mark.openstack_integration
def test_openstack_volume_resize_no_volume(openstack_name, dot_openstack, openstack_variables):
    d = Heat.hostvars_to_stack(openstack_name, openstack_variables)
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key(f'{settings.CONFIG_DIR}/infrastructure_key.pub')
    s.create_or_update()

    o = OpenStack(settings.CONFIG_DIR)

    with pytest.raises(openstack.OpenStackVolumeResizeMissing):
        o.volume_resize(openstack_name, openstack_name, 1)


@pytest.mark.openstack_integration
def test_openstack_security_group(openstack_name, dot_openstack):
    o = OpenStack(settings.CONFIG_DIR)
    o.o.security.group.create(openstack_name)
    assert o.delete_security_group(openstack_name) is True
    assert o.delete_security_group(openstack_name) is False


@pytest.mark.openstack_integration
def test_destroy_volumes_with_same_name(openstack_name, dot_openstack):
    volume_name = f'{openstack_name}-test-destroy-volume'
    o = OpenStack(settings.CONFIG_DIR)
    o.o.volume.create('--size', '1', volume_name)
    o.o.volume.create('--size', '1', volume_name)
    assert 2 == o.o.volume.list().count(volume_name)
    o.destroy_everything(openstack_name)
    assert 0 == o.o.volume.list().count(volume_name)


@pytest.mark.openstack_integration
def test_image_backup_prune(tmpdir, mocker, openstack_name, dot_openstack):
    pathname = f'{tmpdir}/{openstack_name}.qcow2'
    sh.qemu_img('create', '-f', 'qcow2', pathname, '1M')
    o = OpenStack(dot_openstack.config_dir)

    today = o.backup_date()

    old = '2010-01-01'
    mocker.patch('enough.common.openstack.OpenStack.backup_date', return_value=old)
    assert o.image_backup_upload(openstack_name, pathname) is True

    mocker.patch('enough.common.openstack.OpenStack.backup_date', return_value=today)
    assert o.image_backup_upload(openstack_name, pathname) is True
    assert o.image_backup_upload(openstack_name, pathname) is False

    days = 10
    o.image_backup_prune([openstack_name], days)

    assert o.image_list() == [o.backup_name_create(openstack_name)]


def test_backup_is_recent(dot_openstack):
    o = OpenStack(dot_openstack.config_dir)
    name = 'NAME'
    days = 1
    backup_pathname = o.backup_pathname(name)
    assert o.backup_is_recent(name, days) is None
    open(backup_pathname, 'w').write('SOMETHING')
    assert o.backup_is_recent(name, days) is True
    old = time.time() - 2 * days * 60 * 60 * 24
    os.utime(backup_pathname, (old, old))
    assert o.backup_is_recent(name, days) is False


def test_backup_only_old(dot_openstack):
    o = OpenStack(dot_openstack.config_dir)
    new = 'NEW'
    old = 'OLD'
    days = 1
    new_pathname = o.backup_pathname(new)
    open(new_pathname, 'w').write('SOMETHING')
    assert o.backup_only_old([old, new], days) == [old]


def test_backup_latests():
    o = OpenStack(settings.CONFIG_DIR)
    name = 'name1'
    latest = f'2021-03-02-{name}'
    assert o.backup_latests(
        ['ignorethat', latest, f'2020-03-02-{name}', '2021-03-02-name2'],
        [name]
    ) == {name: latest}


@pytest.mark.openstack_integration
def test_backup_download_images(tmpdir, openstack_name, dot_openstack):
    original_pathname = f'{tmpdir}/test.qcow2'
    sh.qemu_img('create', '-f', 'qcow2', original_pathname, '1M')
    original_md5 = sh.md5sum(original_pathname).split(' ')[0]

    o = OpenStack(dot_openstack.config_dir)

    assert len(o.image_list_active()) == 0
    assert o.image_backup_upload(openstack_name, original_pathname) is True
    assert len(o.image_list_active()) > 0
    o.backup_download(volumes=[], hosts=[openstack_name], recent=1)
    backup_pathname = o.backup_pathname(openstack_name)
    backup_md5 = sh.md5sum(backup_pathname).split(' ')[0]

    assert backup_md5 == original_md5


@pytest.mark.openstack_integration
def test_backup_download_volumes(tmpdir, openstack_name, dot_openstack):
    o = OpenStack(dot_openstack.config_dir)
    #
    # create a small volume
    #
    o.o.volume.create('--size=1', openstack_name)
    #
    # create a backup
    #
    o.backup_create([])
    #
    # download the backup
    #
    o.backup_download(volumes=[openstack_name], hosts=[], recent=1)
    backup_pathname = o.backup_pathname(openstack_name)
    assert os.path.exists(backup_pathname)


@pytest.mark.openstack_integration
def test_image_create_from_volume(openstack_name, dot_openstack):
    o = OpenStack(dot_openstack.config_dir)
    o.o.volume.create('--size=1', openstack_name)
    o.volume_wait_for_available(openstack_name)
    assert o.image_list() == []
    o.image_create_from_volume(openstack_name)
    assert o.image_status(openstack_name) == 'active'
    li = [
        i.strip() for i in o.o.image.list(
            '--private', '--format=value', '-c', 'Name', _iter=True)
    ]
    assert li == [openstack_name]
    o.o.image.delete(openstack_name)
