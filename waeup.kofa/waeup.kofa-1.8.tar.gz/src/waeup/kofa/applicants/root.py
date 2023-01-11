## $Id: root.py 13234 2015-08-27 08:50:56Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""
The root for applicants.
"""
import grok
from hurry.query import Eq
from hurry.query.interfaces import IQuery
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.catalog.interfaces import ICatalog
from zope.catalog.field import FieldIndex
from zope.schema import getFields
from waeup.kofa.interfaces import IKofaPluggable
from waeup.kofa.applicants.interfaces import IApplicantsRoot
from waeup.kofa.utils.logger import Logger
from waeup.kofa.utils.helpers import attrs_to_fields

class ApplicantsRoot(grok.Container, Logger):
    """The root of applicants-related components. It contains only
    containers for applicants.
    """
    grok.implements(IApplicantsRoot)

    local_roles = []
    description_dict = {}
    logger_name = 'waeup.kofa.${sitename}.applicants'
    logger_filename = 'applicants.log'

ApplicantsRoot = attrs_to_fields(ApplicantsRoot)

class ApplicantsPlugin(grok.GlobalUtility):
    """A KofaPlugin that creates an applicants root in portal.

    This plugin could be called by a typical
    `waeup.kofa.app.Universtiy` instance on creation time. The
    :meth:`update` method normally can also be triggered manually over
    the main site configuration.

    Implements :class:`waeup.kofa.interfaces.IKofaPluggable`
    """
    grok.name('applicants')
    grok.implements(IKofaPluggable)
    log_prefix = 'ApplicantsPlugin'

    def setup(self, site, name, logger):
        """Create a new :class:`ApplicantsRoot` instance in `site`.
        """
        site['applicants'] = ApplicantsRoot()
        logger.info(
            '%s: Installed applicants root.' % (self.log_prefix,)
            )
        return

    def update(self, site, name, logger):
        """Update site wide ``applicants`` root.

        If the site already contains a suitable ``applicants`` root,
        leave it that way. If not create one and delete the old one if
        appropriate.

        Update applicants catalog.

        Remove deprecated applicant ids from global role map.
        """
        app_folder = site.get('applicants', None)
        site_name = getattr(site, '__name__', '<Unnamed Site>')
        if IApplicantsRoot.providedBy(app_folder):
            items = getFields(IApplicantsRoot).items()
            nothing_to_do = True
            #for i in items:
            #    if not hasattr(app_folder,i[0]):
            #        nothing_to_do = False
            #        setattr(app_folder,i[0],i[1].missing_value)
            #        logger.info(
            #            '%s: %s added to root.' % (self.log_prefix,i[0]))
            # can be removed after upgrading futminna
            #if not hasattr(app_folder, 'description_dict'):
            #    nothing_to_do = False
            #    setattr(app_folder,'description_dict',{})
            #    logger.info(
            #        '%s: description_dict added to root.' % self.log_prefix)

            # Add container_code index
            try:
                cat = getUtility(ICatalog, name='applicants_catalog')
                if 'container_code' not in cat.keys():
                    nothing_to_do = False
                    cat[u'container_code'] = FieldIndex(field_name=u'container_code')
                    cat.updateIndexes()
                    logger.info(
                        '%s: container_code index added to applicants_catalog.'
                        % self.log_prefix)
            except ComponentLookupError: # in unit tests
                pass

            # Remove old applicant ids from global role map.
            try:
                removed_applicant_ids = []
                cat = getUtility(ICatalog, name='applicants_catalog')
                role_manager = IPrincipalRoleManager(grok.getSite())
                principals = role_manager.getPrincipalsForRole('waeup.Applicant')
                for principal in principals:
                    applicant_id = principal[0]
                    results = cat.searchResults(applicant_id=(applicant_id, applicant_id))
                    if len(results):
                        continue
                    # The applicant does no longer exist.
                    nothing_to_do = False
                    role_manager.unsetRoleForPrincipal(
                        'waeup.Applicant', applicant_id)
                    removed_applicant_ids.append(applicant_id)
                if len(removed_applicant_ids):
                    logger.info(
                        '%s: %s applicant ids removed from global role map: %s'
                        % (self.log_prefix, len(removed_applicant_ids),
                           removed_applicant_ids))
            except ComponentLookupError: # in unit tests
                pass

            # Remove old student ids from global role map.
            try:
                removed_student_ids = []
                cat = getUtility(ICatalog, name='students_catalog')
                role_manager = IPrincipalRoleManager(grok.getSite())
                principals = role_manager.getPrincipalsForRole('waeup.Student')
                for principal in principals:
                    student_id = principal[0]
                    results = cat.searchResults(student_id=(student_id, student_id))
                    if len(results):
                        continue
                    # The student does no longer exist.
                    nothing_to_do = False
                    role_manager.unsetRoleForPrincipal(
                        'waeup.Student', student_id)
                    removed_student_ids.append(student_id)
                if len(removed_applicant_ids):
                    logger.info(
                        '%s: %s student ids removed from global role map: %s'
                        % (self.log_prefix, len(removed_student_ids),
                           removed_student_ids))
            except ComponentLookupError: # in unit tests
                pass

            if nothing_to_do:
                logger.info(
                    '%s: Updating site at %s: Nothing to do.' % (
                        self.log_prefix, site_name,)
                    )
            return
        elif app_folder is not None:
            # Applicants need update. Remove old instance.
            logger.warn(
                '%s: Outdated applicants folder detected at site %s.'
                'Removing it.' % (self.log_prefix, site_name)
                    )
            del site['applicants']
        # Add new applicants.
        logger.info(
            '%s: Updating site at %s. Installing '
            'applicants.' % (self.log_prefix, site_name,)
            )
        self.setup(site, name, logger)
        return
