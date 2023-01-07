from enough.internal import cmd


def test_enough_create_test_subdomain(capsys, mocker, tmp_config_dir):
    # do not tamper with logging streams to avoid
    # ValueError: I/O operation on closed file.
    mocker.patch('cliff.app.App.configure_logging')
    api_domain = 'some.domain'
    sub_domain = 'subdomain'
    mocker.patch('enough.common.openstack.Heat.create_test_subdomain',
                 side_effect=lambda domain: f"{sub_domain}.{domain}")
    assert cmd.main(['create', 'test', 'subdomain', api_domain]) == 0
    out, err = capsys.readouterr()
    assert f"{sub_domain}.{api_domain}" in out
