## $Id: permissions.py 12438 2015-01-11 08:27:37Z henrik $
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

# Permissions

class ViewDocuments(grok.Permission):
    grok.name('waeup.viewDocuments')


class ManageDocuments(grok.Permission):
    grok.name('waeup.manageDocuments')


# Local Roles

class DocumentManager(grok.Role):
    grok.name('waeup.local.DocumentManager')
    grok.title(u'Document Manager')
    grok.permissions('waeup.manageDocuments',
                     'waeup.viewDocuments',
                     'waeup.exportData')


# Site Roles
class DocumentsOfficer(grok.Role):
    grok.name('waeup.DocumentsOfficer')
    grok.title(u'Documents Officer (view only)')
    grok.permissions('waeup.viewDocuments')


class DocumentsManager(grok.Role):
    grok.name('waeup.DocumentsManager')
    grok.title(u'Documents Manager')
    grok.permissions('waeup.viewDocuments',
                     'waeup.manageDocuments')