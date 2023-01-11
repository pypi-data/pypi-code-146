## $Id: student.py 16713 2021-11-15 12:47:49Z henrik $
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
Container for the various objects owned by students.
"""
import os
import re
import shutil
import grok
from datetime import datetime, timedelta
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from zope.password.interfaces import IPasswordManager
from zope.component import getUtility, createObject
from zope.component.interfaces import IFactory
from zope.interface import implementedBy
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.schema.interfaces import ConstraintNotSatisfied
from zope.event import notify

from waeup.kofa.authentication import LocalRoleSetEvent
from waeup.kofa.image import KofaImageFile
from waeup.kofa.imagestorage import DefaultFileStoreHandler
from waeup.kofa.interfaces import (
    IObjectHistory, IUserAccount, IFileStoreNameChooser, IFileStoreHandler,
    IKofaUtils, registration_states_vocab, IExtFileStore,
    CREATED, ADMITTED, CLEARANCE, PAID, REGISTERED, VALIDATED, RETURNING,
    GRADUATED, TRANSVAL, TRANSREL)
from waeup.kofa.students.accommodation import StudentAccommodation
from waeup.kofa.students.interfaces import (
    IStudent, IStudentNavigation, IStudentPersonalEdit, ICSVStudentExporter,
    IStudentsUtils)
from waeup.kofa.students.payments import StudentPaymentsContainer
from waeup.kofa.students.utils import generate_student_id
from waeup.kofa.utils.helpers import attrs_to_fields, now, copy_filesystem_tree

RE_STUDID_NON_NUM = re.compile('[^\d]+')

class Student(grok.Container):
    """This is a student container for the various objects
    owned by students.
    """
    grok.implements(IStudent, IStudentNavigation, IStudentPersonalEdit)
    grok.provides(IStudent)

    def __init__(self):
        super(Student, self).__init__()
        # The site doesn't exist in unit tests
        try:
            self.student_id = generate_student_id()
        except TypeError:
            self.student_id = u'Z654321'
        self.password = None
        self.temp_password = None
        self.parents_password = None
        return

    def setTempPassword(self, user, password):
        """Set a temporary password (LDAP-compatible) SSHA encoded for
        officers.
        """
        passwordmanager = getUtility(IPasswordManager, 'SSHA')
        self.temp_password = {}
        self.temp_password[
            'password'] = passwordmanager.encodePassword(password)
        self.temp_password['user'] = user
        self.temp_password['timestamp'] = datetime.utcnow() # offset-naive datetime

    def getTempPassword(self):
        """Check if a temporary password has been set and if it
        is not expired. 

        Return the temporary password if valid,
        None otherwise. Unset the temporary password if expired.
        """
        temp_password_dict = getattr(self, 'temp_password', None)
        kofa_utils = getUtility(IKofaUtils)
        temp_password_minutes =  kofa_utils.TEMP_PASSWORD_MINUTES
        if temp_password_dict is not None:
            delta = timedelta(minutes=temp_password_minutes)
            now = datetime.utcnow()
            if now < temp_password_dict.get('timestamp') + delta:
                return temp_password_dict.get('password')
            else:
                # Unset temporary password if expired
                self.temp_password = None
        return None

    def setParentsPassword(self, password):
        """Set a temporary password (LDAP-compatible) SSHA encoded for
        parents.
        """
        passwordmanager = getUtility(IPasswordManager, 'SSHA')
        self.parents_password = {}
        self.parents_password[
            'password'] = passwordmanager.encodePassword(password)
        self.parents_password['timestamp'] = datetime.utcnow() # offset-naive datetime

    def getParentsPassword(self):
        """Check if a parents password has been set and if it
        is not expired.

        Return the parents password if valid,
        None otherwise. Unset the parents password and replace roles
        if expired.
        """
        parents_password_dict = getattr(self, 'parents_password', None)
        kofa_utils = getUtility(IKofaUtils)
        temp_password_minutes =  kofa_utils.TEMP_PASSWORD_MINUTES
        if parents_password_dict is not None:
            delta = timedelta(minutes=temp_password_minutes)
            now = datetime.utcnow()
            if now < parents_password_dict.get('timestamp') + delta:
                return parents_password_dict.get('password')
            else:
                # Unset parents password if expired
                self.parents_password = None
                # Replace roles if expired
                role_manager = IPrincipalRoleManager(self)
                role_manager.removeRoleFromPrincipal(
                    'waeup.local.Parents', self.student_id)
                notify(LocalRoleSetEvent(
                    self, 'waeup.local.Parents',
                    self.student_id, granted=False))
                role_manager.assignRoleToPrincipal(
                    'waeup.local.StudentRecordOwner', self.student_id)
                notify(LocalRoleSetEvent(
                    self, 'waeup.local.StudentRecordOwner',
                    self.student_id, granted=True))
        return None

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.logger.info(
            '%s - %s - %s' % (ob_class, self.__name__, message))
        return

    @property
    def display_fullname(self):
        middlename = getattr(self, 'middlename', None)
        kofa_utils = getUtility(IKofaUtils)
        return kofa_utils.fullname(self.firstname, self.lastname, middlename)

    @property
    def fullname(self):
        middlename = getattr(self, 'middlename', None)
        if middlename:
            return '%s-%s-%s' % (self.firstname.lower(),
                middlename.lower(), self.lastname.lower())
        else:
            return '%s-%s' % (self.firstname.lower(), self.lastname.lower())

    @property
    def state(self):
        state = IWorkflowState(self).getState()
        return state

    @property
    def translated_state(self):
        try:
            state = registration_states_vocab.getTermByToken(
                self.state).title
        except LookupError:  # in unit tests
            return
        return state

    @property
    def history(self):
        history = IObjectHistory(self)
        return history

    @property
    def student(self):
        return self

    @property
    def certcode(self):
        cert = getattr(self.get('studycourse', None), 'certificate', None)
        if cert is not None:
            return cert.code
        return

    @property
    def faccode(self):
        cert = getattr(self.get('studycourse', None), 'certificate', None)
        if cert is not None:
            return cert.__parent__.__parent__.__parent__.code
        return

    @property
    def depcode(self):
        cert = getattr(self.get('studycourse', None), 'certificate', None)
        if cert is not None:
            return cert.__parent__.__parent__.code
        return

    @property
    def current_session(self):
        session = getattr(
            self.get('studycourse', None), 'current_session', None)
        return session

    @property
    def entry_session(self):
        session = getattr(
            self.get('studycourse', None), 'entry_session', None)
        return session

    @property
    def entry_mode(self):
        session = getattr(
            self.get('studycourse', None), 'entry_mode', None)
        return session

    @property
    def current_level(self):
        level = getattr(
            self.get('studycourse', None), 'current_level', None)
        return level

    @property
    def current_verdict(self):
        current_verdict = getattr(
            self.get('studycourse', None), 'current_verdict', None)
        return current_verdict

    @property
    def current_mode(self):
        certificate = getattr(
            self.get('studycourse', None), 'certificate', None)
        if certificate is not None:
            return certificate.study_mode
        return None

    @property
    def is_postgrad(self):
        is_postgrad = getattr(
            self.get('studycourse', None), 'is_postgrad', False)
        return is_postgrad

    @property
    def is_special_postgrad(self):
        is_special_postgrad = getattr(
            self.get('studycourse', None), 'is_special_postgrad', False)
        return is_special_postgrad

    @property
    def is_fresh(self):
        return self.current_session == self.entry_session

    @property
    def before_payment(self):
        non_fresh_states = (PAID, REGISTERED, VALIDATED, RETURNING, GRADUATED)
        if self.is_fresh and self.state not in non_fresh_states:
            return True
        return False

    @property
    def personal_data_expired(self):
        #if self.state in (CREATED, ADMITTED,):
        #    return False
        now = datetime.utcnow()
        if self.personal_updated is None:
            return True
        try:
            days_ago = getattr(now - self.personal_updated, 'days')
        except TypeError: 
            # This happens after reimport of personal_updated because
            # Python  can't subtract offset-naive and offset-aware datetimes
            return True
        if days_ago > 180:
            return True
        return False

    @property
    def transcript_enabled(self):
        return True

    @property
    def studycourse_locked(self):
        return self.state in (GRADUATED, TRANSREL, TRANSVAL)

    @property
    def clearance_locked(self):
        return self.state != CLEARANCE

    def transfer(self, certificate, current_session=None,
        current_level=None, current_verdict=None, previous_verdict=None):
        """ Creates a new studycourse and backups the old one.
        """
        newcourse = createObject(u'waeup.StudentStudyCourse')
        try:
            newcourse.certificate = certificate
            newcourse.entry_mode = 'transfer'
            newcourse.current_session = current_session
            newcourse.current_level = current_level
            newcourse.current_verdict = current_verdict
            newcourse.previous_verdict = previous_verdict
        except ConstraintNotSatisfied:
            return -1
        oldcourse = self['studycourse']
        if getattr(oldcourse, 'entry_session', None) is None or\
            getattr(oldcourse, 'certificate', None) is None:
            return -2
        newcourse.entry_session = oldcourse.entry_session
        # Students can be transferred only two times.
        if 'studycourse_1' in self.keys():
            if 'studycourse_2' in self.keys():
                return -3
            self['studycourse_2'] = oldcourse
        else:
            self['studycourse_1'] = oldcourse
        del self['studycourse']
        self['studycourse'] = newcourse
        self.__parent__.logger.info(
            '%s - transferred from %s to %s' % (
            self.student_id,
            oldcourse.certificate.code,
            newcourse.certificate.code))
        history = IObjectHistory(self)
        history.addMessage('Transferred from %s to %s' % (
            oldcourse.certificate.code, newcourse.certificate.code))
        return

    def revert_transfer(self):
        """ Revert previous transfer.

        """
        if not self.has_key('studycourse_1'):
            return -1
        del self['studycourse']
        if 'studycourse_2' in self.keys():
            studycourse = self['studycourse_2']
            self['studycourse'] = studycourse
            del self['studycourse_2']
        else:
            studycourse = self['studycourse_1']
            self['studycourse'] = studycourse
            del self['studycourse_1']
        self.__parent__.logger.info(
            '%s - transfer reverted' % self.student_id)
        history = IObjectHistory(self)
        history.addMessage('Transfer reverted')
        return

# Set all attributes of Student required in IStudent as field
# properties. Doing this, we do not have to set initial attributes
# ourselves and as a bonus we get free validation when an attribute is
# set.
Student = attrs_to_fields(Student)

class StudentFactory(grok.GlobalUtility):
    """A factory for students.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Student')
    title = u"Create a new student.",
    description = u"This factory instantiates new student instances."

    def __call__(self, *args, **kw):
        return Student()

    def getInterfaces(self):
        return implementedBy(Student)

@grok.subscribe(IStudent, grok.IObjectAddedEvent)
def handle_student_added(student, event):
    """If a student is added all subcontainers are automatically added
    and the transition create is fired. The latter produces a logging
    message.
    """
    studycourse = createObject(u'waeup.StudentStudyCourse')
    student['studycourse'] = studycourse
    payments = StudentPaymentsContainer()
    student['payments'] = payments
    accommodation = StudentAccommodation()
    student['accommodation'] = accommodation
    # Assign global student role for new student
    account = IUserAccount(student)
    account.roles = ['waeup.Student']
    # Assign local StudentRecordOwner role
    role_manager = IPrincipalRoleManager(student)
    role_manager.assignRoleToPrincipal(
        'waeup.local.StudentRecordOwner', student.student_id)
    if student.state is None:
        IWorkflowInfo(student).fireTransition('create')
    return

def path_from_studid(student_id):
    """Convert a student_id into a predictable relative folder path.

    Used for storing files.

    Returns the name of folder in which files for a particular student
    should be stored. This is a relative path, relative to any general
    students folder with 5 zero-padded digits (except when student_id
    is overlong).

    We normally map 1,000 different student ids into one single
    path. For instance ``K1000000`` will give ``01000/K1000000``,
    ``K1234567`` will give ``0123/K1234567`` and ``K12345678`` will
    result in ``1234/K12345678``.

    For lower numbers < 10**6 we return the same path for up to 10,000
    student_ids. So for instance ``KM123456`` will result in
    ``00120/KM123456`` (there will be no path starting with
    ``00123``).

    Works also with overlong number: here the leading zeros will be
    missing but ``K123456789`` will give reliably
    ``12345/K123456789`` as expected.
    """
    # remove all non numeric characters and turn this into an int.
    num = int(RE_STUDID_NON_NUM.sub('', student_id))
    if num < 10**6:
        # store max. of 10000 studs per folder and correct num for 5 digits
        num = num / 10000 * 10
    else:
        # store max. of 1000 studs per folder
        num = num / 1000
    # format folder name to have 5 zero-padded digits
    folder_name = u'%05d' % num
    folder_name = os.path.join(folder_name, student_id)
    return folder_name

def move_student_files(student, del_dir):
    """Move files belonging to `student` to `del_dir`.

    `del_dir` is expected to be the path to the site-wide directory
    for storing backup data.

    The current files of the student are removed after backup.

    If the student has no associated files stored, nothing is done.
    """
    stud_id = student.student_id

    src = getUtility(IExtFileStore).root
    src = os.path.join(src, 'students', path_from_studid(stud_id))

    dst = os.path.join(
        del_dir, 'media', 'students', path_from_studid(stud_id))

    if not os.path.isdir(src):
        # Do not copy if no files were stored.
        return
    if not os.path.exists(dst):
        os.makedirs(dst, 0755)
    copy_filesystem_tree(src, dst)
    shutil.rmtree(src)
    return

def update_student_deletion_csvs(student, del_dir):
    """Update deletion CSV files with data from student.

    `del_dir` is expected to be the path to the site-wide directory
    for storing backup data.

    Each exporter available for students (and their many subobjects)
    is called in order to export CSV data of the given student to csv
    files in the site-wide backup directory for object data (see
    DataCenter).

    Each exported row is appended a column giving the deletion date
    (column `del_date`) as a UTC timestamp.
    """

    STUDENT_BACKUP_EXPORTER_NAMES = getUtility(
        IStudentsUtils).STUDENT_BACKUP_EXPORTER_NAMES

    for name in STUDENT_BACKUP_EXPORTER_NAMES:
        exporter = getUtility(ICSVStudentExporter, name=name)
        csv_data = exporter.export_student(student)
        csv_data = csv_data.split('\r\n')

        # append a deletion timestamp on each data row
        timestamp = str(now().replace(microsecond=0)) # store UTC timestamp
        for num, row in enumerate(csv_data[1:-1]):
            csv_data[num+1] = csv_data[num+1] + ',' + timestamp
        csv_path = os.path.join(del_dir, '%s.csv' % name)

        # write data to CSV file
        if not os.path.exists(csv_path):
            # create new CSV file (including header line)
            csv_data[0] = csv_data[0] + ',del_date'
            open(csv_path, 'wb').write('\r\n'.join(csv_data))
        else:
            # append existing CSV file (omitting headerline)
            open(csv_path, 'a').write('\r\n'.join(csv_data[1:]))
    return

@grok.subscribe(IStudent, grok.IObjectRemovedEvent)
def handle_student_removed(student, event):
    """If a student is removed a message is logged and data is put
       into a backup location.

    The data of the removed student is appended to CSV files in local
    datacenter and any existing external files (passport images, etc.)
    are copied over to this location as well.

    Documents in the file storage refering to the given student are
    removed afterwards (if they exist). Please make no assumptions
    about how the deletion takes place. Files might be deleted
    individually (leaving the students file directory intact) or the
    whole student directory might be deleted completely.

    All CSV rows created/appended contain a timestamp with the
    datetime of removal in an additional `del_date` column.

    XXX: blocking of used student_ids yet not implemented.
    """
    comment = 'Student record removed'
    target = student.student_id
    try:
        site = grok.getSite()
        site['students'].logger.info('%s - %s' % (
            target, comment))
    except KeyError:
        # If we delete an entire university instance there won't be
        # a students subcontainer
        return

    del_dir = site['datacenter'].deleted_path

    if student.state == GRADUATED:
        del_dir = site['datacenter'].graduated_path

    # save files of the student
    move_student_files(student, del_dir)

    # update CSV files
    update_student_deletion_csvs(student, del_dir)

    # remove global role
    role_manager = IPrincipalRoleManager(grok.getSite())
    role_manager.unsetRoleForPrincipal('waeup.Student', student.student_id)
    return

#: The file id marker for student files
STUDENT_FILE_STORE_NAME = 'file-student'

class StudentFileNameChooser(grok.Adapter):
    """A file id chooser for :class:`Student` objects.

    `context` is an :class:`Student` instance.

    The :class:`StudentImageNameChooser` can build/check file ids for
    :class:`Student` objects suitable for use with
    :class:`ExtFileStore` instances. The delivered file_id contains
    the file id marker for :class:`Student` object and the student id
    of the context student.

    This chooser is registered as an adapter providing
    :class:`waeup.kofa.interfaces.IFileStoreNameChooser`.

    File store name choosers like this one are only convenience
    components to ease the task of creating file ids for student
    objects. You are nevertheless encouraged to use them instead of
    manually setting up filenames for students.

    .. seealso:: :mod:`waeup.kofa.imagestorage`

    """
    grok.context(IStudent)
    grok.implements(IFileStoreNameChooser)

    def checkName(self, name=None, attr=None):
        """Check whether the given name is a valid file id for the context.

        Returns ``True`` only if `name` equals the result of
        :meth:`chooseName`.

        """
        return name == self.chooseName()

    def chooseName(self, attr, name=None):
        """Get a valid file id for student context.

        *Example:*

        For a student with student id ``'A123456'`` and
        with attr ``'nice_image.jpeg'`` stored in
        the students container this chooser would create:

          ``'__file-student__students/A/A123456/nice_image_A123456.jpeg'``

        meaning that the nice image of this applicant would be
        stored in the site-wide file storage in path:

          ``students/A/A123456/nice_image_A123456.jpeg``

        """
        basename, ext = os.path.splitext(attr)
        stud_id = self.context.student_id
        marked_filename = '__%s__%s/%s_%s%s' % (
            STUDENT_FILE_STORE_NAME, path_from_studid(stud_id), basename,
            stud_id, ext)
        return marked_filename


class StudentFileStoreHandler(DefaultFileStoreHandler, grok.GlobalUtility):
    """Student specific file handling.

    This handler knows in which path in a filestore to store student
    files and how to turn this kind of data into some (browsable)
    file object.

    It is called from the global file storage, when it wants to
    get/store a file with a file id starting with
    ``__file-student__`` (the marker string for student files).

    Like each other file store handler it does not handle the files
    really (this is done by the global file store) but only computes
    paths and things like this.
    """
    grok.implements(IFileStoreHandler)
    grok.name(STUDENT_FILE_STORE_NAME)

    def pathFromFileID(self, store, root, file_id):
        """All student files are put in directory ``students``.
        """
        marker, filename, basename, ext = store.extractMarker(file_id)
        sub_root = os.path.join(root, 'students')
        return super(StudentFileStoreHandler, self).pathFromFileID(
            store, sub_root, basename)

    def createFile(self, store, root, filename, file_id, file):
        """Create a browsable file-like object.
        """
        # call super method to ensure that any old files with
        # different filename extension are deleted.
        file, path, file_obj =  super(
            StudentFileStoreHandler, self).createFile(
            store, root,  filename, file_id, file)
        return file, path, KofaImageFile(
            file_obj.filename, file_obj.data)
