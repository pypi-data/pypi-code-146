## $Id: browser.py 16099 2020-05-25 10:18:39Z henrik $
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
"""UI components for documents offered for download by the company.
"""

import sys
import grok
from urllib import urlencode
from datetime import datetime
from hurry.workflow.interfaces import (
    IWorkflowInfo, IWorkflowState, InvalidTransitionError)
from zope.event import notify
from zope.i18n import translate
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility, createObject
from zope.schema.interfaces import ConstraintNotSatisfied, RequiredMissing
from zope.formlib.textwidgets import BytesDisplayWidget
from zope.security import checkPermission
from waeup.kofa.utils.helpers import html2dict, rest2dict
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.interfaces import (
    IContactForm, IKofaObject, IKofaUtils, DOCLINK)
from waeup.kofa.browser.layout import (
    KofaPage, KofaEditFormPage, KofaAddFormPage, KofaDisplayFormPage,
    NullValidator, jsaction, action, UtilityView)
from waeup.kofa.widgets.datewidget import (
    FriendlyDateWidget, FriendlyDateDisplayWidget,
    FriendlyDatetimeDisplayWidget)
from waeup.kofa.browser.breadcrumbs import Breadcrumb
from waeup.kofa.browser.pages import (
    delSubobjects, add_local_role, del_local_roles, msave,
    LocalRoleAssignmentUtilityView)

from waeup.kofa.documents.interfaces import (
    IDocumentsContainer, IPublicDocument,
    IHTMLDocument, IRESTDocument, IDocumentsUtils)
from waeup.kofa.documents.workflow import PUBLISHED

grok.context(IKofaObject) # Make IKofaObject the default context
grok.templatedir('browser_templates')


class DocumentsBreadcrumb(Breadcrumb):
    """A breadcrumb for the customers container.
    """
    grok.context(IDocumentsContainer)
    title = _('Documents')


class DocumentBreadcrumb(Breadcrumb):
    """A breadcrumb for the customer container.
    """
    grok.context(IPublicDocument)

    def title(self):
        return self.context.title


class DocumentsContainerPage(KofaDisplayFormPage):
    """The standard view for document containers.
    """
    grok.context(IDocumentsContainer)
    grok.name('index')
    grok.require('waeup.viewDocuments')
    grok.template('containerpage')
    pnav = 6
    label = _('Documents')
    doclink = DOCLINK + '/documents.html'


class DocumentsContainerManageFormPage(KofaEditFormPage):
    """The manage page for customer containers.
    """
    grok.context(IDocumentsContainer)
    grok.name('manage')
    grok.require('waeup.manageDocuments')
    grok.template('containermanagepage')
    pnav = 6
    label = _('Manage document section')

    @action(_('Add document'), validator=NullValidator, style='primary')
    def addSubunit(self, **data):
        self.redirect(self.url(self.context, 'adddoc'))
        return

    @jsaction(_('Remove selected documents'))
    def delDocuments(self, **data):
        delSubobjects(self, redirect='manage', tab='2')
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return


class DocumentAddFormPage(KofaAddFormPage):
    """Add-form to add a customer.
    """
    grok.context(IDocumentsContainer)
    grok.require('waeup.manageDocuments')
    grok.name('adddoc')
    grok.template('documentaddform')
    label = _('Add document')
    pnav = 6

    form_fields = grok.AutoFields(IPublicDocument)

    @property
    def selectable_doctypes(self):
        doctypes = getUtility(IDocumentsUtils).SELECTABLE_DOCTYPES_DICT
        return sorted(doctypes.items())

    @action(_('Add document'), style='primary')
    def createDocument(self, **data):
        form = self.request.form
        doctype = form.get('doctype', None)
        # Here we can create various instances of PublicDocument derived
        # classes depending on the doctype parameter given in form.
        document = createObject('waeup.%s' % doctype)
        self.applyData(document, **data)
        try:
            self.context.addDocument(document)
        except KeyError:
            self.flash(_('The id chosen already exists.'),
                       type='danger')
            return
        doctype = getUtility(IDocumentsUtils).SELECTABLE_DOCTYPES_DICT[doctype]
        self.flash(_('${a} added.', mapping = {'a': doctype}))
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        self.context.__parent__.logger.info(
            '%s - added: %s %s' % (ob_class, doctype, document.document_id))
        self.redirect(self.url(self.context) +
            '/%s/manage' % document.document_id)
        return

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))


class DocumentDisplayFormPage(KofaDisplayFormPage):
    """ Page to display document data
    """
    grok.context(IPublicDocument)
    grok.name('index')
    grok.require('waeup.viewDocuments')
    grok.template('documentpage')
    pnav = 6
    doclink = DOCLINK + '/documents.html'

    @property
    def form_fields(self):
        return grok.AutoFields(self.context.form_fields_interface)

    @property
    def label(self):
        return self.context.title


class HTMLDocumentDisplayFormPage(DocumentDisplayFormPage):
    """ Page to display html document data
    """
    grok.context(IHTMLDocument)
    grok.template('htmldocumentpage')

    @property
    def form_fields(self):
        return grok.AutoFields(self.context.form_fields_interface).omit(
            'html_dict', 'html_multilingual')

    @property
    def html(self):
        lang = self.request.cookies.get('kofa.language')
        html = self.context.html_dict.get(lang,'')
        if html =='':
            portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
            html = self.context.html_dict.get(portal_language,'')
        return html


class HTMLDocumentDisplayContentPage(KofaPage):
    """ Page to display the html content of document
    """
    grok.context(IHTMLDocument)
    grok.name('display')
    grok.template('htmldisplaypage')
    grok.require('waeup.Public')
    pnav = 6

    @property
    def label(self):
        return self.context.title

    def update(self):
        if self.context.state != PUBLISHED:
            self.flash(_('The document requested has not yet been published.'),
                type="warning")
            self.redirect(self.application_url())
        super(HTMLDocumentDisplayContentPage, self).update()
        return

    @property
    def content(self):
        lang = self.request.cookies.get('kofa.language')
        html = self.context.html_dict.get(lang,'')
        if html =='':
            portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
            html = self.context.html_dict.get(portal_language,'')
        return html


class RESTDocumentDisplayFormPage(HTMLDocumentDisplayFormPage):
    """ Page to display html document data
    """
    grok.context(IRESTDocument)

    @property
    def form_fields(self):
        return grok.AutoFields(self.context.form_fields_interface).omit(
            'html_dict', 'rest_multilingual')


class RESTDocumentDisplayContentPage(HTMLDocumentDisplayContentPage):
    """ Page to display the html content of document
    """
    grok.context(IRESTDocument)

    label = None


class DocumentManageFormPage(KofaEditFormPage,
                            LocalRoleAssignmentUtilityView):
    """ View to manage document data
    """
    grok.context(IPublicDocument)
    grok.name('manage')
    grok.require('waeup.manageDocuments')
    grok.template('documentmanagepage')
    pnav = 6

    taboneactions = [_('Save'),_('Cancel')]
    tabthreeactions1 = [_('Remove selected local roles')]
    tabthreeactions2 = [_('Add local role')]

    deletion_warning = _('Are you sure?')

    @property
    def form_fields(self):
        return grok.AutoFields(
            self.context.form_fields_interface).omit('document_id')

    def label(self):
        return _('Manage document ') + self.context.document_id

    @action(_('Save'), style='primary')
    def save(self, **data):
        return msave(self, **data)

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return

    @action(_('Add local role'), validator=NullValidator)
    def addLocalRole(self, **data):
        return add_local_role(self,3,**data)

    @action(_('Remove selected local roles'))
    def delLocalRoles(self, **data):
        return del_local_roles(self,3,**data)


class HTMLDocumentManageFormPage(DocumentManageFormPage):
    """ View to manage htmldocument data
    """
    grok.context(IHTMLDocument)
    grok.template('htmldocumentmanagepage')

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        html_multilingual = getattr(self.context, 'html_multilingual', None)
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.context.html_dict = html2dict(html_multilingual, portal_language)
        return

    # Actions must be repeated. They are not inherited from the parent class.

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return

    @action(_('Add local role'), validator=NullValidator)
    def addLocalRole(self, **data):
        return add_local_role(self,3,**data)

    @action(_('Remove selected local roles'))
    def delLocalRoles(self, **data):
        return del_local_roles(self,3,**data)

class RESTDocumentManageFormPage(DocumentManageFormPage):
    """ View to manage restdocument data
    """
    grok.context(IRESTDocument)
    grok.template('htmldocumentmanagepage')

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        html_multilingual = getattr(self.context, 'rest_multilingual', None)
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        self.context.html_dict = rest2dict(html_multilingual, portal_language)
        return

    # Actions must be repeated. They are not inherited from the parent class.

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, **data):
        self.redirect(self.url(self.context))
        return

    @action(_('Add local role'), validator=NullValidator)
    def addLocalRole(self, **data):
        return add_local_role(self,3,**data)

    @action(_('Remove selected local roles'))
    def delLocalRoles(self, **data):
        return del_local_roles(self,3,**data)

class DocumentTriggerTransitionFormPage(KofaEditFormPage):
    """ View to trigger public document transitions
    """
    grok.context(IPublicDocument)
    grok.name('trigtrans')
    grok.require('waeup.triggerTransition')
    grok.template('trigtrans')
    label = _('Trigger document transition')
    pnav = 6

    def update(self):
        return super(KofaEditFormPage, self).update()

    def getTransitions(self):
        """Return a list of dicts of allowed transition ids and titles.

        Each list entry provides keys ``name`` and ``title`` for
        internal name and (human readable) title of a single
        transition.
        """
        wf_info = IWorkflowInfo(self.context)
        allowed_transitions = [t for t in wf_info.getManualTransitions()]
        return [dict(name='', title=_('No transition'))] +[
            dict(name=x, title=y) for x, y in allowed_transitions]

    @action(_('Apply now'), style='primary')
    def apply(self, **data):
        form = self.request.form
        if 'transition' in form and form['transition']:
            transition_id = form['transition']
            wf_info = IWorkflowInfo(self.context)
            try:
                wf_info.fireTransition(transition_id)
                self.flash(_("Transition '%s' executed." % transition_id))
            except InvalidTransitionError, error:
                self.flash(error, type="warning")
            self.redirect(self.url(self.context))
        return