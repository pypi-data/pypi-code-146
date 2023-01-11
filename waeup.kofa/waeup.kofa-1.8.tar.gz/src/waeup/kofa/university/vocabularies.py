## $Id: vocabularies.py 16812 2022-02-16 15:50:47Z henrik $
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
"""Vocabularies and sources for the academic section.
"""
from zc.sourcefactory.basic import BasicSourceFactory
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility, queryUtility
from waeup.kofa.interfaces import (
    SimpleKofaVocabulary, IKofaUtils, ContextualDictSourceFactoryBase)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.sourcefactory import SmartBasicContextualSourceFactory
from waeup.kofa.utils.utils import KofaUtils

course_levels = SimpleKofaVocabulary(
    (_('None'),0),
    (_('Pre-Studies'),10),
    (_('100 (Year 1)'),100),
    (_('200 (Year 2)'),200),
    (_('300 (Year 3)'),300),
    (_('400 (Year 4)'),400),
    (_('500 (Year 5)'),500),
    (_('600 (Year 6)'),600),
    (_('700 (Year 7)'),700),
    (_('800 (Year 8)'),800),
    (_('900 (Year 9)'),900),
    (_('Postgraduate Level'),999),
    (_('Modules Level'),1000),
    )

class SemesterSource(ContextualDictSourceFactoryBase):
    """An institution type source delivers semester and/or term descriptors.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'SEMESTER_DICT'

class InstTypeSource(ContextualDictSourceFactoryBase):
    """An institution type source delivers types of institutions
    in the portal.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'INST_TYPES_DICT'

class AppCatSource(ContextualDictSourceFactoryBase):
    """A application category source delivers all application categories
    provided in the portal.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'APP_CATS_DICT'

class StudyModeSource(ContextualDictSourceFactoryBase):
    """A study modes source delivers all study modes provided
    in the portal.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'STUDY_MODES_DICT'

class DegreeSource(ContextualDictSourceFactoryBase):
    """A source for certificate degrees
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'DEGREES_DICT'

    def getTitle(self, context, value):
        utils = getUtility(IKofaUtils)
        return "%s (%s)" % (getattr(utils, self.DICT_NAME)[value], value)

class CourseSource(BasicSourceFactory):
    """A course source delivers all courses inside the portal by looking
       up a catalog.
    """
    def getValues(self):
        catalog = getUtility(ICatalog, name='courses_catalog')
        return sorted(list(
                catalog.searchResults(
                    code=(None, None))),key=lambda value: value.code)

    def getToken(self, value):
        return value.code

    def getTitle(self, value):
        return "%s - %s" % (value.code, value.title[:64])

class CourseCategorySource(ContextualDictSourceFactoryBase):
    """A course category source provides additional information on
    the course.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'COURSE_CATEGORY_DICT'


class CertificateSource(SmartBasicContextualSourceFactory):
    """A certificate source delivers all certificates provided
    in the portal.
    """
    def getValues(self, context):
        catalog = getUtility(ICatalog, name='certificates_catalog')
        return sorted(list(
            catalog.searchResults(
                code=(None, None))),
                      key=lambda value: value.code)

    def getToken(self, context, value):
        return value.code

    def getTitle(self, context, value):
        return "%s - %s" % (value.code, value.title)

class SpecialApplicationSource(ContextualDictSourceFactoryBase):
    """A special application source delivers all types of
    applications which are not linked with certificates.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'SPECIAL_APP_DICT'
