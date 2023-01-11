import shutil
import tempfile
from grokcore.site.interfaces import IUtilityInstaller
from zope import schema
from zope.catalog.catalog import Catalog
from zope.catalog.field import FieldIndex
from zope.catalog.interfaces import ICatalog
from zope.component import getUtility
from zope.component.hooks import setSite
from zope.interface import Interface, implements
from waeup.kofa.app import University
from waeup.kofa.maintenance import update_catalog
from waeup.kofa.testing import FunctionalTestCase, FunctionalLayer

class ISampleContent(Interface):

    age = schema.Int(
        title=u'Age')
    name = schema.TextLine(
        title=u'Name')

class SampleContent(object):
    implements(ISampleContent)

    def __init__(self, age=None, name=None):
        self.age = age
        self.name = name
        return

    def __eq__(self, ob):
        # make sample contents comparable
        if not hasattr(ob, 'name') or not hasattr(ob, 'age'):
            return False
        return self.age == ob.age and self.name == ob.name

class UpdateCatalogTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(UpdateCatalogTests, self).setUp()
        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']
        setSite(self.app)
        return

    def tearDown(self):
        super(UpdateCatalogTests, self).tearDown()
        shutil.rmtree(self.dc_root)
        return

    def create_catalog(self):
        # install catalog in site
        self.catalog = Catalog()
        install = getUtility(IUtilityInstaller)
        install(self.app, self.catalog, ICatalog, 'my_catalog')
        self.create_indexes()
        self.catalog.clear() # make sure cat is empty
        return

    def create_indexes(self):
        # create 'age' and 'name' field index in cat if they do not
        # exist already.
        for name in ('age', 'name'):
            if name in self.catalog.keys():
                continue
            self.catalog[name] = FieldIndex(
                field_name=name, interface=ISampleContent,
                field_callable=False)
        return

    def add_sample_content(self):
        # Add sample content in ZODB
        manfred = SampleContent(42, 'Manfred')
        self.app['manfred'] = manfred
        self.manfred = self.app['manfred'] # this one has __parent__ etc.
        return

    def test_update_catalog_by_list(self):
        ## We can catalog new objects passed in as list
        # create object in ZODB before catalog exists
        self.add_sample_content()
        self.create_catalog()

        # right now we can't find manfred
        result1 = list(self.catalog.searchResults(age=(40,43)))
        self.assertEqual(len(result1), 0)

        # update catalog. We have to feed 'located' objects, which is
        # normally the case for objects from ZODB. In our case
        # 'manfred' could not be catalogued while the located version
        # 'manfred_located' (with a __parent__ and __name__ attribute)
        # can.
        update_catalog(self.app, 'my_catalog', [self.manfred])

        # now we can find manfred in catalog
        result2 = list(self.catalog.searchResults(age=(40,43)))
        self.assertEqual(result2[0], self.manfred)
        return

    def test_update_catalog_iterator(self):
        ## We can catalog new objects via function
        # create object in ZODB before catalog exists
        self.add_sample_content()
        self.create_catalog()

        # right now we can't find manfred
        result1 = list(self.catalog.searchResults(age=(40,43)))
        self.assertEqual(len(result1), 0)

        # update catalog. We have to feed 'located' objects, which is
        # normally the case for objects from ZODB. In our case
        # 'manfred' could not be catalogued while the located version
        # 'manfred_located' (with a __parent__ and __name__ attribute)
        # can.
        def func():
            for x in [self.manfred]:
                yield x
        update_catalog(self.app, 'my_catalog', func=func)

        # now we can find manfred in catalog
        result2 = list(self.catalog.searchResults(age=(40,43)))
        self.assertEqual(result2[0], self.manfred)
        return
