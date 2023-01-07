import os
import pytest
import sh
import shutil
import yaml

from enough import settings
from enough.common import ansible_utils


def test_get_global_variable():
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    assert ansible.get_global_variable('openstack_cloud')
    with pytest.raises(ansible_utils.AnsibleVariableNotFound):
        assert ansible.get_global_variable('UNKNOWN')


def test_get_hostvars():
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    d = ansible.get_hostvars('production_domain', 'bind-host',
                             'icinga-host')
    assert d == {'bind-host': 'enough.community', 'icinga-host': 'enough.community'}


def test_get_hostvars_recursive(tmpdir):
    """Check that we aren't affected by
    https://github.com/ansible/ansible/pull/64282"""

    host = 'test_get_hostvars_recursive_host'  # any host

    os.makedirs(f'{tmpdir}/group_vars/')
    groupvars = {
        'foo': 'blah',
        'bar': '{{ foo }}'
    }

    # An inventory file is required in order to avoid such warning:
    # [WARNING]: Unable to parse /tmp/pytest-0/test_get_hostvars_recursive0
    #            as an inventory source
    with open(f'{tmpdir}/hosts', 'w') as inventory:
        inventory.write(host)
    with open(f'{tmpdir}/group_vars/all.yaml', 'w') as group:
        yaml.dump(groupvars, group)
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR,
                                    inventories=[tmpdir])

    r1 = ansible.get_hostvars(None, host)
    r2 = ansible.get_variable(None, host)

    assert r1[host]['bar'] == r2['bar'] == groupvars['foo']


def test_get_all_hostvars():
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    hostvars = ansible.get_hostvars(None)
    hosts = set(hostvars)

    # Check list of hosts isn't empty
    assert 'bind-host' in hosts
    assert 'icinga-host' in hosts

    inventory = ansible.ansible_inventory()
    inventory_vars = inventory['_meta']['hostvars']
    inventory_hosts = set(inventory_vars)

    # Check that output of ansible and ansible-inventory match
    assert hosts == inventory_hosts


def test_get_hostvars_unknown_host():
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    with pytest.raises(sh.ErrorReturnCode_1):
        ansible.get_hostvars('production_domain', 'inexistent-host')
    with pytest.raises(sh.ErrorReturnCode_1):
        ansible.get_hostvars(None, 'inexistent-host')


def test_get_hostvars_unknown_variable():
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    with pytest.raises(ansible_utils.AnsibleVariableNotFound):
        ansible.get_hostvars('inexistent-variable', 'bind-host')


def test_get_variable():
    test_inventory = 'tests/enough/common/test_ansible_utils/variables_inventory'
    expected = yaml.safe_load(open(f'{test_inventory}/host_vars/api-host.yml'))
    variable = 'api_admin_password'
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR, [test_inventory])
    value = ansible.get_variable(variable, 'api-host')
    assert expected[variable] == value


def test_pipelining_is_enabled(monkeypatch):
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR,
                                    ['localhost,'])
    ansible.bake()('all', '-llocalhost', '-massert',
                   "-athat='ansible_pipelining'")


def test_pipelining_is_enabled_2(monkeypatch):
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR,
                                    ['localhost,'])

    # environment variable takes precedence over ansible.cfg
    monkeypatch.setenv('ANSIBLE_PIPELINING', 'False')
    with pytest.raises(sh.ErrorReturnCode):
        ansible.bake()('all', '-llocalhost', '-massert',
                       "-athat='ansible_pipelining'")


def test_ansible_environment(monkeypatch):
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR,
                                    ['localhost,'])

    # The environment variable must be defined once ansible_utils.Ansible has
    # been called (we expect environment variables to be evaluated as late as
    # possible).
    monkeypatch.setenv('TEST_CANARY', 'test_value')
    ansible.bake()('all', '-llocalhost', '-massert',
                   '''-athat="lookup('env', 'TEST_CANARY') == 'test_value'"''')


def test_playbook_environment(monkeypatch):
    playbook = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)

    # The environment variable must be defined once ansible_utils.Playbook has
    # been called (we expect environment variables to be evaluated as late as
    # possible).
    monkeypatch.setenv('GITLAB_RUNNER_TOKEN', 'test_value')
    monkeypatch.setenv('ANSIBLE_VERBOSITY', '2')
    # default value of role default variable 'gitlab_runner__token' is the
    # 'GITLAB_RUNNER_TOKEN' environment variable (using 'env' lookup)
    value = playbook.get_role_variable('gitlab_runner', 'gitlab_runner__token',
                                       'gitlab-host')
    assert 'test_value' == value


def test_get_role_variable():
    defaults = yaml.safe_load(open('playbooks/api/roles/api/defaults/main.yml'))
    variable = 'api_admin_password'
    playbook = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    value = playbook.get_role_variable('api', variable, 'api-host')
    assert defaults[variable] == value


def test_get_role_unknown_variable():
    playbook = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    with pytest.raises(ansible_utils.AnsibleVariableNotFound):
        playbook.get_role_variable('api', 'inexistent_role_variable', 'api-host')


def test_get_role_variable_unknown_host():
    playbook = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    with pytest.raises(sh.ErrorReturnCode_1):
        playbook.get_role_variable('api', 'api_admin_password', 'inexistent-host')


def test_get_unknown_role_variable():
    playbook = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    with pytest.raises(sh.ErrorReturnCode_1):
        playbook.get_role_variable('inexistent-role', 'inexistent_role_variable', 'inexistent-host')


def test_playbook_roles_path():
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    r = p.roles_path('.')
    assert '/infrastructure/' in r


def test_playbook_ensure_decrypted(tmpdir):
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    shutil.copytree('tests/enough/common/test_ansible_utils/domain.com',
                    f'{tmpdir}/domain.com')
    c = f'{tmpdir}/domain.com'
    p.config_dir = c

    #
    # decryption is needed but no password is found
    #
    with pytest.raises(ansible_utils.Playbook.NoPasswordException):
        assert p.ensure_decrypted() is False
    shutil.copyfile('tests/enough/common/test_ansible_utils/domain.com.pass',
                    f'{tmpdir}/domain.com.pass')

    #
    # all files are decrypted
    #
    for f in p.encrypted_files(c):
        if f.endswith('not-encrypted.key'):
            continue
        assert p.is_encrypted(f)
    assert p.ensure_decrypted() is True
    for f in p.encrypted_files(c):
        assert not p.is_encrypted(f)
    #
    # nothing to do
    #
    assert p.ensure_decrypted() is False


def test_playbook_run_with_args(caplog):
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    p.run('tests/enough/common/test_ansible_utils/playbook-ok.yml')
    assert 'OK_PLAYBOOK' in caplog.text
    assert 'OK_IMPORTED' in caplog.text


def test_playbook_run_no_args(mocker):
    called = {}

    def playbook():
        def run(*args):
            assert '--private-key' in args
            called['playbook'] = True
        return run
    mocker.patch('enough.common.ansible_utils.Playbook.bake',
                 side_effect=playbook)
    kwargs = {
        'args': [],
    }
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    p.run_from_cli(**kwargs)
    assert 'playbook' in called


def test_ansible_inventory():
    i = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR).ansible_inventory()
    assert '_meta' in i


def test_get_groups(monkeypatch):
    monkeypatch.setenv('ANSIBLE_VERBOSITY', '2')
    i = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR).get_groups()
    assert 'all-hosts' in i


def test_flat_inventory():
    inventory = {
        'group1': {
            'children': ['group2', 'group3'],
            'hosts': ['host10', 'host11'],
        },
        'group2': {
            'hosts': ['host20'],
            'children': ['group4'],
        },
        'group3': {
            'hosts': ['host30', 'host31'],
        },
        'group4': {
            'children': ['group5', 'group6'],
        },
        'group5': {
            'hosts': ['host50', 'host51'],
        },
        'group6': {},
        'group7': {
            'hosts': ['host70', 'host71'],
        }
    }
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    expected = ['host10', 'host11', 'host20', 'host30', 'host31', 'host50', 'host51']
    assert sorted(ansible._flat_inventory(inventory, inventory['group1'])) == expected
    expected = ['host70', 'host71']
    assert sorted(ansible._flat_inventory(inventory, inventory['group7'])) == expected
