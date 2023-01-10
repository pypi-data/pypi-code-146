testinfra_hosts = ['ansible://forum-host']


def test_discourse(host):
    cmd = host.run("""
    set -xe
    sudo apt-get install -y curl
    curl --silent https://forum.$(hostname -d) | \
       grep --quiet 'Welcome to Discourse'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
