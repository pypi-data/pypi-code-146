## $Id: container.py 16134 2020-06-28 18:01:52Z henrik $
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
Containers for university applicants.
"""
from random import SystemRandom as r
import grok
import pytz
from datetime import datetime
import zope.location.location
from zope.component import getUtility, ComponentLookupError
from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.catalog.interfaces import ICatalog
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.applicants.interfaces import (
    IApplicantsContainer, IApplicantsContainerAdd, IApplicant,
    IApplicantsUtils)
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.utils.batching import VirtualExportJobContainer

def generate_applicant_id(container=None):
    if container is not None:
        key = r().randint(99999,1000000)
        while str(key) in container.keys():
            key = r().randint(99999,1000000)
        return u"%s_%d" % (container.code, key)
    else:
        # In some tests we don't use containers
        return u"xxx_1234"

class VirtualApplicantsExportJobContainer(VirtualExportJobContainer):
    """A virtual export job container for applicants container.
    """

class ApplicantsContainer(grok.Container):
    """An applicants container contains university applicants.
    """
    grok.implements(IApplicantsContainer,IApplicantsContainerAdd)

    description_dict = {}

    local_roles = [
        'waeup.local.ApplicationsManager',
        ]

    @property
    def picture_editable(self):
        try:
            return getUtility(IApplicantsUtils).isPictureEditable(self)
        except ComponentLookupError:  # happens in unit tests
            return

    def addApplicant(self, applicant):
        """Add an applicant.
        """
        if not IApplicant.providedBy(applicant):
            raise TypeError(
                'ApplicantsContainers contain only IApplicant instances')
        if applicant.applicant_id is None:
            applicant_id = generate_applicant_id(container=self)
            applicant.applicant_id = applicant_id
        self[applicant.application_number] = applicant
        return

    @property
    def counts(self):
        total = len(self)
        code = self.code + '+'
        cat = getUtility(ICatalog, name='applicants_catalog')
        results = list(
           cat.searchResults(container_code=(code, code)))
        return len(self), len(results)

    @property
    def first_unused(self):
        code = self.code + '-'
        cat = getUtility(ICatalog, name='applicants_catalog')
        results = list(
           cat.searchResults(container_code=(code, code)))
        if results:
            return results[0]
        return

    @property
    def statistics(self):
        try:
          statistics = getUtility(
              IApplicantsUtils).getApplicantsStatistics(self)
        except ComponentLookupError:  # happens in unit tests
            return
        return statistics

    @property
    def expired(self):
        # Check if application has started ...
        if not self.startdate or (
            self.startdate > datetime.now(pytz.utc)):
            return True
        # ... or ended
        if not self.enddate or (
            self.enddate < datetime.now(pytz.utc)):
            return True
        return False

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.logger.info(
            '%s - %s - %s' % (ob_class, self.code, message))
        return

    def traverse(self, name):
        """Deliver virtual export container.
        """
        if name == 'exports':
            # create a virtual exports container and return it
            container = VirtualApplicantsExportJobContainer()
            zope.location.location.located(container, self, 'exports')
            return container
        return None

ApplicantsContainer = attrs_to_fields(ApplicantsContainer)

# ApplicantsContainers must be importable. So we need a factory.
class ApplicantsContainerFactory(grok.GlobalUtility):
    """A factory for student online payments.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.ApplicantsContainer')
    title = u"Create a new container for applicants.",
    description = u"This factory instantiates new IApplicantsContainer instances."

    def __call__(self, *args, **kw):
        return ApplicantsContainer()

    def getInterfaces(self):
        return implementedBy(ApplicantsContainer)
