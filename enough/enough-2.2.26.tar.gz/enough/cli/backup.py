import logging
from cliff.command import Command

from enough import settings
from enough.common import options
from enough.common import Enough


def set_common_options(parser):
    parser.add_argument('--target-cloud',
                        default='clone',
                        help='Name of the cloud in which resources are restored')
    parser.add_argument('--target-domain',
                        help='Domain name under which the resources are restored')
    parser.add_argument('--clobber-cloud',
                        action='store_true',
                        help='Destroy all resources in --target-cloud')
    return parser


class Restore(Command):
    """Restore a service from a volume snapshot.

       If --target-domain is specified, a volume is created from the
       snapshot in the --target-cloud region. The corresponding
       service is also created in the --target-cloud region and set to
       use the volume.

       If --target-domain is not specificed, the volume used by the
       service matching the snapshot is replaced with the content of
       the snapshot.
    """

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        options.set_options(parser)
        parser.add_argument('name')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.restore()


class CloneVolume(Command):
    "Create a volume from a volume snapshot"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        options.set_options(parser)
        parser.add_argument('name')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.cli_clone_volume()


class Download(Command):
    "Download backups."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        options.set_options(parser)
        parser.openstack_group.add_argument(
            '--recent', type=int, default=1,
            help='If a backup is newer than --recent days, do not download it')
        parser.openstack_group.add_argument(
            '--volumes', action='append',
            help='Download the latest snapshot of this volume (can be repeated)')
        parser.openstack_group.add_argument(
            '--hosts', action='append',
            help='Download the latest backup image of this host (can be repeated)')
        return parser

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.backup_download()
