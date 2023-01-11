"""
This is a collection of arbitrary scripts for mainly maintenance purposes.

The scripts are not callable via web interface.

Use them (for instance) like so::

    $ ./bin/kofa-debug
    >>> from waeup.kofa.scripts import add_field_index
    >>> add_field_index(root['aaue'], 'things_catalog', 'new_id')

Use at your own risk.

"""
from zope.catalog.field import FieldIndex
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from waeup.kofa.utils.helpers import reindex_cat
import transaction


def get_catalog(app, catalog_name):
    return getUtility(ICatalog, name=catalog_name, context=app)


def add_field_index(app, catalog_name, field_name):
    """Add a catalog FieldIndex.

    This can become cumbersome through the web API as _all_ objects stored in
    ZODB will then be indexed and pulled into memory - might become a problem
    with large databases. This CLI runs faster. You should make sure, that not
    much traffic is on the site when running the script.
    """
    cat = get_catalog(app, catalog_name)
    if field_name in cat.keys():
        # index exists already
        return False
    cat[field_name] = FieldIndex(field_name=field_name)
    transaction.commit()
    reindex_cat(cat)
    transaction.commit()
    return True
