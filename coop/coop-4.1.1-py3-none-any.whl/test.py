"""
Some testing tools that coop projects can use.

Most projects will want to do something like:

.. code-block:: python

    from coop.test import (
        TestThingsWithContentMixin, TestThingsWithoutContentMixin)
    from django.test import TestCase

    class TestContentThings(TestThingsWithContentMixin, TestCase):
        def setUp(self):
            super().setUp()
            root_page = Page.objects.get(pk=1)
            self.home = root_page.add_child(instance=HomePage(
                title='Home'))
            self.site = Site.objects.create(
                root_page=self.home,
                hostname='localhost',
                is_default_site=True)

    class TestOtherThings(TestThingsWithoutContentMixin, TestCase):
        pass
"""
from io import StringIO
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core import mail
from django.core.management import call_command


class CoopAssertionMixin():
    def assertNoMissingMigrations(self):
        try:
            out = StringIO()
            call_command(
                *'makemigrations --check --dry-run --no-color --name=missing_migration'.split(),
                stdout=out)
        except SystemExit:
            out.seek(0)
            self.fail(msg='Missing migrations:\n\n' + out.read())

    def assertTestdataWorks(self):
        """
        Run the ``testdata`` management command. The tests pass if no errors
        are thrown
        """
        call_command('testdata', stdout=StringIO())
        call_command('update_index', stdout=StringIO())

    def assertStandardFilesExist(self):
        for standard_file in ['/favicon.ico', '/robots.txt', '/humans.txt']:
            response = self.client.get(standard_file, follow=True)
            final_url = response.redirect_chain[-1][0]
            path = urlsplit(final_url).path
            self.assertTrue(path.startswith(settings.STATIC_URL))
            tail = path[len(settings.STATIC_URL):]
            self.assertTrue(finders.find(tail), msg='{} exists'.format(path))

    def assert404PageRenders(self):
        url = '/quite/likely/not/a/page/'
        response = self.client.get(url)
        self.assertContains(response, url, status_code=404)

    def assert500PageRenders(self):
        response = self.client.get('/500/')
        self.assertEqual(response.status_code, 500)


class TestThingsWithContentMixin(CoopAssertionMixin):
    """
    Run all the standard coop assertions that require all the site content in
    the database.
    """

    def test_error_pages(self):
        """Test that the 404 and 500 pages render without error"""
        # 404 pages need database content to render site menus and stuff.
        self.assert404PageRenders()
        self.assert500PageRenders()

    def test_standard_files_exist(self):
        """Test that some standard files exist"""
        # This test will find the correct URL for the asset by following
        # redirects, which will also cause the 404 page to be rendered, so this
        # needs page content.
        self.assertStandardFilesExist()

    def test_cache_header_present(self):
        self.client.logout()
        response = self.client.get('/')
        self.assertTrue(response.has_header('X-Wagtail-Cache'))


class TestThingsWithoutContentMixin(CoopAssertionMixin):
    """
    Run all the standard coop assertions that do not require all the site
    content in the database.
    """

    def test_migrations(self):
        self.assertNoMissingMigrations()

    def test_testdata(self):
        self.assertTestdataWorks()


class TestContactPageMixin():
    """
    Use with standard BasicSiteTestCase, tests the email functionality.
    Override setUp with your ContactPageMixin subclass, assign it to self.contact_page
    """
    def get_form_data(self):
        """
        Based on the standard ContactForm, overrride if different
        """
        return {
            'name': 'Example User',
            'email': 'user@example.com',
            'phone_number': '0400 000 000',
            'message': 'Hello, world!',
        }

    def test_send_email(self):
        data = self.get_form_data()

        response = self.client.post(self.contact_page.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['contact_form'].is_valid())
        self.assertTrue(response.context_data.get('success'))
        # Check email
        message = mail.outbox[0]
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(message.to, [self.contact_page.email_to])
