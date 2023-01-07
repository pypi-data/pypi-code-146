from collections import defaultdict
from dataclasses import dataclass
from glob import glob
import logging
import os
import platform
import posixpath
import socket
import sys
from tempfile import NamedTemporaryFile
from typing import Sequence, Dict, List, Set, Iterable

from raft import task
import yaml
from boto3 import Session
from sewer.auth import ErrataItemType
from sewer.client import Client
from sewer.config import ACME_DIRECTORY_URL_STAGING  # noqa: F401, pylint: disable=unused-import
from sewer.dns_providers.common import dns_challenge
from sewer.dns_providers.route53 import Route53Dns as SewerRoute53Dns


log = logging.getLogger(__name__)


@dataclass
class Route53Change:
    name: str = None
    values: Set[str] = None
    domain: str = None
    zone_id: str = None
    action: str = 'UPSERT'
    record_type: str = 'TXT'
    ttl: int = 60

    def __post_init__(self):
        if self.domain and not self.domain.endswith('.'):
            self.domain = f'{self.domain}.'


class Route53Dns(SewerRoute53Dns):
    def __init__(self, profile=None):
        super().__init__()
        self.session = Session(profile_name=profile)
        self.r53 = self.session.client('route53', config=self.aws_config)
        self.waiter = self.r53.get_waiter('resource_record_sets_changed')
        self.resource_records = defaultdict(set)
        self.change_map: Dict[str, Route53Change] = {}
        self.zone_ids = {}
        self.deletes = []
        self.undos: List[Route53Change] = []

    def setup(self, challenges: Sequence[Dict[str, str]]) -> Sequence[ErrataItemType]:
        for x in challenges:
            domain_name = x['ident_value']
            value = dns_challenge(x['key_auth'])
            challenge_domain = f'_acme-challenge.{domain_name}.'
            self.resource_records[challenge_domain].add(value)
            change = self.change_map.setdefault(
                challenge_domain,
                Route53Change(
                    name=challenge_domain,
                    domain=domain_name,
                    record_type='TXT',
                    values=set(),
                ))
            change.values.add(f'"{value}"')
        self.find_zone_ids()
        self.handle_existing()
        self.create_dns_record(domain_name=None, domain_dns_value=None)
        return []

    def find_zone_ids(self):
        for x in self.change_map.values():
            pieces = x.domain.split('.')
            while pieces:
                d = '.'.join(pieces)
                log.info('[route53] finding zone id for %s', d)
                zone_id = self.zone_ids.get(d)
                if not zone_id:
                    response = self.r53.list_hosted_zones_by_name(DNSName=d)
                    for zone in response['HostedZones']:
                        if zone['Name'] == d:
                            zone_id = self.zone_ids[d] = zone['Id']
                            break
                if zone_id:
                    x.zone_id = zone_id
                    log.info('[route53] %s => %s', d, zone_id)
                    break
                pieces = pieces[1:]

    def change_batch(self, changes: List[Route53Change]):
        return {
            'Comment': 'letsencrypt dns certificate validation changes',
            'Changes': [{
                'Action': x.action,
                'ResourceRecordSet': {
                    'Name': x.name,
                    'Type': x.record_type,
                    'TTL': x.ttl,
                    'ResourceRecords': [
                        dict(Value=value)
                        for value in x.values
                    ],
                },
            } for x in changes],
        }

    def handle_existing(self):
        domain_records = defaultdict(list)
        paginator = self.r53.get_paginator('list_resource_record_sets')
        for domain, st_id in self.zone_ids.items():
            log.info('[route53] listing zone for %s', domain)
            rg = paginator.paginate(HostedZoneId=st_id)
            for page in rg:
                domain_records[st_id] += page['ResourceRecordSets']
            log.info('[route53] found %s records', len(domain_records[st_id]))
        for x in self.change_map.values():
            records = domain_records[x.zone_id]
            for record in records:
                if record['Name'] == x.name:
                    log.info(
                        '[route53] found existing record for %s / %s',
                        x.name, record['Type'])
                    change = Route53Change(
                        name=record['Name'],
                        record_type=record['Type'],
                        values={ lx["Value"] for lx in record['ResourceRecords'] },
                        ttl=record['TTL'],
                        action='DELETE',
                        domain=x.domain,
                        zone_id=x.zone_id,
                    )
                    if record['Type'] != x.record_type:
                        self.deletes.append(change)
                    else:
                        change.action = 'UPSERT'
                        self.undos.append(change)

    @classmethod
    def by_zone_id(cls, rg: Iterable[Route53Change]):
        by_zone_id = defaultdict(list)
        for x in rg:
            by_zone_id[x.zone_id].append(x)
        return by_zone_id

    def wait(self, zone_id, change_id):
        log.info('[route53 / %s] waiting for %s', zone_id, change_id)
        self.waiter.wait(Id=change_id, WaiterConfig=dict(
            Delay=5,
            MaxAttempts=24,
        ))
        log.info('[route53 / %s] change is complete', zone_id)

    def change_and_wait(self, changes: Iterable[Route53Change]):
        result = {}
        for x in changes:
            log.info(
                '[route53] %s (%s) %s => %s',
                x.action, x.record_type, x.name, x.values)
        for zone_id, zone_changes in self.by_zone_id(changes).items():
            response = self.r53.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch=self.change_batch(zone_changes),
            )
            change_id = response['ChangeInfo']['Id']
            result[zone_id] = change_id
        for zone_id, change_id in result.items():
            self.wait(zone_id, change_id)
        return result

    def create_dns_record(self, domain_name, domain_dns_value):
        if domain_name and domain_dns_value:
            change = self.change_map.get(domain_name)
            if change:
                change.values.add(domain_dns_value)
        if self.deletes:
            self.change_and_wait(self.deletes)
        result = self.change_and_wait(self.change_map.values())
        return result

    def clear(self, challenges: Sequence[Dict[str, str]]) -> Sequence[ErrataItemType]:
        self.delete_dns_record(None, None)
        return []

    def delete_dns_record(self, domain_name, domain_dns_value):
        for x in self.change_map.values():
            if x.action == 'UPSERT':
                x.action = 'DELETE'
            elif x.action == 'DELETE':
                x.action = 'UPSERT'
        result = self.change_and_wait(self.change_map.values())
        for x in self.deletes:
            x.action = 'UPSERT'
            self.undos.append(x)
        if self.undos:
            self.change_and_wait(self.undos)
        return result


def new_cert(hostname, alt_domains, email=None, profile=None):
    """
    :param str hostname:
        the fqdn of the local host for which we are creating the cert

    :param str alt_domains:
        a comma-separated list of alternative domains to also
        requests certs for.

    :param str email:
        the email of the contact on the cert

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials
    """
    alt_domains = alt_domains.split(',') if alt_domains else []
    client = Client(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=Route53Dns(profile), ACME_AUTH_STATUS_WAIT_PERIOD=5,
        ACME_AUTH_STATUS_MAX_CHECKS=180, ACME_REQUEST_TIMEOUT=60,
        LOG_LEVEL='INFO')
    certificate = client.cert()
    account_key = client.account_key
    key = client.certificate_key
    return certificate, account_key, key


def get_certificate(ns, hostname, profile=None):
    if not ns.startswith('/'):
        ns = f'/{ns}'
    hostname = hostname.replace('*', 'star')
    try:
        session = Session(profile_name=profile)
        ssm = session.client('ssm')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'account_key' ])
        account_key = get_chunked_ssm_parameter(name, profile=profile)
        log.info('account key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'key' ])
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        key = response['Parameter']['Value']
        log.info('private key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'cert' ])
        certificate = get_chunked_ssm_parameter(name, profile=profile)
        log.info('public cert retrieved')
    except:  # noqa: E722, pylint: disable=bare-except
        account_key = None
        key = None
        certificate = None
    return certificate, account_key, key


def get_file_from_s3(s3, bucket, ns, filename, decode=True):
    filename = filename.replace('*', 'star')
    key = filename
    if ns:
        key = posixpath.join(ns, key)
    log.info('retrieving s3://%s/%s', bucket, key)
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read()
    if decode:
        data = data.decode('utf-8')
    return data


def get_certificate_from_s3(bucket, ns, hostname, profile=None):
    hostname = hostname.replace('*', 'star')
    account_key = None
    key_content = None
    certificate = None
    try:
        session = Session(profile_name=profile)
        s3 = session.client('s3')
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception connecting to s3: %s', ex)
        return certificate, account_key, key_content

    try:
        account_key = get_file_from_s3(s3, bucket, None, 'global.account_key')
        log.info('account key retrieved')
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception getting account key: %s', ex)

    try:
        key_content = get_file_from_s3(s3, bucket, ns, f'{hostname}.key')
        log.info('private key retrieved')
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception getting private key: %s', ex)

    try:
        certificate = get_file_from_s3(s3, bucket, ns, f'{hostname}.crt')
        log.info('public cert retrieved')
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception retrieving public cert: %s', ex)
    return certificate, account_key, key_content


def get_chunked_ssm_parameter(name, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    rg = []
    for n in range(1, 10):
        try:
            st = f'{name}{n}'
            log.info('[ssm]  getting %s', st)
            response = ssm.get_parameter(Name=st, WithDecryption=True)
            rg.append(response['Parameter']['Value'])
        except:  # noqa: E722, pylint: disable=bare-except
            break
    data = ''.join(rg)
    return data


def get_pfx(bucket, key, profile=None):
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    key = key.replace('*', 'star')
    if not key.lower().endswith('.pfx'):
        key = f'{key}.pfx'
    pfx_data = get_file_from_s3(s3, bucket, None, key, False)
    log.info('[pfx]  read %s bytes', len(pfx_data))
    return pfx_data


def renew_cert(
        ns, hostname, alt_domains=None,
        email=None, bucket=None, tmp_dir=None, profile=None, **kwargs):
    if alt_domains:
        if isinstance(alt_domains, str):
            alt_domains = alt_domains.split(',')
    else:
        alt_domains = []
    _, account_key, key = get_certificate_from_s3(bucket, ns, hostname, profile)
    client = Client(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=Route53Dns(profile), account_key=account_key,
        certificate_key=key, ACME_AUTH_STATUS_WAIT_PERIOD=5,
        ACME_AUTH_STATUS_MAX_CHECKS=360, ACME_REQUEST_TIMEOUT=3)
    if not account_key:
        client.acme_register()
        content = client.account_key
        save_account_key(bucket, ns, content, tmp_dir, profile)
    if not key:
        client.create_certificate_key()
        content = client.certificate_key
        save_key(bucket, ns, hostname, content, tmp_dir, profile)
    certificate = client.renew()
    account_key = client.account_key
    key = client.certificate_key
    return certificate, account_key, key


def save_account_key(bucket, ns, content, tmp_dir, profile):
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    filename = 'global.account_key'
    save_to_temp(tmp_dir, filename, content)
    if isinstance(content, str):
        content = content.encode('utf-8')
    s3_key = filename
    s3.put_object(Bucket=bucket, Key=s3_key, Body=content, ACL='bucket-owner-full-control')


def save_key(bucket, ns, hostname, content, tmp_dir, profile):
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    hostname = hostname.replace('*', 'star')
    filename = f'{hostname}.key'
    save_to_temp(tmp_dir, filename, content)
    if isinstance(content, str):
        content = content.encode('utf-8')
    s3_key = posixpath.join(ns, filename)
    s3.put_object(Bucket=bucket, Key=s3_key, Body=content, ACL='bucket-owner-full-control')


def full_pfx(ctx, certificate, key, tmp_dir='/tmp', password=None):
    with NamedTemporaryFile(mode='w') as cert, \
            NamedTemporaryFile(mode='w') as f_key, \
            NamedTemporaryFile(mode='wb') as f_pfx:
        with open(cert.name, 'w') as f:
            f.write(certificate)
        with open(f_key.name, 'w') as f:
            f.write(key)
        os.chmod(cert.name, 0o644)
        os.chmod(f_key.name, 0o600)
        if not password:
            ctx.run(
                f'/usr/bin/openssl pkcs12 -export -in {cert.name} -inkey {f_key.name}'
                f' -out {f_pfx.name} -passout pass:')
        else:
            ctx.run(
                f'/usr/bin/openssl pkcs12 -export -in {cert.name} -inkey {f_key.name}'
                f' -out {f_pfx.name} -passout env:SEDGE_PASSWORD',
                env=dict(SEDGE_PASSWORD=password),
            )
        with open(f_pfx.name, 'rb') as f:
            data = f.read()
    return data


@task
def renew_all(ctx, dir_name=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str dir_name:
        the config directory

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(dir_name, 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    dir_name = os.path.join(dir_name, '*.yml')
    files = glob(dir_name)
    for filename in files:
        try:
            # don't let the failure of any one certificate
            # make it so that we don't try to renew the rest
            if filename.endswith('defaults.yml'):
                continue
            request_cert(ctx, filename, profile, defaults)
        except:  # noqa: E722, pylint: disable=bare-except, broad-except
            pass


def request_cert(ctx, filename, profile, defaults):
    log.info('processing %s', filename)
    with open(filename, 'r') as f:
        values = yaml.load(f, Loader=yaml.SafeLoader)
    for key, value in defaults.items():
        values.setdefault(key, value)
    namespaces = values.pop('namespaces', [])
    config_profile = values.pop('profile', None)
    pfx_password = values.pop('pfx_password', None)
    profile = profile or config_profile
    ns = namespaces[0]
    certificate, account_key, key = renew_cert(
        **values, ns=ns, profile=profile)
    tmp_dir = values.pop('tmp_dir', '/tmp')
    bucket = values.pop('bucket')
    buckets = values.pop('buckets') or []
    save_to_file(
        ctx, tmp_dir, values['hostname'],
        certificate, account_key, key)
    if bucket:
        found = False
        for x in buckets:
            if x['name'] == bucket:
                found = True
                break
        if not found:
            buckets.append(dict(name=bucket))
    for x in buckets:
        bucket = x['name']
        role = x.get('assume_role')
        profile = x.get('profile') or profile
        for namespace in namespaces:
            save_to_s3(
                ctx, bucket, namespace, values['hostname'], certificate,
                account_key, key, tmp_dir=tmp_dir, profile=profile,
                pfx_password=pfx_password, role=role)


@task
def request(ctx, filename=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str filename:
        the config file

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(os.path.dirname(filename), 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    request_cert(ctx, filename, profile, defaults)


def save_to_temp(tmp_dir, filename, content):
    filename = os.path.join(tmp_dir, filename)
    log.info('saving %s', filename)
    filename = filename.replace('*', 'star')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir, 0o755, True)
    if isinstance(content, str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        with open(filename, 'wb') as f:
            f.write(content)


def save_to_file(ctx, tmp_dir, hostname, certificate, account_key, key):
    """
    saves the contents of the certificate, key, and account keys
    to a local directory for debugging
    """
    contents = [
        ('.crt', certificate),
        ('.account_key', account_key),
        ('.key', key),
    ]
    for extension, content in contents:
        filename = f'{hostname}{extension}'
        save_to_temp(tmp_dir, filename, content)


def assume_role(session, role):
    sts = session.client('sts')
    r = sts.assume_role(RoleArn=role)
    creds = r['Credentials']
    return Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )


def save_to_s3(ctx, bucket, ns, hostname, certificate, account_key, key,
               tmp_dir='/tmp', profile=None, pfx_password=None, role=None):
    """
    saves the contents of the certificate, key, and account keys
    to a local directory for debugging
    """
    pfx_content = full_pfx(ctx, certificate, key, pfx_password)
    contents = [
        ('.crt', certificate),
        ('.key', key),
        ('.pfx', pfx_content),
    ]
    session = Session(profile_name=profile)
    if role:
        session = assume_role(session, role)
    s3 = session.client('s3')
    for extension, content in contents:
        filename = f'{hostname}{extension}'
        filename = filename.replace('*', 'star')
        filename = posixpath.join(ns, filename)
        log.info('saving s3://%s/%s', bucket, filename)
        if isinstance(content, str):
            content = content.encode('utf-8')
        s3.put_object(Bucket=bucket, Key=filename, Body=content, ACL='bucket-owner-full-control')


def save_to_ssm(ctx, ns, hostname, certificate, account_key, key, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pfx_data = full_pfx(ctx, certificate, key)
    hostname = hostname.replace('*', 'star')
    prefix = ns
    if not prefix.startswith('/'):
        prefix = f'/{prefix}'
    prefix = os.path.join(prefix, 'apps_keystore', hostname)
    contents = [
        ('account_key', account_key),
        ('cert', certificate),
    ]
    for suffix, content in contents:
        name = os.path.join(prefix, suffix)
        log.info('saving %s', name)
        save_chunked_ssm_parameter(ns, name, content, 'String', profile)

    contents = [
        ('key', key),
    ]
    for suffix, content in contents:
        name = os.path.join(prefix, suffix)
        log.info('saving %s', name)
        try:
            ssm.put_parameter(
                Name=name,
                Description=f'sewer / certbot {suffix}',
                Value=content,
                Overwrite=True,
                Type='SecureString',
                KeyId=f'alias/{ns}')
        except Exception as ex:  # pylint: disable=broad-except
            log.info('exception saving to ssm: %s', ex)

    name = os.path.join(prefix, 'pfx')
    save_chunked_ssm_parameter(ns, name, pfx_data, 'SecureString', profile)


def save_chunked_ssm_parameter(ns, name, value, type_, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pieces = []
    while value:
        pieces.append(value[:4096])
        value = value[4096:]
    for n, x in enumerate(pieces, 1):
        st = f'{name}{n}'
        log.info('saving %s', st)
        try:
            if type_ == 'SecureString':
                ssm.put_parameter(
                    Name=st,
                    Description='sewer / certbot',
                    Value=x,
                    Overwrite=True,
                    Type=type_,
                    KeyId=f'alias/{ns}')
            else:
                ssm.put_parameter(
                    Name=st,
                    Description='sewer / certbot',
                    Value=x,
                    Overwrite=True,
                    Type=type_)
        except Exception as ex:  # pylint: disable=broad-except
            log.info('exception saving to ssm: %s', ex)


@task
def install_cert(ctx, config, hostname=None):
    """
    installs a cert on the local system:

        on linux to /etc/ssl/certs
        on windows to cert:/localmachine/my
    """
    with open(config, 'r') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    ns = conf['namespace']
    profile = conf.get('profile')
    owner = conf.get('owner', 'root')
    group = conf.get('group', owner)
    cert_filename = conf.get('certificate')
    key_filename = conf.get('key')
    hostname = hostname or conf.get('hostname')
    pfx_password = conf.get('pfx_password')
    bucket = conf.get('bucket')
    if not hostname:
        hostname = get_hostname(ctx)
    if is_linux():
        install_cert_on_linux(
            ctx, ns, hostname, profile,
            cert_filename, key_filename, owner, group, bucket=bucket)
    elif is_windows():
        install_cert_on_windows(ctx, bucket, hostname, profile, pfx_password)


def get_hostname(ctx):
    if is_linux():
        result = ctx.run('/bin/hostname')
        return result.stdout.strip()
    if is_windows():
        result = socket.getfqdn()
        return result
    return None


def install_cert_on_linux(
        ctx, ns, hostname, profile, cert_filename, key_filename,
        owner, group, bucket=None):
    if bucket:
        certificate, _, key = get_certificate_from_s3(bucket, ns, hostname, profile)
    else:
        certificate, _, key = get_certificate(ns, hostname, profile)
    if not cert_filename:
        st = f'{hostname}.bundled.crt'
        cert_filename = os.path.join('/etc/ssl/certs', st)
    if not key_filename:
        key_filename = os.path.join('/etc/ssl/private', f'{hostname}.key')
    with open(cert_filename, 'w') as f:
        f.write(certificate)
    ctx.run(f'chmod 0644 {cert_filename}')
    ctx.run(f'chown {owner}:{group} {cert_filename}')
    with open(key_filename, 'w', encoding='utf-8') as f:
        f.write(key)
    ctx.run(f'chmod 0600 {key_filename}')
    ctx.run(f'chown {owner}:{group} {key_filename}')


def windows_version(ctx):
    c = r"""
    $key = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    $x = Get-ItemProperty $key
    Write-Host $x.ProductName
    """
    print('checking windows version')
    result = ctx.run(c)
    version = result.stdout.strip()
    return version


@task
def install_cert_on_windows(
        ctx, bucket, key, profile, pfx_password=None, store=None):
    """
    pull a file from s3 and install in the localmachine/my cert store
    """
    from cryptography.hazmat.primitives.serialization import pkcs12
    from cryptography.hazmat.primitives import hashes
    print('getting cert')
    pfx_data = get_pfx(bucket, key, profile)
    print('getting thumbprint')
    _, cert, _ = pkcs12.load_key_and_certificates(pfx_data, pfx_password)
    thumbprint = cert.fingerprint(hashes.SHA1()).hex().upper()
    f = NamedTemporaryFile(mode='w', delete=False)  # pylint: disable=consider-using-with
    filename = f.name
    print(f'importing pfx to cert store from {filename}')
    with open(filename, 'wb') as f:
        f.write(pfx_data)
    cmdlet = ''
    e = {}
    if pfx_password:
        password = '-password (ConvertTo-SecureString -f -a $env:SEDGE_PASSWORD)'
        e['SEDGE_PASSWORD'] = pfx_password
    else:
        password = "-password $null"
    if store:
        store_arg = rf"-certstorelocation 'cert:\localmachine\{store}'"
    else:
        store_arg = r'-certstorelocation cert:\localmachine\my'
    if platform.release().startswith('2008'):
        cmdlet = """
        function Import-PfxCertificate {
            param([string]$filepath
              , [string]$root_store = 'localmachine'
              , [string]$store = 'My'
              , [security.securestring]$password = $null)
            Write-Host "importing $filepath"
            using namespace System.Security.Cryptography.X509Certificates
            $pfx = new-object X509Certificate2
            $flags = [X509KeyStorageFlags]::Exportable
            $flags = $flags -bor [X509KeyStorageFlags]::MachineKeySet
            $flags = $flags -bor [X509KeyStorageFlags]::PersistKeySet
            $pfx.import($filepath, $password, $flags)
            $p = new-object X509Store($store, $root_store)
            $p.open('MaxAllowed')
            $exists = $false
            foreach ($x in $p.certificates) {
                if ($x.thumbprint -eq $pfx.thumbprint) {
                    Write-Host 'cert already exists in cert store'
                    $exists = $true
                }
            }
            if (!($exists)) {
                $p.add($pfx)
            }
            $p.close()
            return $pfx.thumbprint
        }
        """
        store_arg = ''
    lines = [
        cmdlet,
        f"$t = Import-PfxCertificate -filepath '{filename}' {password} "
        f"{store_arg}",
        'Write-Host $t',
    ]
    c = '\n'.join(lines)
    ctx.run(c, env=e)
    print(f'removing {filename}')
    os.remove(filename)
    return thumbprint


def is_linux():
    return sys.platform == 'linux'


def is_windows():
    return sys.platform == 'win32'


@task
def create_account_key(ctx, filename):
    """
    creates an account key and saves it to filename
    """
    import OpenSSL
    key_type = OpenSSL.crypto.TYPE_RSA
    key = OpenSSL.crypto.PKey()
    key.generate_key(key_type, 2048)
    st = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    with open(filename, 'w') as f:
        f.write(st.decode())
