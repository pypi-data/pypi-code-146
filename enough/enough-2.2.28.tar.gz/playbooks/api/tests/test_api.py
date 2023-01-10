import requests
import yaml
import dns.resolver
import gitlab_utils
from urllib.parse import urlparse
from bs4 import BeautifulSoup

#
# debug with
#
# enough ssh api-host
# docker exec -ti enough_enough-enough_1 journalctl -n 200 -f --unit enough
#

testinfra_hosts = ['ansible://gitlab-host']


def get_domain(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return yaml.safe_load(open(vars_dir + '/domain.yml'))['domain']


def api_sign_in(request, pytestconfig, host):
    certs = request.session.infrastructure.certs()
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))

    #
    # GitLab home page
    #
    lab = requests.Session()
    lab_url = f'https://lab.{domain}'
    r = lab.get(lab_url + '/users/sign_in', verify=certs)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    authenticity_token = soup.select(
        'form[action="/users/sign_in"] input[name="authenticity_token"]')[0]['value']

    #
    # GitLab Login
    #
    r = lab.post(lab_url + '/users/sign_in', data={
        'authenticity_token': authenticity_token,
        'user[login]': 'root',
        'user[password]': gitlab_utils.get_password(),
        'user[remember_me]': 0,
    }, verify=certs)
    r.raise_for_status()

    #
    # Revoke all tokens (in case test is run multiple times)
    #
    r = lab.get(lab_url + '/profile/applications', verify=certs)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    for f in soup.select('.oauth-authorized-applications form'):
        data = {}
        for input in f.children:
            if input.name != 'input':
                continue
            data[input['name']] = input['value']
        url = urlparse(f['action'])
        r = lab.post(lab_url + url.path, params=url.query, data=data, verify=certs)
        r.raise_for_status()

    #
    # API login
    #
    api = requests.Session()
    api.url = f'https://api.{domain}'
    r = api.get(api.url + '/accounts/gitlab/login/?process=login',
                allow_redirects=False,
                verify=certs)
    # print(r.headers['Location'])
    assert 'oauth/authorize' in r.headers['Location']
    r.raise_for_status()

    #
    # GitLab OAuth confirmation page
    #
    r = lab.get(r.headers['Location'], verify=certs)
    r.raise_for_status()
    assert 'An error' not in r.text
    soup = BeautifulSoup(r.text, 'html.parser')
    data = {
        'commit': 'Authorize',
    }
    for input in soup.select('form[action="/oauth/authorize"]:nth-child(2) input[type="hidden"]'):
        if input.get('name') is None or input.get('value') is None:
            continue
        data[input['name']] = input['value']
    #  print(str(data))
    #  print(soup.prettify())
    r = lab.post(lab_url + '/oauth/authorize', data=data,
                 allow_redirects=False,
                 verify=certs)
    r.raise_for_status()
    assert 'accounts/gitlab/login/callback' in r.headers['Location']

    # print(r.headers['Location'])
    r = api.get(r.headers['Location'], allow_redirects=False, verify=certs)
    # print(r.headers['Location'])
    r.raise_for_status()
    if '/accounts/social/signup/' == r.headers['Location']:
        #
        # API confirm email
        #
        r = api.get(f"{api.url}{r.headers['Location']}", verify=certs)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        data = {}
        for input in soup.select('form input'):
            if input.get('name') is None or input.get('value') is None:
                continue
            data[input['name']] = input['value']
        # print(str(data))
        # print(soup.prettify())
        r = api.post(f'{api.url}/accounts/social/signup/', data=data,
                     allow_redirects=False, verify=certs)
        r.raise_for_status()

    assert r.headers['Location'] == '/member/'

    #
    # API member page
    #
    r = api.get(f"{api.url}{r.headers['Location']}", verify=certs)
    r.raise_for_status()
    #
    # Get rest-framework token
    #
    soup = BeautifulSoup(r.content, 'html.parser')
    # print(soup.prettify())
    element = soup.select('#token')
    assert len(element) == 1
    token = element[0].contents[0]
    assert len(token) == 40
    return token


#
# debug with
#
# enough ssh api-host
# docker exec -ti enough_enough-enough_1 journalctl -n 200 -f --unit enough
#
def test_delegate_test_dns(request, pytestconfig, host):
    certs = request.session.infrastructure.certs()
    token = api_sign_in(request, pytestconfig, host)
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))
    url = f"https://api.{domain}"
    s = requests.Session()
    s.headers = {'Authorization': f'Token {token}'}
    data = {
        "name": "foo",
        "ip": "1.2.3.4",
    }
    r = s.post(f'{url}/delegate-test-dns/', json=data, timeout=60, verify=certs)
    # print(r.text)
    r.raise_for_status()
    resolver = dns.resolver.Resolver()
    bind_ip = str(resolver.query(f'bind.{domain}.')[0])
    resolver.nameservers = [bind_ip]
    assert '1.2.3.4' == str(resolver.query(f'ns-foo.test.{domain}.', 'a')[0])


def test_delegate_dns(request, pytestconfig, host):
    certs = request.session.infrastructure.certs()
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))
    url = f"https://api.{domain}"
    s = requests.Session()
    data = {
        "name": "bar",
        "ip": "5.6.7.8",
    }
    r = s.post(f'{url}/delegate-dns/', json=data, timeout=60, verify=certs)
    # print(r.text)
    r.raise_for_status()
    resolver = dns.resolver.Resolver()
    bind_ip = str(resolver.query(f'bind.{domain}.')[0])
    resolver.nameservers = [bind_ip]
    assert '5.6.7.8' == str(resolver.query(f'ns-bar.d.{domain}.', 'a')[0])


def test_ping(request, pytestconfig, host):
    certs = request.session.infrastructure.certs()
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))
    url = f"https://api.{domain}"
    s = requests.Session()
    r = s.get(f'{url}/ping/', timeout=60, verify=certs)
    r.raise_for_status()
    assert 'pong' == r.text
