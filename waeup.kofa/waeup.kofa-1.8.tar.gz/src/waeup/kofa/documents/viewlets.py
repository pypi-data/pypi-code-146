## $Id: viewlets.py 16097 2020-05-25 10:10:18Z henrik $
##
## Copyright (C) 2014 Uli Fouquet & Henrik Bettermann
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
"""Viewlet components for documents offered for download by the company.
"""

import grok
from waeup.kofa.browser.viewlets import (
    PrimaryNavTab, ManageActionButton, AddActionButton)
from waeup.kofa.interfaces import IKofaObject
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.browser.viewlets import PrimaryNavTab

from waeup.kofa.documents.interfaces import (
    IDocumentsContainer, IPublicDocument)
from waeup.kofa.documents.browser import (
    DocumentsContainerManageFormPage, DocumentsContainerPage,
    DocumentManageFormPage, DocumentDisplayFormPage)


grok.context(IKofaObject)  # Make IKofaObject the default context
grok.templatedir('browser_templates')


class DocumentsTab(PrimaryNavTab):
    """Documents tab in primary navigation.
    """

    grok.context(IKofaObject)
    grok.order(10)
    grok.require('waeup.viewDocuments')
    grok.name('documentstab')

    pnav = 6
    tab_title = _(u'Documents')

    @property
    def link_target(self):
        return self.view.application_url('documents')

class DocumentsContainerManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IDocumentsContainer)
    grok.view(DocumentsContainerPage)
    grok.require('waeup.manageDocuments')
    text = _('Manage')
    target = 'manage'


class DocumentViewActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IPublicDocument)
    grok.view(DocumentManageFormPage)
    grok.require('waeup.manageDocuments')
    text = _('View')
    target = 'index'
    icon = 'actionicon_view.png'


class DocumentManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IPublicDocument)
    grok.view(DocumentDisplayFormPage)
    grok.require('waeup.manageDocuments')
    text = _('Manage')
    target = 'manage'


class DocumentTrigTransActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IPublicDocument)
    grok.view(DocumentDisplayFormPage)
    grok.require('waeup.manageDocuments')
    icon = 'actionicon_trigtrans.png'
    text = _(u'Transition')
    target = 'trigtrans'


