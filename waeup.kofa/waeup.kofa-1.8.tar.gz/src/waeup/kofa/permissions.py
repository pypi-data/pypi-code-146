# $Id: permissions.py 16529 2021-07-07 06:51:05Z henrik $
#
# Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
import grok
from zope.component import getUtilitiesFor
from zope.interface import Interface
from zope.securitypolicy.interfaces import IRole, IPrincipalRoleMap
from waeup.kofa.interfaces import ILocalRolesAssignable


class Public(grok.Permission):
    """The Public or everyone-can-do-this-permission is being applied
    to views/pages that are used by everyone.
    """
    grok.name('waeup.Public')


class Anonymous(grok.Permission):
    """The Anonymous permission is applied to
    views/pages which are dedicated to anonymous users only.
    Logged-in users can't access these views.
    """
    grok.name('waeup.Anonymous')


class Authenticated(grok.Permission):
    """The Authenticated permission is applied to pages
    which can only be used by logged-in users and not by anonymous users.
    """
    grok.name('waeup.Authenticated')


class ViewAcademics(grok.Permission):
    """The ViewAcademics permission is applied to all
    views of the Academic Section. Users with this permission can view but
    not edit content in the Academic Section.
    """
    grok.name('waeup.viewAcademics')


class ManageAcademics(grok.Permission):
    """The ManageAcademics permission is applied to all edit/manage
    pages in the Academic Section. Users who have this permission
    can change/edit context objects.
    """
    grok.name('waeup.manageAcademics')


class ManagePortal(grok.Permission):
    """The ManagePortal permission is used for very few pages
    (e.g. the DatacenterSettings page). Only PortalManagers have this
    permission. It is furthermore used to control delete methods of container
    pages in the Academic Section. The ManageAcademics permission,
    described above, does enable users to edit content but not to
    remove sub-containers, like faculties, departments or certificates.
    Users must have the ManagePortal permission too to remove
    entire containers.
    """
    grok.name('waeup.managePortal')


class ManageUsers(grok.Permission):
    """The ManageUsers permission is a real superuser permission
    and therefore very 'dangerous'. It allows to add, remove or edit
    user accounts. Editing a user account includes the option to assign
    or remove roles. That means that a user with this permission can lock out
    other users by either removing their account or by removing
    permissions.
    """
    grok.name('waeup.manageUsers')


class ShowStudents(grok.Permission):
    """Users with this permission do not neccessarily see the 'Students' tab
    but they can search for students at department, certificate or course
    level. If they additionally have the ExportData permission they can
    export the data as csv files.

    Bursary or Department Officers don't have the ExportData
    permission (see Roles section) and are only allowed to export bursary
    or payments overview data respectively.
    """
    grok.name('waeup.showStudents')


class ClearAllStudents(grok.Permission):
    """The ClearAllStudents permission allows to clear all students
    in a department at one sweep.
    """
    grok.name('waeup.clearAllStudents')


class EditScores(grok.Permission):
    """The EditScores permission allows to edit scores in course tickets.
    """
    grok.name('waeup.editScores')


class TriggerTransition(grok.Permission):
    """The TriggerTransition permission allows to trigger workflow transitions
    of student and document objects.
    """
    grok.name('waeup.triggerTransition')


class EditUser(grok.Permission):
    """The EditUser permission is required for editing
    single user accounts.
    """
    grok.name('waeup.editUser')


class ManageDataCenter(grok.Permission):
    """The ManageDataCenter permission allows to access all pages
    in the Data Center and to upload files. It does not automatically
    allow to process uploaded data files.
    """
    grok.name('waeup.manageDataCenter')


class ImportData(grok.Permission):
    """The ImportData permission allows to batch process (import) any kind of
    portal data except for user data. The User Data processor
    requires also the ManageUsers permission.
    """
    grok.name('waeup.importData')


class ExportData(grok.Permission):
    """The ExportData permission allows to export any kind of portal data.
    """
    grok.name('waeup.exportData')


class ExportPaymentsOverview(grok.Permission):
    """Department Officers don't have the general exportData
    permission and are only allowed to export payments overviews.
    The ExportPaymentsOverview permission is only used to filter the
    respective exporters in the ExportJobContainerJobConfig view.
    """
    grok.name('waeup.exportPaymentsOverview')


class ExportBursaryData(grok.Permission):
    """Bursary Officers don't have the general exportData
    permission and are only allowed to export bursary data.
    The ExportBursaryData permission is only used to filter the
    respective exporter in the ExportJobContainerJobConfig view.
    """
    grok.name('waeup.exportBursaryData')


class ManagePortalConfiguration(grok.Permission):
    """The ManagePortalConfiguration permission allows to
    edit global and sessional portal configuration data.
    """
    grok.name('waeup.managePortalConfiguration')


class ManageACBatches(grok.Permission):
    """The ManageACBatches permission allows to view and
    manage accesscodes.
    """
    grok.name('waeup.manageACBatches')


class PutBiometricDataPermission(grok.Permission):
    """This permission allows to upload/change biometric data.
    """
    grok.name('waeup.putBiometricData')


class GetBiometricDataPermission(grok.Permission):
    """This permission allows to read biometric data.
    """
    grok.name('waeup.getBiometricData')


# Local Roles

class ApplicationsManager(grok.Role):
    """The local ApplicationsManager role can be assigned at applicants
    container and at department level. At department level an Applications
    Manager can manage all applicants which desire to study a programme
    offered by the department (1st Choice Course of Study).

    At container level (local) Applications Managers gain permissions which
    allow to manage the container and all applicants inside the container.  At
    container level the permission set of this local role corresonds with the
    permission set of the same-named global role.
    """
    grok.name('waeup.local.ApplicationsManager')
    grok.title(u'Applications Manager')
    grok.permissions('waeup.viewAcademics',
                     'waeup.manageApplication', 'waeup.viewApplication',
                     'waeup.payApplicant')


class DepartmentOfficer(grok.Role):
    """The local DepartmentOfficer role can be assigned at faculty or
    department level. The role allows to list all student data within the
    faculty/department the local role is assigned. And it allows to export
    payment data overviews.
    """
    grok.name('waeup.local.DepartmentOfficer')
    grok.title(u'Department Officer')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportPaymentsOverview')


class DepartmentManager(grok.Role):
    """The local DepartmentManager role can be assigned at faculty or
    department level. The role allows to edit all data within this container.
    It does not automatically allow to remove sub-containers.

    Department Managers (Dean of Faculty or Head of Department respectively)
    can also list student data but not access student pages.
    """
    grok.name('waeup.local.DepartmentManager')
    grok.title(u'Department Manager')
    grok.permissions('waeup.manageAcademics',
                     'waeup.showStudents',
                     'waeup.exportData')


class ClearanceOfficer(grok.Role):
    """The local ClearanceOfficer role can be assigned at faculty or
    department level. The role allows to list or export all student
    data within the faculty/department the local role is assigned.

    Clearance Officers can furthermore clear all students or reject clearance
    of all students in their faculty/department. They get the
    StudentsClearanceOfficer role for this subset of students.
    """
    grok.name('waeup.local.ClearanceOfficer')
    grok.title(u'Clearance Officer')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData',
                     'waeup.clearAllStudents')


class LocalStudentsManager(grok.Role):
    """The local LocalStudentsManager role can be assigned at faculty or
    department level. The role allows to view all data and to view or export
    all student data within the faculty/department the local role is assigned.

    Local Students Managers can furthermore manage data of students
    in their faculty/department. They get the StudentsManager role for
    this subset of students.
    """
    grok.name('waeup.local.LocalStudentsManager')
    grok.title(u'Students Manager')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class LocalWorkflowManager(grok.Role):
    """The local LocalWorkflowManager role can be assigned at faculty level.
    The role allows to view all data and to list or export
    all student data within the faculty the local role is assigned.

    Local Workflow Managers can trigger transition of students in their
    faculty/department. They get the WorkflowManager role for
    this subset of students.
    """
    grok.name('waeup.local.LocalWorkflowManager')
    grok.title(u'Student Workflow Manager')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')

class LocalReportsOfficer(grok.Role):
    """The local ReportsOfficer role can be assigned at department level.
    The role allows to view all data and to list or export
    all student data within the department the local role is assigned.

    The LocalReportsOfficer requires the assignment of the global
    ReportsOfficer role to access the reports section. If set, it reduces
    the number of available report generators and selectable certificates.
    Local Reports Officers can create only reports for their department.
    """
    grok.name('waeup.local.ReportsOfficer')
    grok.title(u'Student Reports Officer')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')

class UGClearanceOfficer(grok.Role):
    """UG Clearance Officers are regular Clearance Officers with restricted
    dynamic permission assignment. They can only access undergraduate
    students.
    """
    grok.name('waeup.local.UGClearanceOfficer')
    grok.title(u'UG Clearance Officer')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData',
                     'waeup.clearAllStudents')


class PGClearanceOfficer(grok.Role):
    """PG Clearance Officers are regular Clearance Officers with restricted
    dynamic permission assignment. They can only access postgraduate
    students.
    """
    grok.name('waeup.local.PGClearanceOfficer')
    grok.title(u'PG Clearance Officer')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData',
                     'waeup.clearAllStudents')


class CourseAdviser100(grok.Role):
    """The local CourseAdviser100 role can be assigned at faculty,
    department or certificate level. The role allows to view all data and
    to list or export all student data within the faculty, department
    or certificate the local role is assigned.

    Local Course Advisers can validate or reject course lists of students
    in ther faculty/department/certificate at level 100.
    They get the StudentsCourseAdviser role for this subset of students.
    """
    grok.name('waeup.local.CourseAdviser100')
    grok.title(u'Course Adviser 100L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser200(grok.Role):
    """Same as CourseAdviser100 but for level 200.
    """
    grok.name('waeup.local.CourseAdviser200')
    grok.title(u'Course Adviser 200L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser300(grok.Role):
    """Same as CourseAdviser100 but for level 300.
    """
    grok.name('waeup.local.CourseAdviser300')
    grok.title(u'Course Adviser 300L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser400(grok.Role):
    """Same as CourseAdviser100 but for level 400.
    """
    grok.name('waeup.local.CourseAdviser400')
    grok.title(u'Course Adviser 400L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser500(grok.Role):
    """Same as CourseAdviser100 but for level 500.
    """
    grok.name('waeup.local.CourseAdviser500')
    grok.title(u'Course Adviser 500L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser600(grok.Role):
    """Same as CourseAdviser100 but for level 600.
    """
    grok.name('waeup.local.CourseAdviser600')
    grok.title(u'Course Adviser 600L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser700(grok.Role):
    """Same as CourseAdviser100 but for level 700.
    """
    grok.name('waeup.local.CourseAdviser700')
    grok.title(u'Course Adviser 700L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class CourseAdviser800(grok.Role):
    """Same as CourseAdviser100 but for level 800.
    """
    grok.name('waeup.local.CourseAdviser800')
    grok.title(u'Course Adviser 800L')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class LocalTranscriptOfficer(grok.Role):
    """The LocalTranscriptOfficer role can be assigned at faculty
    level. The role allows to view, to validate and to
    release student transcripts at faculty level.
    Local Transcript Officers get the TranscriptOfficer role
    for this subset of students.
    """
    grok.name('waeup.local.TranscriptOfficer')
    grok.title(u'Transcript Officer')
    grok.permissions('waeup.viewAcademics',)


class LocalTranscriptSignee(grok.Role):
    """The LocalTranscriptSignee role can be assigned at faculty
    level. The role allows to view and to sign student transcripts
    at faculty level. Local Transcript Signees  get the TranscriptSignee role
    for this subset of students.
    """
    grok.name('waeup.local.TranscriptSignee')
    grok.title(u'Transcript Signee')
    grok.permissions('waeup.viewAcademics',)


class Lecturer(grok.Role):
    """The local Lecturer role can be assigned at course level.
    The role allows to export some student
    data within the course the local role is assigned. Lecturers can't access
    student data directly but they can edit the scores in course tickets.
    """
    grok.name('waeup.local.Lecturer')
    grok.title(u'Lecturer')
    grok.permissions('waeup.editScores',
                     'waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportData')


class Owner(grok.Role):
    """Each user 'owns' her/his user object and gains permission to edit
    some of the user attributes.
    """
    grok.name('waeup.local.Owner')
    grok.title(u'Owner')
    grok.permissions('waeup.editUser')


# Site Roles
class AcademicsOfficer(grok.Role):
    """An Academics Officer can view but not edit data in the
    academic section.

    This is the default role which is automatically assigned to all
    officers of the portal. A user with this role can access all display pages
    at faculty, department, course, certificate and certificate course level.
    """
    grok.name('waeup.AcademicsOfficer')
    grok.title(u'Academics Officer (view only)')
    grok.permissions('waeup.viewAcademics')


class AcademicsManager(grok.Role):
    """An Academics Manager can view and edit all data in the
    scademic section, i.e. access all manage pages
    at faculty, department, course, certificate and certificate course level.
    """
    grok.name('waeup.AcademicsManager')
    grok.title(u'Academics Manager')
    title = u'Academics Manager'
    grok.permissions('waeup.viewAcademics',
                     'waeup.manageAcademics')


class ACManager(grok.Role):
    """This is the role for Access Code Managers.
    An AC Manager can view and manage the Accesscodes Section, see
    ManageACBatches permission above.
    """
    grok.name('waeup.ACManager')
    grok.title(u'Access Code Manager')
    grok.permissions('waeup.manageACBatches')


class DataCenterManager(grok.Role):
    """This single-permission role is dedicated to those users
    who are charged with batch processing of portal data.
    A Data Center Manager can access all pages in the Data Center,
    see ManageDataCenter permission above.
    """
    grok.name('waeup.DataCenterManager')
    grok.title(u'Datacenter Manager')
    grok.permissions('waeup.manageDataCenter')


class ImportManager(grok.Role):
    """An Import Manager is a Data Center Manager who is also allowed
    to batch process (import) data. All batch processors (importers) are
    available except for the User Processor. This processor requires the
    Users Manager role too. The ImportManager role includes the
    DataCenterManager role but not vice versa.
    """
    grok.name('waeup.ImportManager')
    grok.title(u'Import Manager')
    grok.permissions('waeup.manageDataCenter',
                     'waeup.importData')


class ExportManager(grok.Role):
    """An Export Manager is a Data Center Manager who is also allowed
    to export all kind of portal data. The ExportManager role includes the
    DataCenterManager role but not vice versa.
    """
    grok.name('waeup.ExportManager')
    grok.title(u'Export Manager')
    grok.permissions('waeup.manageDataCenter',
                     'waeup.exportData',
                     'waeup.showStudents')


class BursaryOfficer(grok.Role):
    """Bursary Officers can export bursary and payments data. They can't  
    access the Data Center but see student data export buttons in the
    Academic Section.
    """
    grok.name('waeup.BursaryOfficer')
    grok.title(u'Bursary Officer')
    grok.permissions('waeup.showStudents',
                     'waeup.viewAcademics',
                     'waeup.exportBursaryData',
                     'waeup.exportPaymentsOverview',
                     'waeup.viewApplicantsTab')


class UsersManager(grok.Role):
    """A Users Manager can add, remove or edit
    user accounts, see ManageUsers permission for further information.
    Be very careful with this role.
    """
    grok.name('waeup.UsersManager')
    grok.title(u'Users Manager')
    grok.permissions('waeup.manageUsers',
                     'waeup.editUser')


class WorkflowManager(grok.Role):
    """The Workflow Manager can trigger workflow transitions
    of student and document objects, see TriggerTransition permission
    for further information.
    """
    grok.name('waeup.WorkflowManager')
    grok.title(u'Workflow Manager')
    grok.permissions('waeup.triggerTransition')


class FingerprintReaderDeviceRole(grok.Role):
    """Fingerprint Reader Devices.

    Fingerprint readers are remote devices that can store and retrieve
    fingerprint data.
    """
    grok.name('waeup.FingerprintDevice')
    grok.title(u'Fingerprint Reader')
    grok.permissions(
        'waeup.getBiometricData',
        'waeup.putBiometricData',
    )


class PortalManager(grok.Role):
    """The PortalManager role is the maximum set of Kofa permissions
    which are needed to manage the entire portal. This set must not
    be customized. It is recommended to assign this role only
    to a few certified Kofa administrators.
    A less dangerous manager role is the CCOfficer role described below.
    For the most tasks the CCOfficer role is sufficient.
    """
    grok.name('waeup.PortalManager')
    grok.title(u'Portal Manager')
    grok.permissions('waeup.managePortal',
                     'waeup.manageUsers',
                     'waeup.viewAcademics', 'waeup.manageAcademics',
                     'waeup.manageACBatches',
                     'waeup.manageDataCenter',
                     'waeup.importData',
                     'waeup.exportData',
                     'waeup.viewTranscript',
                     'waeup.downloadTranscript',
                     'waeup.processTranscript',
                     'waeup.viewDocuments', 'waeup.manageDocuments',
                     'waeup.managePortalConfiguration',
                     'waeup.viewApplication',
                     'waeup.manageApplication', 'waeup.handleApplication',
                     'waeup.viewApplicantsTab', 'waeup.payApplicant',
                     'waeup.viewApplicationStatistics',
                     'waeup.viewStudent', 'waeup.manageStudent',
                     'waeup.clearStudent', 'waeup.payStudent',
                     'waeup.clearStudentFinancially',  # not used in base pkg
                     'waeup.uploadStudentFile', 'waeup.showStudents',
                     'waeup.clearAllStudents',
                     'waeup.createStudents',
                     'waeup.editScores',
                     'waeup.triggerTransition',
                     'waeup.validateStudent',
                     'waeup.viewStudentsContainer',
                     'waeup.handleAccommodation',
                     'waeup.viewHostels', 'waeup.manageHostels',
                     'waeup.editUser',
                     'waeup.loginAsStudent',
                     'waeup.handleReports',
                     'waeup.manageReports',
                     'waeup.manageJobs',
                     )


class CCOfficer(grok.Role):
    """The role of the Computer Center Officer is basically a copy
    of the the PortalManager role. Some 'dangerous' permissions are excluded
    by commenting them out (see source code). If officers need to gain more
    access rights than defined in this role, do not hastily switch to the
    PortalManager role but add further manager roles instead. Additional
    roles could be: UsersManager, ACManager, ImportManager, WorkflowManager
    or StudentImpersonator.

    CCOfficer is a base class which means that this role is subject to
    customization. It is not used in the ``waeup.kofa`` base package.
    """
    grok.baseclass()
    grok.name('waeup.CCOfficer')
    grok.title(u'Computer Center Officer')
    grok.permissions(
        # 'waeup.managePortal',
        # 'waeup.manageUsers',
        'waeup.viewAcademics',
        'waeup.manageAcademics',
        # 'waeup.manageACBatches',
        'waeup.manageDataCenter',
        # 'waeup.importData',
        'waeup.exportData',
        'waeup.viewTranscript',
        'waeup.downloadTranscript',
        'waeup.processTranscript',
        'waeup.viewDocuments', 'waeup.manageDocuments',
        'waeup.managePortalConfiguration', 'waeup.viewApplication',
        'waeup.manageApplication', 'waeup.handleApplication',
        'waeup.viewApplicantsTab', 'waeup.payApplicant',
        'waeup.viewApplicationStatistics',
        'waeup.viewStudent', 'waeup.manageStudent',
        'waeup.clearStudent', 'waeup.payStudent',
        'waeup.uploadStudentFile', 'waeup.showStudents',
        'waeup.clearAllStudents',
        # 'waeup.createStudents',
        'waeup.editScores',
        # 'waeup.triggerTransition',
        'waeup.validateStudent',
        'waeup.viewStudentsContainer',
        'waeup.handleAccommodation',
        'waeup.viewHostels', 'waeup.manageHostels',
        # 'waeup.editUser',
        # 'waeup.loginAsStudent',
        'waeup.handleReports',
        'waeup.manageReports',
        # 'waeup.manageJobs',
        )


def get_all_roles():
    """Return a list of tuples ``<ROLE-NAME>, <ROLE>``.
    """
    return getUtilitiesFor(IRole)


def get_waeup_roles(also_local=False):
    """Get all Kofa roles.

    Kofa roles are ordinary roles whose id by convention starts with
    a ``waeup.`` prefix.

    If `also_local` is ``True`` (``False`` by default), also local
    roles are returned. Local Kofa roles are such whose id starts
    with ``waeup.local.`` prefix (this is also a convention).

    Returns a generator of the found roles.
    """
    for name, item in get_all_roles():
        if not name.startswith('waeup.'):
            # Ignore non-Kofa roles...
            continue
        if not also_local and name.startswith('waeup.local.'):
            # Ignore local roles...
            continue
        yield item


def get_waeup_role_names():
    """Get the ids of all Kofa roles.

    See :func:`get_waeup_roles` for what a 'KofaRole' is.

    This function returns a sorted list of Kofa role names.
    """
    return sorted([x.id for x in get_waeup_roles()])


class LocalRolesAssignable(grok.Adapter):
    """Default implementation for `ILocalRolesAssignable`.

    This adapter returns a list for dictionaries for objects for which
    we want to know the roles assignable to them locally.

    The returned dicts contain a ``name`` and a ``title`` entry which
    give a role (``name``) and a description, for which kind of users
    the permission is meant to be used (``title``).

    Having this adapter registered we make sure, that for each normal
    object we get a valid `ILocalRolesAssignable` adapter.

    Objects that want to offer certain local roles, can do so by
    setting a (preferably class-) attribute to a list of role ids.

    You can also define different adapters for different contexts to
    have different role lookup mechanisms become available. But in
    normal cases it should be sufficient to use this basic adapter.
    """
    grok.context(Interface)
    grok.provides(ILocalRolesAssignable)

    _roles = []

    def __init__(self, context):
        self.context = context
        role_ids = getattr(context, 'local_roles', self._roles)
        self._roles = [(name, role) for name, role in get_all_roles()
                       if name in role_ids]
        return

    def __call__(self):
        """Get a list of dictionaries containing ``names`` (the roles to
        assign) and ``titles`` (some description of the type of user
        to assign each role to).
        """
        list_of_dict = [dict(
                name=name,
                title=role.title,
                description=role.description)
                for name, role in self._roles]
        return sorted(list_of_dict, key=lambda x: x['name'])


def get_users_with_local_roles(context):
    """Get a list of dicts representing the local roles set for `context`.

    Each dict returns `user_name`, `user_title`, `local_role`,
    `local_role_title`, and `setting` for each entry in the local
    roles map of the `context` object.
    """
    try:
        role_map = IPrincipalRoleMap(context)
    except TypeError:
        # no map no roles.
        raise StopIteration
    for local_role, user_name, setting in role_map.getPrincipalsAndRoles():
        user = grok.getSite()['users'].get(user_name, None)
        user_title = getattr(user, 'title', user_name)
        public_name = getattr(user, 'public_name', None)
        if not public_name:
            public_name = user_title
        local_role_title = getattr(
            dict(get_all_roles()).get(local_role, None), 'title', None)
        yield dict(user=user,
                   user_name=user_name,
                   user_title=user_title,
                   public_name=public_name,
                   local_role=local_role,
                   local_role_title=local_role_title,
                   setting=setting,
                   )


def get_users_with_role(role, context):
    """Get a list of dicts representing the usres who have been granted
    a role for `context`.
    """
    try:
        role_map = IPrincipalRoleMap(context)
    except TypeError:
        # no map no roles.
        raise StopIteration
    for user_name, setting in role_map.getPrincipalsForRole(role):
        user = grok.getSite()['users'].get(user_name, None)
        user_title = getattr(user, 'title', user_name)
        user_email = getattr(user, 'email', None)
        yield dict(user_name=user_name,
                   user_title=user_title,
                   user_email=user_email,
                   setting=setting)
