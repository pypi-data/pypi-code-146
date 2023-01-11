## $Id: batching.py 16834 2022-02-24 12:48:18Z henrik $
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
"""Batch processing components for student objects.

Batch processors eat CSV files to add, update or remove large numbers
of certain kinds of objects at once.

Here we define the processors for students specific objects like
students, studycourses, payment tickets and accommodation tickets.
"""
import grok
import unicodecsv as csv # XXX: csv ops should move to dedicated module.
from time import time
from ast import literal_eval
from datetime import datetime
from zope.i18n import translate
from zope.interface import Interface
from zope.schema import getFields
from zope.component import queryUtility, getUtility, createObject
from zope.event import notify
from zope.catalog.interfaces import ICatalog
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from waeup.kofa.interfaces import (
    IBatchProcessor, FatalCSVError, IObjectConverter, IUserAccount,
    IObjectHistory, VALIDATED, REGISTERED, IGNORE_MARKER, DELETION_MARKER)
from waeup.kofa.interfaces import IKofaUtils, DuplicationError
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.students.interfaces import (
    IStudent, IStudentStudyCourse, IStudentStudyCourseTransfer,
    IStudentUpdateByRegNo, IStudentUpdateByMatricNo,
    IStudentStudyLevel, ICourseTicketImport,
    IStudentOnlinePayment, IStudentVerdictUpdate)
from waeup.kofa.payments.interfaces import IPayer
from waeup.kofa.students.workflow import  (
    IMPORTABLE_STATES, IMPORTABLE_TRANSITIONS,
    FORBIDDEN_POSTGRAD_TRANS, FORBIDDEN_POSTGRAD_STATES)
from waeup.kofa.utils.batching import BatchProcessor

def studycourseName(row):
    previous = row.get('previous', None)
    if previous == '1':
        return 'studycourse_1'
    elif previous == '2':
        return 'studycourse_2'
    return 'studycourse'

class StudentProcessor(BatchProcessor):
    """The Student Processor imports student base data.

    In create mode no locator is required. If no `student_id` is given,
    the portal automatically assigns a new student id.

    In update or remove mode the processor uses
    either the `student_id`, `reg_number` or `matric_number` to localize the 
    student object, exactly in this order. If `student_id` is given and an
    object can be found, `reg_number` and `matric_number` will be overwritten
    by the values provided in the import file. If `student_id` is missing,
    `reg_number` is used to localize the object and only `matric_number`
    will be overwritten. `matric_number` is used as locator only if both
    `student_id` and `reg_number` are missing. `student_id` can't be changed
    by the batch processor.

    There are two ways to change the workflow state of the student,
    an unsafe and a safe way. The safe way makes use of workflow transitions.
    Transitions are only possible between allowed workflow states. Only
    transitions ensure that the registration workflow is maintained.

    **Always prefer the safe way!**
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'studentprocessor'
    grok.name(util_name)

    name = _('Student Processor')
    iface = IStudent
    iface_byregnumber = IStudentUpdateByRegNo
    iface_bymatricnumber = IStudentUpdateByMatricNo

    factory_name = 'waeup.Student'

    @property
    def available_fields(self):
        fields = getFields(self.iface)
        return sorted(list(set(
            ['student_id','reg_number','matric_number',
            'password', 'state', 'transition', 'history'] + fields.keys())))

    def checkHeaders(self, headerfields, mode='create'):
        if 'state' in headerfields and 'transition' in headerfields:
            raise FatalCSVError(
                "State and transition can't be imported at the same time!")
        if not 'reg_number' in headerfields and not 'student_id' \
            in headerfields and not 'matric_number' in headerfields:
            raise FatalCSVError(
                "Need at least columns student_id or reg_number " +
                "or matric_number for import!")
        if mode == 'create':
            for field in self.required_fields:
                if not field in headerfields:
                    raise FatalCSVError(
                        "Need at least columns %s for import!" %
                        ', '.join(["'%s'" % x for x in self.required_fields]))
        # Check for fields to be ignored...
        not_ignored_fields = [x for x in headerfields
                              if not x.startswith('--')]
        if len(set(not_ignored_fields)) < len(not_ignored_fields):
            raise FatalCSVError(
                "Double headers: each column name may only appear once.")
        return True

    def parentsExist(self, row, site):
        return 'students' in site.keys()

    def getLocator(self, row):
        if row.get('student_id',None) not in (None, IGNORE_MARKER):
            return 'student_id'
        elif row.get('reg_number',None) not in (None, IGNORE_MARKER):
            return 'reg_number'
        elif row.get('matric_number',None) not in (None, IGNORE_MARKER):
            return 'matric_number'
        else:
            return None

    # The entry never exists in create mode.
    def entryExists(self, row, site):
        return self.getEntry(row, site) is not None

    def getParent(self, row, site):
        return site['students']

    def getEntry(self, row, site):
        if not 'students' in site.keys():
            return None
        if self.getLocator(row) == 'student_id':
            if row['student_id'] in site['students']:
                student = site['students'][row['student_id']]
                return student
        elif self.getLocator(row) == 'reg_number':
            reg_number = row['reg_number']
            cat = queryUtility(ICatalog, name='students_catalog')
            results = list(
                cat.searchResults(reg_number=(reg_number, reg_number)))
            if results:
                return results[0]
        elif self.getLocator(row) == 'matric_number':
            matric_number = row['matric_number']
            cat = queryUtility(ICatalog, name='students_catalog')
            results = list(
                cat.searchResults(matric_number=(matric_number, matric_number)))
            if results:
                return results[0]
        return None

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        parent.addStudent(obj)
        # Reset _curr_stud_id if student_id has been imported
        if self.getLocator(row) == 'student_id':
            parent._curr_stud_id -= 1
        # We have to log this if state is provided. If not,
        # logging is done by the event handler handle_student_added
        if 'state' in row:
            parent.logger.info('%s - Student record created' % obj.student_id)
        return

    def delEntry(self, row, site):
        student = self.getEntry(row, site)
        if student is not None:
            parent = self.getParent(row, site)
            parent.logger.info('%s - Student removed' % student.student_id)
            del parent[student.student_id]
        pass

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the object must fulfill when being updated.

        This method is not used in case of deleting or adding objects.

        Returns error messages as strings in case of requirement
        problems.
        """
        transition = row.get('transition', IGNORE_MARKER)
        if transition not in (IGNORE_MARKER, ''):
            allowed_transitions = IWorkflowInfo(obj).getManualTransitionIds()
            if transition not in allowed_transitions:
                return 'Transition not allowed.'
            if transition in FORBIDDEN_POSTGRAD_TRANS and \
                obj.is_postgrad:
                return 'Transition not allowed (pg student).'
        state = row.get('state', IGNORE_MARKER)
        if state not in (IGNORE_MARKER, ''):
            if state in FORBIDDEN_POSTGRAD_STATES and \
                obj.is_postgrad:
                return 'State not allowed (pg student).'
        return None

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = ''

        # Remove student_id from row if empty
        if 'student_id' in row and row['student_id'] in (None, IGNORE_MARKER):
            row.pop('student_id')

        # Update password
        if 'password' in row:
            passwd = row.get('password', IGNORE_MARKER)
            if passwd not in ('', IGNORE_MARKER):
                if passwd.startswith('{SSHA}'):
                    # already encrypted password
                    obj.password = passwd
                elif passwd == DELETION_MARKER:
                    obj.password = None
                else:
                    # not yet encrypted password
                    IUserAccount(obj).setPassword(passwd)
                items_changed += ('%s=%s, ' % ('password', passwd))
            row.pop('password')

        # Replace entire history
        if 'history' in row:
            new_history = row.get('history', IGNORE_MARKER)
            if new_history not in (IGNORE_MARKER, ''):
                history = IObjectHistory(obj)
                history._annotations[
                    history.history_key] = literal_eval(new_history)
                items_changed += ('%s=%s, ' % ('history', new_history))
            row.pop('history')

        # Update registration state
        if 'state' in row:
            state = row.get('state', IGNORE_MARKER)
            if state not in (IGNORE_MARKER, ''):
                value = row['state']
                IWorkflowState(obj).setState(value)
                msg = _("State '${a}' imported", mapping = {'a':value})
                history = IObjectHistory(obj)
                history.addMessage(msg)
                items_changed += ('%s=%s, ' % ('state', state))
            row.pop('state')

        if 'transition' in row:
            transition = row.get('transition', IGNORE_MARKER)
            if transition not in (IGNORE_MARKER, ''):
                value = row['transition']
                IWorkflowInfo(obj).fireTransition(value)
                items_changed += ('%s=%s, ' % ('transition', transition))
            row.pop('transition')

        # apply other values...
        items_changed += super(StudentProcessor, self).updateEntry(
            obj, row, site, filename)

        # Log actions...
        parent = self.getParent(row, site)
        if hasattr(obj,'student_id'):
            # Update mode: the student exists and we can get the student_id.
            # Create mode: the record contains the student_id
            parent.logger.info(
                '%s - %s - %s - updated: %s'
                % (self.name, filename, obj.student_id, items_changed))
        else:
            # Create mode: the student does not yet exist
            # XXX: It seems that this never happens because student_id
            # is always set.
            parent.logger.info(
                '%s - %s - %s - imported: %s' 
                % (self.name, filename, obj.student_id, items_changed))
        notify(grok.ObjectModifiedEvent(obj))
        return items_changed

    def getMapping(self, path, headerfields, mode):
        """Get a mapping from CSV file headerfields to actually used fieldnames.
        """
        result = dict()
        reader = csv.reader(open(path, 'rb'))
        raw_header = reader.next()
        for num, field in enumerate(headerfields):
            if field not in ['student_id', 'reg_number', 'matric_number'
                             ] and mode == 'remove':
                continue
            if field == u'--IGNORE--':
                # Skip ignored columns in failed and finished data files.
                continue
            result[raw_header[num]] = field
        return result

    def checkConversion(self, row, mode='create'):
        """Validates all values in row.
        """
        iface = self.iface
        if mode in ['update', 'remove']:
            if self.getLocator(row) == 'reg_number':
                iface = self.iface_byregnumber
            elif self.getLocator(row) == 'matric_number':
                iface = self.iface_bymatricnumber
        converter = IObjectConverter(iface)
        errs, inv_errs, conv_dict =  converter.fromStringDict(
            row, self.factory_name, mode=mode)
        # We cannot import both state and transition.
        if 'transition' in row and 'state' in row:
            if row['transition'] not in (IGNORE_MARKER, '') and \
                row['state'] not in (IGNORE_MARKER, ''):
                errs.append(('workflow','not allowed'))
        if 'transition' in row:
            if row['transition'] not in IMPORTABLE_TRANSITIONS:
                if row['transition'] not in (IGNORE_MARKER, ''):
                    errs.append(('transition','not allowed'))
        if 'state' in row:
            if row['state'] not in IMPORTABLE_STATES:
                if row['state'] not in (IGNORE_MARKER, ''):
                    errs.append(('state','not allowed'))
                else:
                    # State is an attribute of Student and must not
                    # be changed if empty.
                    conv_dict['state'] = IGNORE_MARKER
        if 'history' in row:
            if row['history'] not in (IGNORE_MARKER, ''):
                try:
                    new_history = literal_eval(row['history'])
                except:
                    errs.append(('history','malformed string'))
        try:
            # Correct stud_id counter. As the IConverter for students
            # creates student objects that are not used afterwards, we
            # have to fix the site-wide student_id counter.
            site = grok.getSite()
            students = site['students']
            students._curr_stud_id -= 1
        except (KeyError, TypeError, AttributeError):
                pass
        return errs, inv_errs, conv_dict


class StudentProcessorBase(BatchProcessor):
    """A base for student subitem processor.

    Helps reducing redundancy.
    """
    grok.baseclass()

    # additional available fields
    # beside 'student_id', 'reg_number' and 'matric_number'
    additional_fields = []

    # additional required fields (subset of additional_fields)
    additional_fields_required = []

    @property
    def available_fields(self):
        fields = ['student_id','reg_number','matric_number'
                  ] + self.additional_fields
        return sorted(list(set(fields + getFields(
                self.iface).keys())))

    def checkHeaders(self, headerfields, mode='ignore'):
        if not 'reg_number' in headerfields and not 'student_id' \
            in headerfields and not 'matric_number' in headerfields:
            raise FatalCSVError(
                "Need at least columns student_id " +
                "or reg_number or matric_number for import!")
        for name in self.additional_fields_required:
            if not name in headerfields:
                raise FatalCSVError(
                    "Need %s for import!" % name)

        # Check for fields to be ignored...
        not_ignored_fields = [x for x in headerfields
                              if not x.startswith('--')]
        if len(set(not_ignored_fields)) < len(not_ignored_fields):
            raise FatalCSVError(
                "Double headers: each column name may only appear once.")
        return True

    def _getStudent(self, row, site):
        NON_VALUES = ['', IGNORE_MARKER]
        if not 'students' in site.keys():
            return None
        if row.get('student_id', '') not in NON_VALUES:
            if row['student_id'] in site['students']:
                student = site['students'][row['student_id']]
                return student
        elif row.get('reg_number', '') not in NON_VALUES:
            reg_number = row['reg_number']
            cat = queryUtility(ICatalog, name='students_catalog')
            results = list(
                cat.searchResults(reg_number=(reg_number, reg_number)))
            if results:
                return results[0]
        elif row.get('matric_number', '') not in NON_VALUES:
            matric_number = row['matric_number']
            cat = queryUtility(ICatalog, name='students_catalog')
            results = list(
                cat.searchResults(matric_number=(matric_number, matric_number)))
            if results:
                return results[0]
        return None

    def parentsExist(self, row, site):
        return self.getParent(row, site) is not None

    def entryExists(self, row, site):
        return self.getEntry(row, site) is not None

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        converter = IObjectConverter(self.iface)
        errs, inv_errs, conv_dict =  converter.fromStringDict(
            row, self.factory_name, mode=mode)
        return errs, inv_errs, conv_dict

    def getMapping(self, path, headerfields, mode):
        """Get a mapping from CSV file headerfields to actually used fieldnames.
        """
        result = dict()
        reader = csv.reader(open(path, 'rb'))
        raw_header = reader.next()
        for num, field in enumerate(headerfields):
            if field not in ['student_id', 'reg_number', 'matric_number',
                             'p_id', 'code', 'level'
                             ] and mode == 'remove':
                continue
            if field == u'--IGNORE--':
                # Skip ignored columns in failed and finished data files.
                continue
            result[raw_header[num]] = field
        return result


class StudentStudyCourseProcessor(StudentProcessorBase):
    """The Student Study Course Processor imports data which refer
    to the student's course of study. The study course container data
    describe the current state of the course of study and it stores the
    entry conditions, i.e. when the student started the course.

    Most important is the `certificate` attribute which tells us which course 
    the student is studying. The terms 'study course' and 'course of study'
    are used synonymously. The 'certificate' is the study programme described
    in the acadmic section. The study course object stores a referrer to a
    certificate in the acadmic section.

    When importing a new certificate code, `checkConversion` does not only
    check whether a certificate with the same code exists, it also
    proves if `current_level` is inside the level range of the certificate.
    For example, some study programmes start at level 200. The imported
    current level must thus be 200 or higher.

    `checkUpdateRequirements` looks up if the imported values match the
    certificate already stored with the study course object. The imported
    `current_level` must be in the range of the certificate already
    stored.

    .. note::

      The processor does only offer an update mode. An 'empty' study course 
      object is automatically created when the student object is added. So this
      object always exists. It can neither be added a second time nor
      be removed.

    Students can be transferred by import. A transfer is initialized if the
    `entry_mode` value is ``transfer``. In this case `checkConversion` uses a
    different interface for data validation and `checkUpdateRequirements`
    ensures that a student can only be transferred twice. The student transfer
    process is described elsewhere.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'studycourseprocessor'
    grok.name(util_name)

    name = _('StudentStudyCourse Processor')
    iface = IStudentStudyCourse
    iface_transfer = IStudentStudyCourseTransfer
    factory_name = 'waeup.StudentStudyCourse'

    @property
    def available_fields(self):
        return super(
            StudentStudyCourseProcessor, self).available_fields + ['previous',]

    def getParent(self, row, site):
        return self._getStudent(row, site)

    def getEntry(self, row, site):
        student = self.getParent(row, site)
        if student is None:
            return None
        return student.get(studycourseName(row))

    def addEntry(self, obj, row, site):
        if studycourseName(row) == 'studycourse':
            raise NotImplementedError('method not availabe')
        parent = self.getParent(row, site)
        parent[studycourseName(row)] = obj
        return

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        entry_mode = row.get('entry_mode', None)
        certificate = row.get('certificate', None)
        current_session = row.get('current_session', None)
        student = self.getParent(row, site)
        if entry_mode == 'transfer':
            # We do not expect any error here since we
            # checked all constraints in checkConversion and
            # in checkUpdateRequirements
            student.transfer(
                certificate=certificate, current_session=current_session)
            obj = student[studycourseName(row)]
            # Once imported we must ensure that after export and reimport
            # the student is not transferred again.
            row['entry_mode'] = 'transferred'
        items_changed = super(StudentStudyCourseProcessor, self).updateEntry(
            obj, row, site, filename)
        student.__parent__.logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, student.student_id, items_changed))
        # Update the students_catalog
        notify(grok.ObjectModifiedEvent(student))
        return

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        # We have to use the correct interface. Transfer
        # updates have different constraints.
        entry_mode = row.get('entry_mode', None)
        if entry_mode == 'transfer':
            converter = IObjectConverter(self.iface_transfer)
        else:
            converter = IObjectConverter(self.iface)
        errs, inv_errs, conv_dict =  converter.fromStringDict(
            row, self.factory_name, mode=mode)

        # We have to check if current_level is in range of certificate.
        if 'certificate' in conv_dict and 'current_level' in conv_dict:
            cert = conv_dict['certificate']
            level = conv_dict['current_level']
            if level < cert.start_level or level > cert.end_level+120:
                errs.append(('current_level','not in range'))
        return errs, inv_errs, conv_dict

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the object must fulfill when being updated.
        Returns error messages as strings in case of requirement
        problems.
        """
        if obj.student.studycourse_locked:
            return 'Studycourse is locked.'
        certificate = getattr(obj, 'certificate', None)
        entry_session = getattr(obj, 'entry_session', None)
        current_level = row.get('current_level', None)
        entry_mode = row.get('entry_mode', None)
        # We have to ensure that the student can be transferred.
        if entry_mode == 'transfer':
            if certificate is None or entry_session is None:
                return 'Former study course record incomplete.'
            if 'studycourse_1' in obj.__parent__.keys() and \
                'studycourse_2' in obj.__parent__.keys():
                return 'Maximum number of transfers exceeded.'
        if current_level:
            if current_level == 999 and \
                obj.__parent__.state in FORBIDDEN_POSTGRAD_STATES:
                return 'Not a pg student.'
            cert = row.get('certificate', None)
            if certificate is None and cert is None:
                return 'No certificate to check level.'
            if certificate is not None and cert is None and (
                current_level < certificate.start_level or \
                current_level > certificate.end_level+120):
                return 'current_level not in range.'
        return None

class StudentStudyLevelProcessor(StudentProcessorBase):
    """The Student Study Level Processor imports study level data.
    It overwrites the container attributes but not the content of the container,
    i.e. the course tickets stored inside the container. There is nothing
    special about this processor.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'studylevelprocessor'
    grok.name(util_name)

    name = _('StudentStudyLevel Processor')
    iface = IStudentStudyLevel
    factory_name = 'waeup.StudentStudyLevel'

    additional_fields_required = ['level']

    @property
    def available_fields(self):
        fields = super(
            StudentStudyLevelProcessor, self).available_fields + ['previous',]
        fields.remove('total_credits')
        fields.remove('gpa')
        return  fields

    def getParent(self, row, site):
        student = self._getStudent(row, site)
        if student is None:
            return None
        return student[studycourseName(row)]

    def getEntry(self, row, site):
        studycourse = self.getParent(row, site)
        if studycourse is None:
            return None
        try:
            entry = studycourse.get(str(row['level']))
        except KeyError:
            return None
        return entry

    def delEntry(self, row, site):
        studylevel = self.getEntry(row, site)
        parent = self.getParent(row, site)
        if studylevel is not None:
            student = self._getStudent(row, site)
            student.__parent__.logger.info('%s - Level removed: %s'
                % (student.student_id, studylevel.__name__))
            del parent[studylevel.__name__]
        return

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = super(StudentStudyLevelProcessor, self).updateEntry(
            obj, row, site, filename)
        student = self.getParent(row, site).__parent__
        student.__parent__.logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, student.student_id, items_changed))
        return

    def addEntry(self, obj, row, site):
        if IGNORE_MARKER == str(row['level']):
            raise FatalCSVError("level: Invalid value")
        parent = self.getParent(row, site)
        parent[str(row['level'])] = obj
        return

    def checkCreateRequirements(self, parent, row, site):
        """
        """
        if parent.student.studycourse_locked:
            return 'Studycourse is locked.'
        return None

    def checkUpdateRequirements(self, obj, row, site):
        """
        """
        if obj.student.studycourse_locked:
            return 'Studylevel is locked.'
        return None

    def checkRemoveRequirements(self, obj, row, site):
        """
        """
        if obj.student.studycourse_locked:
            return 'Studycourse is locked.'
        return None

class CourseTicketProcessor(StudentProcessorBase):
    """The Course Ticket Processor imports course tickets, the subobjects
    of student study levels (= course lists).

    An imported course ticket contains a copy of the original course data.
    During import only a few attributes can be set/overwritten.

    Like all other student data importers, this processor also requires
    either `student_id`, `reg_number` or `matric_number` to find the student.
    Then it needs `level` and `code` to localize the course ticket.

    `checkConversion` first searches the courses catalog for the imported
    `code` and ensures that a course with such a code really exists
    in the academic section. It furthermore checks if `level_session` in
    the row corresponds with the session of the parent student
    study level object. It fails if one of the conditions is not met.

    In create mode `fcode`, `dcode`, `title`, `credits`, `passmark` and
    `semester` are taken from the course found in the academic section.
    `fcode` and `dcode` can nevermore be changed, neither via the user interface
    nor by import. Other values can be overwritten by import.

    `ticket_session` is an additional field which can be used to store the
    session of the course when it was taken. Usually this information is 
    redundant because the parent study level object already contains this
    information, except for the study level zero container which can be used to
    store 'orphaned' course tickets.

    `checkUpdateRequirements` ensures that the `score` attribute can't
    be accidentally overwritten by import in update mode. The `score`
    attribute can be unlocked by setting the boolean field
    `unlock_score` = 1.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'courseticketprocessor'
    grok.name(util_name)

    name = _('CourseTicket Processor')
    iface = ICourseTicketImport
    factory_name = 'waeup.CourseTicket'

    additional_fields = ['level', 'code']
    additional_fields_required = additional_fields

    @property
    def available_fields(self):
        fields = [
            'student_id','reg_number','matric_number',
            'mandatory', 'score', 'carry_over', 'automatic',
            'outstanding', 'course_category', 'level_session',
            'title', 'credits', 'passmark', 'semester', 'ticket_session',
            'unlock_score', 'previous'
            ] + self.additional_fields
        return sorted(fields)

    def getParent(self, row, site):
        student = self._getStudent(row, site)
        if student is None:
            return None
        return student[studycourseName(row)].get(str(row['level']))

    def getEntry(self, row, site):
        level = self.getParent(row, site)
        if level is None:
            return None
        return level.get(row['code'])

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = super(CourseTicketProcessor, self).updateEntry(
            obj, row, site, filename)
        parent = self.getParent(row, site)
        student = self.getParent(row, site).__parent__.__parent__
        student.__parent__.logger.info(
            '%s - %s - %s - %s - updated: %s'
            % (self.name, filename, student.student_id, parent.level, items_changed))
        return

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        catalog = getUtility(ICatalog, name='courses_catalog')
        entries = list(catalog.searchResults(code=(row['code'],row['code'])))
        obj.fcode = entries[0].__parent__.__parent__.__parent__.code
        obj.dcode = entries[0].__parent__.__parent__.code
        if getattr(obj, 'title', None) is None:
            obj.title = entries[0].title
        if getattr(obj, 'credits', None) is None:
            obj.credits = entries[0].credits
        if getattr(obj, 'passmark', None) is None:
            obj.passmark = entries[0].passmark
        if getattr(obj, 'semester', None) is None:
            obj.semester = entries[0].semester
        parent[row['code']] = obj
        return

    def delEntry(self, row, site):
        ticket = self.getEntry(row, site)
        parent = self.getParent(row, site)
        if ticket is not None:
            student = self._getStudent(row, site)
            student.__parent__.logger.info('%s - Course ticket in %s removed: %s'
                % (student.student_id, parent.level, ticket.code))
            del parent[ticket.code]
        return

    def checkCreateRequirements(self, parent, row, site):
        """
        """
        if parent.student.studycourse_locked:
            return 'Studycourse is locked.'
        return None

    def checkUpdateRequirements(self, obj, row, site):
        """
        """
        if obj.student.studycourse_locked:
            return 'Studycourse is locked.'
        if row.get('score',None) and obj.score and not row.get(
            'unlock_score',None):
            return 'Score attribute is locked.'
        return None

    def checkRemoveRequirements(self, obj, row, site):
        """
        """
        if obj.student.studycourse_locked:
            return 'Studycourse is locked.'
        return None

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        errs, inv_errs, conv_dict = super(
            CourseTicketProcessor, self).checkConversion(row, mode=mode)
        if mode == 'remove':
            return errs, inv_errs, conv_dict
        # In update and create mode we have to check if course really exists.
        # This is not done by the converter.
        catalog = getUtility(ICatalog, name='courses_catalog')
        entries = catalog.searchResults(code=(row['code'],row['code']))
        if len(entries) == 0:
            errs.append(('code','non-existent'))
            return errs, inv_errs, conv_dict
        # If level_session is provided in row we have to check if
        # the parent studylevel exists and if its level_session
        # attribute corresponds with the expected value in row.
        level_session = conv_dict.get('level_session', IGNORE_MARKER)
        if level_session not in (IGNORE_MARKER, None):
            site = grok.getSite()
            studylevel = self.getParent(row, site)
            if studylevel is not None:
                if studylevel.level_session != level_session:
                    errs.append(('level_session','does not match %s'
                        % studylevel.level_session))
            else:
                errs.append(('level object','does not exist'))
        return errs, inv_errs, conv_dict

class StudentOnlinePaymentProcessor(StudentProcessorBase):
    """The Student Online Payment Processor imports student payment tickets.
    The tickets are located in the ``payments`` subfolder of the student
    container. The only additional locator is `p_id`, the object id.

    The `checkConversion` method checks the format of the payment identifier.
    In create mode it does also ensures that same `p_id` does not exist
    elsewhere. It must be portal-wide unique.

    When adding a payment ticket, the `addEntry` method checks if the same
    payment has already been made. It compares `p_category` and `p_session`
    in the row with the corresponding attributes  of existing payment
    tickets in state ``paid``. If they match, a `DuplicationError` is raised.
    """
    grok.implements(IBatchProcessor)
    grok.provides(IBatchProcessor)
    grok.context(Interface)
    util_name = 'paymentprocessor'
    grok.name(util_name)

    name = _('StudentOnlinePayment Processor')
    iface = IStudentOnlinePayment
    factory_name = 'waeup.StudentOnlinePayment'

    additional_fields = ['p_id']

    @property
    def available_fields(self):
        af = super(
            StudentOnlinePaymentProcessor, self).available_fields
        af.remove('display_item')
        return af

    def checkHeaders(self, headerfields, mode='ignore'):
        super(StudentOnlinePaymentProcessor, self).checkHeaders(headerfields)
        if mode in ('update', 'remove') and not 'p_id' in headerfields:
            raise FatalCSVError(
                "Need p_id for import in update and remove modes!")
        return True

    def parentsExist(self, row, site):
        return self.getParent(row, site) is not None

    def getParent(self, row, site):
        student = self._getStudent(row, site)
        if student is None:
            return None
        return student['payments']

    def getEntry(self, row, site):
        payments = self.getParent(row, site)
        if payments is None:
            return None
        p_id = row.get('p_id', None)
        if p_id in (None, IGNORE_MARKER):
            return None
        # We can use the hash symbol at the end of p_id in import files
        # to avoid annoying automatic number transformation
        # by Excel or Calc
        p_id = p_id.strip('#')
        if len(p_id.split('-')) != 3 and not p_id.startswith('p'):
            # For data migration from old SRP only
            p_id = 'p' + p_id[7:] + '0'
        entry = payments.get(p_id)
        return entry

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        items_changed = super(StudentOnlinePaymentProcessor, self).updateEntry(
            obj, row, site, filename)
        student = self.getParent(row, site).__parent__
        student.__parent__.logger.info(
            '%s - %s - %s - updated: %s'
            % (self.name, filename, student.student_id, items_changed))
        return

    def samePaymentMade(self, student, category, p_session):
        for key in student['payments'].keys():
            ticket = student['payments'][key]
            if ticket.p_state == 'paid' and\
               ticket.p_category == category and \
               ticket.p_session == p_session and \
               ticket.p_item != 'Balance':
                  return True
        return False

    def addEntry(self, obj, row, site):
        parent = self.getParent(row, site)
        student = parent.student
        p_id = row['p_id'].strip('#')
        # Requirement added on 19/02/2015: same payment must not exist.
        if obj.p_item != 'Balance' and obj.p_state != 'paid' and self.samePaymentMade(
            student, obj.p_category, obj.p_session):
            student.__parent__.logger.info(
                '%s - %s - previous update cancelled'
                % (self.name, student.student_id))
            raise DuplicationError('Same payment has already been made.')
        if len(p_id.split('-')) != 3 and not p_id.startswith('p'):
            # For data migration from old SRP
            obj.p_id = 'p' + p_id[7:] + '0'
            parent[obj.p_id] = obj
        else:
            parent[p_id] = obj
        return

    def delEntry(self, row, site):
        payment = self.getEntry(row, site)
        parent = self.getParent(row, site)
        if payment is not None:
            student = self._getStudent(row, site)
            student.__parent__.logger.info('%s - Payment ticket removed: %s'
                % (student.student_id, payment.p_id))
            del parent[payment.p_id]
        return

    def checkConversion(self, row, mode='ignore'):
        """Validates all values in row.
        """
        errs, inv_errs, conv_dict = super(
            StudentOnlinePaymentProcessor, self).checkConversion(row, mode=mode)

        # We have to check p_id.
        p_id = row.get('p_id', None)
        if mode == 'create' and p_id in (None, IGNORE_MARKER):
            timestamp = ("%d" % int(time()*10000))[1:]
            p_id = "p%s" % timestamp
            conv_dict['p_id'] = p_id
            return errs, inv_errs, conv_dict
        elif p_id in (None, IGNORE_MARKER):
            errs.append(('p_id','missing'))
            return errs, inv_errs, conv_dict
        else:
            p_id = p_id.strip('#')
            if p_id.startswith('p'):
                if not len(p_id) == 14:
                    errs.append(('p_id','invalid length'))
                    return errs, inv_errs, conv_dict
            elif len(p_id.split('-')) == 3:
                # The SRP used either pins as keys ...
                if len(p_id.split('-')[2]) not in (9, 10):
                    errs.append(('p_id','invalid pin'))
                    return errs, inv_errs, conv_dict
            else:
                # ... or order_ids.
                if not len(p_id) == 19:
                    errs.append(('p_id','invalid format'))
                    return errs, inv_errs, conv_dict
        # Requirement added on 24/01/2015: p_id must be portal-wide unique.
        if mode == 'create':
            cat = getUtility(ICatalog, name='payments_catalog')
            results = list(cat.searchResults(p_id=(p_id, p_id)))
            if len(results) > 0:
                sids = [IPayer(payment).id for payment in results]
                sids_string = ''
                for id in sids:
                    sids_string += '%s ' % id
                errs.append(('p_id','p_id exists in %s' % sids_string))
                return errs, inv_errs, conv_dict
        return errs, inv_errs, conv_dict

class StudentVerdictProcessor(StudentStudyCourseProcessor):
    """The Student Verdict Processor inherits from the Student Study
    Course Processor. It's a pure updater. Import step 2 raises a warning
    message if a datacenter manager tries to select another mode.
    But it does more than only overwriting study course attributes.

    The Student Verdict Processor is the only processor which cannot be
    used for restoring data. Purpose is to announce a verdict at the end of
    each academic session. The processor does not only import a verdict,
    it also conditions the student data so that the student can pay for the
    next session and proceed to the next study level.

    The `checkUpdateRequirements` method ensures that the imported data
    really correspond to the actual state of the student.
    `current_level` and `current_session` in the row must be on par
    with the attributes of the study course object. Thus, the processor
    does not use these values to overwrite the attributes of the study course
    but to control that the verdict is really meant for the current session of
    the student. The verdict is only imported if a corresponding study level
    object exists and the student is in the right registration state,
    either ``courses validated`` or ``courses registered``. Course registration
    can be bypassed by setting `bypass_validation` to ``True``.

    The `updateEntry` method does not only update the current verdict of
    the student study course, it also updates the matching student study
    level object. It saves the current verdict as `level_verdict` and sets
    the `validated_by` and `validation_date` attributes, whereas `validated_by` 
    is taken from the row of the import file and `validation_date` is set to the
    actual UTC datetime. Finally, the student is moved to state ``returning``.
    """

    util_name = 'verdictupdater'
    grok.name(util_name)

    name = _('Verdict Processor (special processor, update only)')
    iface = IStudentVerdictUpdate
    factory_name = 'waeup.StudentStudyCourse'

    additional_fields_required = [
        'current_level', 'current_session', 'current_verdict']

    def checkUpdateRequirements(self, obj, row, site):
        """Checks requirements the studycourse and the student must fulfill
        before being updated.
        """
        # Check if current_levels correspond
        if obj.current_level != row['current_level']:
            return 'Current level does not correspond.'
        # Check if current_sessions correspond
        if obj.current_session != row['current_session']:
            return 'Current session does not correspond.'
        # Check if new verdict is provided
        if row['current_verdict'] in (IGNORE_MARKER, ''):
            return 'No verdict in import file.'
        # Check if studylevel exists
        level_string = str(obj.current_level)
        if obj.get(level_string) is None:
            return 'Study level object is missing.'
        # Check if student is in state REGISTERED or VALIDATED
        if row.get('bypass_validation'):
            if obj.student.state not in (VALIDATED, REGISTERED):
                return 'Student in wrong state.'
        else:
            if obj.student.state != VALIDATED:
                return 'Student in wrong state.'
        return None

    def updateEntry(self, obj, row, site, filename):
        """Update obj to the values given in row.
        """
        # Don't set current_session, current_level
        vals_to_set = dict((key, val) for key, val in row.items()
                           if key not in ('current_session','current_level'))
        super(StudentVerdictProcessor, self).updateEntry(
            obj, vals_to_set, site, filename)
        parent = self.getParent(row, site)
        # Set current_verdict in corresponding studylevel
        level_string = str(obj.current_level)
        obj[level_string].level_verdict = row['current_verdict']
        # Fire transition and set studylevel attributes
        # depending on student's state
        if obj.__parent__.state == REGISTERED:
            validated_by = row.get('validated_by', '')
            if validated_by in (IGNORE_MARKER, ''):
                portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
                system = translate(_('System'),'waeup.kofa',
                                  target_language=portal_language)
                obj[level_string].validated_by = system
            else:
                obj[level_string].validated_by = validated_by
            obj[level_string].validation_date = datetime.utcnow()
            IWorkflowInfo(obj.__parent__).fireTransition('bypass_validation')
        else:
            IWorkflowInfo(obj.__parent__).fireTransition('return')
        # Update the students_catalog
        notify(grok.ObjectModifiedEvent(obj.__parent__))
        return
