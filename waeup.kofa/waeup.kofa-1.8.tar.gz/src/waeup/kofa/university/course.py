## $Id: course.py 15629 2019-10-01 10:22:33Z henrik $
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
"""Courses.
"""
import grok
import zope.location.location
from zope.catalog.interfaces import ICatalog
from zope.interface import implementedBy
from zope.schema import getFields
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.component.interfaces import IFactory, ComponentLookupError
from waeup.kofa.interfaces import IKofaPluggable
from waeup.kofa.university.interfaces import ICourse
from waeup.kofa.utils.batching import VirtualExportJobContainer

class VirtualCourseExportJobContainer(VirtualExportJobContainer):
    """A virtual export job container for courses.
    """

class Course(grok.Model):
    """A university course.
    """
    grok.implements(ICourse)

    local_roles = ['waeup.local.Lecturer']

    def __init__(self,
                 title=u'Unnamed Course',
                 code=u'NA',
                 credits=0,
                 passmark=40,
                 semester=1,
                 former_course=False,
                 **kw):
        super(Course, self).__init__(**kw)
        self.title = title
        self.code = code
        self.credits = credits
        self.passmark = passmark
        self.semester = semester
        self.former_course = former_course
        self.results_validated_by = None
        self.results_validation_date = None
        self.results_validation_session = None
        self.score_editing_disabled = False

    def traverse(self, name):
        """Deliver appropriate containers.
        """
        if name == 'exports':
            # create a virtual exports container and return it
            container = VirtualCourseExportJobContainer()
            zope.location.location.located(container, self, 'exports')
            return container
        return None

    @property
    def longtitle(self):
        return "%s (%s)" % (self.title,self.code)

class CourseFactory(grok.GlobalUtility):
    """A factory for courses.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Course')
    title = u"Create a new course.",
    description = u"This factory instantiates new course instances."

    def __call__(self, *args, **kw):
        return Course(*args, **kw)

    def getInterfaces(self):
        return implementedBy(Course)

@grok.subscribe(ICourse, grok.IObjectRemovedEvent)
def handle_course_removed(course, event):
    """If a course is deleted, we make sure that also referrers in a
       certificatescontainer are removed.
    """
    code = course.code

    # Find all certificatecourses that refer to given course
    try:
        cat = getUtility(ICatalog, name='certcourses_catalog')
    except ComponentLookupError:
        # catalog not available. This might happen during tests.
        return

    results = cat.searchResults(course_code=(code, code))

    # remove each found referrer (certs might refer to same course multiple
    # times)
    certs = [x.__parent__ for x in results]
    unique_certs = list(set(certs))
    for cert in unique_certs:
        cert.delCertCourses(code)
    return

@grok.subscribe(ICourse, grok.IObjectModifiedEvent)
def handle_set_former_course(course, event):
    """If a former course attribute is set, we make sure that referrers in a
       certificatescontainer are removed.
    """
    if event.object.former_course:
        handle_course_removed(course, event)
    return

class CoursesPlugin(grok.GlobalUtility):
    """A plugin that updates courses.
    """

    grok.implements(IKofaPluggable)
    grok.name('courses')

    deprecated_attributes = []

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        cat = getUtility(ICatalog, name='courses_catalog')
        results = cat.apply({'code':(None,None)})
        uidutil = getUtility(IIntIds, context=cat)
        items = getFields(ICourse).items()
        for r in results:
            o = uidutil.getObject(r)
            # Add new attributes
            for i in items:
                if not hasattr(o,i[0]):
                    setattr(o,i[0],i[1].missing_value)
                    logger.info(
                        'CoursesPlugin: %s attribute %s added.' % (
                        o.code,i[0]))
            # Remove deprecated attributes
            for i in self.deprecated_attributes:
                try:
                    delattr(o,i)
                    logger.info(
                        'CoursesPlugin: %s attribute %s deleted.' % (
                        o.code,i))
                except AttributeError:
                    pass
        return
