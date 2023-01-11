# Tests for datetimewidgets
import datetime
import pytz
from zope import schema
from zope.component import getGlobalSiteManager
from zope.formlib import form
from zope.formlib.interfaces import IInputWidget, IDisplayWidget
from zope.formlib.tests.test_functional_textwidget import(
    FunctionalWidgetTestCase,)
from zope.formlib.textwidgets import TextWidget
from zope.interface import Interface, implements
from zope.interface.verify import verifyClass, verifyObject
from zope.publisher.browser import TestRequest
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.widgets.datetimewidget import PytzDatetimeWidget

class IContent(Interface):
    my_dt = schema.Datetime(
        title = u'A datetime.',
        )

class Content(object):
    implements(IContent)
    my_dt = None

class SampleForm(form.EditForm):
    form_fields = form.fields(IContent)
    form_fields['my_dt'].custom_widget = PytzDatetimeWidget

class FakeUtils(object):
    # Fake app-wide set timezone.
    implements(IKofaUtils)
    tzinfo = pytz.timezone('America/Sao_Paulo')


class PytzDatetimeWidgetTests(FunctionalWidgetTestCase):

    widgets = [
        (schema.interfaces.IDatetime, TextWidget),
        ]

    def setUp(self):
        super(PytzDatetimeWidgetTests, self).setUp()
        self.gsm = getGlobalSiteManager()
        self.utils = FakeUtils()
        self.gsm.registerUtility(self.utils)
        return

    def tearDown(self):
        super(PytzDatetimeWidgetTests, self).tearDown()
        self.gsm.unregisterUtility(self.utils)
        return

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = PytzDatetimeWidget(IContent['my_dt'], TestRequest())
        verifyClass(IInputWidget, PytzDatetimeWidget)
        verifyObject(IInputWidget, obj)
        return

    def test_to_value(self):
        # we get always UTC-based values
        content = Content()
        request = TestRequest()

        request.form['form.my_dt'] = u'2012-01-02 12:10:19 GMT+1'
        request.form['form.actions.apply'] = u''
        SampleForm(content, request)()

        self.assertEqual( content.my_dt, datetime.datetime(
            2012, 1, 2, 11, 10, 19, tzinfo=pytz.utc))
        self.assertTrue(content.my_dt.tzinfo is pytz.utc)
        return

    def test_export_values(self):
        # make sure we understand values as exported
        content = Content()
        request = TestRequest()

        request.form['form.my_dt'] = u'2012-01-02 12:10:19+00:00'
        request.form['form.actions.apply'] = u''
        SampleForm(content, request)()

        self.assertEqual( content.my_dt, datetime.datetime(
            2012, 1, 2, 12, 10, 19, tzinfo=pytz.utc))
        self.assertTrue(content.my_dt.tzinfo is pytz.utc)
        return

    def test_datetimes_wo_tz(self):
        # Datetimes w/o tz are considered to be meant in app-wide timezone.
        content = Content()
        request = TestRequest()

        request.form['form.my_dt'] = u'2011-11-11 11:11:11'
        request.form['form.actions.apply'] = u''
        SampleForm(content, request)()

        # Sao Paulo was two hours back UTC on 2011-11-11
        self.assertEqual(content.my_dt, datetime.datetime(
            2011, 11, 11, 13, 11, 11, tzinfo=pytz.utc))
        self.assertTrue(content.my_dt.tzinfo is pytz.utc)
        return
