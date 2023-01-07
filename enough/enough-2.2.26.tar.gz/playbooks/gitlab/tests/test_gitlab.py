import urllib3
import os
import testinfra
import time

import gitlab_utils
from enough.common.gitlab import GitLab

testinfra_hosts = ['ansible://gitlab-host']


def test_ci_runner(request, host, tmpdir):
    certs = request.session.infrastructure.certs()
    domain = host.run("hostname -d").stdout.strip()
    runner_host = testinfra.host.Host.get_host(
        'ansible://runner-host',
        ansible_inventory=host.backend.ansible_inventory)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    gitlab = GitLab(f'https://lab.{domain}')
    gitlab.certs(certs)
    gitlab.login('root', gitlab_utils.get_password())
    gitlab.recreate_project('root', 'testproject')
    runner_host.run("rm -f /tmp/*.out")
    os.system("""
    set -ex
    cd {directory}
    test -d testproject && exit 0
    mkdir testproject
    cd testproject
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
    (
     echo 'jobs:'
     echo '  script: docker ps > /srv/DOCKER.out 2>&1'
    ) > .gitlab-ci.yml
    git add .gitlab-ci.yml
    git commit -m 'test'
    git config http.sslVerify false
    git remote add origin \
         https://root:{password}@{address}/root/testproject.git
    git push -u origin master
    """.format(password=gitlab_utils.get_password(),
               address=f'lab.{domain}',
               directory=str(tmpdir)))

    for (what, expected) in (('DOCKER', 'CONTAINER'),):
        success = False
        for _ in range(40):
            if (runner_host.file('/srv/' + what + '.out').exists and
                    runner_host.file('/srv/' + what + '.out').contains(
                        expected)):
                success = True
                break
            time.sleep(5)
        assert success


def test_docker_cleanup(host):
    runner_host = testinfra.host.Host.get_host(
        'ansible://runner-host',
        ansible_inventory=host.backend.ansible_inventory)

    with runner_host.sudo():
        cmd = runner_host.run("/etc/cron.daily/docker-cleanup")
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert 'Total reclaimed space' in cmd.stdout


def test_notify_email(host):
    domain = host.run("hostname -d").stdout.strip()
    with host.sudo():
        cmd = host.run("systemctl stop postfix")
        command = """\
        docker exec --user git gitlab bin/rails runner -e production \
             "Notify.test_email('root', 'Message Subject', 'Message Body').deliver_now"
        """
        cmd = host.run(command)
        print(cmd.stdout)
        print('--------------------------')
        print(cmd.stderr)
        assert 1 == cmd.rc
        #
        # we're not testing if mail can actually be delivered, only if the
        # SMTP server configured in GitLab is the one we expected
        #
        assert (f'Connection refused - connect(2) for "gitlab-host.{domain}" '
                'port 25 (Errno::ECONNREFUSED)')
