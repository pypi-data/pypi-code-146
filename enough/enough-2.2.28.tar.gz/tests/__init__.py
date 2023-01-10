import os
import sh
import shutil
import textwrap
import time

from enough.common.dotenough import DotEnough, DotEnoughLibvirt, DotEnoughOpenStack
from enough.common import libvirt
from enough.common.openstack import OpenStack
from enough import settings


def make_config_dir(domain, enough_dot_dir):
    os.environ['ENOUGH_DOT'] = str(enough_dot_dir)
    config_dir = f'{enough_dot_dir}/{domain}'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir


def prepare_config_dir(domain, enough_dot_dir):
    os.environ['ENOUGH_DOMAIN'] = domain
    config_dir = make_config_dir(domain, enough_dot_dir)
    all_dir = f'{config_dir}/inventory/group_vars/all'
    if not os.path.exists(all_dir):
        os.makedirs(all_dir)
    shutil.copyfile('tests/clouds.yml', f'{all_dir}/clouds.yml')
    shutil.copyfile('inventory/group_vars/all/provision.yml', f'{all_dir}/provision.yml')
    open(f'{all_dir}/certificate.yml', 'w').write(textwrap.dedent("""\
    ---
    certificate_authority: letsencrypt_staging
    """))
    DotEnough._set_bind_service_group(f'{config_dir}/inventory/services.yml')
    return config_dir


class Infrastructure(object):

    def __init__(self):
        self.config_dir = None

    def init(self, mocker, monkeypatch, tmpdir):
        enough_dot_dir = str(tmpdir)
        self.prefix_set()
        self.domain_set()
        self.config_dir_set(enough_dot_dir)
        self.prepare_config_dir(enough_dot_dir)
        self.mock(mocker)
        self.monkeypatch(monkeypatch, enough_dot_dir)

    def monkeypatch(self, monkeypatch, enough_dot_dir):
        monkeypatch.setenv('ENOUGH_DOT', enough_dot_dir)
        monkeypatch.setenv('ENOUGH_DOMAIN', self.domain)
        monkeypatch.setattr(settings, 'CONFIG_DIR', self.config_dir)

    def prepare_config_dir(self, enough_dot_dir):
        self.all_dir = f'{self.config_dir}/inventory/group_vars/all'
        if not os.path.exists(self.all_dir):
            os.makedirs(self.all_dir)

    def config_dir_set(self, enough_dot_dir):
        os.environ['ENOUGH_DOMAIN'] = self.domain
        os.environ['ENOUGH_DOT'] = str(enough_dot_dir)
        self.config_dir = f'{enough_dot_dir}/{self.domain}'

    def prefix_set(self, prefix=None):
        if prefix is None:
            self._prefix_set()
        else:
            self.prefix = prefix

    def domain_set(self):
        self.domain = f'{self.prefix}.test'

    def mock(self, mocker):
        pass

    def fixture(self):
        return self

    def clobber(self):
        sh.rm('-rf', self.config_dir)


class InfrastructureOpenStack(Infrastructure):

    driver = 'openstack'

    def prepare_config_dir(self, enough_dot_dir):
        super().prepare_config_dir(enough_dot_dir)
        dotenough = DotEnoughOpenStack(self.config_dir, self.domain)
        dotenough.set_bind_service_group()
        shutil.copyfile('tests/clouds.yml', f'{self.all_dir}/clouds.yml')
        shutil.copyfile('inventory/group_vars/all/provision.yml', f'{self.all_dir}/provision.yml')
        open(f'{self.all_dir}/certificate.yml', 'w').write(textwrap.dedent("""\
        ---
        certificate_authority: letsencrypt_staging
        """))

    def _prefix_set(self):
        self.prefix = 'enough_test_' + str(int(time.time()))

    def destroy(self, hosts=[]):
        if not os.path.exists(f'{self.config_dir}/inventory/group_vars/all/clouds.yml'):
            return
        for cloud in ('production', 'clone'):
            o = OpenStack(self.config_dir, cloud=cloud)
            o.destroy_everything(None)

    def certs(self):
        return 'certs'


class InfrastructureLibvirt(Infrastructure):

    driver = 'libvirt'

    def prepare_config_dir(self, enough_dot_dir):
        super().prepare_config_dir(enough_dot_dir)

        lv = libvirt.Libvirt(self.config_dir, '.', domain=self.domain)
        cached_images_dir = os.path.dirname(lv.images_dir)
        filename = lv._image_name()
        cached_image = f'{cached_images_dir}/{filename}'
        if not os.path.exists(lv.image_name()):
            if not os.path.exists(cached_image):
                lv.image_builder()
                os.rename(lv.image_name(), cached_image)
            else:
                lv.image_dir_ensure()
            os.symlink(cached_image, lv.image_name())

        dotenough = DotEnoughLibvirt(self.config_dir, self.domain)
        dotenough.ensure()
        #
        # backups upload to the cloud and need clouds.yml
        #
        shutil.copyfile('tests/clouds.yml', f'{self.all_dir}/clouds.yml')
        shutil.copyfile('inventory/group_vars/all/provision.yml', f'{self.all_dir}/provision.yml')
        open(f'{self.all_dir}/certificate.yml', 'w').write(textwrap.dedent("""\
        ---
        certificate_authority: ownca
        """))
        open(f'{self.all_dir}/infrastructure.yml', 'w').write(textwrap.dedent("""\
        ---
        infrastructure_driver: libvirt
        """))
        dotenough.set_bind_service_group()

    def config_dir_set(self, enough_dot_dir):
        super().config_dir_set(enough_dot_dir)
        lv = libvirt.Libvirt(self.config_dir, '.', domain=self.domain)
        self.images_dir = lv.images_dir

    def mock(self, mocker):
        port = '22'
        network_global_variables = {
            'libvirt_network_external_name': f'{self.prefix}e',
            'libvirt_network_external_prefix': '10.123.43',
            'libvirt_network_internal_name': f'{self.prefix}i',
            'libvirt_network_internal_prefix': '10.4.5',
        }

        def get_global_variable(name):
            if name == 'libvirt_uri':
                return 'qemu:///system'
            elif name == 'libvirt_ssh':
                return []
            else:
                return network_global_variables
        mocker.patch('enough.common.ansible_utils.Ansible.get_global_variable',
                     side_effect=get_global_variable)
        definitions = {
            self.prefix: {
                'name': self.prefix,
                'ansible_port': port,
                'libvirt_ram': '1024',
                'network_interface_unconfigured': 'noname',
                'network_interface_routed': 'enp1s0',
                'network_interface_not_routed': 'enp2s0',
            },
        }
        definitions[self.prefix].update(network_global_variables)
        mocker.patch('enough.common.libvirt.Libvirt.get_definitions',
                     return_value=definitions)

    def _prefix_set(self):
        self.prefix = 'et' + str(int(time.time()))[5:]

    def destroy(self, hosts=[]):
        lv = libvirt.Libvirt(self.config_dir, '.')
        for host in hosts:
            lv.delete(host)
        lv.networks_destroy()
        lv.destroy_everything(self.prefix)
        sh.rm('-fr', self.images_dir)

    def certs(self):
        return f'{self.config_dir}/certs'
