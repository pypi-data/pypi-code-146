def update(host):
    with host.sudo():
        cmd = host.run("""
        set -xe
        flock /tmp/update-website \
              bash -x /srv/update-website.sh \
              >> /var/log/update-website.log 2>&1
        grep --quiet -i enough /usr/share/nginx/html/index.html
        """)
        print(cmd.stdout)
        print(cmd.stderr)
        assert 0 == cmd.rc
