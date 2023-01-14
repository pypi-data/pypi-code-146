# This file is based on Hyde's engine.py
from pathlib import Path
from shutil import copytree
import sys
from commando import (
    Application,
    command,
    store,
    subcommand,
    true,
    version
)
from commando.util import getLoggerWithConsoleHandler
from hyde.exceptions import HydeException
from hyde.model import Config
from hyde.site import Site
from . import generator, server
from . import _version


class Engine(Application):
    def __init__(self, raise_exceptions=False):
        logger = getLoggerWithConsoleHandler('hyde-gopher')
        super(Engine, self).__init__(
            raise_exceptions=raise_exceptions,
            logger=logger
        )
    
    @command(
        description="hyde-gopher - build hyde sites for gopher",
        epilog='Use %(prog)s {command} -h to get help on individual commands'
    )
    @true('-x', '--raise-exceptions', default=None,
          help="Don't handle exceptions.")
    @version('--version', version='%(prog)s ' + _version)
    @store('-s', '--sitepath', default='.', help="Location of the hyde site")
    def main(self, args):
        """
        Will not be executed. A sub command is required. This function exists
        to provide common parameters for the subcommands and some generic stuff
        like version and metadata
        """
        if args.raise_exceptions in (True, False):
            self.raise_exceptions = args.raise_exceptions
        return Path(args.sitepath).absolute()
    
    @subcommand(
        'init', help='Initializes hyde-gopher with an exiting hyde site.'
    )
    @store('-c', '--config-path', default='site.yaml', dest='config',
           help='The configuration used for the site')
    @true('-f', '--force', default=False, dest='overwrite',
          help='Overwrite the current site if it exists')
    def init(self, args):
        """
        The init command. Initializes hyde-gopher with an exiting hyde site
        from a bundled template at the given sitepath.
        """
        sitepath = self.main(args)
        if not (sitepath / 'site.yaml').exists():
            raise HydeException(f"Site {sitepath} is not yet initialized.")
        site = self.make_site(sitepath, args.config, None)
        dest_path = sitepath / site.config.layout_root
        if dest_path.exists() and not args.overwrite:
            raise HydeException(
                "Site {} already has a layout at {}. Use -f to overwrite."
                .format(sitepath, dest_path)
            )
        self.logger.info("Copying default layout to site at %s", sitepath)
        copy_kwargs = dict()
        if dest_path.exists() and args.overwrite:
            if sys.version_info < (3, 8):
                raise HydeException("Can't overwrite layout on Python < 3.8.")
            self.logger.warn("Overwriting %s", dest_path)
            copy_kwargs["dirs_exist_ok"] = True
        copytree(
            Path(__file__).with_name("layout_gopher"),
            dest_path,
            **copy_kwargs,
        )
        self.logger.info("Layout copied")
        if not hasattr(site.config, "gopher_base_url"):
            self.logger.warn(
                "Site at %s has gopher_base_url not set", sitepath
            )
    
    @subcommand('gen', help='Generate the site')
    @store('-c', '--config-path', default='site.yaml', dest='config',
           help='The configuration used to generate the site')
    @store('-d', '--deploy-path', dest='deploy', default=None,
           help='Where should the site be generated?')
    # always regen
    def gen(self, args):
        """
        The generate command. Generates the site at the given
        deployment directory.
        """
        sitepath = self.main(args)
        site = self.make_site(sitepath, args.config, args.deploy)
        self.logger.info("Regenerating the site...")
        generator.generate_all(site)
        self.logger.info("Generation complete.")
    
    @subcommand('serve', help='Serve the website')
    @store('-a', '--address', default='localhost', dest='address',
           help='The address where the website must be served from.')
    @store('-p', '--port', type=int, default=7070, dest='port',
           help='The port where the website must be served from.')
    @store('-c', '--config-path', default='site.yaml', dest='config',
           help='The configuration used to generate the site')
    @store('-d', '--deploy-path', dest='deploy', default=None,
           help='Where should the site be generated?')
    def serve(self, args):
        """
        The serve command. Serves the site at the given
        deployment directory, address and port. Regenerates
        the entire site or specific files based on the request.
        """
        sitepath = self.main(args)
        site = self.make_site(sitepath, args.config, args.deploy)
        server.serve(site, args.address, args.port)

    def make_site(self, sitepath, config, deploy=None):
        """
        Creates a site object from the given sitepath and the config file.
        """
        config = Config(sitepath, config_file=config)
        config.deploy_root = deploy or Path(sitepath) / "deploy_gopher"
        site = Site(sitepath, config)
        site.context['site'] = site
        site.config.layout_root = getattr(
            site.config, "gopher_layout_root", "layout_gopher"
        )
        site.config.gopher_width = getattr(site.config, "gopher_width", 70)
        return site
