import json

from enough import cmd


def test_service(capsys, mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    r = {'fqdn': 'name.domain.com'}
    mocker.patch('enough.common.service.ServiceOpenStack.create_or_update', return_value=r)
    assert cmd.main(['service', 'create', '--format=json', 'name']) == 0
    out, err = capsys.readouterr()
    j = json.loads(out)
    assert {'fqdn': j['name']} == r
