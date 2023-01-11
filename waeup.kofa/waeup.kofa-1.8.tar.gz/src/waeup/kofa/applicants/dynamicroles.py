## $Id: dynamicroles.py 10226 2013-05-24 17:54:10Z henrik $
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
"""Security policy components for applicants.

Applicants need special security policy treatment, as officers with
local roles for departments and faculties might have additional
permissions (local roles on depts/faculties) here.
"""
import grok
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.principalrole import AnnotationPrincipalRoleManager
from waeup.kofa.applicants.interfaces import IApplicant

# All components in here have the same context: Applicant instances
grok.context(IApplicant)

class ApplicantPrincipalRoleManager(AnnotationPrincipalRoleManager,
                                    grok.Adapter):
    grok.provides(IPrincipalRoleManager)

    #: The attribute name to lookup for additional roles
    extra_attrib = 'course1'

    # Role name mapping:
    # role name to look for in `extra_attrib` and parents
    # to
    # role to add in case this role was found
    rolename_mapping = {
        'waeup.local.ApplicationsManager':'waeup.ApplicationsManager',
        }

    def getRolesForPrincipal(self, principal_id):
        """Get roles for principal with id `principal_id`.

        Different to the default implementation, this method also
        takes into account local roles set on any department connected
        to the context student.

        If the given principal has at least one of the
        `external_rolenames` roles granted for the external object, it
        additionally gets `additional_rolename` role for the context
        student.

        For the additional roles the `extra_attrib` and all its parent
        objects are looked up, because 'role inheritance' does not
        work on that basic level of permission handling.

        Some advantages of this approach:

        - we don't have to store extra local roles for clearance
          officers in ZODB for each student

        - when local roles on a department change, we don't have to
          update thousands of students; the local role is assigned
          dynamically.

        Disadvantage:

        - More expensive role lookups when a clearance officer wants
          to see an student form.

        This implementation is designed to be usable also for other
        contexts than students. You can inherit from it and set
        different role names to lookup/set easily via the static class
        attributes.
        """
        apr_manager = AnnotationPrincipalRoleManager(self._context)
        result = apr_manager.getRolesForPrincipal(principal_id)
        if result != []:
            # If there are local roles defined here, no additional
            # lookup is done.
            return result
        # The principal has no local roles yet. Let's lookup the
        # connected course, dept, etc.
        obj = getattr(self._context, self.extra_attrib, None)
        # Lookup local roles for connected course and all parent
        # objects. This way we fake 'role inheritance'.
        while obj is not None:
            extra_roles = IPrincipalRoleManager(obj).getRolesForPrincipal(
                principal_id)
            for role_id, setting in extra_roles:
                if role_id in self.rolename_mapping.keys():
                    # Grant additional role
                    # permissions (allow, deny or unset)
                    # according to the rolename mapping above.
                    result.append(
                        (self.rolename_mapping[role_id], setting))
                    return result
            obj = getattr(obj, '__parent__', None)
        return result
