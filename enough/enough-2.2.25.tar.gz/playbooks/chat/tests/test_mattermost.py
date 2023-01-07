from enough.common import retry

testinfra_hosts = ['ansible://chat-host']


def test_mattermost(host):
    with host.sudo():
        host.run("apt-get install -y curl")

    @retry.retry(AssertionError, tries=5)
    def run():
        r = host.run("curl -s -m 5 https://chat.$(hostname -d)")
        assert r.rc == 0
        assert 'Mattermost' in r.stdout

    run()
