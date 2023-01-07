from tests.modified_environ import modified_environ
from enough.internal import cmd


def test_enough_backup(capsys, mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.openstack.OpenStack.backup_create',
                 side_effect=lambda *args, **kwargs: print('BACKUP'))
    with modified_environ(OS_CLIENT_CONFIG_FILE="/dev/null"):
        assert cmd.main(['backup', 'create']) == 0
    out, err = capsys.readouterr()
    assert 'BACKUP' in out
