## $Id: mandate.py 16550 2021-07-14 06:40:53Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
These are the mandates.
"""
import grok
import hashlib
import os
from urllib import urlencode
from datetime import datetime, timedelta
from grok import index
from waeup.kofa.interfaces import IUserAccount
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.mandates.interfaces import IMandate

class Mandate(grok.Model):
    """This is a mandate.
    """
    grok.implements(IMandate)
    grok.provides(IMandate)
    grok.baseclass()

    REDIRECT_WITH_MANDATE_ID = False

    def __init__(self, days=1, mandate_id=None):
        super(Mandate, self).__init__()
        self.creation_date = datetime.utcnow() # offset-naive datetime
        delta = timedelta(days=days)
        self.expires = datetime.utcnow() + delta
        if mandate_id is None:
            mandate_id = os.urandom(20)
            mandate_id = hashlib.md5(mandate_id).hexdigest()
        self.mandate_id = mandate_id
        self.params = {}
        return

    def execute(self):
        return _('Nothing to do.')

class PasswordMandate(Mandate):
    """This is a mandate which can set a password.
    """

    def _setPassword(self):
        user = self.params.get('user', None)
        pwd = self.params.get('password', None)
        if not None in (user, pwd):
            try:
                IUserAccount(user).setPassword(pwd)
                return True
            except:
                return False
        return False

    def execute(self):
        msg = _('Wrong mandate parameters.')
        redirect_path = ''
        if self.expires < datetime.utcnow():
            msg = _('Mandate expired.')
        elif self._setPassword():
            msg = _('Password has been successfully set. '
                    'Login with your new password.')
            username = IUserAccount(self.params['user']).name
            password = self.params['password']
            grok.getSite().logger.info(
                'PasswordMandate used: %s ' % username)
            args = {'login':username, 'password':password}
            redirect_path = '/login?%s' % urlencode(args)
        del self.__parent__[self.mandate_id]
        return msg, redirect_path

class ParentsPasswordMandate(Mandate):

    def _setPassword(self):
        student = self.params.get('student', None)
        pwd = self.params.get('password', None)
        if not None in (student, pwd):
            try:
                student.setParentsPassword(pwd)
                return True
            except:
                return False
        return False

    def execute(self):
        msg = _('Wrong mandate parameters.')
        redirect_path = ''
        if self.expires < datetime.utcnow():
            msg = _('Mandate expired.')
        elif self._setPassword():
            msg = _('Parents password has been successfully set. '
                    'Login with your new parents password.')
            grok.getSite().logger.info(
                'ParentsPasswordMandate used: %s '
                % self.params['student'].student_id)
            redirect_path = '/login'
        del self.__parent__[self.mandate_id]
        return msg, redirect_path

class RefereeReportMandate(Mandate):
    """This is a mandate which can unlock a `RefereeReportAddFormPage`.
    The mandate is not automatically deleted.
    """

    REDIRECT_WITH_MANDATE_ID = True

    def execute(self):
        if self.expires < datetime.utcnow():
            return _('Mandate expired.'), ''
        redirect_path = self.params.get('redirect_path', None)
        name = self.params.get('name', None)
        email = self.params.get('email', None)
        if None in (redirect_path, name, email):
            return _('Wrong mandate parameters.'), ''
        return None, redirect_path
