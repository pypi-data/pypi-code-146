import os
import yaml
import sh
import shutil

from enough.common import retry

from playbooks.hostea.roles.hostea.files import hosteasetup

testinfra_hosts = ['ansible://gitea-host']


def get_domain(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return yaml.safe_load(open(vars_dir + '/domain.yml'))['domain']


def test_hosteasetup_gitea(request, pytestconfig, host, tmpdir):
    certs = request.session.infrastructure.certs()
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))

    #
    # Login Gitea
    #
    gitea = hosteasetup.Gitea(f'gitea.{domain}')
    gitea.certs(certs)
    username = "root"
    password = "etquofEtseudett"
    gitea.authenticate(username=username, password=password)
    u = gitea.users.get("root")
    assert u.username == "root"
    #
    # Create project
    #
    gitea.projects.delete(username, "testproject")
    assert gitea.projects.get(username, "testproject") is None
    p = gitea.projects.create(username, "testproject")
    assert p.project == "testproject"


def get_fleet_domain(d):
    domain_file = f"{d}/inventory/group_vars/all/domain.yml"
    assert os.path.isfile(domain_file)
    return yaml.safe_load(open(domain_file))['domain']


@retry.retry(AssertionError, tries=60, delay=30, exponential=False)
def wait_for_bootstrap(git, d, gitea_domain):
    #
    # Wait for the bind-host to be created
    #
    shutil.rmtree(d, ignore_errors=True)
    git.clone(f"https://root:etquofEtseudett@gitea.{gitea_domain}/hostea/hostea", d)
    domain = get_fleet_domain(d)
    hosts_file = f"{d}/inventory/hosts.yml"
    assert os.path.isfile(hosts_file)
    #
    # Wait for the Ansible playbook to finish running
    #
    assert os.path.isfile(f"{d}/bind-host-configured")
    #
    # Wait for the DNS to respond
    #
    bind_ip = yaml.safe_load(open(hosts_file))['live']['hosts']['bind-host']['ansible_host']
    try:
        dig_ip = sh.timeout("10", "dig", "@8.8.8.8", "+short", f"bind-host.{domain}")
    except sh.ErrorReturnCode_124:
        assert 0, "timeout"
    assert bind_ip == dig_ip.strip()


def wait_for_destruction(stack):
    clouds = "playbooks/hostea/templates/clouds.yml"
    assert os.path.isfile(clouds), f"{clouds} is not found, copy and adapt {clouds}.sample"
    openstack = sh.openstack.bake(
        '--os-cloud', 'production',
        _tty_out=False,
        _truncate_exc=False,
        _env={
            'OS_CLIENT_CONFIG_FILE': clouds,
            'PATH': os.getenv('PATH'),
        },
    )
    stacks = openstack.stack.list()
    assert stack in stacks

    @retry.retry(AssertionError, tries=20, delay=30, exponential=False)
    def wait():
        stacks = openstack.stack.list()
        assert stack not in stacks
    wait()


def test_hostea_bootstrap(request, pytestconfig, host, tmpdir):
    #
    # Instructions to debug
    #
    # virsh domifaddr gitea-host
    # add the IP to /etc/hosts something like
    # 10.23.10.212 gitea.hostea.test woodpecker.hostea.test
    # login gitea.hostea.test with user hostea password etquofEtseudett
    #    as found in inventory/host_vars/gitea-host/gitea.yml
    # login woodpecker.hostea.test
    # check the CI runs logs
    #
    gitea_domain = get_domain(pytestconfig.getoption("--ansible-inventory"))
    d = f"{tmpdir}/hostea"
    git = sh.git.bake("-c", "http.sslVerify=false")

    wait_for_bootstrap(git, d, gitea_domain)

    #
    # this will be overririden if the playbook runs again and the
    # bind-host created again.
    #
    destroy = f"{d}/hosts-scripts/bind-host.sh"
    open(destroy, "w").write("""
    enough --domain $domain host delete bind-host
    rm /tmp/hostea/.enough/$domain/inventory/hosts.yml
    rm inventory/hosts.yml
    rm /tmp/hostea/.enough/$domain/{.woodpecker.yml,hostea.sh}
    rm .woodpecker.yml hostea.sh
    """)
    git = git.bake("-C", d)
    git.add("hosts-scripts/bind-host.sh")
    git.config("user.email", "test@hostea.org")
    git.config("user.name", "Test")
    git.commit("-m", "Destroy bind-host")
    git.push("-u", "origin", "master")

    wait_for_destruction("bind-host")
