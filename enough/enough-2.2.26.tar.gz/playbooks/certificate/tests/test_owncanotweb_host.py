testinfra_hosts = ['ansible://owncanotweb-host']


def test_ownca_files_present(host):
    host.file("/etc/ssl/certs/enough.pem").exists
    domain = host.run("hostname -d").stdout.strip()
    host.file(f"/etc/certificates/{domain}.crt").exists
