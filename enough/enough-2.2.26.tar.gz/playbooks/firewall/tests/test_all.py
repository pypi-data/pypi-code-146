testinfra_hosts = ['ansible://client-host']


def test_server_visible_from_client(host):
    server_host = host.get_host('ansible://server-host',
                                ansible_inventory=host.backend.ansible_inventory)
    server_ip = server_host.ansible.get_variables()['ansible_host']
    with host.sudo():
        host.run("apt-get install -y nmap")

    #
    # TCP
    #
    r = host.run("nmap  -oG - -Pn -p 1-1024,5665 " + server_ip)
    assert r.rc == 0
    assert ("Ports: "
            "22/open/tcp//ssh///, "
            "53/closed/tcp//domain///, "
            "80/closed/tcp//http///, "
            "443/closed/tcp//https///, "
            "465/closed/tcp//smtps///, "
            "5665/closed/tcp//unknown///\t") in r.stdout
    #
    # UDP
    #
    with host.sudo():
        r = host.run("nmap  -oG - -sU -Pn " + server_ip)
        assert r.rc == 0
    assert ("Ports: "
            "53/closed/udp//domain///\t") in r.stdout
    #
    # ICMP
    #
    r = host.run("ping -W 5 -c 1 " + server_ip)
    assert r.rc == 0
    assert ', 0% packet loss' in r.stdout


def test_server_visible_from_external(host):
    external_host = host.get_host('ansible://external-host',
                                  ansible_inventory=host.backend.ansible_inventory)
    server_host = host.get_host('ansible://server-host',
                                ansible_inventory=host.backend.ansible_inventory)
    server_ip = server_host.ansible.get_variables()['ansible_host']
    with external_host.sudo():
        external_host.run("apt-get install -y nmap")
    #
    # TCP
    #
    r = external_host.run("nmap  -oG - -Pn " + server_ip)
    assert r.rc == 0
    assert ("Ports: "
            "22/open/tcp//ssh///, "
            "53/closed/tcp//domain///, "
            "80/closed/tcp//http///, "
            "443/closed/tcp//https///\t") in r.stdout
    #
    # ICMP
    #
    r = external_host.run("ping -W 5 -c 1 " + server_ip)
    assert r.rc == 1
    assert ', 100% packet loss' in r.stdout


def test_gitlab_visible_from_client(host):
    gitlab_host = host.get_host('ansible://gitlab-host',
                                ansible_inventory=host.backend.ansible_inventory)
    gitlab_ip = gitlab_host.ansible.get_variables()['ansible_host']
    with host.sudo():
        host.run("apt-get install -y nmap")
    #
    # TCP
    #
    r = host.run("nmap  -oG - -Pn -p 2222 " + gitlab_ip)
    assert r.rc == 0
    assert ("Ports: "
            "2222/open/tcp//EtherNetIP-1///") in r.stdout
