from io import StringIO
import os
import pytest
import textwrap

import cliff.app

from tests.modified_environ import modified_environ
from enough import cmd


def test_remap():
    p = '.enough/thing'
    unchanged = '/foo/bar/'
    expected = [f'{os.path.expanduser("~")}/{p}', unchanged]
    assert cmd.EnoughApp.remap([f'/home/user/{p}', unchanged]) == expected
    expected = [f'--option={os.path.expanduser("~")}/{p}', unchanged]
    assert cmd.EnoughApp.remap([f'--option=/home/user/{p}', unchanged]) == expected


def test_preserve_ownership(mocker, tmpdir):
    #
    # not running as root, do nothing
    #
    assert cmd.EnoughApp.preserve_ownership() is False

    #
    # pretend to run as root and chown to self
    #
    mocker.patch('os.geteuid', return_value=0)
    mocker.patch('os.path.expanduser', return_value=str(tmpdir))
    assert cmd.EnoughApp.preserve_ownership() is True


def test_playbook_command(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.ansible_utils.Playbook.run_from_cli',
                 side_effect=lambda **kwargs: print('PLAYBOOK'))
    assert cmd.main(['playbook']) == 0
    out, err = capsys.readouterr()
    assert 'PLAYBOOK' in out


def test_libvirt_command(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')

    def set_args(self, **kwargs):
        self.args = self.init_args.copy()
        self.args.update(kwargs)

    mocker.patch('enough.common.Enough.set_args', set_args)
    mocker.patch('enough.common.libvirt_install',
                 side_effect=lambda *args, **kwargs: print('LIBVIRT'))
    assert cmd.main(['libvirt', 'install', '1.2.3.4']) == 0
    out, err = capsys.readouterr()
    assert 'LIBVIRT' in out


@pytest.mark.ansible_integration
def test_playbook_execution(mocker, monkeypatch):
    monkeypatch.setenv('ANSIBLE_TRANSFORM_INVALID_GROUP_CHARS', 'ignore')

    stderr = StringIO()
    # Pass stderr to cliff.app.App in order to check command output
    init_backup = cliff.app.App.__init__

    def new_init(self, *args, **kwargs):
        init_backup(self, *args, stderr=stderr, **kwargs)
    mocker.patch.object(cliff.app.App, '__init__', new_init)

    assert cmd.main(['playbook', '--', '--limit', 'localhost', '-ilocalhost,',
                     '-clocal', 'tests/enough/playbook.yml']) == 0

    expected_output = textwrap.dedent("""
    PLAY [localhost] ***************************************************************

    TASK [debug] *******************************************************************
    ok: [localhost] => {
    "msg": "localhost hostname"
    }

    PLAY RECAP *********************************************************************
    localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0\
    rescued=0    ignored=0

    """)
    assert stderr.getvalue() == expected_output


def test_openstack(capsys, mocker):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.openstack.OpenStack.run',
                 side_effect=lambda *args, **kwargs: print('OPENSTACK'))
    with modified_environ(OS_CLIENT_CONFIG_FILE="/dev/null"):
        assert cmd.main(['openstack', '--debug', 'help']) == 0
    out, err = capsys.readouterr()
    assert 'OPENSTACK' in out
