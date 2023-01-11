## $Id: export.py 16450 2021-04-11 10:17:28Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
"""Exporters for faculties, departments, and other academics components.
"""
import grok
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.batching import ExporterBase


class FacultyExporter(grok.GlobalUtility, ExporterBase):
    """The Faculty Exporter exports all faculties in the `faculties`
    container. This is the only place where faculties are stored.
    """
    grok.implements(ICSVExporter)
    grok.name('faculties')

    fields = ('code', 'title', 'title_prefix', 'users_with_local_roles',
              'officer_1', 'officer_2')

    title = _(u'Faculties')

    def mangle_value(self, value, name, context=None):
        """The mangler computes the `users_with_local_roles` value which
        is a Python expression like:

        ``[{'user_name': u'bob', 'local_role': u'bobsrole'},
        {'user_name': u'anna', 'local_role': u'annasrole'}]``
        """
        if name == 'users_with_local_roles':
            value = []
            role_map = IPrincipalRoleMap(context)
            for local_role, user_name, setting in \
                role_map.getPrincipalsAndRoles():
                value.append({'user_name':user_name,'local_role':local_role})
        return super(FacultyExporter, self).mangle_value(
            value, name, context)

    def export(self, faculties, filepath=None):
        """Export `faculties`, an iterable, as CSV file.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        for faculty in faculties:
            self.write_item(faculty, writer)
        return self.close_outfile(filepath, outfile)

    def export_all(self, site, filepath=None):
        """Export faculties in facultycontainer into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        faculties = site.get('faculties', {})
        return self.export(faculties.values(), filepath)


class DepartmentExporter(FacultyExporter, grok.GlobalUtility):
    """The Department Exporter exports all departments stored in the faculty
    containers. The exporter iterates over all faculties and then over all
    departments inside each faculty container.
    """
    grok.implements(ICSVExporter)
    grok.name('departments')

    fields = ('code', 'faculty_code', 'title', 'title_prefix',
              'users_with_local_roles',
              'officer_1', 'officer_2','officer_3', 'officer_4')

    title = _(u'Departments')

    def mangle_value(self, value, name, context=None):
        """The mangler additionally computes the faculty_code value
        which is the code (= object id) of the faculty that hosts
        the department.
        """
        if name == 'faculty_code':
            value = getattr(
                getattr(context, '__parent__', None),
                'code', None)
        return super(DepartmentExporter, self).mangle_value(
            value, name, context)

    def export_all(self, site, filepath=None):
        """Export departments in faculty into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        faculties = site.get('faculties', {})
        for faculty in faculties.values():
            for department in faculty.values():
                self.write_item(department, writer)
        return self.close_outfile(filepath, outfile)


class CourseExporter(FacultyExporter, grok.GlobalUtility):
    """The Course Exporter exports all courses in the database. It iterates
    over all departments and faculties.
    """
    grok.implements(ICSVExporter)
    grok.name('courses')

    fields = ('code', 'faculty_code', 'department_code', 'title', 'credits',
              'passmark', 'semester', 'users_with_local_roles', 'former_course',
              'results_validated_by', 'results_validation_date',
              'results_validation_session')

    title = _(u'Courses')

    def mangle_value(self, value, name, context=None):
        """The mangler additionally computes the department_code value
        which is the code of the department that offers the course.
        """
        if name == 'users_with_local_roles':
            value = []
            role_map = IPrincipalRoleMap(context)
            for local_role, user_name, setting in \
                role_map.getPrincipalsAndRoles():
                value.append({'user_name':user_name,'local_role':local_role})
        elif name == 'faculty_code':
            try:
                value = context.__parent__.__parent__.__parent__.code
            except AttributeError:
                value = None
        elif name == 'department_code':
            try:
                value = context.__parent__.__parent__.code
            except AttributeError:
                value = None
        return super(CourseExporter, self).mangle_value(
            value, name, context)

    def export_all(self, site, filepath=None):
        """Export courses into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        faculties = site.get('faculties', {})
        for faculty in faculties.values():
            for department in faculty.values():
                for course in department.courses.values():
                    self.write_item(course, writer)
        return self.close_outfile(filepath, outfile)


class CertificateExporter(CourseExporter, grok.GlobalUtility):
    """The Certificate Exporter exports all certificates in the database.
    It iterates over all departments and faculties.
    """
    grok.implements(ICSVExporter)
    grok.name('certificates')

    fields = ('code', 'faculty_code', 'department_code', 'title', 'study_mode',
              'degree','key',
              'start_level', 'end_level', 'application_category', 'ratio',
              'school_fee_1', 'school_fee_2', 'school_fee_3', 'school_fee_4',
              'custom_textline_1', 'custom_textline_2',
              'custom_float_1', 'custom_float_2',
              'users_with_local_roles')

    title = _(u'Certificates')

    def mangle_value(self, value, name, context=None):
        """The mangler additionally computes the department_code value
        which is the code of the department that offers the certificate.
        """
        if name == 'key':
            value = context.__name__
        return super(CertificateExporter, self).mangle_value(
            value, name, context)

    def export_all(self, site, filepath=None):
        """Export certificates into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        faculties = site.get('faculties', {})
        for faculty in faculties.values():
            for department in faculty.values():
                for cert in department.certificates.values():
                    self.write_item(cert, writer)
        return self.close_outfile(filepath, outfile)


class CertificateCourseExporter(CourseExporter, grok.GlobalUtility):
    """The Certificate Course Exporter exports all certificate courses
    (:class:`CertificateCourse
    <waeup.kofa.university.certificate.CertificateCourse>` instances) in
    the database. It iterates over all departments and faculties.
    """
    grok.implements(ICSVExporter)
    grok.name('certificate_courses')

    fields = ('course', 'faculty_code', 'department_code', 'certificate_code',
              'level', 'mandatory', 'course_category')

    title = _(u'Courses in Certificates')

    def mangle_value(self, value, name, context=None):
        """The mangler computes the codes of the faculty, the department and
        the certificate which require the course. It also exports the
        course code.

        .. note:: The course must not necessarily be offered by the same
                  department.
        """
        if name == 'faculty_code':
            try:
                value = context.__parent__.__parent__.__parent__.__parent__.code
            except AttributeError:
                value = None
        elif name == 'department_code':
            try:
                value = context.__parent__.__parent__.__parent__.code
            except AttributeError:
                value = None
        elif name == 'certificate_code':
            value = getattr(context, '__parent__', None)
            value = getattr(value, 'code', None)
        if name == 'course':
            value = getattr(value, 'code', None)
        return super(CourseExporter, self).mangle_value(
            value, name, context)

    def export_all(self, site, filepath=None):
        """Export certificate courses into filepath as CSV data.
        If `filepath` is ``None``, a raw string with CSV data is returned.
        """
        writer, outfile = self.get_csv_writer(filepath)
        faculties = site.get('faculties', {})
        for faculty in faculties.values():
            for department in faculty.values():
                for cert in department.certificates.values():
                    for certref in cert.values():
                        self.write_item(certref, writer)
        return self.close_outfile(filepath, outfile)
