## $Id: browser.py 15633 2019-10-03 10:09:25Z henrik $
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
"""UI components for hostels and related components.
"""
import grok
import sys
from zope.i18n import translate
from zope.component import getUtility, createObject
from zope.catalog.interfaces import ICatalog
from waeup.kofa.browser.layout import (
    KofaEditFormPage, KofaAddFormPage, KofaDisplayFormPage,
    NullValidator, UtilityView)
from waeup.kofa.browser.breadcrumbs import Breadcrumb
from waeup.kofa.browser.layout import default_primary_nav_template
from waeup.kofa.browser.pages import delSubobjects
from waeup.kofa.browser.viewlets import (
    ManageActionButton, PrimaryNavTab)
from waeup.kofa.browser.layout import jsaction, action
from waeup.kofa.interfaces import IKofaObject, IKofaUtils, DOCLINK
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.hostels.vocabularies import NOT_OCCUPIED
from waeup.kofa.hostels.hostel import Hostel
from waeup.kofa.hostels.interfaces import (
    IHostelsContainer, IHostel, IBed)
from waeup.kofa.widgets.datewidget import FriendlyDatetimeDisplayWidget

# Save function used for save methods in manager pages
def msave(view, **data):
    changed_fields = view.applyData(view.context, **data)
    # Turn list of lists into single list
    if changed_fields:
        changed_fields = reduce(lambda x,y: x+y, changed_fields.values())
    fields_string = ' + '.join(changed_fields)
    view.context._p_changed = True
    view.flash(_('Form has been saved.'))
    if fields_string:
        view.context.writeLogMessage(view, 'saved: %s' % fields_string)
    return

class HostelsTab(PrimaryNavTab):
    """Hostels tab in primary navigation.
    """

    grok.context(IKofaObject)
    grok.order(5)
    grok.require('waeup.viewHostels')
    grok.name('hostelstab')
    template = default_primary_nav_template
    pnav = 5
    tab_title = _(u'Hostels')

    @property
    def link_target(self):
        return self.view.application_url('hostels')

class HostelsBreadcrumb(Breadcrumb):
    """A breadcrumb for the hostels container.
    """
    grok.context(IHostelsContainer)
    title = _(u'Hostels')

class HostelBreadcrumb(Breadcrumb):
    """A breadcrumb for the hostel container.
    """
    grok.context(IHostel)

    def title(self):
        return self.context.hostel_name

class BedBreadcrumb(Breadcrumb):
    """A breadcrumb for the hostel container.
    """
    grok.context(IBed)

    def title(self):
        co = self.context.coordinates
        return _('Block ${a}, Room ${b}, Bed ${c}',
            mapping = {'a':co[1], 'b':co[2], 'c':co[3]})

class HostelsContainerPage(KofaDisplayFormPage):
    """The standard view for hostels containers.
    """
    grok.context(IHostelsContainer)
    grok.name('index')
    grok.require('waeup.viewHostels')
    grok.template('containerpage')
    label = _('Accommodation Section')
    pnav = 5
    form_fields = grok.AutoFields(IHostelsContainer)
    form_fields[
        'startdate'].custom_widget = FriendlyDatetimeDisplayWidget('le')
    form_fields[
        'enddate'].custom_widget = FriendlyDatetimeDisplayWidget('le')

class HostelsContainerManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IHostelsContainer)
    grok.view(HostelsContainerPage)
    grok.require('waeup.manageHostels')
    text = _('Manage accommodation section')

class HostelsStatisticsActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IHostelsContainer)
    grok.view(HostelsContainerPage)
    grok.require('waeup.manageHostels')
    icon = 'actionicon_statistics.png'
    text = _('Bed statistics')
    target = 'statistics'

class ReleaseExpiredAllocationsActionButton(ManageActionButton):
    grok.order(3)
    grok.context(IHostelsContainer)
    grok.view(HostelsContainerPage)
    grok.require('waeup.manageHostels')
    icon = 'actionicon_sweep.png'
    target = 'releaseexpired'
    text = _('Release all expired bed space allocations')

    @property
    def target_url(self):
        if self.target and self.context.allocation_expiration:
            return self.view.url(self.view.context, self.target)
        return

    @property
    def onclick(self):
        msg = _("'All expired bed space allocations will be annulled. " + \
              "Are you sure? \\n\\n" + \
              "Bed space allocation expires ${a} days after accommodation " + \
              "booking if maintenance fee is not " + \
              "paid.'")
        msg = _(msg, mapping={'a': self.context.allocation_expiration,})
        portal_language = getUtility(IKofaUtils).PORTAL_LANGUAGE
        return "return window.confirm(%s);" % translate(
            msg, 'waeup.kofa', target_language=portal_language)

class HostelsContainerManagePage(KofaEditFormPage):
    """The manage page for hostel containers.
    """
    grok.context(IHostelsContainer)
    grok.name('manage')
    grok.require('waeup.manageHostels')
    grok.template('containermanagepage')
    pnav = 5
    label = _('Manage accommodation section')
    form_fields = grok.AutoFields(IHostelsContainer)
    taboneactions = [_('Save')]
    tabtwoactions = [_('Add hostel'),
        _('Clear all hostels'),
        _('Remove selected')]
    doclink = DOCLINK + '/hostels.html#accommodation-section'

    # It's quite dangerous to remove entire hostels with its content (beds).
    # Thus, this remove method should be combined with an archiving function.
    @jsaction(_('Remove selected'))
    def delHostels(self, **data):
        form = self.request.form
        if 'val_id' in form:
            deleted = []
            child_id = form['val_id']
            if not isinstance(child_id, list):
                child_id = [child_id]
            for id in child_id:
                deleted.append(id)
            self.context.writeLogMessage(
                self, 'deleted: % s' % ', '.join(deleted))
        delSubobjects(self, redirect='@@manage', tab='2')
        return

    @action(_('Add hostel'), validator=NullValidator)
    def addSubunit(self, **data):
        self.redirect(self.url(self.context, 'addhostel'))
        return

    @jsaction(_('Clear all hostels'), style='danger')
    def clearHostels(self, **data):
        self.context.clearAllHostels()
        self.flash(_('All hostels cleared.'))
        self.context.writeLogMessage(self, 'all hostels cleared')
        self.redirect(self.url(self.context, '@@manage')+'#tab2')
        return

    @action(_('Save'), style='primary')
    def save(self, **data):
        if data['accommodation_session'] != self.context.accommodation_session:
            catalog = getUtility(ICatalog, name='beds_catalog')
            beds = catalog.searchResults(bed_type=(None,None))
            if len(beds) and not self.request.principal.id == 'admin':
                self.flash(_('You can\'t change the booking session '
                             'before clearing all hostels.'),
                           type='warning')
                return
        msave(self, **data)
        return

class ReleaseExpiredAllocationsPage(UtilityView, grok.View):
    """Release all expired allocated beds.
    """
    grok.context(IHostelsContainer)
    grok.name('releaseexpired')
    grok.require('waeup.manageHostels')

    def update(self):
        n = self.context.allocation_expiration
        if not n:
            self.flash(
                _('Forbidden'), type='danger')
            self.redirect(self.url(self.context))
            return
        if not grok.getSite()['configuration'].maintmode_enabled_by:
            self.flash(
                _('Portal must be in maintenance mode for releasing expired '
                  'bed allocations.'),
                type='danger')
            self.redirect(self.url(self.context))
            return
        released = self.context.releaseExpiredAllocations(n)
        if len(released):
            message = ', '.join(released)
            self.context.writeLogMessage(self, 'released: %s' % message)
            if len(released) > 50:
                flash_msg = _('Successfully released ${a} beds.',
                    mapping = {'a':len(released)})
            else:
                flash_msg = _('Successfully released beds: ${a}',
                    mapping = {'a':message})
        else:
            flash_msg = _('No bed released.')
        self.flash(flash_msg, type='success')
        self.redirect(self.url(self.context))
        return

    def render(self):
        return

class HostelsStatisticsPage(KofaDisplayFormPage):
    """Some statistics about beds in hostels.
    """
    grok.context(IHostelsContainer)
    grok.name('statistics')
    grok.require('waeup.manageHostels')
    grok.template('containerstatistics')
    label = _('Bed Statistics')

class HostelAddFormPage(KofaAddFormPage):
    """Add-form to add a hostel.
    """
    grok.context(IHostelsContainer)
    grok.require('waeup.manageHostels')
    grok.name('addhostel')
    #grok.template('hosteladdpage')
    form_fields = grok.AutoFields(IHostel).omit('beds_reserved', 'hostel_id')
    label = _('Add hostel')
    pnav = 5
    doclink = DOCLINK + '/hostels.html#accommodation-section'

    @action(_('Create hostel'))
    def addHostel(self, **data):
        hostel = container = createObject(u'waeup.Hostel')
        self.applyData(hostel, **data)
        hostel.hostel_id = data['hostel_name'].lower().replace(
            ' ','-').replace('_','-').replace('.','')
        try:
            self.context.addHostel(hostel)
        except KeyError:
            self.flash(_('The hostel already exists.'), type='warning')
            return
        self.flash(_('Hostel created.'))
        self.context.writeLogMessage(self, 'added: % s' % data['hostel_name'])
        self.redirect(self.url(self.context[hostel.hostel_id], 'index'))
        return

class HostelDisplayFormPage(KofaDisplayFormPage):
    """ Page to display hostel data
    """
    grok.context(IHostel)
    grok.name('index')
    grok.require('waeup.viewHostels')
    grok.template('hostelpage')
    form_fields = grok.AutoFields(IHostel).omit('beds_reserved')
    pnav = 5

    @property
    def label(self):
        return self.context.hostel_name

class HostelManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IHostel)
    grok.view(HostelDisplayFormPage)
    grok.require('waeup.manageHostels')
    text = _('Manage')
    target = 'manage'

class HostelManageFormPage(KofaEditFormPage):
    """ View to edit hostel data
    """
    grok.context(IHostel)
    grok.name('manage')
    grok.require('waeup.manageHostels')
    form_fields = grok.AutoFields(IHostel).omit('hostel_id', 'beds_reserved')
    grok.template('hostelmanagepage')
    label = _('Manage hostel')
    pnav = 5
    taboneactions = [_('Save')]
    tabtwoactions = [_('Update all beds'),
        _('Switch reservation of selected beds'),
        _('Release selected beds'),
        _('Clear hostel')]
    not_occupied = NOT_OCCUPIED
    doclink = DOCLINK + '/hostels.html#browser-pages'

    @property
    def students_url(self):
        return self.url(grok.getSite(),'students')

    @action(_('Save'), style='primary')
    def save(self, **data):
        msave(self, **data)
        return

    @action(_('Update all beds'), style='primary',
            warning=_('Attention: The updater removes all reservation flags of existing beds.'
                        ' You really want to update?'))
    def updateBeds(self, **data):
        if not grok.getSite()['configuration'].maintmode_enabled_by:
            self.flash(
                _('Portal must be in maintenance mode for bed updates.'),
                type='danger')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        removed, added, modified, modified_beds = self.context.updateBeds()
        message = '%d empty beds removed, %d beds added, %d occupied beds modified (%s)' % (
            removed, added, modified, modified_beds)
        if modified > 50:
            flash_message = _(
                '${a} empty beds removed, ${b} beds added, '
                + '${c} occupied beds modified',
                mapping = {'a':removed, 'b':added, 'c':modified})
        else:
            flash_message = _(
                '${a} empty beds removed, ${b} beds added, '
                + '${c} occupied beds modified (${d})',
                mapping = {'a':removed, 'b':added, 'c':modified, 'd':modified_beds})
        self.flash(flash_message)
        self.context.writeLogMessage(self, message)
        self.redirect(self.url(self.context, '@@manage')+'#tab2')
        return

    @action(_('Switch reservation of selected beds'))
    def switchReservations(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No item selected.'), type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        switched = [] # for log file
        switched_translated = [] # for flash message
        # Here we know that the cookie has been set
        preferred_language = self.request.cookies.get('kofa.language')
        for bed_id in child_id:
            message = self.context[bed_id].switchReservation()
            switched.append('%s (%s)' % (bed_id,message))
            m_translated = translate(message, 'waeup.kofa',
                target_language=preferred_language)
            switched_translated.append('%s (%s)' % (bed_id,m_translated))
        if len(switched):
            message = ', '.join(switched)
            m_translated = ', '.join(switched_translated)
            if len(switched) > 50:
                self.flash(_('Successfully switched ${a} beds.',
                    mapping = {'a':len(switched)}))
            else:
                self.flash(_('Successfully switched beds: ${a}',
                    mapping = {'a':m_translated}))
            self.context.writeLogMessage(self, 'switched: %s' % message)
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
        return

    @action(_('Release selected beds'))
    def releaseBeds(self, **data):
        form = self.request.form
        if 'val_id' in form:
            child_id = form['val_id']
        else:
            self.flash(_('No item selected.'), type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
            return
        if not isinstance(child_id, list):
            child_id = [child_id]
        released = []
        for bed_id in child_id:
            message = self.context[bed_id].releaseBed()
            if message:
                released.append('%s (%s)' % (bed_id,message))
        if len(released):
            message = ', '.join(released)
            self.flash(_('Successfully released beds: ${a}',
                mapping = {'a':message}))
            self.context.writeLogMessage(self, 'released: %s' % message)
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
        else:
            self.flash(_('No allocated bed selected.'), type='warning')
            self.redirect(self.url(self.context, '@@manage')+'#tab2')
        return

    @jsaction(_('Clear hostel'), style='danger')
    def clearHostel(self, **data):
        self.context.clearHostel()
        self.flash(_('Hostel cleared.'))
        self.context.writeLogMessage(self, 'cleared')
        self.redirect(self.url(self.context, '@@manage')+'#tab2')
        return

class BedManageFormPage(KofaEditFormPage):
    """ View to edit bed data
    """
    grok.context(IBed)
    grok.name('index')
    grok.require('waeup.manageHostels')
    form_fields = grok.AutoFields(IBed).omit(
        'bed_id', 'bed_number', 'bed_type')
    label = _('Allocate student')
    pnav = 5
    doclink = DOCLINK + '/hostels.html#manage-bed'

    @action(_('Save'))
    def save(self, **data):
        if data['owner'] == NOT_OCCUPIED:
            self.flash(_('No valid student id.'), type='warning')
            self.redirect(self.url(self.context))
            return
        msave(self, **data)
        self.redirect(self.url(self.context.__parent__, '@@manage')+'#tab2')
        return

    def update(self):
        if self.context.owner != NOT_OCCUPIED:
            # Don't use this form for exchanging students.
            # Beds must be released first before they can be allocated to
            # other students.
            self.redirect(self.url(self.context.__parent__, '@@manage')+'#tab2')
        return
