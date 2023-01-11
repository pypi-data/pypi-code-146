from itsicli.setup_logging import logger, set_content_pack_id
import re
import configparser

from pathlib import Path

from itsicli.content_packs.commands.base import BaseCommand, request_input
from itsicli.content_packs.files import ContentPackConfig
from itsicli.content_packs.scaffold import Scaffolder

INVALID_ID = 'Content pack id can only contain alphanumeric, underscore, or dash characters.\n'
CP_PREFIX = 'DA-ITSI-CP-'


def valid_id(id_value):
    return re.search('^[\w\-_]+$', id_value)


def load_conf(path):
    confparser = configparser.ConfigParser()
    confparser.read(path)
    return confparser


class InitCommand(BaseCommand):
    HELP = 'initialize an ITSI Content Pack'

    NAME = 'init'
    
    ITSI_DIR = 'itsi'
    DEFAULT_DIR = 'default'
    APPSERVER_DIR = 'appserver'

    def __init__(self, content_pack_id=None, content_pack_title=None, base_dir=Path.cwd()):
        super().__init__()
        self.content_pack_id = content_pack_id
        self.content_pack_title = content_pack_title
        self.base_dir = base_dir
        
        
    class Args(object):
        CONTENT_PACK_ID = 'content_pack_id'
        CONTENT_PACK_TITLE = 'content_pack_title'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        subparser.add_argument('--{}'.format(cls.Args.CONTENT_PACK_ID), help='the content pack id')
        subparser.add_argument('--{}'.format(cls.Args.CONTENT_PACK_TITLE), help='the content pack title')

    def run(self, args):
        logger.info("Initializing content pack...")

        # files under itsi dir
        self.INPUT_ARGS = args

        # files under itsi dir
        logger.info('\nProcessing directory: {} -->'.format(self.ITSI_DIR))
        config = self.init_config(args)
        self.scaffold_itsi_files()

        logger.info('\nProcessing directory: {} -->'.format(self.DEFAULT_DIR))
        self.scaffold_default_files(config)

        logger.info('\nProcessing directory: {} -->'.format(self.APPSERVER_DIR))
        self.scaffold_appserver_files()

        logger.info("\nCompleted initializing content pack {}.".format(config.get_cp_id()))

    def scaffold_itsi_files(self):
        scaffolder = Scaffolder(self.base_dir.joinpath(self.ITSI_DIR))

        scaffolder.create_file('README.md')
        scaffolder.create_file('manifest.json')

    def scaffold_default_files(self, config):
        # app.conf
        scaffolder = Scaffolder(self.base_dir.joinpath(self.DEFAULT_DIR))
        app_conf_file = scaffolder.create_file('app.conf')
        self.update_app_conf_with_config(config, app_conf_file)

    def scaffold_appserver_files(self):
        appserver_dirs = self.base_dir.joinpath(self.APPSERVER_DIR).joinpath('static', 'screenshots')
        if appserver_dirs.exists():
            logger.info('{} already exists.'.format(appserver_dirs))
        else:
            appserver_dirs.mkdir(parents=True, exist_ok=True)
            logger.info('Created dirs {}'.format(appserver_dirs))

    def update_app_conf_with_config(self, config, app_conf_file):
        app_conf = load_conf(app_conf_file)
        app_conf['ui']['label'] = config.get_cp_title()
        app_conf['package']['id'] = config.get_cp_id()
        app_conf['launcher']['description'] = 'Description for ' + config.get_cp_title()

        with open(app_conf_file, 'w') as conf_file:
            app_conf.write(conf_file)
            logger.info('Completed updating {} with content pack config.'.format(app_conf_file))

    def load_cp_title_config(self, args, existing_config, new_data):
        existing_title = existing_config.get_cp_title()
        existing_title = existing_config.get_cp_title()
        content_pack_title = getattr(args, self.Args.CONTENT_PACK_TITLE)

        if not content_pack_title and not existing_title:
            new_data[ContentPackConfig.attr_title] = request_input('Content pack title')

        return new_data

    def load_cp_id_config(self, args, existing_config, new_data):
        existing_id = existing_config.get_cp_id()
        cp_id = getattr(args, self.Args.CONTENT_PACK_ID)

        if cp_id and not valid_id(cp_id):
            logger.error(INVALID_ID)

            new_data[ContentPackConfig.attr_id] = self.request_content_pack_id()
        elif not existing_id:
            new_data[ContentPackConfig.attr_id] = self.request_content_pack_id()
        
        return new_data

    def persist_new_config(self, config, new_data):
        if config.exists():
            logger.info('Updating file at {}'.format(config.path))
        else:
            config.path.parent.mkdir()
            logger.info('Creating file at {}'.format(config.path))

        config.update(new_data)
        config.write()

    # load existing config data
    # fill in from arg input or user input for missing data (id, title)
    # return the config
    def init_config(self, args):
        config = ContentPackConfig(self.base_dir)
        new_data = {}
        if self.content_pack_id:
            new_data[ContentPackConfig.attr_id] = self.content_pack_id
        else:
            new_data = self.load_cp_id_config(args, config, new_data)
        if self.content_pack_title:
            new_data[ContentPackConfig.attr_title] = self.content_pack_title
        else:
            new_data = self.load_cp_title_config(args, config, new_data)
        if not new_data:
            #Setting the content pack id in the global dictionary so that it is added in the logger
            set_content_pack_id(config.get_cp_id())
            logger.info('Content pack {} already has config initialized.'.format(config.get_cp_id()))
            return config

        self.persist_new_config(config, new_data)
        #Setting the content pack id in the global dictionary so that it is added in the logger
        set_content_pack_id(config.get_cp_id())

        return config


    def request_content_pack_id(self):
        while True:
            content_pack_id = input('Content pack id (will prefix with DA-ITSI-CP- if not provided) : ')

            if not valid_id(content_pack_id):
                logger.error(INVALID_ID)
                continue

            if content_pack_id:
                break

        if not content_pack_id.startswith(CP_PREFIX):
            content_pack_id = CP_PREFIX + content_pack_id
            logger.info('NOTE: Auto appended {} to content pack id --> {}'.format(
                CP_PREFIX,
                content_pack_id
            ))

        return content_pack_id