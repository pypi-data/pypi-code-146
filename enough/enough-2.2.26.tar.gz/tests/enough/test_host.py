import json

from enough import cmd


def test_host_create(capsys, mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    r = {'port': '22', 'ipv4': '127.0.0.1'}
    mocker.patch('enough.common.host.HostOpenStack.create_or_update', return_value=r)
    assert cmd.main(['host', 'create', '--format=json', 'name']) == 0
    out, err = capsys.readouterr()
    j = json.loads(out)
    assert {'port': j['port'], 'ipv4': j['ip']} == r


def test_host_delete(mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    mocker.patch('enough.common.host.HostOpenStack.delete')
    assert cmd.main(['host', 'delete', 'name']) == 0
