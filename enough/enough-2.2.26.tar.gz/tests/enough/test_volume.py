from enough import cmd


def test_volume_resize(mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.Enough.volume_resize')
    assert cmd.main(['volume', 'resize', 'HOST', 'VOLUME']) == 0
