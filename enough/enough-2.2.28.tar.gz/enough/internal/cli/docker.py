import os
import sh

from cliff.command import Command

from enough.common.docker import Docker


class Build(Command):
    "Build the enough docker image."

    class DockerEnough(Docker):

        def create_image(self, version=None):
            name = super().create_image(version=version)
            sh.rm('-fr', 'dist')
            sh.python('setup.py', '--quiet', 'sdist')
            dockerfile = os.path.join(self.root, 'internal/data/enough-source.dockerfile')
            return self._create_image(None,
                                      '--build-arg', f'IMAGE_NAME={name}',
                                      '-f', dockerfile, '.', version=version)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--name', default='enough')
        parser.add_argument('--tag')
        return parser

    def take_action(self, parsed_args):
        args = vars(parsed_args)
        version = args.pop('tag')
        args['domain'] = self.app.options.domain
        Build.DockerEnough(**args).create_image(version=version)
