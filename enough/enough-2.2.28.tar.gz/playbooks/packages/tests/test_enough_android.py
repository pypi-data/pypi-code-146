testinfra_hosts = ['ansible://packages-host']


def test_enough_android(host):
    cmd = host.run("""
    set -xe
    flock /tmp/update-packages \
          bash -x /srv/enough-android-update-packages.sh
    test -f /usr/share/nginx/html/enough.apk
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
