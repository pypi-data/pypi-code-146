## $Id: webservices.py 12110 2014-12-02 06:43:10Z henrik $
##
## Copyright (C) 2013 Uli Fouquet & Henrik Bettermann
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
import grok
from hurry.query.query import Query
from hurry.query import Eq
from zope.component import getUtility
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from waeup.kofa.interfaces import IUniversity


class ApplicantsXMLRPC(grok.XMLRPC):
    """Applicant related XMLRPC webservices.

    Please note, that XMLRPC does not support real keyword arguments
    but positional arguments only.
    """
    grok.context(IUniversity)

    @grok.require('waeup.xmlrpc')
    def check_applicant_credentials(self, username, password):
        """Returns applicant data if username and password are valid,
        None else.

        We only query the applicants authenticator plugin in order not
        to mix up with other credentials (admins, staff, etc.).

        All additional checks performed by usual applicant
        authentication apply.

        This method can be used by CAS to authentify applicants for
        external systems like moodle.
        """
        auth = getUtility(IAuthenticatorPlugin, name='applicants')
        creds = dict(login=username, password=password)
        principal = auth.authenticateCredentials(creds)
        if principal is None:
            return None
        return dict(email=principal.email, id=principal.id,
                    type=principal.user_type,
                    description=principal.description)

    @grok.require('waeup.xmlrpc')
    def get_applicant_moodle_data(self, identifier=None):
        """Returns applicant data to update user data and enroll user
        in Moodle courses.

        """
        results = Query().searchResults(
            Eq(('applicants_catalog', 'applicant_id'), identifier))
        if not results:
            return None
        applicant = list(results)[0]
        return dict(email=applicant.email,
                    firstname=applicant.firstname,
                    lastname=applicant.lastname,
                    )