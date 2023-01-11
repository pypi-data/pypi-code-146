## $Id: catalog.py 13076 2015-06-19 05:49:57Z henrik $
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
"""Catalog and searching components for academics stuff.
"""
import grok
from grok import index
from hurry.query import Eq, Text
from hurry.query.query import Query
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.index.text.parsetree import ParseError
from zope.intid import IIntIds
#from waeup.kofa.catalog import QueryResultItem
from waeup.kofa.interfaces import IUniversity, IQueryResultItem
from waeup.kofa.university.interfaces import (
    ICourse, ICertificateCourse, IDepartment,
    ICertificate,
    )

class CourseIndexes(grok.Indexes):
    """This catalog is needed for building sources.
    """
    grok.site(IUniversity)
    grok.name('courses_catalog')
    grok.context(ICourse)

    code = index.Field(attribute='code')
    title = index.Text(attribute='title')

class CertificatesIndexes(grok.Indexes):
    """This catalog is needed for building sources.
    """
    grok.site(IUniversity)
    grok.name('certificates_catalog')
    grok.context(ICertificate)

    code = index.Field(attribute='code')
    application_category = index.Field(attribute='application_category')
    title = index.Text(attribute='title')

class CertificateCoursesIndexes(grok.Indexes):
    """This catalog is needed for automatic removal of certificate courses
    and later for selection of course tickets in the students section.
    """
    grok.site(IUniversity)
    grok.name('certcourses_catalog')
    grok.context(ICertificateCourse)

    course_code = index.Field(attribute='getCourseCode')
    level = index.Field(attribute='level')

@grok.subscribe(ICourse, grok.IObjectAddedEvent)
def handle_course_added(obj, event):
    """Index an add course with the local catalog.

    Courses are not indexed automatically, as they are not a
    dictionary subitem of the accompanied site object
    (`IUniversity`). I.e. one cannot get them by asking for
    ``app['FACCODE']['DEPTCODE']['COURSECODE']`` but one has to ask for
    ``app.faculties['FACCODE']['DEPTCODE'].courses['COURSECODE']``.

    Once, a course is indexed we can leave the further handling to
    the default component architechture. At least removals will
    be handled correctly then (and the course unindexed).
    """
    try:
        cat = getUtility(ICatalog, name='courses_catalog')
    except ComponentLookupError:
        # catalog not available. This might happen during tests.
        return
    intids = getUtility(IIntIds)
    index = cat['code']
    index.index_doc(intids.getId(obj), obj)

@grok.subscribe(ICourse, grok.IObjectAddedEvent)
def handle_certificate_added(obj, event):
    """Index an added certificate with the local catalog.

    See handleCourseAdd.
    """
    try:
      cat = getUtility(ICatalog, name='certificates_catalog')
    except ComponentLookupError:
      # catalog not available. This might happen during tests.
      return
    intids = getUtility(IIntIds)
    index = cat['code']
    index.index_doc(intids.getId(obj), obj)

@grok.subscribe(ICertificateCourse, grok.IObjectAddedEvent)
def handlecertificatecourse_added(obj, event):
    """Index an added certificatecourse with the local catalog.

    See handleCourseAdd.
    """
    try:
      cat = getUtility(ICatalog, name='certcourses_catalog')
    except ComponentLookupError:
      # catalog not available. This might happen during tests.
      return
    intids = getUtility(IIntIds)
    index = cat['course_code']
    index.index_doc(intids.getId(obj), obj)

@grok.subscribe(IDepartment, grok.IObjectRemovedEvent)
def handle_department_removed(obj, event):
    """Clear courses and certificates when a department is killed.
    """
    # We cannot use the 'clear()' method of respective subcontainers
    # (courses, certificates), because that would not trigger
    # IObjectRemoved events.
    for subobj_name in ['courses', 'certificates']:
        key_list = list(getattr(obj, subobj_name, {}).keys())
        for key in key_list:
            del getattr(obj, subobj_name)[key]
    return

class CoursesQueryResultItem(object):
    grok.implements(IQueryResultItem)

    def __init__(self, context, view):
        self.context = context
        self.url = view.url(context)
        self.title = context.title
        self.code = context.code
        self.dep = context.__parent__.__parent__.code
        self.fac = context.__parent__.__parent__.__parent__.code
        self.type = 'Course'

class CertificatesQueryResultItem(object):
    grok.implements(IQueryResultItem)

    def __init__(self, context, view):
        self.context = context
        self.url = view.url(context)
        self.title = context.title
        self.code = context.code
        self.dep = context.__parent__.__parent__.code
        self.fac = context.__parent__.__parent__.__parent__.code
        self.type = 'Certificate'

class CertificateCoursesQueryResultItem(object):
    grok.implements(IQueryResultItem)

    def __init__(self, context, view):
        self.context = context
        self.url = view.url(context)
        self.title = context.course.title
        self.code = context.getCourseCode
        self.dep = context.__parent__.__parent__.__parent__.code
        self.fac = context.__parent__.__parent__.__parent__.__parent__.code
        self.type = 'Certificate Course'

def search(query=None, view=None):
    if not query:
        view.flash('Empty search string.')
        return

    hitlist = []
    try:
        results = Query().searchResults(
            Eq(('courses_catalog', 'code'), query))
        for result in results:
            hitlist.append(CoursesQueryResultItem(result, view=view))
        results = Query().searchResults(
            Text(('courses_catalog', 'title'), query))
        for result in results:
            hitlist.append(CoursesQueryResultItem(result, view=view))
        results = Query().searchResults(
            Eq(('certificates_catalog', 'code'), query))
        for result in results:
            hitlist.append(CertificatesQueryResultItem(result, view=view))
        results = Query().searchResults(
            Text(('certificates_catalog', 'title'), query))
        for result in results:
            hitlist.append(CertificatesQueryResultItem(result, view=view))
        results = Query().searchResults(
            Eq(('certcourses_catalog', 'course_code'), query))
        for result in results:
            hitlist.append(CertificateCoursesQueryResultItem(result, view=view))
    except ParseError:
        view.flash('Search string not allowed.')
        return
    return hitlist
