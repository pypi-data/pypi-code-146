## $Id: objecthistory.py 11068 2014-02-11 07:34:30Z henrik $
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
import grok
from datetime import datetime
from persistent.list import PersistentList
from zope.component import getUtility
from zope.i18n import translate
from zope.annotation.interfaces import IAnnotations
from waeup.kofa.interfaces import IObjectHistory, IKofaObject, IKofaUtils
from waeup.kofa.utils.helpers import get_current_principal, now

from waeup.kofa.interfaces import MessageFactory as _

class ObjectHistory(grok.Adapter):
    """A history for objects.

    For any object implementing `IKofaObject` which is annotatable,
    we provide histories. A history for such an object can be obtained
    by adapting it to `IObjectHistory`.
    """
    grok.context(IKofaObject)
    grok.implements(IObjectHistory)

    history_key = 'waeup.history'

    def __init__(self, context):
        from zope.security.proxy import removeSecurityProxy
        self.context = removeSecurityProxy(context)
        self._annotations = IAnnotations(self.context)

    def _getMessages(self):
        return self._annotations.get(self.history_key, PersistentList())

    @property
    def messages(self):
        """Get all messages as a persistent list of strings.
        """
        return self._getMessages()

    def addMessage(self, msg, user=None):
        """Add the message (history entry) in msg.

        Any message will be stored with a timestamp and the current
        user (principal) if user parameter is None.
        """
        msgs = self._getMessages()
        tz = getUtility(IKofaUtils).tzinfo
        timestamp = now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        msg = translate(msg,'waeup.kofa',target_language=portal_language)
        by = translate(_('by'),'waeup.kofa',target_language=portal_language)
        if user == None:
            user = get_current_principal()
            if user is None:
                usertitle = 'system'
            elif user.id == 'zope.anybody':
                usertitle = 'Anonymous'
            else:
                usertitle = getattr(user, 'public_name', None)
                if not usertitle:
                    usertitle = user.title
            msg = u'%s - %s %s %s' % (timestamp, msg, by, usertitle)
        elif user == 'undisclosed':
            msg = u'%s - %s' % (timestamp, msg)
        else:
            msg = u'%s - %s %s %s' % (timestamp, msg, by, user)
        msgs.append(msg)
        self._annotations[self.history_key] = msgs
        return

    def modifyMessages(self, old, new):
        """Replaces history messages.

        Substring 'old' will be replaced by 'new' in all
        messages.
        """
        old_msgs = self._getMessages()
        new_msgs = PersistentList()
        for msg in old_msgs:
            new_msg = msg.replace(old, new)
            new_msgs.append(new_msg)
        self._annotations[self.history_key] = new_msgs
        return

    def removeMessage(self, number):
        """Removes a single history message.

        """
        msgs = self._getMessages()
        if not isinstance(number, int):
            return False, 'Not a number'
        try:
            line = msgs[number]
        except IndexError:
            return False, 'Number out of range'
        msgs.pop(number)
        self._annotations[self.history_key] = msgs
        return True, line