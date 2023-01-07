# pylint: disable=line-too-long
# flake8: noqa
import os
import posixpath
from raft import task
from raft.collection import Collection


@task
def pan(ctx, host, bucket, namespace, cert,
        profile=None, region=None, passphrase=None):
    """
    uploads the specified cert and key files to a panos device.  the username
    and password used to access the api must be specified by the
    PALO_ALTO_USERNAME and PALO_ALTO_PASSWORD environment variables
    """
    import requests
    from boto3 import Session
    from xml.etree import ElementTree as ET
    from OpenSSL.crypto import dump_privatekey
    from OpenSSL.crypto import load_privatekey
    from OpenSSL.crypto import FILETYPE_PEM
    session = requests.Session()
    session.verify = False
    aws_session = Session(profile_name=profile, region_name=region)
    s3 = aws_session.client('s3')
    s3_key = posixpath.join(namespace, cert)
    username = os.environ['PALO_ALTO_USERNAME']
    password = os.environ['PALO_ALTO_PASSWORD']
    base_url = f'https://{host}/api/'

    print('generating api key')
    data = dict(user=username, password=password)
    data['type'] = 'keygen'
    doc = session.post(base_url, data=data)
    root = ET.fromstring(doc.text)
    api_key = root.find('result/key').text
    session.headers = {
        'X-PAN-KEY': api_key,
    }

    print(f'reading cert from s3://{bucket}/{s3_key}')
    response = s3.get_object(Bucket=bucket, Key=f'{s3_key}.crt')

    print(f'importing certificate as {cert}')
    params = {
        'type': 'import',
        'category': 'certificate',
    }
    data = {
        'type': 'import',
        'category': 'certificate',
        'certificate-name': cert,
        'format': 'pem',
        'key': api_key,
    }
    files = dict(file=response['Body'].read())
    response = session.post(base_url, params=params, data=data, files=files)
    print(f'{response.text}')

    print(f'reading key from s3://{bucket}/{s3_key}.key')
    response = s3.get_object(Bucket=bucket, Key=f'{s3_key}.key')
    print(f'importing key to {cert}')
    params['category'] = data['category'] = 'private-key'
    # all private keys uploaded to the palo alto require a passphrase.
    # when the cert has no passphrase, add a passphrase of `stupid_palo_alto`
    # because, well, that's stupid.
    stupid_palo_alto = 'stupid_palo_alto'
    data['passphrase'] = passphrase or stupid_palo_alto
    x509_key = response['Body'].read()
    if not passphrase:
        x509_key = load_privatekey(FILETYPE_PEM, x509_key)
        x509_key = dump_privatekey(
            FILETYPE_PEM,
            x509_key,
            passphrase=stupid_palo_alto.encode())
    files = dict(file=x509_key)
    response = session.post(base_url, params=params, data=data, files=files)
    print(f'{response.text}')

    print('committing')
    xml = '<commit><description>imported certificate from secure_sedge</description></commit>'
    data = {
        'type': 'commit',
        'cmd': xml,
        'key': api_key,
    }
    response = session.post(base_url, data=data)
    print(f'{response.text}')


@task
def linux(ctx, bucket, cert_key, private_key, services=None, profile=None):
    """
    installs certs to /etc/ssl/certs
    installs keys to /etc/ssl/private
    services is a comma separated list of services to reload once
    the keys have been updated
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    filename = os.path.join('/etc/ssl/certs', os.path.basename(cert_key))
    s3.download_file(bucket, cert_key, filename)
    filename = os.path.join('/etc/ssl/private', os.path.basename(private_key))
    s3.download_file(bucket, private_key, filename)
    if services:
        services = services.split(',')
        services = [ x.strip() for x in services ]
        for x in services:
            ctx.run(f'systemctl reload {x}')


@task
def redis(
        ctx, bucket, cert_key, private_key, redis_dir='/var/lib/redis',
        host=None, port=6379, profile=None):
    """
    installs certs and keys to redis_dir
    uses the redis-cli to update the certs
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    cert = os.path.join(redis_dir, 'redis.crt')
    s3.download_file(bucket, cert_key, cert)
    key = os.path.join(redis_dir, 'redis.key')
    s3.download_file(bucket, private_key, key)
    host = host or os.environ.get('HOST')
    with ctx.cd(redis_dir):
        for x in cert, key:
            ctx.run(f'chown redis:redis {x}')
        ctx.run(f'chmod 0640 {key}')
        ctx.run(f'chmod 0644 {cert}')
    ctx.run(
        f'redis-cli --tls -h {host} -p {port} config '
        f'set tls-cert-file "{os.path.basename(cert)}"')
    ctx.run(
        f'redis-cli --tls -h {host} -p {port} config '
        f'set tls-key-file "{os.path.basename(key)}"')


@task
def postgres(
        ctx, bucket, cert, key, dest_dir='/etc/postgresql/ssl',
        reload=True, command='pg_ctlcluster 15 main reload',
        config_file=None, profile=None):
    """
    installs certs and keys to dest_dir as postgres.crt and postgres.key
    by default, we will call the reload command specified after downloading
    to force postgres to reload the ssl certs
    if config_file is specified, the installer will update the
    `ssl_cert_file` and `ssl_key_file` parameters using sed
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    dest_cert = os.path.join(dest_dir, 'postgres.crt')
    s3.download_file(bucket, cert, dest_cert)
    dest_key = os.path.join(dest_dir, 'postgres.key')
    s3.download_file(bucket, key, dest_key)
    for x in dest_cert, dest_key:
        ctx.run(f'chown postgres:postgres {x}')
    ctx.run(f'chmod 0600 {dest_key}')
    ctx.run(f'chmod 0644 {dest_cert}')
    if config_file:
        ctx.run(f"sed -i -e 's,^ssl_cert_file.*,ssl_cert_file = '\"'\"'{dest_cert}'\"'\"',g' {config_file}")
        ctx.run(f"sed -i -e 's,^ssl_key_file.*,ssl_key_file = '\"'\"'{dest_key}'\"'\"',g' {config_file}")
    if reload:
        ctx.run(command)


@task
def xrdp(ctx, bucket, cert_key, private_key, profile=None):
    """
    installs certs to /etc/ssl/certs
    installs keys to /etc/ssl/private
    services is a comma separated list of services to reload once
    the keys have been updated
    """
    from boto3 import Session
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    filename = '/etc/xrdp/cert.pem'
    s3.download_file(bucket, cert_key, filename)
    filename = '/etc/xrdp/key.pem'
    s3.download_file(bucket, private_key, filename)


@task
def iis(ctx, bucket, key, sites='', password=None, profile=None):
    """
    installs pfx to `cert:/localmachine/my`
    installs cert to one or more iis sites (separate with comma)
    if no sites are specified, will install the ssl certs to any unnamed sites
      e.g., *:443:

    example:

        sedge install.iis -b ssl.example.com -k wildcard.pfx `
            --sites www.example.com,site2.example.com
    """
    from .sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(ctx, bucket, key, profile, password)
    sites = sites.split(',')
    suffix = """
    ipmo webadministration
    $bindings = Get-WebBinding -Name $site -Protocol https
    foreach ($binding in $bindings) {
        $pieces = $binding.bindingInformation.split(':')
        $bsite = $pieces[-1]
        if ($bsite -ne $site) {
            Write-Host "skipping $($bsite), not a match"
            continue
        }
        if ($binding.certificateHash -eq $thumbprint) {
            Write-Host "skipping $($binding.bindingInformation), cert already installed"
            continue
        }
        Write-Host "updating certificate for $($binding.bindingInformation)"
        $binding.addSslCertificate($thumbprint, 'my')
    }
    """
    for site in sites:
        lines = [
            f"$site = '{site}'",
            f"$thumbprint = '{thumbprint}'",
            suffix,
        ]
        c = '\n'.join(lines)
        ctx.run(c)


@task
def rds(ctx, bucket, key, password=None, profile=None):
    """
    installs pfx to `cert:/localmachine/my`
    installs cert for use with rds
    """
    from .sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, password, 'my')
    c = (
        rf"""
        $klass = 'Win32_TSGeneralSetting'
        $ns = 'root\cimv2\terminalservices'
        $thumbprint = '{thumbprint}'
        $path = Get-WmiObject -class $klass -Namespace $ns -Filter "TerminalName=`'RDP-tcp`'"
        if ($path.sslcertificatesha1hash -ne $thumbprint) {'{'}
            $hash = @{'{'}SSLCertificateSHA1Hash=$thumbprint{'}'}
            Set-WmiInstance -Path $path.__path -argument $hash
        {'}'}
        $cert = Get-Item "cert:/localmachine/my/$($thumbprint)"
        $filename = $cert.privatekey.cspkeycontainerinfo.uniquekeycontainername
        $root = 'c:\programdata\microsoft\crypto\rsa\machinekeys'
        $p = [io.path]::combine($root, $filename)
        $root = 'c:\programdata\microsoft\crypto\keys'
        $private_key = [Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
        $q = $private_key.key.UniqueName
        $q = [io.path]::combine($root, $q)
        $rule = new-object security.accesscontrol.filesystemaccessrule 'NETWORK SERVICE', 'Read', allow
        if ([io.file]::exists($p)) {'{'}
            $acl = get-acl -path $p
            $acl.addaccessrule($rule)
            echo "modifying acl on $p"
            set-acl $p $acl
        {'}'}
        if ([io.file]::exists($q)) {'{'}
            $acl = get-acl -path $q
            $acl.addaccessrule($rule)
            echo "modifying acl on $q"
            set-acl $q $acl
        {'}'}
        """
    )
    print(c)
    ctx.run(c)


@task
def winrm(ctx, bucket, key, password=None, profile=None):
    """
    installs pfx to `cert:/localmachine/my`
    installs cert for use with winrm

    if you encounter ssl error 234, check the sslbindings https://stackoverflow.com/questions/21859308/failed-to-enumerate-ssl-bindings-error-code-234
    if you encounter internal error with SSL library, that usually means you have to enable schannel for tls 1.2
      https://docs.rackspace.com/support/how-to/enabling-tls-1.2-on-windows-server/
    """
    from .sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, password, 'my')
    c = (
        rf"""
        $thumbprint = '{thumbprint}'
        $cert = Get-Item "cert:/localmachine/my/$($thumbprint)"
        $filename = $cert.privatekey.cspkeycontainerinfo.uniquekeycontainername
        $root = 'c:\programdata\microsoft\crypto\rsa\machinekeys'
        $p = [io.path]::combine($root, $filename)
        $root = 'c:\programdata\microsoft\crypto\keys'
        $private_key = [Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
        $q = $private_key.key.UniqueName
        $q = [io.path]::combine($root, $q)
        $rule = new-object security.accesscontrol.filesystemaccessrule 'NETWORK SERVICE', 'Read', allow
        foreach ($x in @($p, $q)) {'{'}
            if ([io.file]::exists($p)) {'{'}
                $acl = get-acl -path $x
                $acl.addaccessrule($rule)
                echo "modifying acl on $x"
                set-acl $x $acl
            {'}'}
        {'}'}
        $valueset = @{'{'}
            Hostname = $cert.subject.split('=', 2)[1]
            CertificateThumbprint = $thumbprint
        {'}'}

        $selectorset = @{'{'}
            Transport = 'HTTPS'
            Address = '*'
        {'}'}
        Remove-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet $selectorset
        New-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet $selectorset -ValueSet $valueset
        """
    )
    print(c)
    ctx.run(c)


@task
def exchange(ctx, bucket, key, connector=None, password=None, profile=None):
    from sedge.sewer import install_cert_on_windows
    thumbprint = install_cert_on_windows(
        ctx, bucket, key, profile, pfx_password=password)
    lines = [ f"""
    Add-PSSnapin -Name Microsoft.Exchange.Management.PowerShell.SnapIn
    ipmo webadministration
    Enable-ExchangeCertificate -Thumbprint '{thumbprint}' -services 'iis,smtp'
    """, ]
    if connector:
        lines. append(f"""
        $pfx = Get-Item 'cert:/localmachine/my/{thumbprint}'
        $name = "<I>$($pfx.issuer)<S>$($pfx.subject)"
        Write-Host $name
        Set-SendConnector -Identity '{connector}' -TLSCertificateName $name
        """)
    lines.append('Restart-Service -Name MSExchangeTransport')
    c = '\n'.join(lines)
    ctx.run(c)


installers_collection = Collection(
    pan,
    linux,
    iis,
    exchange,
    rds,
    xrdp,
    winrm,
    redis,
    postgres,
)
