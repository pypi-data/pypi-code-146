## $Id: breadcrumbs.py 12912 2015-05-08 07:03:44Z henrik $
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
""" Components to get breadcrumbs for any object.
"""
import grok
from grokcore.view.interfaces import IGrokView
from zope.component import getAdapter
from zope.publisher.browser import TestRequest

from waeup.kofa.interfaces import (
    IConfigurationContainer, ISessionConfiguration, IExportJobContainer)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.browser.interfaces import (
    IBreadcrumb, IBreadcrumbIgnorable, IBreadcrumbContainer, IKofaObject,
    IUniversity, IFacultiesContainer, IUsersContainer, IDataCenter, IFaculty,
    IDepartment, ICourse, ICertificate, ICoursesContainer, ICertificateCourse,
    ICertificatesContainer
    )
from waeup.kofa.reports import IReportsContainer

class Breadcrumb(grok.Adapter):
    """A most general breadcrumb generator.
    """
    grok.provides(IBreadcrumb)
    grok.context(IKofaObject)
    grok.name('index')

    _title = None
    _parent = 0
    _request = None
    parent_viewname = 'index'
    viewname = 'index'

    def __init__(self, context):
        """Turn a context into a breadcrumb.
        """
        self.context = context

    @property
    def title(self):
        """Get a title for a context.
        """
        if self._title is not None:
            return self._title
        if hasattr(self.context, 'title'):
            return self.context.title
        if hasattr(self.context, 'name'):
            return self.context.name
        return None

    @property
    def parent(self):
        """Get the contexts parent object and viewname or None.
        """
        if self._parent is None:
            return None
        if self._parent is not 0:
            return (self._parent, self.parent_viewname)

        if self.viewname != 'index':
            self._parent = self.context
        else:
            site = grok.getSite()
            if self.context is not site:
                self._parent = getattr(self.context, '__parent__', None)

        if self._parent is not None:
            return (self._parent, self.parent_viewname)
        return None

    @property
    def target(self):
        return self.viewname

class UniversityBreadcrumb(Breadcrumb):
    """A breadcrumb for university index pages.
    """
    grok.context(IUniversity)
    title = _(u'Home')
    parent = None

class PortalSettingsBreadcrumb(Breadcrumb):
    """A breadcrumb for the manage view of universities.

    Here we need a special `parent()` implementation, because the
    parent object is not a real parent (the University object has no
    valid parent in terms of breadcrumbs). Instead it is the
    ``administration`` view of the same context the ``manage`` page
    itself is bound to.
    """
    grok.context(IUniversity)
    grok.name('manage')
    title = _(u'Portal Settings')

    @property
    def parent(self):
        """Return the 'administration' view of our context as parent.
        """
        return (self.context, 'administration')

class FacultiesContainerBreadcrumb(Breadcrumb):
    """A breadcrumb for faculty containers.
    """
    grok.context(IFacultiesContainer)
    title = _(u'Academics')

class AdministrationBreadcrumb(Breadcrumb):
    """A breadcrumb for administration areas of University instances.
    """
    grok.context(IUniversity)
    grok.name('administration')
    title = _(u'Administration')
    viewname = 'administration'

class ConfigurationContainerBreadcrumb(Breadcrumb):
    """A breadcrumb for the configuration container.
    """
    grok.context(IConfigurationContainer)
    title = _(u'Portal Configuration')
    parent_viewname = 'administration'

class SessionConfigurationBreadcrumb(Breadcrumb):
    """A breadcrumb for the configuration container.
    """
    grok.context(ISessionConfiguration)
    title = u'Portal Session Configuration'

    @property
    def title(self):
        session_string = self.context.getSessionString()
        return 'Session %s' % session_string

class UsersContainerBreadcrumb(Breadcrumb):
    """A breadcrumb for user containers.
    """
    grok.context(IUsersContainer)
    title = _(u'Officers')
    parent_viewname = 'administration'

class DataCenterBreadcrumb(Breadcrumb):
    """A breadcrumb for data centers.
    """
    grok.context(IDataCenter)
    title = _(u'Data Center')
    parent_viewname = 'administration'

class ReportsBreadcrumb(Breadcrumb):
    """A breadcrumb for reports.
    """
    grok.context(IReportsContainer)
    title = _(u'Reports')
    parent_viewname = 'administration'
    target = None

class ExportsBreadcrumb(Breadcrumb):
    """A breadcrumb for exports.
    """
    grok.context(IExportJobContainer)
    title = _(u'Student Data Exports')
    target = None

class FacultyBreadcrumb(Breadcrumb):
    """A breadcrumb for faculties.
    """
    grok.context(IFaculty)

    @property
    def title(self):
        return self.context.longtitle

class DepartmentBreadcrumb(FacultyBreadcrumb):
    """A breadcrumb for departments.
    """
    grok.context(IDepartment)

class CourseBreadcrumb(FacultyBreadcrumb):
    """A breadcrumb for courses.
    """
    grok.context(ICourse)

class CertificateBreadcrumb(FacultyBreadcrumb):
    """A breadcrumb for certificates.
    """
    grok.context(ICertificate)

class CoursesContainerBreadcrumb(Breadcrumb):
    """ We don't want course container breadcrumbs.
    """
    grok.context(ICoursesContainer)
    grok.implements(IBreadcrumbIgnorable)

class CertificatesContainerBreadcrumb(Breadcrumb):
    """ We don't want course container breadcrumbs.
    """
    grok.context(ICertificatesContainer)
    grok.implements(IBreadcrumbIgnorable)

class CertificateCourseBreadcrumb(Breadcrumb):
    """ We don't want course container breadcrumbs.
    """
    grok.context(ICertificateCourse)
    @property
    def title(self):
        return self.context.longtitle

def getBreadcrumb(obj, viewname=None):
    """ Get a breadcrumb for an object and a viewname.

    If there is no breadcrumb defined for such a combination, a
    breadcrumb for the ``index`` view will be looked up.
    """
    try:
        return getAdapter(obj, IBreadcrumb, name=viewname)
    except:
        pass
    return getAdapter(obj, IBreadcrumb, name='index')

def getBreadcrumbList(obj, viewname):
    """Get an ordered list of breadcrumbs for an object and a viewname.

    Ignorables are excluded from the result.
    """
    current = getBreadcrumb(obj, viewname)
    result = [current]
    while current.parent is not None:
        context, viewname = current.parent
        current = getBreadcrumb(context, viewname)
        if IBreadcrumbIgnorable.providedBy(current):
            # Ignore empty breadcrumbs...
            continue
        result.append(current)
    result.reverse()
    return result

def getBreadcrumbListForView(view):
    """Get an ordered list of breadcrumbs a certain view.

    Ignorables are excluded from the result.
    """
    context = getattr(view, 'context')
    viewname = getattr(view, '__name__')
    return getBreadcrumbList(context, viewname)

class BreadcrumbContainer(grok.Adapter):
    """An adapter to adapt grok views to list of breadcrumbs.
    """
    grok.context(IGrokView)
    grok.provides(IBreadcrumbContainer)

    _breadcrumbs = None

    def __init__(self, context):
        self.context = context
        self._breadcrumbs = getBreadcrumbListForView(self.context)

    def __iter__(self):
        """Allow iteration.
        """
        return self._breadcrumbs.__iter__()

    def getList(self):
        """Get the (ordered) list of breadcrumbs liked to the context view.
        """
        return self._breadcrumbs
