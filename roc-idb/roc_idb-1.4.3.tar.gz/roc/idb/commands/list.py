# -*- coding: utf-8 -*-
from poppy.core.command import Command
from roc.idb.tasks import ListReleasesTask, ListPalisadeMetadataTask

__all__ = ['List', 'ListReleases', 'ListPalisadeMetadata']


class List(Command):
    """
    Command to list the IDB content
    """

    __command__ = 'idb_list'
    __command_name__ = 'list'
    __parent__ = 'idb'
    __parent_arguments__ = ['base']
    __help__ = 'List the IDB content'


class ListReleases(Command):
    """
    Command to list the different idb releases
    """

    __command__ = 'idb_list_releases'
    __command_name__ = 'releases'
    __parent__ = 'idb_list'
    __parent_arguments__ = ['base']
    __help__ = 'Command to list the different idb releases'

    def setup_tasks(self, pipeline):
        """
        List the different idb releases
        """

        # the task
        list_idb_releases = ListReleasesTask()

        # set the pipeline for this situation
        pipeline | list_idb_releases
        pipeline.start = list_idb_releases


class ListPalisadeMetadata(Command):
    """
    Command to list the different idb releases
    """

    __command__ = 'idb_list_palisade_metadata'
    __command_name__ = 'palisade_metadata'
    __parent__ = 'idb_list'
    __parent_arguments__ = ['base']
    __help__ = 'Command to list the palisade metadata'

    def setup_tasks(self, pipeline):
        """
        List the palisade metadata
        """

        # the task
        list_palisade_metadata = ListPalisadeMetadataTask()

        # set the pipeline for this situation
        pipeline | list_palisade_metadata
        pipeline.start = list_palisade_metadata


# TODO: List packets/parameters
