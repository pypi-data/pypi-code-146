import os, sys
from dataclasses import dataclass, field


def open_port():
    """
    https://gist.github.com/jdavis/4040223
    """

    import socket

    sock = socket.socket()
    sock.bind(('', 0))
    x, port = sock.getsockname()
    sock.close()

    return port


def checkPort(port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = bool(sock.connect_ex(('127.0.0.1', int(port))))
    sock.close()
    return result


def getPort(ports=[], prefix="-p"):
    if ports is None or ports == []:
        return ''
    return ' '.join([
        f"{prefix} {port if checkPort(port) else open_port()}:{port}" for port in ports
    ])


@dataclass
class dock:
    """Class for keeping track of an item in inventory."""
    docker: str = "docker"
    image: str = "frantzme/pythondev:lite"
    ports: list = field(default_factory=list)
    cmd: str = None
    nocmd: bool = False
    nonet: bool = False
    dind: bool = False
    shared: bool = False
    detach: bool = False
    sudo: bool = False
    remove: bool = True
    mountto: str = "/sync"
    mountfrom: str = None
    name: str = "current_running"
    login: bool = False
    loggout: bool = False
    logg: bool = False
    macaddress: str = None
    postClean: bool = False
    preClean: bool = False
    extra: str = None

    def clean(self):
        return "; ".join([
            "{} kill $({} ps -a -q)".format(self.docker, self.docker),
            "{} kill $({} ps -q)".format(self.docker, self.docker),
            "{} rm $({} ps -a -q)".format(self.docker, self.docker),
            "{} rmi $({} images -q)".format(self.docker, self.docker),
            "{} volume rm $({} volume ls -q)".format(self.docker, self.docker),
            "{} image prune -f".format(self.docker),
            "{} container prune -f".format(self.docker),
            "{} builder prune -f -a".format(self.docker)
        ])

    def string(self):
        if self.dind or self.shared:
            import platform
            if False and platform.system().lower() == "darwin":  # Mac
                dockerInDocker = "--privileged=true -v /private/var/run/docker.sock:/var/run/docker.sock"
            else:  # if platform.system().lower() == "linux":
                dockerInDocker = "--privileged=true -v /var/run/docker.sock:/var/run/docker.sock"
        else:
            dockerInDocker = ""

        if self.shared:
            exchanged = "-e EXCHANGE_PATH=" + os.path.abspath(os.curdir)
        else:
            exchanged = ""

        dir = '%cd%' if sys.platform in ['win32', 'cygwin'] else '`pwd`'
        use_dir = "$EXCHANGE_PATH" if self.shared else (self.mountfrom if self.mountfrom else dir)

        if self.nocmd:
            cmd = ''
        else:
            cmd = self.cmd or '/bin/bash'

        network = ""
        if self.nonet:
            network = "--network none" #https://docs.docker.com/network/none/

        return str(self.clean()+";" if self.preClean else "") + "{0} run ".format(self.docker) + " ".join([
            dockerInDocker,
            '--rm' if self.remove else '',
            '-d' if self.detach else '-it',
            '-v "{0}:{1}"'.format(use_dir, self.mountto),
            exchanged,
            network,
            getPort(self.ports),
            '--mac-address ' + str(self.macaddress) if self.macaddress else '',
            self.extra if self.extra else '',
            self.image,
            cmd
        ]) + str(self.clean()+";" if self.postClean else "")

    def __str__(self):
        return self.string()
