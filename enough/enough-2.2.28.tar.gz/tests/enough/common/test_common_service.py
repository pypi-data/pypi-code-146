import os
import pytest
import requests_mock as requests_mock_module

from enough import settings
from enough.common import openstack
from enough.common import service

from tests import prepare_config_dir


@pytest.mark.openstack_integration
def test_openstack_create_or_update(request, tmpdir, requests_mock):
    try:
        domain = 'enough.test'
        config_dir = prepare_config_dir(domain, tmpdir)
        requests_mock.post(requests_mock_module.ANY, status_code=201)
        requests_mock.get(requests_mock_module.ANY, status_code=200)
        playbook = 'tests/enough/common/test_common_service/enough-playbook.yml'
        s = service.ServiceOpenStack(config_dir, settings.SHARE_DIR, **{
            'driver': 'openstack',
            'playbook': os.path.abspath(playbook),
            'domain': domain,
            'name': 'essential',
            'cloud': 'production',
        })
        s.dotenough.set_certificate('ownca')
        s.dotenough.set_clouds_file('inventory/group_vars/all/clouds.yml')
        r = s.create_or_update()
        assert r['fqdn'] == f'essential.{domain}'
        # the second time around the hosts.yml are reused
        r = s.create_or_update()
        assert r['fqdn'] == f'essential.{domain}'

    finally:
        o = openstack.OpenStack(s.config_dir, **s.args)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


def test_service_from_host(tmpdir):
    s = service.Service(config_dir=tmpdir, share_dir=settings.SHARE_DIR,
                        domain='test.com')
    assert s.service_from_host('icinga-host') is None
    assert s.service_from_host('cloud-host') == 'cloud'
    assert s.service_from_host('unknown-host') is None


def test_set_service_info(tmpdir):
    s = service.Service(config_dir=tmpdir, share_dir=settings.SHARE_DIR,
                        domain='test.com')
    assert 'forum-host' in s.service2hosts['forum']
    assert len(s.service2hosts['forum']) > 0
    assert 'forum-host' in s.service2group['forum']


def test_update_vpn_dependencies(tmpdir):
    s = service.Service(config_dir=tmpdir, share_dir=settings.SHARE_DIR,
                        domain='test.com')
    assert s.hosts_with_internal_network(['bind-host']) == []
    assert 'website-host' not in s.service2hosts['openvpn']
    assert 'website-host' not in s.service2hosts['weblate']
    inventories = ('tests/enough/common/test_common_service/vpn_inventory',)
    s = service.Service(config_dir=tmpdir, share_dir=settings.SHARE_DIR,
                        domain='test.com', inventory=inventories)
    assert 'website-host' in s.service2hosts['openvpn']
    assert s.hosts_with_internal_network(['icinga-host']) == ['icinga-host']
    s.update_vpn_dependencies()
    assert 'website-host' not in s.service2hosts['weblate']
    assert 'weblate-host' in s.service2hosts['weblate']


def test_ensure_non_empty_service_group(tmpdir):
    name = 'wekan'
    s = service.Service(tmpdir, settings.SHARE_DIR,
                        name=name,
                        domain='test.com')
    with pytest.raises(service.Service.NoHost):
        s.ensure_non_empty_service_group()
    host = 'HOST'
    s = service.Service(tmpdir, settings.SHARE_DIR,
                        name=name,
                        host=host,
                        domain='test.com')
    hosts = s.ensure_non_empty_service_group()
    assert hosts == [host]
    assert hosts == s.ensure_non_empty_service_group()
