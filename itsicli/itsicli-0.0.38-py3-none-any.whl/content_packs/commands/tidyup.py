import json

from itsicli.content_packs.commands.base import WorkspaceCommand
from itsicli.content_packs.content_types import ContentType, ContentTypes
from itsicli.content_packs.files import ContentPackConfig, ITSI_DIR
from itsicli.setup_logging import logger, set_content_pack_id
from pathlib import Path

class TidyUpCommand(WorkspaceCommand):

    HELP = 'tidy up a content pack by removing extraneous files'

    NAME = 'tidyup'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        return subparser

    def run(self, args):
        #Setting the content pack id in the global dictionary so that it is added in the logger
        content_pack_config = ContentPackConfig(Path.cwd())
        set_content_pack_id(content_pack_config.get_cp_id())

        update_manifest = self.tidy_glass_tables()
        update_manifest = self.tidy_service_analyzers() or update_manifest

        if update_manifest:
            logger.info('Updating "{}"'.format(self.manifest.path))
            self.manifest.write()

    def tidy_glass_tables(self):
        glass_tables = getattr(self.manifest, ContentType.GLASS_TABLE, []) or []
        GlassTable = ContentTypes[ContentType.GLASS_TABLE]

        keep_glass_tables = []

        for glass_table in glass_tables:
            contents = self.read_contents(ContentType.GLASS_TABLE, glass_table)
            if not contents:
                continue

            model = GlassTable(contents)

            if not model.definition:
                logger.info('Removing definition-less glass table: "{}"'.format(model.title))
                file_path = self.content_file_path(ContentType.GLASS_TABLE, glass_table)
                file_path.unlink()
            else:
                keep_glass_tables.append(glass_table)

        if len(keep_glass_tables) != len(glass_tables):
            self.manifest.data[ContentType.GLASS_TABLE] = keep_glass_tables
            return True

        return False

    def tidy_service_analyzers(self):
        service_analyzers = getattr(self.manifest, ContentType.SERVICE_ANALYZER, []) or []
        ServiceAnalyzer = ContentTypes[ContentType.SERVICE_ANALYZER]

        keep_service_analyzers = []

        for service_analyzer in service_analyzers:
            contents = self.read_contents(ContentType.SERVICE_ANALYZER, service_analyzer)
            if not contents:
                continue

            model = ServiceAnalyzer(contents)

            if model.title == 'Service Analyzer':
                logger.info('Removing "{}"...'.format(model.title))
                file_path = self.content_file_path(ContentType.SERVICE_ANALYZER, service_analyzer)
                file_path.unlink()
            else:
                keep_service_analyzers.append(service_analyzer)

        if len(keep_service_analyzers) != len(service_analyzers):
            self.manifest.data[ContentType.SERVICE_ANALYZER] = keep_service_analyzers
            return True

        return False

    def read_contents(self, content_type, content_file):
        file_path = self.content_file_path(content_type, content_file)
        if not file_path.exists():
            return None

        with open(file_path, 'rb') as fobj:
            contents = json.loads(fobj.read())

        return contents

    def content_file_path(self, content_type, content_file):
        return self.home_path.joinpath(ITSI_DIR, content_type, content_file)

