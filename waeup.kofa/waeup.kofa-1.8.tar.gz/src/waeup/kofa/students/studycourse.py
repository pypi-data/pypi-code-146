## $Id: studycourse.py 16901 2022-03-23 07:05:20Z henrik $
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
"""
Container which holds the data of the student study courses
and contains the (student) study level objects.
"""
import grok
from zope.component.interfaces import IFactory
from zope.component import createObject
from zope.interface import implementedBy
from waeup.kofa.students.interfaces import (
    IStudentStudyCourse, IStudentNavigation, IStudentStudyLevel)
from waeup.kofa.students.studylevel import CourseTicket
from waeup.kofa.students.workflow import CLEARED, RETURNING, PAID
from waeup.kofa.utils.helpers import attrs_to_fields

class StudentStudyCourse(grok.Container):
    """This is a container for study levels.
    """
    grok.implements(IStudentStudyCourse, IStudentNavigation)
    grok.provides(IStudentStudyCourse)

    is_special_postgrad = False

    def __init__(self):
        super(StudentStudyCourse, self).__init__()
        return

    @property
    def student(self):
        return self.__parent__

    def writeLogMessage(self, view, message):
        return self.__parent__.writeLogMessage(view, message)

    @property
    def next_session_allowed(self):
        certificate = getattr(self, 'certificate', None)
        if certificate == None:
            return False
        if self.student.state in (CLEARED, RETURNING):
            return True
        if self.student.state == PAID \
            and self.student.is_postgrad:
            return True
        return False

    @property
    def is_postgrad(self):
        if self.certificate is None:
            return False
        return self.certificate.study_mode.startswith('pg')

    @property
    def is_current(self):
        if self.__name__ and '_' in self.__name__:
            return False
        return True

    @property
    def is_previous(self):
        if self.__name__ == 'studycourse_2':
            return True
        if self.__name__ == 'studycourse_1' and  \
            not self.__parent__.has_key('studycourse_2'):
            return True
        return False

    def addStudentStudyLevel(self, cert, studylevel, course_category=None):
        """Add a study level object.
        """
        if not IStudentStudyLevel.providedBy(studylevel):
            raise TypeError(
                'StudentStudyCourses contain only IStudentStudyLevel instances')
        self[str(studylevel.level)] = studylevel
        studylevel.addCertCourseTickets(cert)
        # Collect carry-over courses in base levels (not in repeating levels)
        try:
            co_enabled = grok.getSite()['configuration'].carry_over
        except TypeError:
            # In tests we might not have a site object
            co_enabled = True
        if not co_enabled or studylevel.level % 100 != 0:
            return
        levels = sorted(self.keys())
        index = levels.index(str(studylevel.level))
        if index <= 0:
            return
        previous_level = self[levels[index-1]]
        for key, val in previous_level.items():
            if val.total_score >= val.passmark:
                continue
            if course_category and val.course_category != course_category:
                continue
            if key in self[str(studylevel.level)]:
                # Carry-over ticket exists
                continue
            co_ticket = createObject(u'waeup.CourseTicket')
            for name in ['code', 'title', 'credits', 'passmark',
                         'semester', 'mandatory', 'fcode', 'dcode',
                         'course_category']:
                setattr(co_ticket, name, getattr(val, name))
            co_ticket.automatic = True
            co_ticket.carry_over = True
            self[str(studylevel.level)][co_ticket.code] = co_ticket
        return

    def getTranscriptData(self):
        """Get a sorted list of dicts with level and course ticket data.

        This method is used for transcripts.
        """
        levels = []
        cgpa = 0.0
        total_credits_counted = 0
        for level_key, level_val in self.items():
            # Skip Level Zero
            if level_key == '0':
                continue
            tickets_1 = []
            tickets_2 = []
            tickets_3 = []
            tickets = sorted(level_val.values(), key=lambda ticket: ticket.code)
            for ticket in tickets:
                if ticket.outstanding:
                    continue
                if ticket.total_score is None:
                    continue
                if ticket.semester == 1:
                    tickets_1.append(ticket)
                elif ticket.semester == 2:
                    tickets_2.append(ticket)
                elif ticket.semester == 3:
                    tickets_3.append(ticket)
            gpa_params = level_val.gpa_params_rectified
            sgpa = gpa_params[0]
            total_credits_counted += gpa_params[1]
            cgpa += gpa_params[2]
            levels.append(
                dict(level_key=level_key,
                     level=level_val,
                     tickets_1=tickets_1,
                     tickets_2=tickets_2,
                     tickets_3=tickets_3,
                     sgpa=sgpa))
        if total_credits_counted:
            cgpa = cgpa/total_credits_counted
        # Override cgpa if value has been imported
        # (not implemented in base package)
        imported_cgpa = getattr(self, 'imported_cgpa', None)
        if imported_cgpa:
            cgpa = imported_cgpa
        return sorted(levels, key=lambda level: level['level_key']), cgpa

StudentStudyCourse = attrs_to_fields(StudentStudyCourse)

class StudentStudyCourseFactory(grok.GlobalUtility):
    """A factory for student study courses.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.StudentStudyCourse')
    title = u"Create a new student study course.",
    description = u"This factory instantiates new student study course instances."

    def __call__(self, *args, **kw):
        return StudentStudyCourse()

    def getInterfaces(self):
        return implementedBy(StudentStudyCourse)
