## $Id: catalog.py 15417 2019-05-21 09:16:47Z henrik $
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
"""Cataloging and searching components for students.
"""
import grok
from grok import index
from hurry.query import Eq, Text
from hurry.query.query import Query
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from waeup.kofa.catalog import FilteredCatalogQueryBase
from waeup.kofa.interfaces import (
    IUniversity, IQueryResultItem, academic_sessions_vocab)
from waeup.kofa.students.interfaces import IStudent, ICourseTicket
from waeup.kofa.university.vocabularies import course_levels
from waeup.kofa.students.workflow import TRANSREQ, TRANSVAL, GRADUATED

class StudentsCatalog(grok.Indexes):
    """A catalog for students.
    """
    grok.site(IUniversity)
    grok.name('students_catalog')
    grok.context(IStudent)

    student_id = index.Field(attribute='student_id')
    fullname = index.Text(attribute='fullname')
    email = index.Field(attribute='email')
    reg_number = index.Field(attribute='reg_number')
    matric_number = index.Field(attribute='matric_number')
    state = index.Field(attribute='state')
    certcode = index.Field(attribute='certcode')
    depcode = index.Field(attribute='depcode')
    faccode = index.Field(attribute='faccode')
    current_session = index.Field(attribute='current_session')
    current_level = index.Field(attribute='current_level')
    current_mode = index.Field(attribute='current_mode')

class StudentQueryResultItem(object):
    grok.implements(IQueryResultItem)

    title = u'Student Query Item'
    description = u'Some student found in a search'

    def __init__(self, context, view):
        self.context = context
        self.url = view.url(context)
        self.student_id = context.student_id
        self.display_fullname = context.display_fullname
        self.reg_number = context.reg_number
        self.matric_number = context.matric_number
        self.state = context.state
        self.translated_state = context.translated_state
        self.current_level = context['studycourse'].current_level
        try:
            current_session = academic_sessions_vocab.getTerm(
                context['studycourse'].current_session).title
        except LookupError:
            current_session = None
        self.current_session = current_session
        self.certificate = context['studycourse'].certificate
        self.comment = getattr(context, 'officer_comment', None)

def search(query=None, searchtype=None, view=None):
    hitlist = []
    if searchtype in ('fullname',):
        results = Query().searchResults(
            Text(('students_catalog', searchtype), query))
    elif searchtype == 'suspended':
        # 'suspended' is not indexed
        cat = queryUtility(ICatalog, name='students_catalog')
        all = cat.searchResults(student_id=(None, None))
        for student in all:
            if student.suspended:
                hitlist.append(StudentQueryResultItem(student, view=view))
        return hitlist
    elif searchtype in (TRANSREQ, TRANSVAL, GRADUATED):
        cat = queryUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(state=(searchtype, searchtype))
    else:
        # Temporary solution to display all students added
        if query == '*':
            cat = queryUtility(ICatalog, name='students_catalog')
            results = cat.searchResults(student_id=(None, None))
        else:
            results = Query().searchResults(
                Eq(('students_catalog', searchtype), query))
    for result in results:
        hitlist.append(StudentQueryResultItem(result, view=view))
    return hitlist

class SimpleFieldSearch(object):
    """A programmatic (no UI required) search.

    Looks up a given field attribute of the students catalog for a
    single value. So normally you would call an instance of this
    search like this:

      >>> SimpleFieldSearch()(reg_number='somevalue')

    """
    catalog_name = 'students_catalog'
    def __call__(self, **kw):
        """Search students catalog programmatically.
        """
        if len(kw) != 1:
            raise ValueError('must give exactly one index name to search')
        cat = queryUtility(ICatalog, name=self.catalog_name)
        index_name, query_term = kw.items()[0]
        results = cat.searchResults(index_name=(query_term, query_term))
        return results

#: an instance of `SimpleFieldSearch` looking up students catalog.
simple_search = SimpleFieldSearch()

class CourseTicketIndexes(grok.Indexes):
    """A catalog for course tickets.
    """
    grok.site(IUniversity)
    grok.name('coursetickets_catalog')
    grok.context(ICourseTicket)

    level = index.Field(attribute='level')
    session = index.Field(attribute='level_session')
    code = index.Field(attribute='code')

class StudentsQuery(FilteredCatalogQueryBase):
    """Query students in a site. See waeup.kofa.catalog for more info.
    """
    cat_name = 'students_catalog'
    defaults = dict(student_id=None) # make sure we get all studs by default

class CourseTicketsQuery(FilteredCatalogQueryBase):
    """Query students in a site. See waeup.kofa.catalog for more info.
    """
    cat_name = 'coursetickets_catalog'
    defaults = dict(code=None) # make sure we get all tickets by default
