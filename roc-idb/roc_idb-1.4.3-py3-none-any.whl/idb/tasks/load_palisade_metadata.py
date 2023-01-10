#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.db.handlers import get_or_create
from poppy.core.logger import logger
from poppy.core.task import Task
from roc.idb.models.palisade_metadata import PalisadeMetadata
from roc.idb.parsers import PALISADEMetadataParser

__all__ = ['LoadPalisadeMetadataTask', 'put_palisade_metadata']


def put_palisade_metadata(session, parser):
    """
    Put PALISADE metadata into roc database
    """

    # get the palisade version
    palisade_version = parser.version()

    for srdb_id in parser.palisade_metadata_map:

        palisade_id = parser.palisade_metadata_map[srdb_id]['palisade_id']

        get_or_create(
            session,
            PalisadeMetadata,
            palisade_version=palisade_version,
            srdb_id=srdb_id.strip(),
            palisade_id=palisade_id.strip()
            if isinstance(palisade_id, str)
            else palisade_id,
            packet_category=parser.palisade_metadata_map[srdb_id][
                'palisade_category'
            ].strip(),
        )


class LoadPalisadeMetadataTask(Task):
    plugin_name = 'roc.idb'

    name = 'idb_load_palisade_metadata'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        Parse the PALISADE XML database to insert PALISADE metadata into the ROC
        database.
        """
        # get the database session
        session = self.pipeline.db.session

        idb_path = self.pipeline.args.idb_path

        mapping_path = os.path.join(
            idb_path, 'xml', 'IDB_SRDB_Mapping_Table_by_MapGen.xml'
        )

        # create the metadata parser
        parser = PALISADEMetadataParser(idb_path, mapping_path)

        # parse the XML file
        logger.debug('Parsing the Palisade metadata')
        parser.parse()

        # put palisade metadata into the database
        put_palisade_metadata(session, parser)

        # update the database
        self.pipeline.db.update_database()
