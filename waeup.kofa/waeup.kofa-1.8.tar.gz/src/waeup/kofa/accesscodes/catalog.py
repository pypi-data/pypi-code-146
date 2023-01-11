## $Id: catalog.py 7811 2012-03-08 19:00:51Z uli $
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
"""Cataloging and searching components for access codes.
"""
import grok
from grok import index
from hurry.query import Eq, Text
from hurry.query.query import Query
from zope.index.text.parsetree import ParseError
from waeup.kofa.interfaces import IUniversity, IQueryResultItem
from waeup.kofa.accesscodes.interfaces import IAccessCode

class AccessCodeIndexes(grok.Indexes):
    """A catalog for access codes.
    """
    grok.site(IUniversity)
    grok.name('accesscodes_catalog')
    grok.context(IAccessCode)

    code = index.Field(attribute='representation')
    history = index.Text(attribute='history')
    batch_serial = index.Field(attribute='batch_serial')
    state = index.Field(attribute='state')

class AccessCodeQueryResultItem(object):
    grok.implements(IQueryResultItem)

    title = u'Access Code Query Item'
    description = u'Some access code found in a search'

    def __init__(self, context, view):
        self.context = context
        self.url = view.url(context)
        self.code = context.representation
        self.history = context.history
        self.translated_state = context.translated_state
        self.owner = context.owner
        self.batch_serial = context.batch_serial

def search(query=None, searchtype=None, view=None):
    if not query:
        view.flash('Empty search string.')
        return
    hitlist = []
    if searchtype == 'history':
        results = Query().searchResults(
            Text(('accesscodes_catalog', searchtype), query))
    elif searchtype == 'batch_serial':
        try:
            results = Query().searchResults(
                Eq(('accesscodes_catalog', searchtype), int(query)))
        except ValueError:
            return
    else:
        results = Query().searchResults(
            Eq(('accesscodes_catalog', searchtype), query))
    for result in results:
        hitlist.append(AccessCodeQueryResultItem(result, view=view))
    return hitlist
