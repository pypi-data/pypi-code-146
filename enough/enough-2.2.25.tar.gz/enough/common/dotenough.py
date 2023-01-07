import os
import sh
import shutil
import textwrap
import yaml
from enough.common import ansible_utils


class Hosts(object):

    def __init__(self, config_dir):
        self.d = f'{config_dir}/inventory'
        self.f = f'{self.d}/hosts.yml'
        self.load()

    def load(self):
        if os.path.exists(self.f):
            inventory = yaml.safe_load(open(self.f).read())
            group = inventory.get('live')
            if group is None:
                # backward compatibility: 'all' group was used before
                try:
                    group = inventory['all']
                except KeyError:
                    raise Exception(f"Missing expected group 'live' in {self.f!r}")
                self.hosts = group['hosts']
                self.save()
            else:
                self.hosts = group['hosts']
        else:
            self.hosts = {}
        return self

    def get_ip(self, host):
        return self.hosts.get(host, {}).get('ansible_host')

    def get_port(self, host):
        return self.hosts.get(host, {}).get('ansible_port', '22')

    def save(self):
        if not os.path.exists(self.d):
            os.makedirs(self.d)
        content = yaml.dump(
            {
                'live': {
                    'hosts': self.hosts,
                },
            }
        )
        open(self.f, 'w').write(content)

    def missings(self, names):
        return [name for name in names if name not in self.hosts]

    def ensure(self, name):
        if name not in self.hosts:
            self.hosts[name] = {}
            self.save()
            return True
        else:
            return False

    def create_or_update(self, name, ipv4, port):
        if self.get_ip(name) != ipv4:
            self.hosts[name] = {'ansible_host': ipv4, 'ansible_port': port}
            self.save()
            return True
        else:
            return False

    def delete(self, name):
        if name in self.hosts:
            del self.hosts[name]
        self.save()

    def info(self, host):
        return f'{host} ip={self.get_ip(host)} port={self.get_port(host)}'


class DotEnough(object):

    def __init__(self, config_dir, domain):
        self.domain = domain
        self.config_dir = config_dir
        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(d):
            os.makedirs(d)

    def ensure(self):
        self.ensure_ssh_key()

    def ensure_ssh_key(self):
        path = f'{self.config_dir}/infrastructure_key'
        if not os.path.exists(path):
            sh.ssh_keygen('-f', path, '-N', '', '-b', '4096', '-t', 'rsa')
        return path

    def public_key(self):
        return f'{self.ensure_ssh_key()}.pub'

    def private_key(self):
        return self.ensure_ssh_key()

    def populate_config(self, certificate_authority):
        d = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(d):
            os.makedirs(d)

        if not os.path.exists(f'{d}/private-key.yml'):
            open(f'{d}/private-key.yml', 'w').write(textwrap.dedent(f"""\
            ---
            ansible_ssh_private_key_file: {self.config_dir}/infrastructure_key
            """))

        if not os.path.exists(f'{d}/domain.yml'):
            open(f'{d}/domain.yml', 'w').write(textwrap.dedent(f"""\
            ---
            domain: {self.domain}
            production_domain: {self.domain}
            """))

        if not os.path.exists(f'{d}/infrastructure.yml'):
            open(f'{d}/infrastructure.yml', 'w').write(textwrap.dedent(f"""\
            ---
            infrastructure_driver: {self.infrastructure_driver}
            """))

        if not os.path.exists(f'{d}/certificate.yml'):
            self.set_certificate(certificate_authority)

        self.set_bind_service_group()

    def set_bind_service_group(self):
        self._set_bind_service_group(f'{self.config_dir}/inventory/services.yml')

    @staticmethod
    def _set_bind_service_group(services_pathname):
        if not os.path.exists(services_pathname):
            open(services_pathname, 'w').write(textwrap.dedent("""\
            ---
            essential-service-group:
               hosts:
                 bind-host:
            bind-service-group:
               hosts:
                 bind-host:
            """))

    @staticmethod
    def service2group(service):
        return f'{service}-service-group'

    def service_add_to_group(self, service, host):
        s = f'{self.config_dir}/inventory/services.yml'
        if os.path.exists(s):
            services = yaml.safe_load(open(s).read())
        else:
            services = {}
        group = self.service2group(service)
        if group not in services:
            services[group] = {'hosts': {}}
        if host not in services[group]['hosts']:
            services[group]['hosts'][host] = None
            open(s, 'w').write(yaml.dump(services, indent=4))
        return services

    def set_certificate(self, certificate_authority):
        d = f'{self.config_dir}/inventory/group_vars/all'
        open(f'{d}/certificate.yml', 'w').write(textwrap.dedent(f"""\
        ---
        certificate_authority: {certificate_authority}
        """))


class DotEnoughLibvirt(DotEnough):

    infrastructure_driver = "libvirt"

    def __init__(self, config_dir, domain):
        super().__init__(config_dir, domain)

    def ensure(self):
        super().ensure()
        self.populate_config('ownca')


class DotEnoughOpenStackUnknownProvider(Exception):
    pass


class DotEnoughOpenStack(DotEnough):

    infrastructure_driver = "openstack"

    def __init__(self, config_dir, domain):
        super().__init__(config_dir, domain)
        self.clouds_file = f'{self.config_dir}/inventory/group_vars/all/clouds.yml'

    def set_clouds_file(self, clouds_file):
        shutil.copy(clouds_file, self.clouds_file)

    def ensure(self):
        super().ensure()
        self.populate_config('letsencrypt')

    def populate_provider(self, ansible, cloud):
        try:
            return ansible.get_global_variable('openstack_provider')
        except ansible_utils.AnsibleVariableNotFound:
            pass

        try:
            clouds = ansible.get_global_variable('clouds')
        except ansible_utils.AnsibleVariableNotFound:
            return None

        url = clouds[cloud]['auth']['auth_url']
        string2provider = (('ovh.net', 'ovh'),
                           ('fuga.cloud', 'fuga'))
        provider = None
        for (string, found) in string2provider:
            if string in url:
                provider = found
                break
        if provider is None:
            raise DotEnoughOpenStackUnknownProvider(
                f'url {url} does not match any known providers {string2provider}')

        f = f'{self.config_dir}/inventory/group_vars/all/openstack-provider.yml'
        open(f, 'w').write(textwrap.dedent(f"""\
        ---
        openstack_provider: {provider}
        """))
        return f
