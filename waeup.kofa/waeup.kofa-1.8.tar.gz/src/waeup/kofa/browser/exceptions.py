## $Id: exceptions.py 7819 2012-03-08 22:28:46Z henrik $
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
import zope.errorview.browser
from zope.interface.common.interfaces import IException
from zope.errorview.http import SystemErrorViewMixin
from zope.publisher.interfaces import INotFound
from zope.security.interfaces import IUnauthorized
from waeup.kofa.browser.layout import KofaPage

grok.templatedir('templates')

class ExceptionView(grok.View, zope.errorview.browser.ExceptionView,
                    SystemErrorViewMixin):
    """Base class for rendering views for uncaught exceptions that occur during
    the application run-time and are not otherwise rendered.

    Backport from Grok 1.6.

    XXX: This view is shared for all apps and objects in the ZODB root.
    """
    grok.context(IException)
    grok.name('index.html')
    grok.template('exception')

    def update(self):
        return zope.errorview.browser.ExceptionView.update(self)

class UnauthorizedView(grok.View, zope.errorview.browser.UnauthorizedView):
    """Base class for rendering views for IUnauthorized exceptions.

    Backport from grok 1.6. This is only a view (not a page) because
    we cannot trust that the associated :exc:`Unauthorized` exceptions
    happened inside a w.k. site.

    If not, then we have no layout available at time of rendering.

    XXX: This view is shared for all apps and objects in the ZODB root.
    """
    grok.context(IUnauthorized)
    grok.name('index.html')
    grok.template('unauthorized')

    def update(self):
        return zope.errorview.browser.UnauthorizedView.update(self)


class NotFoundPage(KofaPage):
    """A page rendered when an object cannot be found.

    XXX: This page won't work for objects above a w.k.University.
    """
    grok.context(INotFound)
    grok.name('index.html')
    grok.template('notfound')

    title = u'404: File Not Found'

    def update(self):
        try:
            self.context = grok.getSite()
        except:
            pass
        self.response.setStatus(404)
        return
