testinfra_hosts = ['ansible://bind-host']


#
# Enough is installed on bind-host using the script from packages-host
#
def test_enough_pip(host):
    assert host.file("/usr/local/bin/enough-build-docker-image.sh").exists
    cmd = host.run("""
    set -ex
    docker run --rm --entrypoint enough enough --help > /tmp/e
    cat /tmp/e
    grep -q 'service create' /tmp/e
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
