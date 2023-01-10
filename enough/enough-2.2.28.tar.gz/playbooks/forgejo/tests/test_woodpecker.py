import yaml
import os

from enough.common import retry
from playbooks.hostea.roles.hostea.files import hosteasetup

testinfra_hosts = ['ansible://forgejo-host']


def get_domain(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return yaml.safe_load(open(vars_dir + '/domain.yml'))['domain']


def test_woodpecker_run(request, pytestconfig, host, tmpdir):
    certs = request.session.infrastructure.certs()
    domain = host.run("hostname -d").stdout.strip()
    deploy = f"{tmpdir}/key"
    os.system(f"ssh-keygen -q -f {deploy} -N ''")

    hostea = hosteasetup.Hostea(
        certs=certs,
        forgejo_hostname=f'forgejo.{domain}',
        admin_user="root",
        admin_password="etquofEtseudett",
        user="testuser1",
        password="etquoaoiusdf53",
        email="contact+testuser1@enough.community",
        project="testproject",
        woodpecker_hostname=f'woodpecker.{domain}',
        debug=True,
        deploy=deploy)

    hostea.destroy()
    hostea.setup()
    hostea.update_project("playbooks/forgejo/tests/woodpecker")

    expected_file = "/tmp/out/done"
    with host.sudo():
        host.run(f"rm -f {expected_file}")

    @retry.retry(AssertionError, tries=9)
    def wait_for_expected_file():
        assert host.file(expected_file).exists
    wait_for_expected_file()

    hostea.forgejo_browser.revoke_application("woodpecker")
