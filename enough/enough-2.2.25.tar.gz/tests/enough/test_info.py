from enough import cmd


def test_info(capsys, mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.Enough.info', side_effect=lambda **kwargs: ['INFO'])
    assert cmd.main(['info']) == 0
    out, err = capsys.readouterr()
    assert 'INFO' in out
