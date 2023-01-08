import sh

testinfra_hosts = ['ansible://authorized-keys-host']


def test_all(host):
    address = host.ansible.get_variables()['ansible_host']
    marker = "MARKER"
    key = 'playbooks/authorized_keys/roles/authorized_keys/files/test_keys/testkey'
    sh.chmod('600', key)
    r = sh.ssh('-oStrictHostKeyChecking=no', '-i', key, 'debian@' + address, 'echo', marker)
    assert r.stdout.decode('utf-8').strip() == marker


def test_remove(host):
    assert host.file("/home/debian/.ssh/authorized_keys").contains("cigale.amie.coop")
    assert not host.file("/home/debian/.ssh/authorized_keys").contains("MBPG.local")
