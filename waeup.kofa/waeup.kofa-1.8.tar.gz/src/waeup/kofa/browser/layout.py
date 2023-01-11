## $Id: layout.py 17174 2022-11-25 08:42:37Z henrik $
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
"""Basic layout components.
"""
import os
import grok
from datetime import date, datetime
from grokcore.view import PageTemplateFile
from grokcore.formlib.formlib import Action
from cgi import escape
from zope.i18n import translate
from zope.i18nmessageid import Message
from megrok.layout import Page, Layout, Form, EditForm, DisplayForm, AddForm
from z3c.flashmessage.interfaces import IMessageSource, IMessageReceiver
from zope.component import getUtility, queryUtility, ComponentLookupError
from zope.formlib.utility import setUpWidgets
from zope.interface import Interface
from zope.site.hooks import getSite
from waeup.kofa.interfaces import IKofaObject, IUserAccount, IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import to_timezone
from waeup.kofa.browser.interfaces import IStudentNavigationBase
from waeup.kofa.authentication import get_principal_role_manager

grok.templatedir('templates')
default_waeup_display_template = PageTemplateFile(
    os.path.join('templates', 'default_waeup_display_form.pt'))
default_waeup_display_template.__grok_name__ = 'default_waeup_display_form'

default_waeup_edit_template = PageTemplateFile(
    os.path.join('templates', 'default_waeup_edit_form.pt'))
default_waeup_edit_template.__grok_name__ = 'default_waeup_edit_form'

default_primary_nav_template = PageTemplateFile(
    os.path.join('templates', 'primarynavtab.pt'))
default_primary_nav_template.__grok_name__ = 'default_primary_nav'

default_filedisplay_template = PageTemplateFile(
    os.path.join('templates', 'filedisplay.pt'))
default_filedisplay_template.__grok_name__ = 'default_filedisplay'

default_fileupload_template = PageTemplateFile(
    os.path.join('templates', 'fileupload.pt'))
default_fileupload_template.__grok_name__ = 'default_fileupload'

class action(grok.action):

    def __call__(self, success):
        action = KofaAction(self.label, success=success, **self.options)
        self.actions.append(action)
        return action

class KofaAction(Action):

    def __init__(self, label, style='', tooltip='', warning='', **options):
        super(KofaAction, self).__init__(label, **options)
        self.style = style
        self.tooltip = tooltip
        self.warning = warning
        if style == '':
            self.style = 'default'

    def render(self):
        if not self.available():
            return ''
        label = self.label
        if isinstance(label, Message):
            label = translate(self.label, context=self.form.request)
        if self.warning:
            warning = translate(self.warning, context=self.form.request)
            self.warning = ' onclick="return window.confirm(\'%s\')"' % warning
        if self.tooltip:
            tooltip = translate(self.tooltip, context=self.form.request)
            self.tooltip = ' data-toggle="tooltip" title="%s"' % tooltip
        if self.style:
            if self.style == 'invisible':
                style = ' class="invisible"'
            else:
                style = ' class="btn btn-%s"' % self.style
        else:
            style = ' class="btn btn-default"'
        html = ('<input type="submit" id="%s" name="%s" value="%s"' %
                (self.__name__, self.__name__, escape(label, quote=True))
                + style + self.tooltip + self.warning
                + ' />')
        return html

class jsaction(grok.action):

    msg = _('Are you sure?')

    def __call__(self, success):
        action = KofaAction(self.label,
                            success=success, warning=self.msg,
                            **self.options)
        self.actions.append(action)
        return action

def NullValidator(*args, **kw):
    """A validator that does not validate.

    This is needed especially for cancel buttons. We don't want data
    to be validated that will be thrown away in the next step.

    You can use it with ``grok.action`` decorator like this::

      @grok.action('Cancel', validator=NullValidator)
      def cancel(self, **data):
        self.redirect(<whereever-you-go>)
    """
    return dict()

class Messages(grok.View):
    """Display messages of message receivers.
    """

    grok.context(Interface)

    @property
    def messages(self):
        receiver = getUtility(IMessageReceiver)
        return receiver.receive()

class UtilityView(object):
    """A view mixin with useful methods.

    The ``pnav`` attribute (a number) tells, to which primary
    navigation tab a page declares to belong.
    """
    title = u'' # What appears in the content title...
    pnav = 0 # Primary navigation index...

    def application_url(self, name=None):
        """Return the URL of the nearest site.
        """
        site = getSite()
        #if not site:
        #    raise ComponentLookupError("No site found.")
        return self.url(site, name)

    def flash(self, message, type='success'):
        """Send a short message to the user.
        """
        cssClass = 'alert alert-%s' % type
        source = queryUtility(IMessageSource, name='session')
        if source is None:
            return None
        source.send(message, cssClass)
        return True

class KofaLayout(UtilityView,Layout):
    """A megrok.layout.Layout with additional methods.
    """
    grok.baseclass()

class KofaPage(UtilityView,Page):
    """A megrok.layout page with additional methods.
    """
    grok.baseclass()

class KofaFormPage(UtilityView,Form):
    """A megrok.layout.Form with additional methods.
    """
    grok.baseclass()

    def setUpWidgets(self,ignore_request=False):
        super(KofaFormPage,self).setUpWidgets(ignore_request)
        # Width parameters will be overridden by Bootstrap
        # so we have to set the css class
        if self.widgets.get('body'):
            self.widgets['body'].height = 10

class KofaDisplayFormPage(UtilityView,DisplayForm):
    """A megrok.layout.DisplayForm with additional methods.
    """
    grok.baseclass()
    template = default_waeup_display_template
    hide_hint = True

class KofaEditFormPage(UtilityView,EditForm):
    """A megrok.layout.EditForm with additional methods.
    """
    grok.baseclass()
    template = default_waeup_edit_template

    def setUpWidgets(self,ignore_request=False):
        super(KofaEditFormPage,self).setUpWidgets(ignore_request)
        for widget in self.widgets:
            if 'address' in widget.name or \
                'comment' in widget.name or \
                'message' in widget.name or \
                'notice' in widget.name:
                widget.height = 6
        if self.widgets.get('transcript_comment'):
            self.widgets['transcript_comment'].height = 12
        if self.widgets.get('transcript_remark'):
            self.widgets['transcript_remark'].height = 6
        if self.widgets.get('jamb_subjects'):
            self.widgets['jamb_subjects'].height = 6

class KofaAddFormPage(UtilityView,AddForm):
    """A megrok.layout.AddForm with additional methods.
    """
    grok.baseclass()
    template = default_waeup_edit_template

class SiteLayout(KofaLayout):
    """ The general site layout.
    """
    grok.context(IKofaObject)

    #: An instance of the default theme to use for the site layout
    stafftemp = grok.PageTemplateFile('templates/staffsitelayout.pt')
    studenttemp = grok.PageTemplateFile('templates/studentsitelayout.pt')

    @property
    def site(self):
        return grok.getSite()

    def getAppTitle(self):
        return getattr(grok.getSite()['configuration'], 'name', u'Sample University')

    def getAppAcronym(self):
        return getattr(grok.getSite()['configuration'], 'acronym', u'Acronym')

    def isAuthenticated(self):
        """Return True if the calling user is authenticated.
        """
        usertitle = self.request.principal.title
        return usertitle != 'Unauthenticated User'

    def isMaintenanceMode(self):
        """Return True if portal is in maintenance mode.
        """
        if grok.getSite()['configuration'].maintmode_enabled_by:
            return True
        return False

    def getUserTitle(self):
        """Return principal title of current user.
        """
        usertitle = self.request.principal.title
        if usertitle == 'Unauthenticated User':
            return u'Anonymous User'
        return usertitle

    def getUserId(self):
        """Return id of current user.
        """
        userid = self.request.principal.id
        return userid

    def isStudent(self):
        usertype = getattr(self.request.principal, 'user_type', None)
        if not usertype:
            return False
        return self.request.principal.user_type == 'student'

    def isApplicant(self):
        usertype = getattr(self.request.principal, 'user_type', None)
        if not usertype:
            return False
        return self.request.principal.user_type == 'applicant'

    def getStudentName(self):
        """Return the student name.
        """
        if IStudentNavigationBase.providedBy(self.context):
            return self.context.student.display_fullname
        return

    def formatDatetime(self,datetimeobj):
        if isinstance(datetimeobj, datetime):
            tz = getUtility(IKofaUtils).tzinfo
            try:
                timestamp = to_timezone(
                    datetimeobj, tz).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None
            return timestamp
        else:
            return None

    def formatDate(self,dateobj):
        if isinstance(dateobj, date):
            return dateobj.strftime("%d/%m/%Y")
        else:
            return None
            
    def formatTZDate(self,datetimeobj):
        if isinstance(datetimeobj, datetime):
            if datetimeobj.year == 2099:
                return _('OE')
            tz = getUtility(IKofaUtils).tzinfo
            date = to_timezone(
                datetimeobj, tz).strftime("%d/%m/%Y")
            return date
        else:
            return None          

    @property
    def course_cat_used(self):
        if len(getUtility(IKofaUtils).COURSE_CATEGORY_DICT):
            return True
        return False

    def render(self):
        if self.isStudent() or self.isApplicant() or not self.isAuthenticated():
            return self.studenttemp.render(self)
        return self.stafftemp.render(self)
