## $Id: applicant.py 17055 2022-08-02 22:53:36Z henrik $
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
import os
import grok
from cStringIO import StringIO
from grok import index
from hurry.query import Eq, Text
from hurry.query.query import Query
from urllib import urlencode
from zope.component import getUtility, createObject, getAdapter
from zope.component.interfaces import IFactory
from zope.event import notify
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.interface import implementedBy
from zope.schema.interfaces import (
    RequiredMissing, ConstraintNotSatisfied, WrongType)
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from waeup.kofa.image import KofaImageFile
from reportlab.platypus.doctemplate import LayoutError
from waeup.kofa.imagestorage import DefaultFileStoreHandler
from waeup.kofa.interfaces import (
    IObjectHistory, IFileStoreHandler, IFileStoreNameChooser, IKofaUtils,
    IExtFileStore, IPDF, IUserAccount, IUniversity)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.students.vocabularies import RegNumNotInSource
from waeup.kofa.students.studycourse import StudentStudyCourse
from waeup.kofa.utils.helpers import attrs_to_fields
from waeup.kofa.applicants.interfaces import (
    IApplicant, IApplicantEdit, ISpecialApplicant, IApplicantsUtils)
from waeup.kofa.applicants.workflow import application_states_dict
from waeup.kofa.applicants.payment import ApplicantOnlinePayment
from waeup.kofa.applicants.refereereport import ApplicantRefereeReport

def search(query=None, searchtype=None, view=None):
    if searchtype in ('fullname',):
        results = Query().searchResults(
            Text(('applicants_catalog', searchtype), query))
    else:
        results = Query().searchResults(
            Eq(('applicants_catalog', searchtype), query))
    return results

class Applicant(grok.Container):
    grok.implements(IApplicant, IApplicantEdit, ISpecialApplicant)
    grok.provides(IApplicant)

    applicant_student_mapping = [
        ('firstname', 'firstname'),
        ('middlename', 'middlename'),
        ('lastname', 'lastname'),
        ('sex', 'sex'),
        ('date_of_birth', 'date_of_birth'),
        ('email', 'email'),
        ('phone', 'phone'),
        ]

    applicant_graduated_mapping = [
        ('firstname', 'firstname'),
        ('middlename', 'middlename'),
        ('lastname', 'lastname'),
        ('sex', 'sex'),
        ('date_of_birth', 'date_of_birth'),
        ('email', 'email'),
        ('phone', 'phone'),
        ]

    def __init__(self):
        super(Applicant, self).__init__()
        self.password = None
        self.application_date = None
        self.applicant_id = None
        return

    @property
    def payments(self):
        payments = [value for value in self.values()
            if isinstance(value, ApplicantOnlinePayment)]
        return payments

    @property
    def refereereports(self):
        reports = [value for value in self.values()
            if isinstance(value, ApplicantRefereeReport)]
        return reports

    def writeLogMessage(self, view, message):
        ob_class = view.__implemented__.__name__.replace('waeup.kofa.','')
        self.__parent__.__parent__.logger.info(
            '%s - %s - %s' % (ob_class, self.applicant_id, message))
        return

    @property
    def state(self):
        return IWorkflowState(self).getState()

    @property
    def container_code(self):
        try:
            code = self.__parent__.code
        except AttributeError:  # in unit tests
            return
        if (self.password,
            self.firstname,
            self.lastname,
            self.email) == (None, None, None, None):
            return code + '-'
        return code + '+'

    @property
    def translated_state(self):
        try:
            state = application_states_dict[self.state]
        except LookupError:  # in unit tests
            return
        return state

    @property
    def history(self):
        history = IObjectHistory(self)
        return history

    @property
    def special(self):
        try:
            special = self.__parent__.prefix.startswith('special')
        except AttributeError:  # in unit tests
            return
        return special

    @property
    def application_number(self):
        try:
            return self.applicant_id.split('_')[1]
        except AttributeError:
            return None

    @property
    def display_fullname(self):
        middlename = getattr(self, 'middlename', None)
        kofa_utils = getUtility(IKofaUtils)
        return kofa_utils.fullname(self.firstname, self.lastname, middlename)

    def _setStudyCourseAttributes(self, studycourse):
        studycourse.entry_mode = self.course_admitted.study_mode
        studycourse.current_level = self.course_admitted.start_level
        studycourse.certificate = self.course_admitted
        studycourse.entry_session = self.__parent__.year
        studycourse.current_session = self.__parent__.year
        return

    def _setGraduatedStudyCourseAttributes(self, studycourse):
        studycourse.entry_mode = self.course_studied.study_mode
        studycourse.current_level = self.course_studied.start_level
        studycourse.certificate = self.course_studied
        studycourse.entry_session = self.__parent__.year
        studycourse.current_session = self.__parent__.year
        return

    def createStudent(self, view=None, graduated=False, send_email=False):
        """Create a student, fill with base data, create an application slip,
        copy applicant data and files, send an email (optional).
        """
        site = grok.getSite()
        # Is applicant in the correct state?
        if graduated:
            if self.state != 'processed':
                return False, _('Applicant has not yet been processed.')
            certificate = getattr(self, 'course_studied', None)
            mapping = self.applicant_graduated_mapping
        else:
            if self.state != 'admitted':
                return False, _('Applicant has not yet been admitted.')
            certificate = getattr(self, 'course_admitted', None)
            mapping = self.applicant_student_mapping
        # Set (fallback) reg_number
        if self.reg_number is None:
            self.reg_number = self.applicant_id
        # Does registration number exist?
        student = createObject(u'waeup.Student')
        try:
            student.reg_number = self.reg_number
        except RegNumNotInSource:
            # Reset _curr_stud_id 
            site['students']._curr_stud_id -= 1
            return False, _('Registration Number exists.')
        # Has the course_admitted/course_studied field been properly filled?
        if certificate is None:
            # Reset _curr_stud_id
            site['students']._curr_stud_id -= 1
            return False, _('No study course provided.')
        # Set student attributes
        try:
            for item in mapping:
                if item[0] == 'email':
                    # The field type in the application section might be
                    # TextLineChoice to guarantee uniqueness of email addresses.
                    setattr(student, item[1], str(getattr(self, item[0], None)))
                else:
                    setattr(student, item[1], getattr(self, item[0], None))
        except RequiredMissing, err:
            site['students']._curr_stud_id -= 1
            return False, 'RequiredMissing: %s' % err
        except WrongType, err:
            site['students']._curr_stud_id -= 1
            return False, 'WrongType: %s' % err
        except UnicodeEncodeError, err:
            return False, 'UnicodeEncodeError: %s' % err
        except:
            site['students']._curr_stud_id -= 1
            return False, 'Unknown Error'
        # Prove if the certificate still exists
        try:
            StudentStudyCourse().certificate = certificate
        except ConstraintNotSatisfied, err:
            # Reset _curr_stud_id
            site['students']._curr_stud_id -= 1
            return False, 'ConstraintNotSatisfied: %s' % certificate.code
        # Finally prove if an application slip can be created
        try:
            test_applicant_slip = getAdapter(self, IPDF, name='application_slip')(
                view=view)
        except IOError:
            site['students']._curr_stud_id -= 1
            return False, _('IOError: Application Slip could not be created.')
        except LayoutError, err:
            site['students']._curr_stud_id -= 1
            return False, _('Reportlab LayoutError: %s' % err)
        except AttributeError, err:
            site['students']._curr_stud_id -= 1
            return False, _('Reportlab AttributeError: ${a}', mapping = {'a':err})
        except:
            site['students']._curr_stud_id -= 1
            return False, _('Unknown Reportlab error')
        # Add student
        site['students'].addStudent(student)
        # Save student_id
        self.student_id = student.student_id
        if graduated:
            # Set state
            IWorkflowState(student).setState('graduated')
            # Save the certificate and set study course attributes
            self._setGraduatedStudyCourseAttributes(student['studycourse'])
        else:
            # Fire transitions
            IWorkflowInfo(self).fireTransition('create')
            IWorkflowInfo(student).fireTransition('admit')
            # Save the certificate and set study course attributes
            self._setStudyCourseAttributes(student['studycourse'])
        # Set password
        IUserAccount(student).setPassword(self.application_number)
        self._copyPassportImage(student)
        self._copyFiles(student)
        # Update the catalog
        notify(grok.ObjectModifiedEvent(student))
        # Save application slip
        applicant_slip = getAdapter(self, IPDF, name='application_slip')(
            view=view)
        self._saveApplicationPDF(student, applicant_slip, view=view)
        if view and send_email:
            kofa_utils = getUtility(IKofaUtils)
            pw = self.application_number
            args = {'login':student.student_id, 'password':pw}
            login_url = view.url(grok.getSite()) + '/login?%s' % urlencode(args)
            rpw_url = view.url(grok.getSite(), 'changepw')
            kofa_utils.informNewStudent(
                IUserAccount(student), pw, login_url, rpw_url)
        return True, _('Student ${a} created', mapping = {'a':student.student_id})

    def _saveApplicationPDF(self, student, applicant_slip, view=None):
        """Create an application slip as PDF and store it in student folder.
        """
        file_store = getUtility(IExtFileStore)
        file_id = IFileStoreNameChooser(student).chooseName(
            attr="application_slip.pdf")
        file_store.createFile(file_id, StringIO(applicant_slip))
        return

    def _copyPassportImage(self, student):
        """Copy any passport image over to student location.
        """
        file_store = getUtility(IExtFileStore)
        appl_file = file_store.getFileByContext(self)
        if appl_file is None:
            return
        stud_file_id = IFileStoreNameChooser(student).chooseName(
            attr="passport.jpg")
        file_store.createFile(stud_file_id, appl_file)
        return

    def _copyFiles(self, student):
        """Copy all other files over to student location. Not
        used in base package but tested with fake file.
        """
        file_store = getUtility(IExtFileStore)
        filenames = getUtility(IApplicantsUtils).ADDITIONAL_FILES
        for filename in filenames:
            appl_file = file_store.getFileByContext(self, attr=filename[1])
            if appl_file is None:
                continue
            ext = os.path.splitext(appl_file.name)[1]
            stud_file_id = IFileStoreNameChooser(student).chooseName(
                attr=filename[1] + ext)
            file_store.createFile(stud_file_id, appl_file)
        return

# Set all attributes of Applicant required in IApplicant as field
# properties. Doing this, we do not have to set initial attributes
# ourselves and as a bonus we get free validation when an attribute is
# set.
Applicant = attrs_to_fields(Applicant)

class ApplicantsCatalog(grok.Indexes):
    """A catalog indexing :class:`Applicant` instances in the ZODB.
    """
    grok.site(IUniversity)
    grok.name('applicants_catalog')
    grok.context(IApplicant)

    fullname = index.Text(attribute='display_fullname')
    applicant_id = index.Field(attribute='applicant_id')
    reg_number = index.Field(attribute='reg_number')
    email = index.Field(attribute='email')
    state = index.Field(attribute='state')
    container_code = index.Field(attribute='container_code')

class ApplicantFactory(grok.GlobalUtility):
    """A factory for applicants.
    """
    grok.implements(IFactory)
    grok.name(u'waeup.Applicant')
    title = u"Create a new applicant.",
    description = u"This factory instantiates new applicant instances."

    def __call__(self, *args, **kw):
        return Applicant()

    def getInterfaces(self):
        return implementedBy(Applicant)


#: The file id marker for applicant passport images
APPLICANT_IMAGE_STORE_NAME = 'img-applicant'

class ApplicantImageNameChooser(grok.Adapter):
    """A file id chooser for :class:`Applicant` objects.

    `context` is an :class:`Applicant` instance.

    The :class:`ApplicantImageNameChooser` can build/check file ids
    for :class:`Applicant` objects suitable for use with
    :class:`ExtFileStore` instances. The delivered file_id contains
    the file id marker for :class:`Applicant` object and the
    registration number or access code of the context applicant. Also
    the name of the connected applicant container will be part of the
    generated file id.

    This chooser is registered as an adapter providing
    :class:`waeup.kofa.interfaces.IFileStoreNameChooser`.

    File store name choosers like this one are only convenience
    components to ease the task of creating file ids for applicant
    objects. You are nevertheless encouraged to use them instead of
    manually setting up filenames for applicants.

    .. seealso:: :mod:`waeup.kofa.imagestorage`

    """
    grok.context(IApplicant)
    grok.implements(IFileStoreNameChooser)

    def checkName(self, name=None, attr=None):
        """Check whether the given name is a valid file id for the context.

        Returns ``True`` only if `name` equals the result of
        :meth:`chooseName`.

        The `attr` parameter is not taken into account for
        :class:`Applicant` context as the single passport image is the
        only file we store for applicants.
        """
        return name == self.chooseName()

    def chooseName(self, name=None, attr=None):
        """Get a valid file id for applicant context.

        *Example:*

        For an applicant with applicant_id. ``'app2001_1234'``
        and stored in an applicants container called
        ``'mycontainer'``, this chooser would create:

          ``'__img-applicant__mycontainer/app2001_1234.jpg'``

        meaning that the passport image of this applicant would be
        stored in the site-wide file storage in path:

          ``mycontainer/app2001_1234.jpg``

        If the context applicant has no parent, ``'_default'`` is used
        as parent name.

        In the beginning the `attr` parameter was not taken into account for
        :class:`Applicant` context as the single passport image was the
        only file we store for applicants. Meanwhile many universities require
        uploads of other documents too. Now we store passport image
        files without attribute but all other documents with.

        """
        parent_name = getattr(
            getattr(self.context, '__parent__', None),
            '__name__', '_default')
        if attr is None or attr == 'passport.jpg':
            marked_filename = '__%s__%s/%s.jpg' % (
                APPLICANT_IMAGE_STORE_NAME,
                parent_name, self.context.applicant_id)
        else:
            basename, ext = os.path.splitext(attr)
            marked_filename = '__%s__%s/%s_%s%s' % (
                APPLICANT_IMAGE_STORE_NAME,
                parent_name, basename, self.context.applicant_id, ext)
        return marked_filename


class ApplicantImageStoreHandler(DefaultFileStoreHandler, grok.GlobalUtility):
    """Applicant specific image handling.

    This handler knows in which path in a filestore to store applicant
    images and how to turn this kind of data into some (browsable)
    file object.

    It is called from the global file storage, when it wants to
    get/store a file with a file id starting with
    ``__img-applicant__`` (the marker string for applicant images).

    Like each other file store handler it does not handle the files
    really (this is done by the global file store) but only computes
    paths and things like this.
    """
    grok.implements(IFileStoreHandler)
    grok.name(APPLICANT_IMAGE_STORE_NAME)

    def pathFromFileID(self, store, root, file_id):
        """All applicants images are filed in directory ``applicants``.
        """
        marker, filename, basename, ext = store.extractMarker(file_id)
        sub_root = os.path.join(root, 'applicants')
        return super(ApplicantImageStoreHandler, self).pathFromFileID(
            store, sub_root, basename)

    def createFile(self, store, root, filename, file_id, file):
        """Create a browsable file-like object.
        """
        # call super method to ensure that any old files with
        # different filename extension are deleted.
        file, path, file_obj =  super(
            ApplicantImageStoreHandler, self).createFile(
            store, root,  filename, file_id, file)
        return file, path, KofaImageFile(
            file_obj.filename, file_obj.data)

@grok.subscribe(IApplicant, grok.IObjectAddedEvent)
def handle_applicant_added(applicant, event):
    """If an applicant is added local and site roles are assigned.
    """
    role_manager = IPrincipalRoleManager(applicant)
    role_manager.assignRoleToPrincipal(
        'waeup.local.ApplicationOwner', applicant.applicant_id)
    # Assign current principal the global Applicant role
    role_manager = IPrincipalRoleManager(grok.getSite())
    role_manager.assignRoleToPrincipal(
        'waeup.Applicant', applicant.applicant_id)
    if applicant.state is None:
        IWorkflowInfo(applicant).fireTransition('init')

    # Assign global applicant role for new applicant (alternative way)
    #account = IUserAccount(applicant)
    #account.roles = ['waeup.Applicant']

    return

@grok.subscribe(IApplicant, grok.IObjectRemovedEvent)
def handle_applicant_removed(applicant, event):
    """If an applicant is removed a message is logged, passport images are
    deleted and the global role is unset.
    """
    comment = 'Application record removed'
    target = applicant.applicant_id
    try:
        grok.getSite()['applicants'].logger.info('%s - %s' % (
            target, comment))
    except KeyError:
        # If we delete an entire university instance there won't be
        # an applicants subcontainer
        return
    # Remove any passport image.
    file_store = getUtility(IExtFileStore)
    file_store.deleteFileByContext(applicant)
    # Remove all other files too
    filenames = getUtility(IApplicantsUtils).ADDITIONAL_FILES
    for filename in filenames:
        file_store.deleteFileByContext(applicant, attr=filename[1])
    # Remove global role
    role_manager = IPrincipalRoleManager(grok.getSite())
    role_manager.unsetRoleForPrincipal(
        'waeup.Applicant', applicant.applicant_id)
    return
