testinfra_hosts = ['ansible://forgejo-host']


def test_admin_user(host):
    with host.sudo():
        cmd = host.run("docker exec --user 1000 forgejo gitea admin user list --admin")
        print(cmd.stdout)
        print('--------------------------')
        print(cmd.stderr)
        assert 0 == cmd.rc
        assert "root" in cmd.stdout
