## $Id: faculty.py 15163 2018-09-23 05:05:04Z henrik $
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
"""Faculty components.
"""

import grok
import zope.location.location
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from zope.component import getUtility
from zope.schema import getFields
from waeup.kofa.interfaces import IKofaUtils, IKofaPluggable
from waeup.kofa.utils.batching import VirtualExportJobContainer
from waeup.kofa.university.interfaces import (
    IFaculty, IDepartment)

def longtitle(inst):
    insttypes_dict = getUtility(IKofaUtils).INST_TYPES_DICT
    if inst.title_prefix == 'none':
        return "%s (%s)" % (inst.title, inst.code)
    return "%s %s (%s)" % (
        insttypes_dict[inst.title_prefix],
        inst.title, inst.code)

class VirtualFacultyExportJobContainer(VirtualExportJobContainer):
    """A virtual export job container for facultiess.
    """

class Faculty(grok.Container):
    """A university faculty.
    """
    grok.implements(IFaculty)

    local_roles = [
        'waeup.local.DepartmentOfficer',
        'waeup.local.DepartmentManager',
        'waeup.local.ClearanceOfficer',
        'waeup.local.UGClearanceOfficer',
        'waeup.local.PGClearanceOfficer',
        'waeup.local.CourseAdviser100',
        'waeup.local.CourseAdviser200',
        'waeup.local.CourseAdviser300',
        'waeup.local.CourseAdviser400',
        'waeup.local.CourseAdviser500',
        'waeup.local.CourseAdviser600',
        'waeup.local.CourseAdviser700',
        'waeup.local.CourseAdviser800',
        'waeup.local.LocalStudentsManager',
        'waeup.local.LocalWorkflowManager',
        'waeup.local.TranscriptOfficer',
        'waeup.local.TranscriptSignee',
        ]

    def __init__(self,
                 title=u'Unnamed Faculty',
                 title_prefix=u'faculty',
                 code=u'NA',
                 officer_1=None,
                 officer_2=None,
                 **kw):
        super(Faculty, self).__init__(**kw)
        self.title = title
        self.title_prefix = title_prefix
        self.code = code
        self.officer_1 = officer_1
        self.officer_2 = officer_2

    def traverse(self, name):
        """Deliver appropriate containers.
        """
        if name == 'exports':
            # create a virtual exports container and return it
            container = VirtualFacultyExportJobContainer()
            zope.location.location.located(container, self, 'exports')
            return container
        return None

    def addDepartment(self, department):
        """Add a department to the faculty.
        """
        if not IDepartment.providedBy(department):
            raise TypeError('Faculties contain only IDepartment instances')
        self[department.code] = department

    @property
    def longtitle(self):
        return longtitle(self)

class FacultyFactory(grok.GlobalUtility):
    """A factory for faculty containers.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Faculty')
    title = u"Create a new faculty.",
    description = u"This factory instantiates new faculty instances."

    def __call__(self, *args, **kw):
        return Faculty()

    def getInterfaces(self):
        return implementedBy(Faculty)

class FacultiesPlugin(grok.GlobalUtility):
    """A plugin that updates faculties.
    """

    grok.implements(IKofaPluggable)
    grok.name('faculties')

    deprecated_attributes = []

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        items = getFields(IFaculty).items()
        for faculty in site['faculties'].values():
             # Add new attributes
            for i in items:
                if not hasattr(faculty,i[0]):
                    setattr(faculty,i[0],i[1].missing_value)
                    logger.info(
                        'FacultiesPlugin: %s attribute %s added.' % (
                        faculty.code,i[0]))
            # Remove deprecated attributes
            for i in self.deprecated_attributes:
                try:
                    delattr(faculty,i)
                    logger.info(
                        'FacultiesPlugin: %s attribute %s deleted.' % (
                        faculty.code,i))
                except AttributeError:
                    pass
        return