## $Id: dynamicroles.py 15968 2020-01-30 22:47:56Z henrik $
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
"""Security policy components for students.

Students need special security policy treatment, as officers with
local roles for departments and faculties might have additional
permissions (local roles on depts/faculties) here.
"""
import grok
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.principalpermission import (
    AnnotationPrincipalPermissionManager,)
from zope.securitypolicy.principalrole import AnnotationPrincipalRoleManager
from waeup.kofa.students.interfaces import IStudent

class StudentPrincipalRoleManager(AnnotationPrincipalRoleManager,
                                    grok.Adapter):
    grok.provides(IPrincipalRoleManager)
    grok.context(IStudent)

    #: The attribute name to lookup for additional roles
    extra_attrib = 'certificate'
    subcontainer = 'studycourse'

    # Role name mapping:
    # role name to look for in `extra_attrib` and parents
    # to
    # role to add in case this role was found
    rolename_mapping = {
        'waeup.local.ClearanceOfficer': 'waeup.StudentsClearanceOfficer',
        'waeup.local.LocalStudentsManager': 'waeup.StudentsManager',
        'waeup.local.LocalWorkflowManager': 'waeup.WorkflowManager',
        'waeup.local.TranscriptOfficer': 'waeup.TranscriptOfficer',
        'waeup.local.TranscriptSignee': 'waeup.TranscriptSignee',
        'waeup.local.ReportsOfficer': 'waeup.ReportsOfficer',
        }

    def getRolesForPrincipal(self, principal_id):
        """Get roles for principal with id `principal_id`.

        See waeup.kofa.applicants.dynamicroles.ApplicantPrincipalRoleManager
        for further information.
        """
        apr_manager = AnnotationPrincipalRoleManager(self._context)
        result = apr_manager.getRolesForPrincipal(principal_id)
        if result != []:
            # If there are local roles defined here, no additional
            # lookup is done.
            return result
        # The principal has no local roles yet. Let's lookup the
        # connected course, dept, etc.
        if self.subcontainer:
            obj = getattr(
                self._context[self.subcontainer], self.extra_attrib, None)
            current_level = getattr(
                self._context[self.subcontainer], 'current_level', 0)
        else:
            obj = getattr(self._context, self.extra_attrib, None)
            current_level = 0
        # Lookup local roles for connected certificate and all parent
        # objects. This way we fake 'role inheritance'.
        while obj is not None:
            extra_roles = IPrincipalRoleManager(obj).getRolesForPrincipal(
                principal_id)
            for role_id, setting in extra_roles:
                if 'CourseAdviser' in role_id:
                    # Found a Course Adviser role in external attribute or parent
                    # thereof. We need a special treatment for Course Advisers.
                    if current_level and str(100*(current_level/100)) in role_id:
                        # Grant additional role, which allows to validate or reject
                        # course lists, only if external role corresponds
                        # with current_level of student.
                        result.append(
                            ('waeup.StudentsCourseAdviser', setting))
                    else:
                        # Otherwise grant at least view permissions.
                        result.append(
                            ('waeup.StudentsOfficer', setting))
                elif 'UGClearanceOfficer' in role_id:
                    if not self._context.is_postgrad:
                        result.append(
                            ('waeup.StudentsClearanceOfficer', setting))
                    else:
                        # Otherwise grant at least view permissions.
                        result.append(
                            ('waeup.StudentsOfficer', setting))
                elif 'PGClearanceOfficer' in role_id:
                    if self._context.is_postgrad:
                        result.append(
                            ('waeup.StudentsClearanceOfficer', setting))
                    else:
                        # Otherwise grant at least view permissions.
                        result.append(
                            ('waeup.StudentsOfficer', setting))
                elif role_id in self.rolename_mapping.keys():
                    # Grant additional role
                    # permissions (allow, deny or unset)
                    # according to the rolename mapping above.
                    result.append(
                        (self.rolename_mapping[role_id], setting))
                    # Local roles have been found, no need to climb up further.
                    obj = None
            obj = getattr(obj, '__parent__', None)
        return result
