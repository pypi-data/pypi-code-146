## $Id: certificate.py 14652 2017-03-24 06:45:54Z henrik $
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
"""Kofa certificates and certificate courses
"""
import grok
import zope.location.location
from zope.event import notify
from zope.catalog.interfaces import ICatalog
from zope.intid.interfaces import IIntIds
from zope.schema import getFields
from zope.component import getUtility
from zope.component.interfaces import IFactory, ComponentLookupError
from zope.interface import implementedBy
from waeup.kofa.interfaces import IKofaPluggable
from waeup.kofa.university.interfaces import (
    ICertificate, ICertificateCourse)
from waeup.kofa.university.vocabularies import course_levels
from waeup.kofa.utils.batching import VirtualExportJobContainer

class VirtualCertificateExportJobContainer(VirtualExportJobContainer):
    """A virtual export job container for certificates.
    """

class Certificate(grok.Container):
    """A certificate.
    """
    grok.implements(ICertificate)

    local_roles = [
        'waeup.local.CourseAdviser100',
        'waeup.local.CourseAdviser200',
        'waeup.local.CourseAdviser300',
        'waeup.local.CourseAdviser400',
        'waeup.local.CourseAdviser500',
        'waeup.local.CourseAdviser600',
        'waeup.local.CourseAdviser700',
        'waeup.local.CourseAdviser800',
        'waeup.local.DepartmentOfficer',
        'waeup.local.ClearanceOfficer',
        ]

    def __init__(self, code=u'NA', title=u'Unnamed Certificate',
                 study_mode=None, start_level=None,
                 end_level=None, application_category=None,
                 school_fee_1=None, school_fee_2=None,
                 school_fee_3=None, school_fee_4=None,
                 ratio=None, degree=None,
                 custom_textline_1=None, custom_textline_2=None,
                 custom_float_1=None, custom_float_2=None):
        super(Certificate, self).__init__()
        self.code = code
        self.title = title
        self.study_mode = study_mode
        self.start_level = start_level
        self.end_level = end_level
        self.application_category = application_category
        self.school_fee_1 = school_fee_1
        self.school_fee_2 = school_fee_2
        self.school_fee_3 = school_fee_3
        self.school_fee_4 = school_fee_4
        self.ratio = ratio
        self.degree = degree
        self.custom_textline_1 = custom_textline_1
        self.custom_textline_2 = custom_textline_2
        self.custom_float_1 = custom_float_1
        self.custom_float_2 = custom_float_2

    def traverse(self, name):
        """Deliver appropriate containers.
        """
        if name == 'exports':
            # create a virtual exports container and return it
            container = VirtualCertificateExportJobContainer()
            zope.location.location.located(container, self, 'exports')
            return container
        return None

    @property
    def longtitle(self):
        return "%s (%s)" % (self.title,self.code)

    def addCertCourse(self, course, level=100,
                      mandatory=True, course_category=None):
        """Add a certificate course.
        """
        code = "%s_%s" % (course.code, level)
        self[code] = CertificateCourse(course, level, mandatory, course_category)
        self[code].__parent__ = self
        self[code].__name__ = code
        self._p_changed = True

    def delCertCourses(self, code, level=None):
        """Delete certificate courses.

        We might have more than one certificate course for a course.
        If level is not provided all certificate courses referring
        to the same course will be deleted.
        """
        keys = list(self.keys()) # create list copy
        for key in keys:
            if self[key].getCourseCode() != code:
                continue
            if level is not None and str(self[key].level) != str(level):
                # found a course with correct key but wrong level...
                continue
            del self[key]
            self._p_changed = True
        return

    def moveCertificate(self, facname, depname, newcode):
        self.moved = True
        cert = self
        oldcode = cert.code
        cert.code = newcode
        del self.__parent__[oldcode]
        newdep = grok.getSite()['faculties'][facname][depname]
        newdep.certificates[newcode] = cert
        #self.__parent__._p_changed = True
        cat = getUtility(ICatalog, name='students_catalog')
        results = cat.searchResults(certcode=(oldcode, oldcode))
        for student in results:
            notify(grok.ObjectModifiedEvent(student))
            student.__parent__.logger.info(
                '%s - Certificate moved' % student.__name__)
        return

class CertificateFactory(grok.GlobalUtility):
    """A factory for certificates.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Certificate')
    title = u"Create a new certificate.",
    description = u"This factory instantiates new certificate instances."

    def __call__(self, *args, **kw):
        return Certificate(*args, **kw)

    def getInterfaces(self):
        return implementedBy(Certificate)

class CertificateCourse(grok.Model):
    grok.implements(ICertificateCourse)

    def __init__(self, course=None, level=100,
                 mandatory=True, course_category=None):
        self.course = course
        self.level = level
        self.mandatory = mandatory
        self.course_category = course_category

    def getCourseCode(self):
        """Get code of a course.
        """
        return self.course.code

    @property
    def longtitle(self):
        return "%s in level %s" % (self.course.code,
                   course_levels.getTerm(self.level).title)

class CertificateCourseFactory(grok.GlobalUtility):
    """A factory for certificate courses.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.CertificateCourse')
    title = u"Create a new certificate course.",
    description = u"This factory instantiates new certificate courses."

    def __call__(self, *args, **kw):
        return CertificateCourse(*args, **kw)

    def getInterfaces(self):
        return implementedBy(CertificateCourse)

@grok.subscribe(ICertificate, grok.IObjectRemovedEvent)
def handle_certificate_removed(certificate, event):
    """If a certificate is deleted, we make sure that also referrers to
    student studycourse objects are removed.
    """
    # Do not remove referrer if certificate is going to move
    if getattr(certificate, 'moved', False):
        return

    code = certificate.code

    # Find all student studycourses that refer to given certificate...
    try:
        cat = getUtility(ICatalog, name='students_catalog')
    except ComponentLookupError:
        # catalog not available. This might happen during tests.
        return

    results = cat.searchResults(certcode=(code, code))
    for student in results:
        # Remove that referrer...
        studycourse = student['studycourse']
        studycourse.certificate = None
        notify(grok.ObjectModifiedEvent(student))
        student.__parent__.logger.info(
            'ObjectRemovedEvent - %s - removed: certificate' % student.__name__)
    return

class CertificatesPlugin(grok.GlobalUtility):
    """A plugin that updates certificates.
    """

    grok.implements(IKofaPluggable)
    grok.name('certificates')

    deprecated_attributes = []

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        cat = getUtility(ICatalog, name='certificates_catalog')
        results = cat.apply({'code':(None,None)})
        uidutil = getUtility(IIntIds, context=cat)
        items = getFields(ICertificate).items()
        for r in results:
            o = uidutil.getObject(r)
            # Add new attributes
            for i in items:
                if not hasattr(o,i[0]):
                    setattr(o,i[0],i[1].missing_value)
                    logger.info(
                        'CertificatesPlugin: %s attribute %s added.' % (
                        o.code,i[0]))
            # Remove deprecated attributes
            for i in self.deprecated_attributes:
                try:
                    delattr(o,i)
                    logger.info(
                        'CertificatesPlugin: %s attribute %s deleted.' % (
                        o.code,i))
                except AttributeError:
                    pass
        return

class CertificateCoursesPlugin(grok.GlobalUtility):
    """A plugin that updates certificate courses.
    """

    grok.implements(IKofaPluggable)
    grok.name('certcourses')

    deprecated_attributes = []

    def setup(self, site, name, logger):
        return

    def update(self, site, name, logger):
        cat = getUtility(ICatalog, name='certcourses_catalog')
        results = cat.apply({'course_code':(None,None)})
        uidutil = getUtility(IIntIds, context=cat)
        items = getFields(ICertificateCourse).items()
        for r in results:
            o = uidutil.getObject(r)
            # Add new attributes
            for i in items:
                if not hasattr(o,i[0]):
                    setattr(o,i[0],i[1].missing_value)
                    logger.info(
                        'CertificateCoursesPlugin: %s/%s_%s attribute %s added.' % (
                        o.__parent__.code,o.course.code,o.level,i[0]))
            # Remove deprecated attributes
            for i in self.deprecated_attributes:
                try:
                    delattr(o,i)
                    logger.info(
                        'CertificateCoursesPlugin: %s/%s_%s attribute %s deleted.' % (
                        o.__parent__.code,o.course.code,o.level,i))
                except AttributeError:
                    pass
        return
