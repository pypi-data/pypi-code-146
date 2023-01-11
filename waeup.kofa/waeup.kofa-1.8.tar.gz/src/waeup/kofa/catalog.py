## $Id: catalog.py 12951 2015-05-15 08:56:17Z henrik $
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
"""Components to help cataloging and searching objects.
"""
import grok
from hurry.query.interfaces import IQuery
from hurry.query.query import Query
from zope.catalog.catalog import ResultSet
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility, queryUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from waeup.kofa.interfaces import (
    IQueryResultItem, IFilteredQuery, IFilteredCatalogQuery)

# not yet used
@implementer(IQuery)
class KofaQuery(Query):
    """A `hurry.query.query.Query` compatible query that also supports
    retrival of plain ``Bree`` result sets as used inside a catalog.

    Like `hurry.query.query.Query` objects, `KofaQuery` is some kind
    of a meta query or 'compound query' that can give the cataloged
    objects (or their int ids) matching one or more 'subqueries'.

    This way you can search for objects (or their int ids) that match
    several criteria at the same time. See ``examples`` section below.

    A singleton instance of this class is also available as global
    utility.

    A hurry.query-like query that supports also ``apply``.
    """
    def apply(self, query):
        """Get the list of int ids (a `BTree` result set) for objects
        determined by ``query``.

        The list of int ids is less expensive to compute than the
        complete search results and sufficient, for instance, when you
        only need the number of objects that match a query and not the
        objects themselves.
        """
        return query.apply()

    def searchResults(self, query):
        """Get a set of ZODB objects conforming to a query.
        """
        results = self.apply(query)
        if results is not None:
            uidutil = getUtility(IIntIds)
            results = ResultSet(results, uidutil)
        return results

grok.global_utility(KofaQuery)

# not yet used
@implementer(IQueryResultItem)
class QueryResultItem(object):
    url = None
    title = None
    description = None

    def __init__(self, context, view):
        self.context = context
        self.url = view.url(context)
        self.title = context.title
        self.description = ''

@implementer(IFilteredQuery)
class FilteredQueryBase(object):
    """A filter to find objects that match certain parameters.

    Parameters are passed to constructor as keyword arguments. The
    real data retrieval then happens when `query()` is called.

    The `defaults` attribute, a dict, can set certain default values
    for parameters that are used if the constructor is called without
    any parameters.
    """
    defaults = dict()

    def __init__(self, **kw):
        self._kw = dict(self.defaults)
        self._kw.update(kw)
        return

    def query(self, context=None):
        err_msg = 'class %s does not implement the query() method.' % (
            self.__class__.__name__, )
        raise NotImplementedError(err_msg)

@implementer(IFilteredCatalogQuery)
class FilteredCatalogQueryBase(FilteredQueryBase):
    """Base for filtered queries based on catalog lookups.

    This type of query asks a catalog to find objects.

    You would normally use this type of query like this:

      >>> query = FilteredCatalogQueryBase(name='bob')
      >>> objects = query.query()

    The name of the catalog to use can be set via `cat_name`
    attribute.

    Looked up are all objects that match keywords passed to
    constructor where the keyword names must match a certain index of
    the chosen catalog. So, if some catalog has indexes `name` and
    `age`, then keywords `name='bob', age='12'` would search for all
    objects with name ``bob`` and age ``12``.

    This query supports single values (exact matches) and ranges of
    values passed in via ``(min_value, max_value)`` tuples. So,
    constructor keyword args `name=('a', 'd')` would find objects with
    name ``alice``, ``bob``, ``d``, but not ``donald``, ``john``, or
    ``zak``.
    """
    cat_name = None

    def query_catalog(self, catalog):
        """Search ``catalog``.

        Use `catalog`, some ``Catalog`` instance, to search objects
        denoted by constructor keywords.
        """
        query = dict()
        for idx_name, value in self._kw.items():
            if idx_name == 'catalog':
                continue
            if value is not None:
                if 'session' in idx_name or 'level' in idx_name:
                    value = int(value)
                if idx_name in ('level', 'current_level'):
                    value = int(value)
                    if value not in (10, 999):
                        value = (value, value + 90)
            if not isinstance(value, tuple):
                value = (value, value)
            query[idx_name] = value
        result = catalog.searchResults(**query)
        return result

    def query(self):
        """Perform a query with parameters passed to constructor.

        Returns some iterable, normally a list or a catalog result
        set.
        """
        catalog = queryUtility(
            ICatalog, name=self.cat_name, default=None)
        if catalog is None:
            return []
        return self.query_catalog(catalog)
