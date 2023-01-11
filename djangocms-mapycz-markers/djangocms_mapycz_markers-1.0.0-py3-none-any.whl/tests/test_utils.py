from django.test import SimpleTestCase

from djangocms_mapycz_markers.utils import keep_only_tags, strip_href, strip_src


class StripHrefTest(SimpleTestCase):

    def test_empty_string(self):
        self.assertEqual(strip_href(''), '')

    def test_http(self):
        self.assertEqual(strip_href('http://test'), 'http://test')

    def test_https(self):
        self.assertEqual(strip_href('https://test'), 'https://test')

    def test_mailto(self):
        self.assertEqual(strip_href('mailto:test'), 'mailto:test')

    def test_root(self):
        self.assertEqual(strip_href('/test'), '/test')

    def test_no_root(self):
        self.assertEqual(strip_href('test'), '')


class StripSrcTest(SimpleTestCase):

    def test_empty_string(self):
        self.assertEqual(strip_src(''), '')

    def test_http(self):
        self.assertEqual(strip_src('http://test'), 'http://test')

    def test_https(self):
        self.assertEqual(strip_src('https://test'), 'https://test')

    def test_mailto(self):
        self.assertEqual(strip_src('mailto:test'), '')

    def test_root(self):
        self.assertEqual(strip_src('/test'), '/test')

    def test_no_root(self):
        self.assertEqual(strip_src('test'), '')


class KeepOnlyTagsText(SimpleTestCase):

    def test_none(self):
        self.assertIsNone(keep_only_tags(None))

    def test_empty_string(self):
        self.assertEqual(keep_only_tags(''), '')

    def test_only_text(self):
        self.assertEqual(keep_only_tags('only text'), 'only text')

    def test_html(self):
        self.assertEqual(keep_only_tags('<html>The doc.</html>'), '')

    def test_html_body(self):
        self.assertEqual(keep_only_tags('<html><body>The doc.</body></html>'), 'The doc.')

    def test_body(self):
        self.assertEqual(keep_only_tags('<body>The doc.</body>'), 'The doc.')

    def test_text_with_tags(self):
        self.assertEqual(keep_only_tags('Begin: <strong>Aloha!</strong> End.'), 'Begin: <strong>Aloha!</strong> End.')

    def test_tags(self):
        src = """
            <p>Text</p>
            <a href="/path">Link</a>
        """
        dest = keep_only_tags(src)
        self.assertHTMLEqual(dest, src)

    def test_strip_not_allowed_tags(self):
        src = """
            <p>Text</p>
            <script>alert('Alert!')</script>
            <a href="path">No path</a>
            <a href="/path">Path</a>
            <a href="javascript:alert('Alert!')">Link</a>
            <a href="https://www.nic.cz">www.nic.cz</a>
            <p>End.</p>
        """
        dest = """
            <p>Text</p>
            <a>No path</a>
            <a href="/path">Path</a>
            <a>Link</a>
            <a href="https://www.nic.cz">www.nic.cz</a>
            <p>End.</p>
        """
        self.assertHTMLEqual(keep_only_tags(src), dest)

    def test_custom_allowed_tags(self):
        src = """
            <p>Text</p>
            <script>alert('Alert!')</script>
            <a href="path">Path</a>
            <a href="javascript:alert('Alert!')">Link</a>
            <a href="https://www.nic.cz">www.nic.cz</a>
            <p>End.</p>
        """
        dest = """
            <p>Text</p>
            <p>End.</p>
        """
        self.assertHTMLEqual(keep_only_tags(src, {'p': []}), dest)

    def test_custom_attribute_callbacks(self):
        src = """
            <p class="foo">Text</p>
            <script>alert('Alert!')</script>
            <a href="path">Path</a>
            <a href="javascript:alert('Alert!')">Link</a>
            <a href="https://www.nic.cz">www.nic.cz</a>
            <p>End.</p>
        """
        dest = """
            <p class="myclass-foo">Text</p>
            <p>End.</p>
        """
        def custom_class(value):
            return f"myclass-{value}"
        self.assertHTMLEqual(keep_only_tags(src, {'p': ['class']}, {'p_class': custom_class}), dest)
