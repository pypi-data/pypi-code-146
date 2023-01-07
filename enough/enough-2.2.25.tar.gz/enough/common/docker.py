from __future__ import print_function
import logging
import os
import sh

from enough.version import __version__

log = logging.getLogger(__name__)


class Docker(object):

    def __init__(self, **kwargs):
        self.root = kwargs.get('root', os.path.join(os.path.dirname(__file__), '..'))
        self.name = kwargs.get('name')
        self.bake_docker(kwargs.get('docker'))

    def bake_docker(self, docker):
        cmd = docker or 'docker'
        self.docker = sh.Command(cmd).bake(
            _truncate_exc=False,
            _tee=True,
            _tty_out=False,
            _out=lambda x: log.info(x.strip()),
            _err=lambda x: log.info(x.strip()),
        )

    def create_image(self, version=None):
        dockerfile = os.path.join(self.root, 'common/data/base.dockerfile')
        return self._create_image('base', '-f', dockerfile, '.',
                                  version=version)

    def _create_image(self, suffix, *args, version=None):
        name = self.get_image_name_with_version(suffix, version=version)
        build_args = ['--quiet', '--tag', name]
        self.docker.build(build_args + list(args))
        if version is None:
            # tag with latest only when a version isn't specified
            self.docker.tag(name, self.get_image_name(suffix))
        return name

    def get_image_name(self, suffix):
        if suffix:
            return self.name + '_' + suffix
        else:
            return self.name

    def get_image_name_with_version(self, suffix, version=None):
        if version is None:
            version = str(__version__)
        return self.get_image_name(suffix) + ':' + version
