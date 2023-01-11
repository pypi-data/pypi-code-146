## $Id: permissions.py 15085 2018-07-11 04:28:32Z henrik $
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
Local permissions for applicants/applications.
"""
import grok

# Application permissions

class HandleApplication(grok.Permission):
    """The HandleApplication permission is reserved for applicants.
    Applicants 'handle' their data. Officers 'manage' the data.
    """
    grok.name('waeup.handleApplication')

class ViewApplication(grok.Permission):
    """The ViewApplication permission allows to view application records.
    """
    grok.name('waeup.viewApplication')

class ViewApplicationsTab(grok.Permission):
    grok.name('waeup.viewApplicantsTab')

class ViewMyApplicationDataTab(grok.Permission):
    grok.name('waeup.viewMyApplicationDataTab')

class ManageApplication(grok.Permission):
    """The ManageApplication permission allows to edit the data. This
    permission is reserved for officers and portal managers.
    """
    grok.name('waeup.manageApplication')

class ViewApplicationStatistics(grok.Permission):
    """The ViewApplicationStatistics permission allows to perform statistical
    evaluations.
    """
    grok.name('waeup.viewApplicationStatistics')

class PayApplicant(grok.Permission):
    """The PayApplicant permission allows to add an online payment ticket.
    """
    grok.name('waeup.payApplicant')

class CreateStudents(grok.Permission):
    """The CreateStudents permission allows to create a bunch student
    records from application records.
    """
    grok.name('waeup.createStudents')

# Local role

class ApplicationOwner(grok.Role):
    """An applicant 'owns' her/his application record and
    gains permissions to handle the record, upload a passport picture or
    add payment tickets.
    """
    grok.name('waeup.local.ApplicationOwner')
    grok.title(u'Application Owner')
    grok.permissions('waeup.handleApplication',
                     'waeup.viewApplication',
                     'waeup.payApplicant')

# Site roles

class ApplicantRole(grok.Role):
    """This role is dedicated to applicants only. It defines the permissions
    an applicant gains portal-wide.
    """
    grok.name('waeup.Applicant')
    grok.title(u'Applicant (do not assign)')
    grok.permissions('waeup.viewAcademics', 'waeup.viewMyApplicationDataTab',
                     'waeup.Authenticated')

class ApplicationsOfficer(grok.Role):
    """The Applications Officer is allowed to view all application records.
    """
    grok.name('waeup.ApplicationsOfficer')
    grok.title(u'Applications Officer (view only)')
    grok.permissions('waeup.viewApplication', 'waeup.viewApplicantsTab')

class ApplicationsManager(grok.Role):
    """The Applications Manager is allowed to edit all application records.
    The role also allows to add payment tickets and view statistics.
    """
    grok.name('waeup.ApplicationsManager')
    grok.title(u'Applications Manager')
    grok.permissions('waeup.manageApplication', 'waeup.viewApplication',
                     'waeup.viewApplicantsTab', 'waeup.payApplicant',
                     'waeup.viewApplicationStatistics')

class StudentsCreator(grok.Role):
    """The Students Creator is allowed to create a bunch of student 
    records from application records.
    """
    grok.name('waeup.StudentsCreator')
    grok.title(u'Students Creator')
    grok.permissions('waeup.viewApplication',
                     'waeup.viewApplicantsTab',
                     'waeup.createStudents')
