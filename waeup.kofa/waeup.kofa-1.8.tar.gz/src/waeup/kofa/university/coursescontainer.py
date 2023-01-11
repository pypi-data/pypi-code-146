## $Id: coursescontainer.py 8367 2012-05-06 11:19:38Z henrik $
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
"""Course containers.
"""
import grok
from zope.interface import implementedBy
from zope.component.interfaces import IFactory, ComponentLookupError
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from waeup.kofa.interfaces import DuplicationError
from waeup.kofa.university.interfaces import ICoursesContainer, ICourse

class CoursesContainer(grok.Container):
    """See interfaces for description.
    """
    grok.implements(ICoursesContainer)

    def __setitem__(self, name, course):
        """See corresponding docstring in certificatescontainer.py.
        """
        if not ICourse.providedBy(course):
            raise TypeError('CoursesContainers contain only '
                            'ICourse instances')

        # Only accept courses with code == key.
        if course.code != name:
            raise ValueError('key must match course code: '
                             '%s, %s' % (name, course.code))

        # Lookup catalog. If we find none: no duplicates possible.
        cat = queryUtility(ICatalog, name='courses_catalog', default=None)
        if cat is not None:
            entries = cat.searchResults(
                code=(course.code,course.code))
            if len(entries) > 0:
                raise DuplicationError(
                    'Course exists already elsewhere.', entries)
        else:
            # No catalog, then this addition won't do harm to anything.
            pass
        super(CoursesContainer, self).__setitem__(name, course)

    def addCourse(self, course):
        """See corresponding docstring in certificatescontainer.py.
        """
        self[getattr(course, 'code', None)] = course

    def clear(self):
        """See corresponding docstring and comments in certificatescontainer.py.
        """
        self._SampleContainer__data.clear()
        del self.__dict__['_BTreeContainer__len']

class CoursesContainerFactory(grok.GlobalUtility):
    """A factory for course containers.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.CoursesContainer')
    title = u"Create a new container for courses.",
    description = u"This factory instantiates new containers for courses."

    def __call__(self, *args, **kw):
        return CoursesContainer(*args, **kw)

    def getInterfaces(self):
        return implementedBy(CoursesContainer)
