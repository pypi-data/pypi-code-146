testinfra_hosts = ['ansible://icinga-host']


def test_ns1_test(host):
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run("dig +short NS test.{}".format(domain))
    assert 0 == cmd.rc
    assert "ns1.{}.".format(domain) == cmd.stdout.strip()


def test_bind(host):
    domain = host.run("hostname -d").stdout.strip()
    cmd = host.run("getent hosts ns1.{}".format(domain))
    assert 0 == cmd.rc


def test_update(host):
    domain = host.run("hostname -d").stdout.strip()
    hostname = host.run("hostname -s").stdout.strip()
    bind_host = host.get_host('ansible://bind-host',
                              ansible_inventory=host.backend.ansible_inventory)
    address = bind_host.ansible.get_variables()['ansible_host']
    cmd = bind_host.run(f'''
        nsupdate <<EOF
        server {address}
        zone test.{domain}
        update add {hostname}.test.{domain}. 1800 TXT "Updated by nsupdate"
        show
        send
        quit
        EOF
        ''')
    assert 0 == cmd.rc


def test_dig_update(host):
    domain = host.run("hostname -d").stdout.strip()
    hostname = host.run("hostname -s").stdout.strip()
    cmd = host.run("dig +short TXT {}.test.{}".format(hostname, domain))
    print(cmd.stdout.strip())
    assert 0 == cmd.rc
    assert "Updated by nsupdate" in cmd.stdout.strip()


def test_clean_update(host):
    domain = host.run("hostname -d").stdout.strip()
    hostname = host.run("hostname -s").stdout.strip()
    host = host.get_host('ansible://bind-host',
                         ansible_inventory=host.backend.ansible_inventory)
    address = host.ansible.get_variables()['ansible_host']
    cmd = host.run(f'''
        nsupdate <<EOF
        server {address}
        zone test.{domain}
        update delete {hostname}.test.{domain}. TXT
        show
        send
        quit
        EOF
        ''')
    assert 0 == cmd.rc
