import time
import requests
import yaml


def get_address(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return 'https://openedx.' + yaml.safe_load(
        open(vars_dir + '/domain.yml'))['domain']


def test_openedx(request, pytestconfig):
    certs = request.session.infrastructure.certs()
    # openedx freshly recreated may take few mins to be operationnal
    url = get_address(pytestconfig.getoption("--ansible-inventory"))
    for i in range(60, 0, -1):
        r = requests.get(url, timeout=5, verify=certs)
        if r.status_code == requests.codes.ok:
            break
        time.sleep(5)
    assert 'openedx' in r.text
