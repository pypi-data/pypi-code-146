import pytest


testinfra_hosts = ['ansible://icinga-host']


def test_bind(host):
    domain = host.run("hostname -d").stdout.strip()
    bind_host = host.get_host('ansible://bind-host',
                              ansible_inventory=host.backend.ansible_inventory)
    address = bind_host.ansible.get_variables()['ansible_host']
    for h in ('ns1', 'bind', 'bind-host'):
        cmd = host.run("getent hosts {}.{}".format(h, domain))
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert address in cmd.stdout.strip()
        assert h + "." + domain in cmd.stdout.strip()
        # try also with shortnames
        cmd = host.run("getent hosts {}".format(h))
        assert 0 == cmd.rc
        assert address in cmd.stdout.strip()
        assert h + "." + domain in cmd.stdout.strip()


@pytest.mark.parametrize("bindhost", ('bind-host', 'otherbind-host'))
def test_dig_icinga(host, bindhost):
    domain = host.run("hostname -d").stdout.strip()
    bind_host = host.get_host(f'ansible://{bindhost}',
                              ansible_inventory=host.backend.ansible_inventory)
    icinga_address = host.ansible.get_variables()['ansible_host']
    cmd = bind_host.run(f'dig @127.0.0.1 icinga.{domain}')
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    assert icinga_address in cmd.stdout.strip()


def test_recursion(host):
    cmd = host.run("getent hosts fsf.org")
    assert 0 == cmd.rc
    assert 'fsf.org' in cmd.stdout.strip()
