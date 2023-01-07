import requests
import yaml

testinfra_hosts = ['ansible://bind-host']


def get_address(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return 'icinga.' + yaml.safe_load(
        open(vars_dir + '/domain.yml'))['domain']


def test_icingaweb2_login_screen(request, host, pytestconfig):
    certs = request.session.infrastructure.certs()
    address = get_address(pytestconfig.getoption("--ansible-inventory"))
    proto_srv = f"https://{address}"
    s = requests.Session()
    r = s.get(proto_srv+'/icingaweb2/authentication/login', timeout=20, verify=certs)
    cookies = dict(r.cookies)
    r = s.get(proto_srv+'/icingaweb2/authentication/login?_checkCookie=1',
              cookies=cookies, timeout=5, verify=certs)
    r.raise_for_status()
    assert 'Icinga Web 2 Login' in r.text
