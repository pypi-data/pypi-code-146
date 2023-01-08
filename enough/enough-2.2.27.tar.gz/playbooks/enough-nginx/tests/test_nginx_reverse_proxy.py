testinfra_hosts = ['ansible://other-host']


def test_proxy(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    r = host.run("curl -s -m 5 http://other-host.$(hostname -d)/index.html")
    assert r.rc == 0
    assert 'SOMETHING' in r.stdout


def test_named_proxy(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    for name in ('name1', 'name2', 'name3'):
        r = host.run(f"curl -s -m 5 http://{name}.$(hostname -d)/index.html")
        assert r.rc == 0
        assert 'NAMEDBACKEND' in r.stdout
