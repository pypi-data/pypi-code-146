import logging
import os
import re
import requests
import yaml

from enough import settings
from enough.common import openstack
from enough.common import libvirt
from enough.common import dotenough
from enough.common import ansible_utils

log = logging.getLogger(__name__)


class Service(object):

    class NoHost(Exception):
        pass

    def __init__(self, config_dir, share_dir, **kwargs):
        self.args = kwargs
        self.config_dir = config_dir
        self.share_dir = share_dir
        self.ansible = ansible_utils.Ansible(
            self.config_dir, self.share_dir, kwargs.get('inventory', []))
        self.dotenough = dotenough.DotEnough(config_dir, self.args['domain'])
        self.dotenough.ensure()
        self.set_service_info()
        self.update_vpn_dependencies()

    def set_service_info(self):
        groups = self.ansible.get_groups()
        suffix = '-service-hosts'
        self.service2hosts = {
            name.replace(suffix, ''): hosts for name, hosts in groups.items()
            if name.endswith(suffix)
        }
        suffix = '-service-group'
        self.service2group = {
            name.replace(suffix, ''): hosts for name, hosts in groups.items()
            if name.endswith(suffix)
        }

    def ensure_non_empty_service_group(self):
        service = self.args['name']
        hosts = self.service2group.get(service)
        if not hosts and not self.args.get('host'):
            raise ServiceOpenStack.NoHost(
                f"service {service} needs a host, specify one with --host")
        if self.args.get('host'):
            self.dotenough.service_add_to_group(service, self.args['host'])
            self.set_service_info()
            hosts = self.service2group[service]
        return hosts

    def update_vpn_dependencies(self):
        hosts = self.ansible.ansible_inventory()['_meta']['hostvars'].keys()
        internal_hosts = set(self.hosts_with_internal_network(hosts))
        if not internal_hosts:
            return
        assert 'openvpn' in self.service2hosts
        openvpn_hosts = set(self.service2hosts['openvpn'])
        for service in self.service2hosts.keys():
            if service == 'openvpn':
                continue
            hosts = set(self.service2hosts[service])
            if internal_hosts & hosts:
                self.service2hosts[service] = list(internal_hosts | openvpn_hosts)

    def get_vpn_host(self):
        hosts = self.service2group.get('openvpn')
        if hosts:
            return hosts[0]
        else:
            return None

    def add_vpn_hosts_if_needed(self, hosts):
        internal_hosts = set(self.hosts_with_internal_network(hosts))
        if not internal_hosts:
            return hosts
        assert 'openvpn' in self.service2hosts
        openvpn_hosts = set(self.service2hosts['openvpn'])
        hosts = set(hosts)
        return list(hosts | openvpn_hosts)

    def hosts_with_internal_network(self, hosts):
        info = self.ansible.get_hostvars('network_internal_only', *hosts)
        return [host for (host, internal_only) in info.items() if internal_only is True]

    def service_from_host(self, host):
        found = None
        hosts_count = 0
        for service, hosts in self.service2hosts.items():
            if host in hosts:
                if hosts_count > 0 and len(hosts) > hosts_count:
                    continue
                found = service
                hosts_count = len(hosts)
        return found

    def services_on_host(self, host):
        services = []
        for service, group in self.service2group.items():
            if service == 'essential':
                continue
            if host in group:
                services.append(service)
        return services

    def create_or_update(self):
        self.ensure_non_empty_service_group()
        service = self.args['name']
        hosts = self.service2hosts[service]
        self.create_missings(hosts)
        self.maybe_delegate_dns()
        playbook = ansible_utils.Playbook(self.config_dir, self.share_dir)
        if os.path.isabs(self.args["playbook"]):
            playbook_file = self.args["playbook"]
        else:
            playbook_file = f'{self.config_dir}/{self.args["playbook"]}'
            if not os.path.exists(playbook_file):
                playbook_file = f'{self.share_dir}/{self.args["playbook"]}'

        playbook.run([
            f'--private-key={self.dotenough.private_key()}',
            '--limit', ','.join(hosts + ['localhost']),
            playbook_file,
        ])
        return {'fqdn': f'{self.args["name"]}.{self.args["domain"]}'}

    def info(self, hostvars, service, show_passwords):
        domain = self.args['domain']
        fields = []
        passwords = []
        urls = []
        files = []
        comment = None
        if service == 'cloud':
            urls = [f'https://cloud.{domain}']
            fields = ['nextcloud_admin_user', 'enough_nextcloud_version']
            passwords = ['nextcloud_admin_pass']
            files = ['playbooks/enough/roles/nextcloud/defaults/main.yml']
        elif service == 'forum':
            urls = [f'https://forum.{domain}']
        elif service == 'chat':
            urls = [f'https://chat.{domain}']
        elif service == 'pad':
            urls = [f'https://pad.{domain}']
            comment = 'user=admin'
            fields = ['pad_etherpad_version']
            passwords = ['pad_admin_password']
            files = ['playbooks/pad/roles/pad/defaults/main.yml']
        elif service == 'weblate':
            urls = [f'https://weblate.{domain}']
            comment = 'user=admin'
            fields = ['weblate_server_email', 'weblate_version']
            passwords = ['weblate_admin_password']
            files = ['playbooks/weblate/roles/weblate/defaults/main.yml']
        elif service == 'gitlab':
            urls = [f'https://lab.{domain}']
            comment = 'user=root'
            passwords = ['gitlab_password']
            files = ['inventory/group_vars/gitlab/gitlab.yml']
        elif service == 'website':
            urls = [f'https://www.{domain}']
        elif service == 'pages':
            urls = [f'https://www.{domain}']
        elif service == 'hosteadashboard':
            urls = [f'https://hosteadashboard.{domain}']
        elif service == 'wekan':
            urls = [f'https://wekan.{domain}']
            comment = 'user=admin'
            passwords = ['wekan_password']
            files = ['playbooks/wekan/roles/wekan/defaults/main.yml']
        elif service == 'openedx':
            urls = [f'https://openedx.{domain}', f'https://studio.{domain}']
            fields = ['openedx_contact', 'openedx_language', 'openedx_user']
            passwords = ['openedx_password']
            files = ['playbooks/openedx/roles/openedx/defaults/main.yml']
        elif service == 'securedrop':
            fields = ['securedrop_admin_user', 'securedrop_version']
            passwords = ['securedrop_admin_password', 'securedrop_admin_otp_secret']
            files = ['playbooks/securedrop/roles/securedrop/defaults/main.yml']
        elif service == 'psono':
            urls = [f'https://psono.{domain}']
            fields = ['psono_contact', 'psono_version']
            files = ['playbooks/psono/roles/psono/defaults/main.yml']
        elif service == 'gitea':
            urls = [f'https://gitea.{domain}']
            fields = ['gitea_version']
            passwords = ['gitea_password']
            files = ['playbooks/gitea/roles/gitea/defaults/main.yml']
        elif service == 'wazuh':
            fields = ['wazuh_mailto']
        elif service == 'icinga':
            urls = [f'https://icinga.{domain}']
            fields = ['icingaweb2_user']
            passwords = ['icingaweb2_user_pass']
            files = ['playbooks/icinga/roles/icinga2/defaults/main.yml']
        elif service == 'jitsi':
            urls = [f'https://jitsi.{domain}']
            fields = ['jitsi_startAudioOnly',
                      'jitsi_requireDisplayName',
                      'jitsi_defaultLanguage',
                      'jitsi_release']
            files = ['playbooks/jitsi/roles/jitsi/defaults/main.yml']
        elif service == 'wordpress':
            urls = [f'https://wordpress.{domain}']
            fields = ['wordpress_admin_user', 'wordpress_admin_email', 'wordpress_version']
            passwords = ['wordpress_admin_password']
            files = ['playbooks/wordpress/roles/wordpress/defaults/main.yml']
        elif service in ('backup', 'bind', 'postfix', 'openvpn', 'gitlab-runner', 'api'):
            return []
        else:
            return ['(unknown service)']
        defaults = {}
        for file in files:
            defaults.update(yaml.safe_load(open(f'{self.share_dir}/{file}').read()))
        info = urls
        if comment:
            info.append(comment)
        for field in fields + passwords:
            if field in passwords and not show_passwords:
                value = '*****'
            elif field in hostvars:
                value = hostvars[field]
            elif field in defaults:
                value = defaults[field]
            else:
                value = '(unknown value)'
            info.append(f'{field}={value}')
        return info


class ServiceOpenStack(Service):

    class PingException(Exception):
        pass

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir, **kwargs)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughOpenStack(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def maybe_delegate_dns(self):
        subdomain_regexp = r'(.*)\.d\.(.*)'
        m = re.match(subdomain_regexp, self.args['domain'])
        if not m:
            log.debug(f'{self.args["domain"]} does not match "{subdomain_regexp}", '
                      'do not attempt to delegate the DNS')
            return False
        (subdomain, domain) = m.group(1, 2)
        api = f'api.{domain}'
        ping = f'https://{api}/ping/'
        r = requests.get(ping)
        if not r.ok:
            raise ServiceOpenStack.PingException(f'{ping} does not respond')

        h = openstack.Heat(self.config_dir, cloud=self.args['cloud'])
        s = openstack.Stack(self.config_dir,
                            h.get_stack_definition('bind-host'),
                            cloud=self.args['cloud'])
        s.set_public_key(self.dotenough.public_key())
        bind_host = s.create_or_update()
        r = requests.post(f'https://{api}/delegate-dns/',
                          json={
                              'name': subdomain,
                              'ip': bind_host['ipv4'],
                          })
        r.raise_for_status()
        return True

    def create_missings(self, hosts):
        h = openstack.Heat(self.config_dir, cloud=self.args['cloud'])
        h.create_missings(hosts, self.dotenough.public_key())


class ServiceLibvirt(Service):

    class PingException(Exception):
        pass

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir, **kwargs)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughLibvirt(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def create_missings(self, hosts):
        lv = libvirt.Libvirt(self.config_dir, self.share_dir, **self.args)
        lv.create_or_update(dotenough.Hosts(self.config_dir).missings(hosts))

    def maybe_delegate_dns(self):
        pass


def service_factory(config_dir=settings.CONFIG_DIR, share_dir=settings.SHARE_DIR, **kwargs):
    if kwargs['driver'] == 'openstack':
        return ServiceOpenStack(config_dir, share_dir, **kwargs)
    elif kwargs['driver'] == 'libvirt':
        return ServiceLibvirt(config_dir, share_dir, **kwargs)
