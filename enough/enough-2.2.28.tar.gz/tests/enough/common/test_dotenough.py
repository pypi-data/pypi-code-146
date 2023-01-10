import pytest
import os
import yaml
from enough.common import ansible_utils


from enough.common.dotenough import (
    Hosts,
    DotEnough,
    DotEnoughOpenStack,
    DotEnoughLibvirt,
    DotEnoughOpenStackUnknownProvider,
)


#
# Hosts
#
def test_hosts_create_delete(tmpdir):
    config_dir = str(tmpdir)
    h = Hosts(config_dir)
    host = 'HOST'
    ip = '1.2.3.4'
    port = '22'
    assert h.create_or_update(host, ip, port) is True
    assert h.create_or_update(host, ip, port) is False
    assert os.path.exists(f'{config_dir}/inventory/hosts.yml')
    h = Hosts(config_dir)
    assert h.create_or_update(host, ip, port) is False
    assert h.hosts[host]['ansible_host'] == ip
    assert h.hosts[host]['ansible_port'] == port

    assert h.missings([host, 'MISSING']) == ['MISSING']

    h.delete(host)
    h = Hosts(config_dir)
    assert h.hosts == {}


def test_hosts_ensure(tmpdir):
    config_dir = str(tmpdir)
    h = Hosts(config_dir)
    host = 'HOST'
    assert h.ensure(host) is True
    assert h.ensure(host) is False
    assert os.path.exists(f'{config_dir}/inventory/hosts.yml')
    h = Hosts(config_dir)
    assert h.ensure(host) is False
    assert h.hosts[host] == {}


@pytest.mark.parametrize('group_name', ('all', 'live', 'unexpected'))
def test_hosts_group_name(tmpdir, group_name):
    config_dir = str(tmpdir)
    h = Hosts(config_dir)
    assert not h.hosts

    h.save()  # create '{config_dir}/inventory' directory

    f = f'{config_dir}/inventory/hosts.yml'
    open(f, 'w').write(yaml.dump({
        group_name: {
            'hosts': {
                'some-host': {
                    'ansible_host': '1.2.3.4',
                }
            }
        }
    }))
    try:
        h.load()
    except Exception:
        assert group_name == 'unexpected'
    else:
        assert group_name in ('live', 'all')
        assert 'some-host' in h.hosts


#
# DotEnough
#
def test_service_add_to_group(tmpdir):
    d = DotEnough(tmpdir, 'test.com')
    service = 'SERVICE'
    group = DotEnough.service2group(service)
    host = 'HOST'
    expected = {
        group: {
            'hosts': {
                host: None,
            }
        }
    }
    assert d.service_add_to_group(service, host) == expected
    assert d.service_add_to_group(service, host) == expected
    other_host = 'OTHER'
    expected[group]['hosts'][other_host] = None
    assert d.service_add_to_group(service, other_host) == expected
    os.system(f'cat {tmpdir}/services.yml')


@pytest.mark.parametrize("cls,driver", (
    (DotEnoughOpenStack, 'openstack'),
    (DotEnoughLibvirt, 'libvirt'),
    ))
def test_dotenough_populate_infrastructure_driver(tmpdir, cls, driver):
    d = cls(tmpdir, 'test.com')
    d.populate_config('ownca')
    all_dir = f'{d.config_dir}/inventory/group_vars/all'
    v = yaml.safe_load(open(f'{all_dir}/infrastructure.yml').read())
    assert v['infrastructure_driver'] == driver


#
# DotEnoughOpenStack
#
@pytest.mark.parametrize("clouds,cloud,provider", [
    (
        {
            'clouds': {
                'production': {
                    'auth': {
                        'auth_url': 'https://identity.api.ams.fuga.cloud:443/v3'
                    }
                }
            }
        },
        'production', 'fuga'),
    (
        {
            'clouds': {
                'production': {
                    'auth': {
                        'auth_url': 'https://auth.cloud.ovh.net/v3/'
                    }
                }
            }
        },
        'production', 'ovh'),
])
def test_populate_provider_supported(tmpdir, clouds, cloud, provider):
    d = DotEnoughOpenStack(tmpdir, 'test.com')
    f = f'{d.config_dir}/inventory/group_vars/all/clouds.yml'
    open(f, 'w').write(yaml.dump(clouds))
    a = ansible_utils.Ansible(d.config_dir, d.config_dir,
                              ['tests/enough/common/test_init/provider'])
    f = d.populate_provider(a, 'production')
    v = yaml.safe_load(open(f).read())
    assert v['openstack_provider'] == provider


def test_populate_provider_set(tmpdir):
    d = DotEnoughOpenStack(tmpdir, 'test.com')
    f = f'{d.config_dir}/inventory/group_vars/all/openstack_provider.yml'
    open(f, 'w').write(yaml.dump({'openstack_provider': 'known'}))
    a = ansible_utils.Ansible(d.config_dir, d.config_dir,
                              ['tests/enough/common/test_init/provider'])
    assert d.populate_provider(a, 'production') == 'known'


def test_populate_provider_no_clouds(tmpdir):
    d = DotEnoughOpenStack(tmpdir, 'test.com')
    a = ansible_utils.Ansible(d.config_dir, d.config_dir,
                              ['tests/enough/common/test_init/provider'])
    assert d.populate_provider(a, 'production') is None


def test_populate_provider_unknown(tmpdir):
    d = DotEnoughOpenStack(tmpdir, 'test.com')
    clouds = {
        'clouds': {
            'production': {
                'auth': {
                    'auth_url': 'https://example.com/'
                }
            }
        }
    }
    f = f'{d.config_dir}/inventory/group_vars/all/clouds.yml'
    open(f, 'w').write(yaml.dump(clouds))
    a = ansible_utils.Ansible(d.config_dir, d.config_dir,
                              ['tests/enough/common/test_init/provider'])
    with pytest.raises(DotEnoughOpenStackUnknownProvider) as e:
        assert d.populate_provider(a, 'production') == ''
    assert 'example.com' in str(e)
