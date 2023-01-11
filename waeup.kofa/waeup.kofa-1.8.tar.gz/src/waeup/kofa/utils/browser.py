## $Id: browser.py 16028 2020-03-06 20:40:04Z henrik $
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
"""UI components for utilities and helpers.
"""

import grok
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility, createObject
from waeup.kofa.browser.layout import UtilityView
from waeup.kofa.interfaces import IObjectHistory
from waeup.kofa.interfaces import IUniversity
from waeup.kofa.university.interfaces import IDepartment, ICertificate
from waeup.kofa.utils.helpers import reindex_cat

def replaceStudentMessages(old, new):
    students = grok.getSite()['students']
    for student in students.values():
        history = IObjectHistory(student)
        history.modifyMessages(old, new)
    return

def replaceApplicantMessages(old, new):
    applicants = grok.getSite()['applicants']
    for container in applicants.values():
        for applicant in container.values():
            history = IObjectHistory(applicant)
            history.modifyMessages(old, new)
    return

def removeStudentMessage(student_id, number):
    students = grok.getSite()['students']
    student = students.get(student_id, None)
    if student:
        history = IObjectHistory(student)
        success, text = history.removeMessage(number)
    return success, text

def removeApplicantMessage(applicant_id, number):
    applicants = grok.getSite()['applicants']
    try:
        container, application_number = applicant_id.split('_')
    except:
        return False, 'applicant_id is wrong'
    container = applicants.get(container, None)
    if not container:
        return False, 'No such container'
    applicant = container.get(application_number, None)
    if applicant is None:
        return False, 'No such applicant'
    history = IObjectHistory(applicant)
    success, text = history.removeMessage(number)
    return success, text

class ReindexPage(UtilityView, grok.View):
    """ Reindex view.

    Reindexes a catalog. For managers only.
    """
    grok.context(IUniversity)
    grok.name('reindex')
    grok.require('waeup.managePortal')

    def update(self,ctlg=None):
        if ctlg is None:
            self.flash('No catalog name provided.')
            return
        cat = queryUtility(ICatalog, name='%s_catalog' % ctlg)
        if cat is None:
            self.flash('%s_catalog does not exist' % ctlg)
            return
        self.context.logger.info(
            'Catalog `%s_catalog` re-indexing started.' % ctlg)
        # Use Uli's updateIndexes method.
        # cat.updateIndexes()
        reindex_cat(cat)
        no_of_entries = cat.values()[0].documentCount()
        self.flash('%d %s re-indexed.' % (no_of_entries,ctlg))
        self.context.logger.info(
            'Re-indexing of %d objects finished.' % no_of_entries)
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class ModifyAllStudentHistory(UtilityView, grok.View):
    """ View to modify all student histories.

    """
    grok.context(IUniversity)
    grok.name('modify_student_history')
    grok.require('waeup.managePortal')

    def update(self,old=None, new=None):
        if None in (old, new):
            self.flash('Syntax: /modify_student_history?old=[old string]&new=[new string]')
            return
        replaceStudentMessages(old, new)
        self.context.logger.info(
            "'%s' replaced by '%s' in all student histories." % (old, new))
        self.flash('Finished')
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class RemoveStudentHistoryMessage(UtilityView, grok.View):
    """ View to remove a single student history entry.

    """
    grok.context(IUniversity)
    grok.name('remove_student_history_message')
    grok.require('waeup.managePortal')

    def update(self,student_id=None, number=None):
        if None in (student_id, number):
            self.flash('Syntax: /remove_student_history_message?student_id=[id]&number=[line number, starting with 0]')
            return
        try:
            number=int(number)
        except:
            self.flash('Error')
            return
        success, text = removeStudentMessage(student_id, number)
        if not success:
            self.flash('Error: %s' % text)
            return
        self.context.logger.info(
            "line '%s' removed in %s history" % (text, student_id))
        self.flash('Finished')
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class ModifyAllApplicantHistory(UtilityView, grok.View):
    """ View to modify all student histories.

    """
    grok.context(IUniversity)
    grok.name('modify_applicant_history')
    grok.require('waeup.managePortal')

    def update(self,old=None, new=None):
        if None in (old, new):
            self.flash('Syntax: /modify_applicant_history?old=[old string]&new=[new string]')
            return
        replaceApplicantMessages(old, new)
        self.context.logger.info(
            "'%s' replaced by '%s' in all applicant histories." % (old, new))
        self.flash('Finished')
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class RemoveApplicantHistoryMessage(UtilityView, grok.View):
    """ View to remove a single applicant history entry.

    """
    grok.context(IUniversity)
    grok.name('remove_applicant_history_message')
    grok.require('waeup.managePortal')

    def update(self,applicant_id=None, number=None):
        if None in (applicant_id, number):
            self.flash('Syntax: /remove_applicant_history_message?applicant_id=[id]&number=[line number, starting with 0]')
            return
        try:
            number=int(number)
        except:
            self.flash('Error')
            return
        success, text = removeApplicantMessage(applicant_id, number)
        if not success:
            self.flash('Error: %s' % text)
            return
        self.context.logger.info(
            "line '%s' removed in %s history" % (text, applicant_id))
        self.flash('Finished')
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return


class MoveDepartment(UtilityView, grok.View):
    """ View to move a department.

    """
    grok.context(IDepartment)
    grok.name('move_department')
    grok.require('waeup.managePortal')

    def update(self,fac=None, dep=None):
        if None in (fac, dep):
            self.flash('Syntax: /move_department?fac=[new faculty code]&dep=[new department code]')
            return
        oldcode = self.context.code
        try:
            self.context.moveDepartment(fac, dep)
        except:
            self.flash('Error')
            return
        grok.getSite().logger.info(
            "Department %s moved to %s/%s" % (oldcode, fac, dep))
        self.flash('Finished')
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return

class MoveCertificate(UtilityView, grok.View):
    """ View to move a certificate.

    """
    grok.context(ICertificate)
    grok.name('move_certificate')
    grok.require('waeup.managePortal')

    def update(self,fac=None, dep=None, cert=None):
        if None in (fac, dep, cert):
            self.flash('Syntax: /move_certificate?fac=[new faculty code]&dep=[new department code]&cert=[new certificate code]')
            return
        oldcode = self.context.code
        try:
            self.context.moveCertificate(fac, dep, cert)
        except:
            self.flash('Error')
            return
        grok.getSite().logger.info(
            "Certificate %s moved to %s/%s/%s" % (oldcode, fac, dep, cert))
        self.flash('Finished')
        return

    def render(self):
        self.redirect(self.url(self.context, '@@index'))
        return