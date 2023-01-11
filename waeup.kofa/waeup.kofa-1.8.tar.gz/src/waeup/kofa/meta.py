## $Id: meta.py 15769 2019-11-07 13:20:25Z uli $
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
"""Grokkers for Kofa components.

Stuff in here is mainly taken from grok.meta, with some modifications
to provide a possibility to update catalogs in a running site. This is
to solve the very common problem of already running sites for which
the software changes and adds catalogs. These catalogs will not be
automatically added in a running site.

With the following Grokker and the upgrade helper class we can fire
IObjectUpgradedEvents for any existing site and all catalogs
registered will be really created.

Please note that yet these catalogs are not filled automatically! That
means the catalogs will exist but are empty in the beginning.

We might solve this second problem by firing extra events like some
ICatalogUpdatedEvent (which still do not exist) or similar.
"""
import grok
import grokcore.component
import martian
from grok import components
from grok.meta import IndexesSetupSubscriber
from martian.error import GrokError
from zope import component
from zope.processlifetime import IDatabaseOpened
from waeup.kofa.interfaces import IObjectUpgradeEvent

class IndexesGrokker(martian.InstanceGrokker):
    """Grokker for Grok index bundles."""
    martian.component(components.IndexesClass)

    def grok(self, name, factory, module_info, config, **kw):
        site = grok.site.bind().get(factory)
        context = grok.context.bind().get(factory, module_info.getModule())
        catalog_name = grok.name.bind().get(factory)

        if site is None:
            raise GrokError("No site specified for grok.Indexes "
                            "subclass in module %r. "
                            "Use grok.site() to specify."
                            % module_info.getModule(),
                            factory)
        indexes = getattr(factory, '__grok_indexes__', None)
        if indexes is None:
            return False

        subscriber = KofaIndexesUpgradeSubscriber(
            catalog_name, indexes, context, module_info)
        subscribed = (site, IObjectUpgradeEvent)
        config.action(
            discriminator=None,
            callable=component.provideHandler,
            args=(subscriber, subscribed),
            )
        return True


class KofaIndexesUpgradeSubscriber(IndexesSetupSubscriber):
    """Helper that sets up indexes when their Grok site is upgraded.

    Each `grok.Indexes` class serves as an assertion that, whenever an
    instance of its `grok.site()` is upgraded, the given list of
    indexes should be generated if not already created as well.  But a
    long period of time could elapse between when the application
    starts (and its indexes are grokked), and the moment, maybe days
    or weeks later, when a new instance of that `grok.Site` is
    created.  Hence this `IndexesSetupSubscriber`: it can be
    instantiated at grokking time with the index information, and then
    registered with the Component Architecture as an event that should
    be fired later, whenever the right kind of `grok.Site` is
    instantiated.  At that point its `__call__` method is kicked off
    and it makes sure the index catalogs get created properly.

    """
    def __call__(self, site, event):
        #site.logger.info('Create catalog `%s` if not installed yet.'  % (
        #        self.catalog_name,))
        # make sure we have an intids
        self._createIntIds(site)
        # get the catalog
        catalog = self._createCatalog(site)
        # now install indexes
        for name, index in self.indexes.items():
            try:
                #site.logger.info('Create index `%s` in catalog.' % name)
                index.setup(catalog, name, self.context, self.module_info)
                site.logger.info('%s: Index %s created.' % (self.catalog_name,name))
            except KeyError: #, DuplicationError:
                #site.logger.info('Index `%s` already in catalog.' % name)
                pass
        #site.logger.info('Catalog `%s` ready.' % self.catalog_name)



@grokcore.component.subscribe(IDatabaseOpened)
def disable_broken_handlers(event):
    """This one is fired after ZODB setup.

    Unregsiter handlers etc., that are broken or meant trouble in the past.
    """
    from zope.component import getGlobalSiteManager
    from zope.catalog.catalog import indexAdded
    worked = getGlobalSiteManager().unregisterHandler(indexAdded)
    if worked:
        print("Unregistered handler zope.catalog.catalog.indexAdded")
    # TODO: register a replacement that copes better with large indexes.
