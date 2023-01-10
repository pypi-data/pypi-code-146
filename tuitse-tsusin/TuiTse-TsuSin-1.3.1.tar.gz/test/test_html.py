from bs4 import BeautifulSoup
from django.test.testcases import TestCase
from tuitse import THAU_JI, LIAN_JI, KHIN_SIANN_JI
from tuitse.html import tuitse_html
import re


class TanGuanTshiGiam(TestCase):

    def test_ok(self):
        kiatko = tuitse_html([
            ('好', 'hó', THAU_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            soup.ruby.rb.string, 'hó'
        )

    def test_nng_su(self):
        kiatko = tuitse_html([
            ('真', 'tsin', THAU_JI, True),
            ('好', 'hó', THAU_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('rb')), 2
        )

    def test_siangji_e_lomaji(self):
        kiatko = tuitse_html([
            ('姑', 'koo', THAU_JI, True),
            ('娘', 'niû', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('rb')), 3
        )
        self.assertEqual(soup.find_all('rt')[2].text, '娘', kiatko)
        self.assertEqual(soup.find_all('rb')[2].text, 'niû', kiatko)
        self.assertEqual(soup.find_all('rt')[1].text, '', kiatko)
        self.assertEqual(soup.find_all('rb')[1].text, '-', kiatko)

    def test_khinsiann_hu(self):
        kiatko = tuitse_html([
            ('轉', 'tńg', THAU_JI, True),
            ('去', 'khì', KHIN_SIANN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('rb')), 3
        )

    def test_tsuanlo_su(self):
        kiatko = tuitse_html([
            ('koo', 'koo', THAU_JI, True),
            ('niu', 'niu', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(soup.find_all('rt')[2].text, 'niu', kiatko)
        self.assertEqual(soup.find_all('rb')[2].text, 'niu', kiatko)
        self.assertEqual(soup.find_all('rt')[1].text, '-', kiatko)
        self.assertEqual(soup.find_all('rb')[1].text, '-', kiatko)

    def test_khinsiann_e_tsuanlo_su(self):
        kiatko = tuitse_html([
            ('tńg', 'tńg', THAU_JI, True),
            ('khì', 'khì', KHIN_SIANN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('ruby')), 1
        )

    def test_hanlo_su_e_hanji(self):
        kiatko = tuitse_html([
            ('芳', 'phang', THAU_JI, True),
            ('kòng', 'kòng', LIAN_JI, True),
            ('kòng', 'kòng', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('ruby')), 1
        )

    def test_hanlo_su_e_lomaji(self):
        kiatko = tuitse_html([
            ('芳', 'phang', THAU_JI, True),
            ('kòng', 'kòng', LIAN_JI, True),
            ('kòng', 'kòng', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('ruby')), 1
        )

    def test_kinnkinn叫_e_hanji(self):
        kiatko = tuitse_html([
            ('kinn', 'kinn', THAU_JI, True),
            ('kinn', 'kinn', LIAN_JI, True),
            ('叫', '叫', THAU_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('ruby')), 2
        )

    def test_kinnkinn叫_e_lomaji(self):
        kiatko = tuitse_html([
            ('kinn', 'kinn', THAU_JI, True),
            ('kinn', 'kinn', LIAN_JI, True),
            ('叫', '叫', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('ruby')), 1
        )

    def test_tsuanhan_su(self):
        kiatko = tuitse_html([
            ('帥', '帥', THAU_JI, True),
            ('哥', '哥', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(
            len(soup.find_all('ruby')), 1
        )

    def test_khinsiann(self):
        kiatko = tuitse_html([
            ('禁', 'kìm', THAU_JI, True),
            ('起', 'khí', KHIN_SIANN_JI, True),
            ('來', 'lâi', LIAN_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(soup.find_all('rt')[2].text, '起', kiatko)
        self.assertEqual(soup.find_all('rb')[2].text, 'khí', kiatko)
        self.assertEqual(soup.find_all('rt')[1].text, '', kiatko)
        self.assertEqual(soup.find_all('rb')[1].text, '--', kiatko)

    '''
    Ē-té sī lak-jī kah tîng-tânn
    '''

    def test_khiam_hanji(self):
        kiatko = tuitse_html([
            ('', 'hó', THAU_JI, False),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(soup.find_all('rt')[0]['class'], ['fail'])

    def test_khiam_lomaji(self):
        kiatko = tuitse_html([
            ('好', '', THAU_JI, False),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(soup.find_all('rb')[0]['class'], ['fail'])

    def test_khiam_bue(self):
        kiatko = tuitse_html([
            ('姑', 'koo', THAU_JI, True),
            ('娘', '', LIAN_JI, False),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertNotIn('class', soup.find_all('rb')[0])
        self.assertEqual(soup.find_all('rb')[2]['class'], ['fail'])

    def test_khiam_tiongng(self):
        kiatko = tuitse_html([
            ('歡', 'huann', THAU_JI, True),
            ('歡', '', LIAN_JI, True),
            ('喜', 'hí', LIAN_JI, True),
            ('喜', '', THAU_JI, True),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        lomaji = ''
        for rb in soup.ruby.find_all('rb'):
            lomaji += re.sub(r'\s', ' ', rb.text)
        self.assertEqual(lomaji, 'huann  hí')

    def test_bo_tuitang(self):
        kiatko = tuitse_html([
            ('好', 'bái', THAU_JI, False),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertEqual(soup.find_all('rb')[0]['class'], ['fail'])

    def test_tiongng_bo_tuitang(self):
        kiatko = tuitse_html([
            ('行', 'kiânn', THAU_JI, True),
            ('轉', 'ng', KHIN_SIANN_JI, False),
            ('去', 'i', LIAN_JI, False),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        self.assertNotIn('class', soup.find_all('rb')[0])
        self.assertEqual(soup.find_all('rb')[2]['class'], ['fail'])
        self.assertEqual(soup.find_all('rb')[4]['class'], ['fail'])

    def test_lianjihu_mai_laklohlai(self):
        kiatko = tuitse_html([
            ('tánn', '', THAU_JI, False),
            ('pān', '', LIAN_JI, False),
        ])
        soup = BeautifulSoup(kiatko, "html.parser")
        khangpeh = soup.find_all('rb')[1].text
        self.assertEqual(len(khangpeh), 1)
