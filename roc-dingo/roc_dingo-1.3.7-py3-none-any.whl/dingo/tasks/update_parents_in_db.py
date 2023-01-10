#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to synchronize the file tree with the ROC database."""

import re

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task

from roc.dingo.constants import PIPELINE_DATABASE
from roc.dingo.models.file import FileLog


__all__ = ['UpdateParentsInDb']


class UpdateParentsInDb(Task):
    """
    Update database linking files and their parents, based on the
    error_log field containing "Missing parents"
    """
    plugin_name = 'roc.dingo'
    name = 'update_parents_in_db'

    def add_targets(self):
        pass

    def setup_inputs(self):
        pass

    def remove_parent_from_log(child, parent):
        """
        Take a pair child/parent and remove the child error_log
        part containing the parent message

        :param child: FileLog element for child
        :param parent: FileLog element for parent
        """

        miss_expr = re.compile('Missing parents : (.*)$')

        logger.debug('Child basename : {}'.format(child.basename))
        logger.debug('Child error_log : {}'.format(child.error_log))
        logger.debug('Parent basename : {}'.format(parent.basename))

        # search into the error_log message
        old_missing_parents = miss_expr.search(child.error_log)
        missing_parents = old_missing_parents.group(1).split(', ')

        logger.debug('Child missing parents : {}'.format(missing_parents))

        # remove parent error message
        if parent.basename in missing_parents:
            missing_parents.remove(parent.basename)
        else:
            logger.warning(
                'Parent {} not found in error_log \'{}\'. '
                'This should not happen.'.format(
                    parent.basename,
                    child.error_log
                ))

        # if the parent has .h5 or .cdf as extension
        # try to remove the other extension (both are in the error_log)

        if '.cdf' in parent.basename:
            h5name = parent.basename.replace('.cdf', '.h5')
            if h5name in missing_parents:
                missing_parents.remove(h5name)

        if '.h5' in parent.basename:
            cdfname = parent.basename.replace('.h5', '.cdf')
            if cdfname in missing_parents:
                missing_parents.remove(cdfname)

        # restore the error_log message
        if len(missing_parents) > 0:
            missing_parents = 'Missing parents : ' + \
                ', '.join(missing_parents)
        else:
            missing_parents = ''

        # update error_log in DB
        child.error_log = child.error_log.replace(
            old_missing_parents.group(0),
            missing_parents)

    def run(self):
        logger.debug('UpdateParentsInDb() : run')

        # Get the database connection if needed
        if not hasattr(self, 'session'):
            self.session = Connector.manager[PIPELINE_DATABASE].session

        # Update Database with
        # the pairs (child/parent) which can be linked
        # based on the error_log
        # Returns the pairs inserted

        sql1 = """
            with f1 (id, file, parent) as (select distinct f.id, f.basename ,
                trim(unnest(string_to_array(substring(substring(f.error_log
                    from 'Missing parents : .*$') from 19), ', ')))
                from pipeline.file_log f
                where f.is_removed = False and f.error_log ~ 'Missing parents')
            insert into pipeline.parents_file_log (id_child, id_parent) (
                select f1.id , f2.id
                from f1 inner join pipeline.file_log f2
                on f1.parent = f2.basename
                except (
                    select id_child, id_parent from pipeline.parents_file_log))
            -- on conflict do nothing
            -- to be restored when bdd-lesia will be > 9.4
            returning id_child, id_parent;
            """

        results1 = self.session.execute(sql1)

        cpt = 0
        for row in results1:
            cpt += 1
            file = self.session.query(FileLog).get(row[0])
            parent = self.session.query(FileLog).get(row[1])

            logger.debug(row)
            logger.info('Add parent {:60s} to {:60s} '
                        '[{:05.2f}% complete]'.format(
                            parent.basename,
                            file.basename,
                            100 * cpt / results1.rowcount))

            UpdateParentsInDb.remove_parent_from_log(file, parent)

        # Returns the pairs that could be linked based on the error_log
        # but are already linked in parents_file_log
        # This should not happen, but may be useful after a pipeline error

        sql2 = """
            with f1 (id, file, parent) as (select distinct f.id, f.basename ,
                trim(unnest(string_to_array(substring(substring(f.error_log
                    from 'Missing parents : .*$') from 19), ', ')))
                from pipeline.file_log f
                where f.is_removed = False and f.error_log ~ 'Missing parents')
            select f1.id , f2.id
                from f1 inner join pipeline.file_log f2
                on f1.parent = f2.basename
                intersect (
                    select id_child, id_parent from pipeline.parents_file_log)
            """

        # ensure that preceding instructions have been committed
        self.session.commit()

        results2 = self.session.execute(sql2)

        cpt = 0
        for row in results2:
            cpt += 1
            file = self.session.query(FileLog).get(row[0])
            parent = self.session.query(FileLog).get(row[1])

            logger.debug(row)
            logger.info('Parent {:60s} to {:60s} was already added '
                        '[{:05.2f}% complete]'.format(
                            parent.basename,
                            file.basename,
                            100 * cpt / results2.rowcount))

            UpdateParentsInDb.remove_parent_from_log(file, parent)

        if results1.rowcount + results2.rowcount == 0:
            logger.info('Nothing to be done.')
