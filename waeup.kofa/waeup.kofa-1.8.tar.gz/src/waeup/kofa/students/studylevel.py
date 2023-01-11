## $Id: studylevel.py 16662 2021-10-05 10:30:09Z henrik $
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
Container which holds the data of a student study level
and contains the course tickets.
"""
import grok
import pytz
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.catalog.interfaces import ICatalog
from zope.component import createObject, queryUtility, getUtility
from zope.interface import implementedBy
from zope.event import notify
from waeup.kofa.interfaces import academic_sessions_vocab, VALIDATED, IKofaUtils
from waeup.kofa.students.interfaces import (
    IStudentStudyLevel, IStudentNavigation, ICourseTicket)
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.students.vocabularies import StudyLevelSource
from waeup.kofa.interfaces import MessageFactory as _

@grok.subscribe(IStudentStudyLevel, grok.IObjectModifiedEvent)
def handle_update_coursetickets(studylevel, event):
    """If level_session has changed, coursetickets_catalog
    must be informed.
    """
    # Catalog must be informed
    for ticket in studylevel.values():
        notify(grok.ObjectModifiedEvent(ticket))
    return

def find_carry_over(ticket):
    studylevel = ticket.__parent__
    studycourse = ticket.__parent__.__parent__
    levels = sorted(studycourse.keys())
    index = levels.index(str(studylevel.level))
    try:
        next_level = levels[index+1]
    except IndexError:
        return None
    next_studylevel = studycourse[next_level]
    co_ticket = next_studylevel.get(ticket.code, None)
    return co_ticket

class StudentStudyLevel(grok.Container):
    """This is a container for course tickets.
    """
    grok.implements(IStudentStudyLevel, IStudentNavigation)
    grok.provides(IStudentStudyLevel)

    def __init__(self):
        super(StudentStudyLevel, self).__init__()
        return

    @property
    def student(self):
        try:
            return self.__parent__.__parent__
        except AttributeError:
            return None

    @property
    def certcode(self):
        try:
            return self.__parent__.certificate.code
        except AttributeError:
            return None

    @property
    def number_of_tickets(self):
        return len(self)

    @property
    def total_credits(self):
        total = 0
        for ticket in self.values():
            if not ticket.outstanding:
                total += ticket.credits
        return total

    @property
    def getSessionString(self):
        try:
            session_string = academic_sessions_vocab.getTerm(
                self.level_session).title
        except LookupError:
            return None
        return session_string

    @property
    def gpa_params_rectified(self):
        """Calculate corrected level (sessional) gpa parameters.
        The corrected gpa is displayed on transcripts only.
        """
        credits_weighted = 0.0
        credits_counted = 0
        level_gpa = 0.0
        for ticket in self.values():
            if ticket.carry_over is False and ticket.total_score:
                if ticket.total_score < ticket.passmark:
                    co_ticket = find_carry_over(ticket)
                    if co_ticket is not None and co_ticket.weight is not None:
                        credits_counted += co_ticket.credits
                        credits_weighted += co_ticket.credits * co_ticket.weight
                    continue
                credits_counted += ticket.credits
                credits_weighted += ticket.credits * ticket.weight
        if credits_counted:
            level_gpa = credits_weighted/credits_counted
        return level_gpa, credits_counted, credits_weighted

    @property
    def gpa_params(self):
        """Calculate gpa parameters for this level.
        """
        credits_weighted = 0.0
        credits_counted = 0
        level_gpa = 0.0
        for ticket in self.values():
            if ticket.total_score is not None:
                credits_counted += ticket.credits
                credits_weighted += ticket.credits * ticket.weight
        if credits_counted:
            level_gpa = credits_weighted / credits_counted
        # Override level_gpa if value has been imported
        # (not implemented in base package)
        imported_gpa = getattr(self, 'imported_gpa', None)
        if imported_gpa:
            level_gpa = imported_gpa
        return level_gpa, credits_counted, credits_weighted

    @property
    def gpa(self):
        """Return string formatted gpa value.
        """
        format_float = getUtility(IKofaUtils).format_float
        return format_float(self.gpa_params[0], 2)

    @property
    def passed_params(self):
        """Determine the number and credits of passed and failed courses.
        Count the number of courses registered but not taken.
        This method is used for level reports and the
        OutstandingCoursesExporter.
        """
        passed = failed = 0
        courses_failed = ''
        credits_failed = 0
        credits_passed = 0
        courses_not_taken = ''
        courses_passed = ''
        for ticket in self.values():
            if ticket.total_score is not None:
                if ticket.total_score < ticket.passmark:
                    failed += 1
                    credits_failed += ticket.credits
                    if ticket.mandatory:
                        courses_failed += 'm_%s_m ' % ticket.code
                    else:
                        courses_failed += '%s ' % ticket.code
                else:
                    passed += 1
                    credits_passed += ticket.credits
                    courses_passed += '%s ' % ticket.code
            else:
                courses_not_taken += '%s ' % ticket.code
        return (passed, failed, credits_passed,
                credits_failed, courses_failed,
                courses_not_taken, courses_passed)

    @property
    def cumulative_params(self):
        """Calculate the cumulative gpa and other cumulative parameters
        for this level.
        All levels below this level are taken under consideration
        (including repeating levels).
        This method is used for level reports and meanwhile also 
        for session results presentations.
        """
        credits_passed = 0
        total_credits = 0
        total_credits_counted = 0
        total_credits_weighted = 0
        cgpa = 0.0
        if self.__parent__:
            for level in self.__parent__.values():
                if level.level > self.level:
                    continue
                credits_passed += level.passed_params[2]
                total_credits += level.total_credits
                gpa_params = level.gpa_params
                total_credits_counted += gpa_params[1]
                total_credits_weighted += gpa_params[2]
            if total_credits_counted:
                cgpa = total_credits_weighted/total_credits_counted
            # Override cgpa if value has been imported
            # (not implemented in base package)
            imported_cgpa = getattr(self, 'imported_cgpa', None)
            if imported_cgpa:
                cgpa = imported_cgpa
        return (cgpa, total_credits_counted, total_credits_weighted,
               total_credits, credits_passed)

    @property
    def is_current_level(self):
        try:
            return self.__parent__.current_level == self.level
        except AttributeError:
            return False

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.__parent__.__parent__.logger.info(
            '%s - %s - level %s - %s' % (
                ob_class,
                self.__parent__.__parent__.__name__,
                self.__name__,
                message))
        return

    @property
    def level_title(self):
        studylevelsource = StudyLevelSource()
        return studylevelsource.factory.getTitle(self.__parent__, self.level)

    @property
    def course_registration_forbidden(self):
        try:
            deadline = grok.getSite()['configuration'][
                str(self.level_session)].coursereg_deadline
        except (TypeError, KeyError):
            return 
        if not deadline or deadline > datetime.now(pytz.utc):
            return 
        if len(self.student['payments']):
            for ticket in self.student['payments'].values():
                if ticket.p_category == 'late_registration' and \
                    ticket.p_session == self.level_session and \
                    ticket.p_state == 'paid':
                        return
        return _("Course registration has ended. "
                 "Please pay the late registration fee.")

    def addCourseTicket(self, ticket, course):
        """Add a course ticket object.
        """
        if not ICourseTicket.providedBy(ticket):
            raise TypeError(
                'StudentStudyLevels contain only ICourseTicket instances')
        ticket.code = course.code
        ticket.title = course.title
        ticket.fcode = course.__parent__.__parent__.__parent__.code
        ticket.dcode = course.__parent__.__parent__.code
        ticket.credits = course.credits
        ticket.passmark = course.passmark
        ticket.semester = course.semester
        self[ticket.code] = ticket
        return

    def addCertCourseTickets(self, cert):
        """Collect all certificate courses and create course
        tickets automatically.
        """
        if cert is not None:
            for key, val in cert.items():
                if val.level != self.level:
                    continue
                ticket = createObject(u'waeup.CourseTicket')
                ticket.automatic = True
                ticket.mandatory = val.mandatory
                ticket.carry_over = False
                ticket.course_category = val.course_category
                self.addCourseTicket(ticket, val.course)
        return

    def updateCourseTicket(self, ticket, course):
        """Updates a course ticket object and return code
        if ticket has been invalidated.
        """
        if not course:
            if ticket.title.endswith('cancelled)'):
                # Skip this tiket
                return
            # Invalidate course ticket
            ticket.title += u' (course cancelled)'
            ticket.credits = 0
            ticket.passmark = 0
            return ticket.code
        ticket.code = course.code
        ticket.title = course.title
        ticket.fcode = course.__parent__.__parent__.__parent__.code
        ticket.dcode = course.__parent__.__parent__.code
        ticket.credits = course.credits
        ticket.passmark = course.passmark
        ticket.semester = course.semester
        return

StudentStudyLevel = attrs_to_fields(
    StudentStudyLevel, omit=['total_credits', 'gpa'])

class StudentStudyLevelFactory(grok.GlobalUtility):
    """A factory for student study levels.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.StudentStudyLevel')
    title = u"Create a new student study level.",
    description = u"This factory instantiates new student study level instances."

    def __call__(self, *args, **kw):
        return StudentStudyLevel()

    def getInterfaces(self):
        return implementedBy(StudentStudyLevel)

class CourseTicket(grok.Model):
    """This is a course ticket which allows the
    student to attend the course. Lecturers will enter scores and more at
    the end of the term.

    A course ticket contains a copy of the original course and
    certificate course data. If the courses and/or the referring certificate
    courses are removed, the corresponding tickets remain unchanged.
    So we do not need any event triggered actions on course tickets.
    """
    grok.implements(ICourseTicket, IStudentNavigation)
    grok.provides(ICourseTicket)

    def __init__(self):
        super(CourseTicket, self).__init__()
        self.code = None
        return

    @property
    def student(self):
        """Get the associated student object.
        """
        try:
            return self.__parent__.__parent__.__parent__
        except AttributeError: # in unit tests
            return None

    @property
    def certcode(self):
        try:
            return self.__parent__.__parent__.certificate.code
        except AttributeError: # in unit tests
            return None

    @property
    def removable_by_student(self):
        """True if student is allowed to remove the ticket.
        """
        return not self.mandatory

    @property
    def editable_by_lecturer(self):
        """True if lecturer is allowed to edit the ticket.
        """
        try:
            cas = grok.getSite()[
                'configuration'].current_academic_session
            if self.student.state == VALIDATED and \
                self.student.current_session == cas:
                return True
        except (AttributeError, TypeError): # in unit tests
            pass
        return False

    def writeLogMessage(self, view, message):
        return self.__parent__.__parent__.__parent__.writeLogMessage(
            view, message)

    @property
    def level(self):
        """Returns the id of the level the ticket has been added to.
        """
        try:
            return self.__parent__.level
        except AttributeError: # in unit tests
            return None

    @property
    def level_session(self):
        """Returns the session of the level the ticket has been added to.
        """
        try:
            return self.__parent__.level_session
        except AttributeError: # in unit tests
            return None

    @property
    def total_score(self):
        """Returns the total score of this ticket. In the base package
        this is simply the score. In customized packages this could be
        something else.
        """
        return self.score

    @property
    def _getGradeWeightFromScore(self):
        """Nigerian Course Grading System
        """
        if self.total_score is None:
            return (None, None)
        if self.total_score >= 70:
            return ('A',5)
        if self.total_score >= 60:
            return ('B',4)
        if self.total_score >= 50:
            return ('C',3)
        if self.total_score >= 45:
            return ('D',2)
        if self.total_score >= self.passmark: # passmark changed in 2013 from 40 to 45
            return ('E',1)
        return ('F',0)

    @property
    def grade(self):
        """Returns the grade calculated from total score.
        """
        return self._getGradeWeightFromScore[0]

    @property
    def weight(self):
        """Returns the weight calculated from total score.
        """
        return self._getGradeWeightFromScore[1]

CourseTicket = attrs_to_fields(CourseTicket)

class CourseTicketFactory(grok.GlobalUtility):
    """A factory for student study levels.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.CourseTicket')
    title = u"Create a new course ticket.",
    description = u"This factory instantiates new course ticket instances."

    def __call__(self, *args, **kw):
        return CourseTicket()

    def getInterfaces(self):
        return implementedBy(CourseTicket)
