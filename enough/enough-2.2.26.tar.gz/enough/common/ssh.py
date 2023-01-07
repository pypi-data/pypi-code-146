import logging
import socket
import subprocess
import sys

from enough.common import dotenough
from enough.common.retry import retry

log = logging.getLogger(__name__)


class SSH(object):

    def __init__(self, config_dir, **kwargs):
        self.config_dir = config_dir
        self.args = kwargs
        self.dot = dotenough.DotEnoughOpenStack(self.config_dir,
                                                self.args['domain'])
        self.dot.ensure()

    def ssh(self, host, args, interactive=True):
        hosts = dotenough.Hosts(self.config_dir)
        ip = hosts.get_ip(host)
        if not ip:
            raise Exception(f'{host} is not found in {hosts.f}')
        ssh = ['ssh', '-oStrictHostKeyChecking=no']
        port = hosts.get_port(host)
        if port != '22':
            ssh.append(f'-p{port}')
        ssh.append(f'-i{self.dot.private_key()}')
        ssh.append(f'debian@{ip}')
        if interactive:
            kwargs = dict(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        else:
            kwargs = dict(capture_output=True)
        return subprocess.run(ssh + args, **kwargs)

    @staticmethod
    @retry((socket.timeout, ConnectionRefusedError, OSError), 8)
    def wait_for_ssh(ip, port):
        log.info('Check if SSH is available on %s:%s', ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, int(port)))
        line = s.makefile("rb").readline()
        assert line.startswith(b'SSH-')
