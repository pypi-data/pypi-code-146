import glob
import json
import logging
import os
import sh
import tempfile
import textwrap

log = logging.getLogger(__name__)


class AnsibleVariableNotFound(Exception):
    pass


class Ansible(object):

    bake_method = sh.ansible

    def __init__(self, config_dir, share_dir, inventories=None):
        self.config_dir = config_dir
        self.share_dir = share_dir

        self.inventories = [
            '-i', f'{self.share_dir}/inventory',
        ]
        if self.config_dir != self.share_dir:
            self.inventories.extend(['-i', f'{self.config_dir}/inventory'])
        if inventories:
            self.inventories.extend([f'-i{i}' for i in inventories])

        self.ansible_env = {
            'SHARE_DIR': self.share_dir,
            'CONFIG_DIR': self.config_dir,
            'ANSIBLE_NOCOLOR': 'true',
        }

    def bake(self, env=None, verbose=True):
        args = [
            '--extra-vars', f'enough_domain_config_directory={self.config_dir}',
        ]
        args.extend(self.inventories)
        if self.vault_password_option():
            args.append(self.vault_password_option())
        logger = logging.getLogger(__name__)

        # Fetch environment variables as late as possible
        _env = os.environ.copy()
        _env.update(self.ansible_env)
        if env:
            _env.update(env)
        kwargs = dict(
            _truncate_exc=False,
            _env=_env,
        )
        if verbose:
            kwargs.update(
                _tee=True,
                _out=lambda x: logger.info(x.strip()),
                _err=lambda x: logger.info(x.strip()),
            )
        return self.bake_method.bake(*args, **kwargs)

    def vault_password_option(self):
        password_file = f'{self.config_dir}.pass'
        if os.path.exists(password_file):
            return f'--vault-password-file={password_file}'
        else:
            log.debug(f'no decryption because {password_file} does not exist')
            return None

    def ansible_inventory(self):
        args = [
            '--list',
        ] + self.inventories
        if self.vault_password_option():
            args.append(self.vault_password_option())
        _env = os.environ.copy()
        _env.update(ANSIBLE_VERBOSE_TO_STDERR='yes')
        i = sh.ansible_inventory(
            *args,
            _cwd=self.share_dir,
            _env=_env,
        )
        return json.loads(i.stdout.decode('utf-8'))

    def _flat_inventory(self, i, content):
        hosts = content.get('hosts', [])
        for child in content.get('children', []):
            hosts.extend(self._flat_inventory(i, i.get(child, {})))
        return hosts

    def get_groups(self):
        i = self.ansible_inventory()
        del i['_meta']
        groups = {}
        for name, content in i.items():
            groups[name] = self._flat_inventory(i, content)
        return groups

    def get_global_variable(self, variable):
        # the variable we're looking for is not bound to a host but it
        # can only be found by looking into the variables of a
        # host. Since it is global, we just pick one at random.
        value = [v for k, v in self.get_hostvars(variable, 'all[0]').items()
                 if v != 'VARIABLE IS NOT DEFINED!']
        if not value:
            raise KeyError("%r is not defined" % variable)
        return value[0]

    def get_variable(self, variable, host):
        """Render variable for one inventory host

        :param variable: the variable to render. `hostvars[inventory_hostname]`
            is used when the provided ``variable`` is ``None``.
        :type variable: str
        :param host: the inventory host for which the variable is rendered
        :type hosts: str

        :raises: :class:`sh.ErrorReturnCode_1`: when the host is unknown
        :raises: :class:`KeyError`: when the host is known but the variable is
            undefined

        :returns: the deserialized instance of the JSON rendered variable
        """
        return self.get_hostvars(variable, host)[host]

    def get_hostvars(self, variable, *hosts):
        """Render variable for hosts

        :param variable: the variable to render. `hostvars[inventory_hostname]`
            is used when the provided ``variable`` is ``None``.
        :type variable: str
        :param hosts: the list of hosts for which the variable is rendered,
            defaults to all.
        :type hosts: list of inventory hostname, optional

        :raises: :class:`sh.ErrorReturnCode_1`: when an host is unknown
        :raises: :class:`KeyError`: when all host are known but the variable is
            undefined

        :returns: the deserialized instance of the JSON rendered variable
        """
        if not variable:
            variable = "hostvars[inventory_hostname]"

        args = [
            'all',
            '-mdebug',
            f'-avar="{variable}"',
        ]
        if hosts:
            args.extend(('--limit', ','.join(hosts)))
        env = {
            'ANSIBLE_LOAD_CALLBACK_PLUGINS': 'yes',
            'ANSIBLE_STDOUT_CALLBACK': 'json',
            'ANSIBLE_VERBOSE_TO_STDERR': 'yes',
        }
        r = self.bake(env=env, verbose=False)(*args)
        return self.extract_values(r, variable)

    @staticmethod
    def extract_values(result, variable):
        # There is one play and we want to fetch the output of the last task.
        out = json.loads(str(result))['plays'][0]['tasks'][-1]['hosts']
        values = {k: v.get(variable) for k, v in out.items()}
        for k, v in values.items():
            if v == 'VARIABLE IS NOT DEFINED!':
                raise AnsibleVariableNotFound("%r is not defined" % variable)
        return values


class Playbook(Ansible):

    bake_method = sh.ansible_playbook

    class NoPasswordException(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ansible_env['ANSIBLE_ROLES_PATH'] = self.roles_path(self.share_dir)

    @staticmethod
    def is_encrypted(p):
        if not os.path.exists(p):
            return False
        c = open(p).read()
        return c.startswith('$ANSIBLE_VAULT')

    @staticmethod
    def encrypted_files(d):
        return [
            f'{d}/infrastructure_key',
            f'{d}/inventory/group_vars/all/clouds.yml',
        ] + glob.glob(f'{d}/certs/*.key')

    def ensure_decrypted(self):
        encrypted = [f for f in self.encrypted_files(self.config_dir)
                     if self.is_encrypted(f)]
        if len(encrypted) == 0:
            return False
        vault_password_option = self.vault_password_option()
        if not vault_password_option:
            raise Playbook.NoPasswordException(
                f'{encrypted} are encrypted but {self.config_dir}.pass does not exist')
        for f in encrypted:
            log.info(f'decrypt {f}')
            sh.ansible_vault.decrypt(
                vault_password_option,
                f,
                _tee=True,
                _out=lambda x: log.info(x.strip()),
                _err=lambda x: log.info(x.strip()),
                _truncate_exc=False,
                _env={
                    'ANSIBLE_NOCOLOR': 'true',
                }
            )
        return True

    @staticmethod
    def roles_path(d):
        r = glob.glob(f'{d}/playbooks/*/roles')
        r.append(f'{d}/playbooks/wazuh/wazuh-ansible/roles/wazuh')
        return ":".join(r)

    def run_from_cli(self, **kwargs):
        if not kwargs['args']:
            args = [
                '--private-key', f'{self.config_dir}/infrastructure_key',
                f'{self.config_dir}/enough-playbook.yml'
            ]
        else:
            args = kwargs['args'][1:]
        self.run(*args)

    def run(self, *args):
        self.ensure_decrypted()
        self.bake()(*args)

    def get_role_variable(self, role, variable, host):
        """Return the value of a role default variable in context of host.

        The role default variable can be overriden by an inventory variable.

        :param role: name of the role
        :type role: str
        :param variable: variable name
        :type variable: str
        :param host: inventory hostname
        :type host: str

        :raises: :class:`sh.ErrorReturnCode_1`: when the host is unknown
        :raises: :class:`AnsibleVariableNotFound`: when the host is known but the
            variable is undefined

        :returns: the value of the rendered variable.
        """
        return self.get_role_variables(role, variable, host)[host]

    def get_role_variables(self, role, variable, *hosts):
        """Return the values of a role default variable in context of hosts.

        The role default variable can be overriden by an inventory variable.

        :param role: name of the role
        :type role: str
        :param variable: variable name
        :type variable: str
        :param hosts: list of inventory hostnames
        :type hosts: list of str

        :raises: :class:`sh.ErrorReturnCode_1`: when the host is unknown
        :raises: :class:`AnsibleVariableNotFound`: when the host is known but the
            variable is undefined

        :returns: a dict where keys are inventory hostnames and values are the
            rendered variable.
        """
        with tempfile.NamedTemporaryFile() as f:
            playbook = textwrap.dedent(f"""
            ---
            - hosts: all
              gather_facts: false
              serial: 1

              roles:
                - role: "{role}"
                  when: false

              tasks:
                - name: print variable
                  debug:
                    var: "{variable}"
            """)
            f.write(bytearray(playbook, 'utf-8'))
            f.flush()
            args = [
                '--limit', ','.join(hosts),
                f.name,
            ]
            env = {
                'ANSIBLE_LOAD_CALLBACK_PLUGINS': 'yes',
                'ANSIBLE_STDOUT_CALLBACK': 'json',
                'ANSIBLE_VERBOSE_TO_STDERR': 'yes',
            }
            r = self.bake(env=env, verbose=False)(*args)
            return self.extract_values(r, variable)
