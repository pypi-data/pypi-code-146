from tuitse import kiamtsa
from tuitse import tuitse_boolean
from django.test.testcases import TestCase


class KangJiSooTshiGiam(TestCase):
    def tearDown(self):
        kiat_ko = kiamtsa(self.hanji, self.lomaji)
        self.assertEqual(tuitse_boolean(kiat_ko), self.bool)

    def test_ok(self):
        self.hanji = '我'
        self.lomaji = 'guá'
        self.bool = True

    def test_khiam_lomaji(self):
        self.hanji = '媠姑娘'
        self.lomaji = 'suí niû'
        self.bool = False
