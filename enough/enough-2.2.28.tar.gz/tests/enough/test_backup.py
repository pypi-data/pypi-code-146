from enough import cmd


def test_backup_restore(mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.Enough.restore_local')
    assert cmd.main(['--debug', 'backup', 'restore', 'name']) == 0


def test_backup_clone_volume(mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.Enough.cli_clone_volume')
    assert cmd.main(['--debug', 'backup', 'clone', 'volume', 'name']) == 0


def test_enough_download(capsys, mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.Enough.backup_download',
                 side_effect=lambda *args, **kwargs: print('DOWNLOAD'))
    assert cmd.main(['backup', 'download']) == 0
    out, err = capsys.readouterr()
    assert 'DOWNLOAD' in out
