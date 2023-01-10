import json

from enough import settings
from enough.common import ansible_utils

testinfra_hosts = ['ansible://cloud-host']


def test_nextcloud(host):
    with host.sudo():
        host.run("apt-get install -y curl")
    cmd = host.run("""
    set -xe
    curl --silent https://cloud.$(hostname -d)/login |
       grep --quiet 'This application requires JavaScript'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc


def test_nextcloud_apps(host, pytestconfig):
    cmd = host.run("""
        set -xe
        cd /srv/nextcloud/apache/
        docker-compose exec -T -u www-data app php -f occ app:list --output=json
    """)
    assert 0 == cmd.rc

    playbook = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR,
                                      inventories=['playbooks/enough/inventory'])
    apps = playbook.get_role_variable('nextcloud', 'enough_nextcloud_apps', 'cloud-host')
    apps = set(eval(apps))
    # ensure apps are enabled
    assert apps <= set(json.loads(cmd.stdout)['enabled'])
