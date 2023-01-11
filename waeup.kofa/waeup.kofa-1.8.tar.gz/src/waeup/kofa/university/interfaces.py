## $Id: interfaces.py 16703 2021-11-08 08:32:52Z henrik $
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
"""Interfaces of academics specific objects.
"""

from zope import schema
from zope.interface import Attribute, invariant, Invalid
from waeup.kofa.interfaces import (
    IKofaObject, IKofaContainer, validate_id, academic_sessions_vocab)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.university.vocabularies import (
    course_levels,
    CourseSource,
    StudyModeSource,
    AppCatSource,
    InstTypeSource,
    SemesterSource,
    DegreeSource,
    CourseCategorySource
    )

class IFaculty(IKofaContainer):
    """Representation of a university faculty.
    """
    code = schema.TextLine(
        title = _(u'Code'),
        default = u'NA',
        required = True,
        constraint=validate_id,
        )

    title = schema.TextLine(
        title = _(u'Name of faculty'),
        default = u'Unnamed',
        required = True,
        )

    title_prefix = schema.Choice(
        title = _(u'Name prefix'),
        default = u'faculty',
        source = InstTypeSource(),
        required = True,
        )

    officer_1 = schema.TextLine(
        title = _(u'Faculty Officer 1'),
        default = u'',
        required = False,
        )

    officer_2 = schema.TextLine(
        title = _(u'Faculty Officer 2'),
        default = u'',
        required = False,
        )


class IFacultiesContainer(IKofaContainer):
    """A container for faculties.
    """
    def addFaculty(faculty):
        """Add an IFactulty object.
        """


class IDepartment(IKofaObject):
    """Representation of a department.
    """
    code = schema.TextLine(
        title = _(u'Code'),
        default = u'NA',
        required = True,
        constraint=validate_id,
        )

    title = schema.TextLine(
        title = _(u'Name of department'),
        default = u'Unnamed',
        required = True,
        )

    title_prefix = schema.Choice(
        title = _(u'Name prefix'),
        source = InstTypeSource(),
        default = u'department',
        required = True,
        )

    score_editing_disabled = schema.Bool(
        title = _(u'Score editing disabled'),
        description = _(
            u'Lectures can not edit scores if ticked.'),
        required = False,
        default = False,
        )

    officer_1 = schema.TextLine(
        title = _(u'Department Officer 1'),
        default = u'',
        required = False,
        )

    officer_2 = schema.TextLine(
        title = _(u'Department Officer 2'),
        default = u'',
        required = False,
        )

    officer_3 = schema.TextLine(
        title = _(u'Department Officer 3'),
        default = u'',
        required = False,
        )

    officer_4 = schema.TextLine(
        title = _(u'Department Officer 4'),
        default = u'',
        required = False,
        )

    courses = Attribute("A container for courses.")
    certificates = Attribute("A container for certificates.")


class IFlashNotice(IKofaObject):
    """An interface for the flash notice edit form page.
    """

    flash_notice = schema.TextLine(
        title = _(u'Flash Notice'),
        description = _(
            u'If you save an empty field, all flash notices will be removed.'),
        required = False,
        readonly = False,
        )


class ICoursesContainer(IKofaContainer):
    """A container for faculties.
    """
    def addCourse(course):
        """Add an ICourse object.

        Returns the key, under which the object was stored.
        """


class ICourse(IKofaObject):
    """Representation of a course.
    """
    code = schema.TextLine(
        title = _(u'Code'),
        default = u'NA',
        required = True,
        constraint=validate_id,
        )

    title = schema.TextLine(
        title = _(u'Title of course'),
        default = u'Unnamed',
        required = True,
        )

    credits = schema.Int(
        title = _(u'Credits'),
        default = 0,
        required = True,
        )

    passmark = schema.Int(
        title = _(u'Passmark'),
        default = 40,
        required = True,
        )

    semester = schema.Choice(
        title = _(u'Semester/Term'),
        default = 9,
        source = SemesterSource(),
        required = True,
        )

    former_course = schema.Bool(
        title = _(u'Former course'),
        description = _(
            u'If this attribute is being set all certificate courses '
            'referring to this course will be automatically deleted.'),
        required = False,
        default = False,
        )

    results_validated_by = schema.TextLine(
        title = _(u'Results validated by'),
        default = None,
        required = False,
        )

    results_validation_date = schema.Datetime(
        title = _(u'Results validation date'),
        required = False,
        readonly = False,
        )

    results_validation_session = schema.Choice(
        title = _(u'Results validation session'),
        source = academic_sessions_vocab,
        required = False,
        readonly = False,
        )

    score_editing_disabled = schema.Bool(
        title = _(u'Score editing disabled'),
        description = _(
            u'Lectures can not edit scores if ticked.'),
        required = False,
        default = False,
        )


class ICertificate(IKofaObject):
    """Representation of a certificate.
    """
    code = schema.TextLine(
        title = _(u'Code'),
        default = u'NA',
        required = True,
        constraint=validate_id,
        )

    title = schema.TextLine(
        title = _(u'Title'),
        default = u'Unnamed',
        required = True,
        )

    study_mode = schema.Choice(
        title = _(u'Study Mode'),
        source = StudyModeSource(),
        default = u'ug_ft',
        required = True,
        )

    degree = schema.Choice(
        title = _(u'Degree'),
        source = DegreeSource(),
        required = False,
        )

    start_level = schema.Choice(
        title = _(u'Start Level'),
        vocabulary = course_levels,
        default = 100,
        required = True,
        )

    end_level = schema.Choice(
        title = _(u'End Level'),
        vocabulary = course_levels,
        default = 500,
        required = True,
        )

    application_category = schema.Choice(
        title = _(u'Application Category'),
        source = AppCatSource(),
        default = u'basic',
        required = True,
        )

    school_fee_1 = schema.Float(
        title = _(u'Initial School Fee'),
        required = False,
        default = 0.0,
        )

    school_fee_2 = schema.Float(
        title = _(u'Returning School Fee'),
        required = False,
        default = 0.0,
        )

    school_fee_3 = schema.Float(
        title = _(u'Foreigner Initial School Fee'),
        required = False,
        default = 0.0,
        )

    school_fee_4 = schema.Float(
        title = _(u'Foreigner Returning School Fee'),
        required = False,
        default = 0.0,
        )

    #ratio = schema.Float(
    #    title = _(u'Installment Ratio'),
    #    required = False,
    #    min = 0.0,
    #    max = 1.0,
    #    )

    custom_textline_1 = schema.TextLine(
        title = _(u'Custom Textline 1 (not used)'),
        required = False,
        )

    custom_textline_2 = schema.TextLine(
        title = _(u'Custom Textline 2 (not used)'),
        required = False,
        )

    custom_float_1 = schema.Float(
        title = _(u'Custom Float 1 (not used)'),
        required = False,
        )

    custom_float_2 = schema.Float(
        title = _(u'Custom Float 2 (not used)'),
        required = False,
        )

    @invariant
    def check_pg_conditions(cert):
        if cert.start_level == 999 and not cert.end_level == 999:
            raise Invalid(_("Start level and end level must correspond."))
        if cert.end_level == 999 and not cert.start_level == 999:
            raise Invalid(_("Start level and end level must correspond."))
        if cert.study_mode.startswith('pg') and not cert.start_level == 999:
            raise Invalid(_(
                "Study mode, start level and end level must correspond."))
        if cert.start_level == 999  and not cert.study_mode.startswith('pg'):
            raise Invalid(_(
                "Study mode, start level and end level must correspond."))


class ICertificatesContainer(IKofaContainer):
    """A container for certificates.
    """
    def addCertificate(certificate):
        """Add an ICertificate object.

        Returns the key, under which the object was stored.
        """


class ICertificateCourse(IKofaObject):
    """A certificatecourse is referring a course and provides some own
       attributes.
    """
    course = schema.Choice(
        title = _(u'Course'),
        source = CourseSource(),
        )

    level = schema.Choice(
        title = _(u'Level'),
        required = True,
        vocabulary = course_levels,
        readonly = False,
        )

    course_category = schema.Choice(
        title = _(u'Course Category'),
        source = CourseCategorySource(),
        required = False,
        )

    mandatory = schema.Bool(
        title = _(u'Registration required'),
        required = False,
        default = True,
        )

    def getCourseCode():
        """Return the code of the course referred to.

        This is needed for cataloging.
        """