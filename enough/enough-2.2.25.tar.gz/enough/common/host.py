from abc import ABC, abstractmethod

from enough import settings
from enough.common import openstack
from enough.common import libvirt
from enough.common import dotenough


class Host(ABC):

    def __init__(self, config_dir, share_dir, **kwargs):
        self.config_dir = config_dir
        self.share_dir = share_dir
        self.args = kwargs

    @abstractmethod
    def create_or_update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class HostOpenStack(Host):

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir, **kwargs)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughOpenStack(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def create_or_update(self):
        dotenough.Hosts(self.config_dir).ensure(self.args['name'])
        h = openstack.Heat(self.config_dir, **self.args)
        s = openstack.Stack(self.config_dir, h.get_stack_definition(self.args['name']), **self.args)
        s.set_public_key(f'{self.config_dir}/infrastructure_key.pub')
        return s.create_or_update()

    def delete(self):
        self.delete_hosts(self.args['name'])

    def delete_hosts(self, names):
        h = openstack.Heat(self.config_dir, **self.args)
        complete_deletion = []
        for name in names:
            definition = h.get_stack_definition(name)
            if not definition:
                continue
            s = openstack.Stack(self.config_dir, definition, **self.args)
            if s.delete_no_wait():
                complete_deletion.append(name)
        for name in complete_deletion:
            s = openstack.Stack(self.config_dir, h.get_stack_definition(name), **self.args)
            s.delete_wait()


class HostLibvirt(Host):

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir, **kwargs)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughLibvirt(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def create_or_update(self):
        name = self.args['name']
        dotenough.Hosts(self.config_dir).ensure(name)
        lv = libvirt.Libvirt(self.config_dir, self.share_dir, **self.args)
        return lv.create_or_update([name])[name]

    def delete(self):
        self.delete_hosts(self.args['name'])

    def delete_hosts(self, names):
        lv = libvirt.Libvirt(self.config_dir, self.share_dir, **self.args)
        for name in names:
            lv.delete(name)


def host_factory(config_dir=settings.CONFIG_DIR, share_dir=settings.SHARE_DIR, **kwargs):
    if kwargs['driver'] == 'openstack':
        return HostOpenStack(config_dir, share_dir, **kwargs)
    elif kwargs['driver'] == 'libvirt':
        return HostLibvirt(config_dir, share_dir, **kwargs)
