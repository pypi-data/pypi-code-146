#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pprint import pformat

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.logger import logger
from poppy.core.task import Task
from roc.idb.models.idb import IdbRelease
from roc.idb.models.palisade_metadata import PalisadeMetadata

__all__ = ['ListReleasesTask', 'ListPalisadeMetadataTask']


class ListReleasesTask(Task):
    plugin_name = 'roc.idb'

    name = 'idb_list_releases'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        List the different idb releases
        """
        idb_release_query = self.pipeline.db.session.query(IdbRelease).all()

        idb_count = len(idb_release_query)
        if idb_count > 0:
            logger.info('IDB release available:')
            for idb_release in idb_release_query:
                logger.info(
                    json.dumps(
                        {
                            'source': idb_release.idb_source,
                            'version': idb_release.idb_version,
                            'validity_min': str(idb_release.validity_min),
                            'validity_max': str(idb_release.validity_max),
                            'current': idb_release.current,
                        }
                    )
                )
        else:
            logger.info('No IDB release stored in the database')


class ListPalisadeMetadataTask(Task):
    plugin_name = 'roc.idb'

    name = 'idb_list_palisade_metadata'

    @Connector.if_connected(settings.PIPELINE_DATABASE)
    def run(self):
        """
        List the palisade metadata
        """

        palisade_metadata_query = self.pipeline.db.session.query(
            PalisadeMetadata
        ).all()

        logger.info('Palisade metadata list:')

        fields = [
            'palisade_version',
            'srdb_id',
            'palisade_id',
            'packet_category',
        ]

        data = [
            {field: getattr(palisade_metadata, field) for field in fields}
            for palisade_metadata in palisade_metadata_query
        ]

        logger.info(pformat(data))
