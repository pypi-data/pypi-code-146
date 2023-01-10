from enough import cmd


def test_ssh(mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.ssh.SSH.ssh')
    assert cmd.main(['--debug', 'ssh', 'host']) == 0
