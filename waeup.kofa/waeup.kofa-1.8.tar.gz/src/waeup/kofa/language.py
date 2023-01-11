## $Id: language.py 7832 2012-03-10 04:29:35Z uli $
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
"""Handle language as requested by users.
"""
import grokcore.component
from zope.component import getUtility
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.session.interfaces import ISession
from zope.i18n.interfaces import IUserPreferredLanguages
from waeup.kofa.configuration import ConfigurationContainer
from waeup.kofa.interfaces import IKofaUtils

class KofaLanguage(grokcore.component.Adapter):
    """Set preferred languages"""
    grokcore.component.context(IBrowserRequest)
    grokcore.component.implements(IUserPreferredLanguages)

    def getPreferredLanguages(self):
        # This an adapter for the request, so self.context is the request.
        request = self.context

        # Extract the preferred language from a cookie:
        lang = request.cookies.get('kofa.language', None)
        if lang is None:
            lang = getUtility(IKofaUtils).PORTAL_LANGUAGE
            request.response.setCookie('kofa.language', lang, path='/')

        # According to IUserPreferredLanguages, we must return a list.
        return [lang]
