from functools import partial

from burlap import Satchel
from burlap.constants import *
from burlap.decorators import task

# pylint: disable=import-error,no-name-in-module


class OpenVPNClientSatchel(Satchel):
    """
    Manages configuration and installation of an OpenVPN client.
    """

    name = 'openvpnclient'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_post_role_load_callback(self.register_callbacks)

    def set_defaults(self):
        self.env.user = 'root'
        self.env.directory = None
        self.env.daemon_name = 'openvpn-{name}'
        self.env.command = 'openvpn --config {ovpn}'
        self.env.log_path = '/var/log/openvpn-{name}.log'
        self.env.networks = {} # {name: {ovpn: path, p12:path, key:path, directory:path, user:str}

    @property
    def packager_system_packages(self):
        return {
            UBUNTU: [
                'openvpn',
            ],
        }

    @task(post_callback=True)
    def register_callbacks(self):
        # Called after all other Satchels are defined.
        from burlap.supervisor import supervisor

        for name, params in self.env.networks.items():
            supervisor.register_callback(partial(self.create_supervisor_services, name, params))

    def create_supervisor_services(self, name, params, **kwargs):
        """
        Deploy supervisor configuration to automatically launch script in daemon mode.
        """
        r = self.local_renderer
        params = params or {}
        r.env.name = name
        r.env.daemon_name = r.format(r.env.daemon_name)
        r.env.update(params)
        r.env.directory = r.format(r.env.directory)
        r.env.command = r.format(r.env.command)
        r.env.log_path = r.format(r.env.log_path)
        return f'{name}.conf', r.render_to_string('openvpn/supervisor.template.conf')

    @task(precursors=['packager', 'user'])
    def configure(self):
        super().configure()


openvpnclient = OpenVPNClientSatchel()
