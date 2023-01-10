testinfra_hosts = ['ansible://bind-host', 'ansible://bind-client-host']


def test_resolvconf(host):
    resolvconf_before = host.run("cat /etc/resolv.conf").stdout.strip()
    with host.sudo():
        host.run("""
        for i in eth0 eth1 ens3 ens7 enp1s0 enp2s0 ; do
          ifdown $i
          ifup $i
        done
        """)
    resolvconf_after = host.run("cat /etc/resolv.conf").stdout.strip()
    assert resolvconf_before == resolvconf_after
