## $Id: browser.py 11254 2014-02-22 15:46:03Z uli $
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
"""UI components for accesscodes.
"""
import grok
from datetime import datetime
from zope.component import getUtility
from hurry.workflow.interfaces import InvalidTransitionError
from waeup.kofa.browser.layout import KofaPage, KofaAddFormPage, NullValidator
from waeup.kofa.browser.breadcrumbs import Breadcrumb
from waeup.kofa.browser.viewlets import (
    AdminTask, AddActionButton, SearchActionButton, BatchOpButton, ManageLink)
from waeup.kofa.interfaces import IKofaObject, IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.accesscodes.interfaces import (
    IAccessCodeBatchContainer, IAccessCodeBatch,
    )
from waeup.kofa.accesscodes.catalog import search
from waeup.kofa.browser.layout import action

grok.context(IKofaObject)

class BatchContainerPage(KofaPage):
    grok.name('index')
    grok.context(IAccessCodeBatchContainer)
    grok.template('batchcontainer')
    grok.require('waeup.manageACBatches')
    archive_button = _('Archive')
    delete_button = _('Archive and delete')

    label = _('Access Code Batches')
    pnav = 0

    def update(self, batches=None, archive=None, delete=None):
        if archive is None and delete is None:
            return
        if not batches:
            self.flash(_('No batch selected.'), type='warning')
            return
        if isinstance(batches, basestring):
            batches = [batches]
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        for name in batches:
            batch = self.context[name]
            csv_file = batch.archive()
            self.flash(_('Archived ${a} (${b})',
                mapping = {'a':name, 'b':csv_file}))
            message = 'archived: %s (%s)' % (name,csv_file)
            self.context.logger_info(ob_class, message)
            if delete is None:
                continue
            del self.context[name]
            self.context._p_changed = True
            self.flash(_('Deleted batch ${a}', mapping = {'a':name}))
            message = 'deleted: %s' % name
            self.context.logger_info(ob_class, message)

class AddBatchPage(KofaAddFormPage):
    grok.name('add')
    grok.context(IAccessCodeBatchContainer)
    grok.require('waeup.manageACBatches')

    label = _('Create Access Code Batch')
    pnav = 0

    form_fields = grok.AutoFields(IAccessCodeBatch).select(
        'prefix', 'entry_num', 'cost')

    @action(_('Create batch'), style='primary')
    def createBatch(self, **data):
        creator = self.request.principal.id
        creation_date = datetime.utcnow()
        data.update(creation_date=creation_date, creator=creator)
        batch = self.context.createBatch(**data)
        csv_file = batch.createCSVLogFile()
        self.context._p_changed = True
        self.flash(_('Batch created (${a} entries)',
            mapping = {'a':data['entry_num']}))
        self.flash(_('Data written to ${a}', mapping = {'a':csv_file}))
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        message = 'created: %s (%d, %f)' % (
            csv_file, data['entry_num'], data['cost'])
        self.context.logger_info(ob_class, message)
        self.redirect(self.url(self.context))

    @action(_('Cancel'), validator=NullValidator)
    def cancel(self, *args, **kw):
        self.flash(_('Batch creation cancelled.'), type='warning')
        self.redirect(self.url(self.context))

class ReimportBatchPage(KofaPage):
    """Screen for reimporting AC batches.
    """
    grok.name('reimport')
    grok.context(IAccessCodeBatchContainer)
    grok.template('reimportbatchpage')
    grok.require('waeup.manageACBatches')
    reimport_button = _('Reimport')
    cancel_button = _('Cancel')

    label = _('Reimport Access Code Batches')
    pnav = 0

    def update(self, filenames=None, reimport=None, cancel=None):
        if cancel is not None:
            self.flash(_('Reimport cancelled.'), type='warning')
            self.redirect(self.url(self.context))
            return
        if reimport is None:
            return
        if not filenames:
            self.flash(_('No file chosen. Action cancelled.'), type='warning')
            self.redirect(self.url(self.context))
            return
        if isinstance(filenames, basestring):
            filenames = [filenames]
        userid = self.request.principal.id
        for filename in filenames:
            try:
                self.context.reimport(filename, userid)
            except KeyError:
                self.flash(_('This batch already exists: ${a}',
                    mapping = {'a':filename}), type='warning')
                continue
            self.flash(_('Successfully reimported: ${a}',
                mapping = {'a':filename}))
            ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
            message = 'reimported: %s' % filename
            self.context.logger_info(ob_class, message)
        self.redirect(self.url(self.context))

class BatchContainerSearchPage(KofaPage):
    grok.name('search')
    grok.context(IAccessCodeBatchContainer)
    grok.template('searchpage')
    grok.require('waeup.manageACBatches')
    pnav = 0
    label = _('Search and Manage Access Codes')
    search_button = _('Search')
    disable_button = _('Disable ACs')
    enable_button = _('Enable ACs')
    cancel_button = _('Cancel Search')

    def update(self, *args, **kw):
        form = self.request.form
        if 'cancel' in form:
            self.redirect(self.url(self.context))
            return
        self.hitlist = []
        if 'searchterm' in form and form['searchterm']:
            self.searchterm = form['searchterm']
            self.searchtype = form['searchtype']
        elif 'old_searchterm' in form:
            self.searchterm = form['old_searchterm']
            self.searchtype = form['old_searchtype']
        else:
            return
        if not 'entries' in form:
            self.hitlist = search(query=self.searchterm,
                searchtype=self.searchtype, view=self)
            return
        entries = form['entries']
        if isinstance(entries, basestring):
            entries = [entries]
        ob_class = self.__implemented__.__name__.replace('waeup.kofa.','')
        for entry in entries:
            if 'disable' in form:
                try:
                    comment = _(u"disabled")
                    self.context.disable(entry, comment)
                    self.flash(_('${a} disabled.', mapping = {'a':entry}))
                    message = 'disabled: %s' % entry
                    self.context.logger_info(ob_class, message)
                except InvalidTransitionError:
                    self.flash(_('${a}: Disable transition not allowed.',
                        mapping = {'a':entry}), type='danger')
            elif 'enable' in form:
                try:
                    comment = _(u"re-enabled")
                    self.context.enable(entry, comment)
                    self.flash(_('${a} (re-)enabled.', mapping = {'a':entry}))
                    message = '(re-)enabled: %s' % entry
                    self.context.logger_info(ob_class, message)
                except InvalidTransitionError:
                    self.flash(_('${a}: Re-enable transition not allowed.',
                               mapping = {'a':entry}), type='danger')
        self.hitlist = search(query=self.searchterm,
            searchtype=self.searchtype, view=self)
        return

class BatchContainerBreadcrumb(Breadcrumb):
    """A breadcrumb for ac batch containers.
    """
    grok.require('waeup.manageACBatches')
    grok.context(IAccessCodeBatchContainer)
    title = _(u'Access Code Batches')
    parent_viewname = 'administration'

#class BatchContainerSearchBreadcrumb(Breadcrumb):
#    """A breadcrumb for ac batch containers search page.
#    """
#    grok.require('waeup.manageACBatches')
#    grok.context(IAccessCodeBatchContainer)
#    grok.name('search')
#    title = u'Search Access Codes'
#    viewname = 'search'
#    parent_viewname = 'index'

class AdminTaskManageACBatches(AdminTask):
    """Entry on administration page that links to batch container.
    """
    grok.order(5)
    grok.require('waeup.manageACBatches')
    grok.template('admintaskacbatches')

    link_title = _('Access Code Batches')
    target_viewname = 'accesscodes'

class CreateBatchButton(AddActionButton):
    """Action button on batch container page which links to batch creation.
    """
    grok.context(IAccessCodeBatchContainer)
    grok.view(BatchContainerPage)
    grok.require('waeup.manageACBatches')
    text = _('Add Access Code Batch')

class ReimportBatchButton(BatchOpButton):
    """Action button on batch container page which links to batch reimport.
    """
    grok.context(IAccessCodeBatchContainer)
    grok.view(BatchContainerPage)
    grok.require('waeup.manageACBatches')
    target = 'reimport'
    text = _('Reimport Access Code Batch')

class SearchAccessCodeButton(SearchActionButton):
    """Action button on batch container page which links to search.
    """
    grok.context(IAccessCodeBatchContainer)
    grok.view(BatchContainerPage)
    grok.require('waeup.manageACBatches')
    text = _('Search Access Codes')

class ManageAccessCodes(ManageLink):
    """Link in upper left box to access code management.
    """
    grok.order(5)
    grok.require('waeup.manageACBatches')

    link = u'accesscodes'
    text = _(u'Access Codes')
