from enough.common import host


def test_host_factory(tmpdir):
    h = host.host_factory(config_dir=tmpdir, driver='openstack', domain='a.b')
    assert type(h).__name__ == 'HostOpenStack'
    h = host.host_factory(config_dir=tmpdir, driver='libvirt', domain='a.b')
    assert type(h).__name__ == 'HostLibvirt'
