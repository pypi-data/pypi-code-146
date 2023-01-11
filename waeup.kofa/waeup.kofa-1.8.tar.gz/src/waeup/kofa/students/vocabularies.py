## $Id: vocabularies.py 16825 2022-02-22 08:13:17Z henrik $
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
"""Vocabularies and sources for the students section.
"""
from zope.component import getUtility, queryUtility
from zope.catalog.interfaces import ICatalog
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import ISource, IContextSourceBinder
from zope.schema.interfaces import ValidationError
from zc.sourcefactory.basic import BasicSourceFactory
from zc.sourcefactory.contextual import BasicContextualSourceFactory
from waeup.kofa.interfaces import SimpleKofaVocabulary
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import get_sorted_preferred
from waeup.kofa.utils.countries import COUNTRIES
from waeup.kofa.university.vocabularies import course_levels
from waeup.kofa.university.certificate import Certificate


#: a tuple of tuples (<COUNTRY-NAME>, <ISO-CODE>) with Nigeria first.
COUNTRIES = get_sorted_preferred(COUNTRIES, ['NG'])
nats_vocab = SimpleKofaVocabulary(*COUNTRIES)

def levels_from_range(start_level=None, end_level=None):
    """Get a list of valid levels for given start/end level.

    Start and end level must be numbers (or ``None``).

    If no start/end level is given, return the default list of levels.

    If only one of start_level or end_level is given, the result is
    undefined.
    """
    if 999 in (start_level, end_level):
        return [999]
    if 1000 in (start_level, end_level):
        return [1000]
    levels = [10,] + [
        level for level in range(100,1000,10) if level % 100 < 30]
    if start_level is None and end_level is None:
        return levels + [999, 1000]
    if start_level == 10 == end_level:
        return [10,]
    start_level, end_level = (start_level or 10, end_level or 900)
    levels = [x for x in levels
              if x >= start_level and x <= (end_level + 120)]
    return levels

def study_levels(context):
    if isinstance(context, Certificate):
        certificate = context
    else:
        certificate = getattr(context, 'certificate', None)
    start_level, end_level = (None, None)
    if  certificate is not None:
        start_level = int(certificate.start_level)
        end_level = int(certificate.end_level)
    return [0,] + levels_from_range(start_level, end_level)

class StudyLevelSource(BasicContextualSourceFactory):
    """The StudyLevelSource is based on and extends the
    course_levels vocabulary defined in the university package.
    Repeating study levels are denoted by increments of 10, the
    first spillover level by the certificate's end level plus 100
    and the second spillover level by the end level plus 110.
    The level zero contains all courses without level
    affiliation.
    """
    def getValues(self, context):
        return study_levels(context)

    def getToken(self, context, value):
        return str(value)

    def getTitle(self, context, value):
        if isinstance(context, Certificate):
            # We use this source also for various reports.
            # In such a case the context of the source will be the
            # certificate itself.
            certificate = context
        else:
            certificate = getattr(context, 'certificate', None)
        if certificate is not None:
            start_level = int(certificate.start_level)
            end_level = int(certificate.end_level)
        else:
            # default level range
            start_level = 10
            end_level = 900
        if 999 in (start_level, end_level):
            if value != 999:
                return _('Error: wrong level id ${value}',
                    mapping={'value': value})
        if value == 0:
            return _('Level Zero')
        if value == 999:
            return course_levels.by_value[999].title
        if 1000 in (start_level, end_level):
            if value != 1000:
                return _('Error: wrong level id ${value}',
                    mapping={'value': value})
        if value == 1000:
            return course_levels.by_value[1000].title
        if start_level == 10 and end_level == 10 and value != 10:
            return _('Error: level id ${value} out of range',
                mapping={'value': value})
        if value < start_level or value > end_level + 120:
            return _('Error: level id ${value} out of range',
                mapping={'value': value})
        # Special treatment for pre-studies level
        if value == 10:
            return course_levels.by_value[value].title
        level,repeat = divmod(value, 100)
        level = level * 100
        repeat = repeat//10
        title = course_levels.by_value[level].title
        if level > end_level and repeat == 1:
            title = course_levels.by_value[level - 100].title
            return _('${title} 2nd spillover', mapping={'title': title})
        if level > end_level and repeat == 2:
            title = course_levels.by_value[level - 100].title
            return _('${title} 3rd spillover', mapping={'title': title})
        if level > end_level:
            title = course_levels.by_value[level - 100].title
            return  _('${title} 1st spillover', mapping={'title': title})
        if repeat == 1:
            return _('${title} on 1st probation', mapping={'title': title})
        if repeat == 2:
            return _('${title} on 2nd probation', mapping={'title': title})
        return title

class GenderSource(BasicSourceFactory):
    """A gender source delivers basically a mapping
       ``{'m': 'Male', 'f': 'Female'}``

       Using a source, we make sure that the tokens (which are
       stored/expected for instance from CSV files) are something one
       can expect and not cryptic IntIDs.
    """
    def getValues(self):
        return ['m', 'f']

    def getToken(self, value):
        return value[0].lower()

    def getTitle(self, value):
        if value == 'm':
            return _('male')
        if value == 'f':
            return _('female')

class RegNumNotInSource(ValidationError):
    """Registration number exists already
    """
    # The docstring of ValidationErrors is used as error description
    # by zope.formlib.
    pass

class MatNumNotInSource(ValidationError):
    """Matriculation number exists already
    """
    # The docstring of ValidationErrors is used as error description
    # by zope.formlib.
    pass

class RegNumberSource(object):
    """A source that accepts any entry for a certain field if not used
    already.

    Using this kind of source means a way of setting an invariant.

    We accept a value iff:
    - the value cannot be found in catalog or
    - the value can be found as part of some item but the bound item
    is the context object itself.
    """
    implements(ISource)
    cat_name = 'students_catalog'
    field_name = 'reg_number'
    validation_error = RegNumNotInSource
    comp_field = 'student_id'
    def __init__(self, context):
        self.context = context
        return

    def __contains__(self, value):
        """We accept all values not already given to other students.
        """
        cat = queryUtility(ICatalog, self.cat_name)
        if cat is None:
            return True
        kw = {self.field_name: (value, value)}
        results = cat.searchResults(**kw)
        for entry in results:
            if not hasattr(self.context, self.comp_field):
                # we have no context with comp_field (most probably
                # while adding a new object, where the container is
                # the context) which means that the value was given
                # already to another object (as _something_ was found in
                # the catalog with that value). Fail on first round.
                raise self.validation_error(value)
            if getattr(entry, self.comp_field) != getattr(
                self.context, self.comp_field):
                # An entry already given to another student is not in our
                # range of acceptable values.
                raise self.validation_error(value)
                #return False
        return True

def contextual_reg_num_source(context):
    source = RegNumberSource(context)
    return source
directlyProvides(contextual_reg_num_source, IContextSourceBinder)

class MatNumberSource(RegNumberSource):
    field_name = 'matric_number'
    validation_error = MatNumNotInSource

def contextual_mat_num_source(context):
    source = MatNumberSource(context)
    return source
directlyProvides(contextual_mat_num_source, IContextSourceBinder)
